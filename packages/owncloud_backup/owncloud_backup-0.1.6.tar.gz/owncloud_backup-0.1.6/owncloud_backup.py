#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import os
import sys
import time
import argparse
import datetime
import ConfigParser
from collections import namedtuple

import owncloud

# to disable SSL complaints
import requests
if hasattr(requests, "packages"):
    requests.packages.urllib3.disable_warnings()


# Functions & classes =========================================================
FileObj = namedtuple("FileObj", "timestamp filename")


def collect_files(path, listdir):
    """
    Collect all files in `path` using `listdir` function.

    This function collects only files with `%%Y.%%m.%%d` prefix, which is
    parsable to timestamp.

    Args:
        path (str): Path where you want to do the listing.
        listdir (fn reference): Function, which takes `path` argument and
            returns list of filenames.

    Returns:
        list: :class:`FileObj` instances.
    """
    def parse_ts(fn):
        """
        Parse timestamp from `fn` (filename). Timestamp is expected to be in
        `%%Y.%%m.%%d_` format.

        Args:
            fn (str): Filename.

        Returns:
            int: Timestamp.
        """
        date_string = fn.split("_")[0]

        try:
            date = datetime.datetime.strptime(date_string, "%Y.%m.%d")
            date = date.timetuple()
        except ValueError:
            return None

        return time.mktime(date)

    return [
        FileObj(timestamp=parse_ts(fn), filename=os.path.join(path, fn))
        for fn in listdir(path)
        if "_" in fn and parse_ts(fn) is not None
    ]


def pick_n(dataset, n):
    """
    Pick `n` items from `dataset`. The function tries to divide the items into
    same-sized groups and then picks first item from each of the group.

    Args:
        dataset (list): Array of items.
        n (int): How many items to pick from `dataset`.

    Returns:
        list: Picked items.
    """
    if len(dataset) == 1:
        return [dataset[0]]

    if n == 1 or n >= len(dataset):
        return dataset

    elif n == 2:
        return [dataset[0], dataset[len(dataset) / 2]]

    elif n == 3:
        return [dataset[0], dataset[len(dataset) / 2], dataset[-1]]

    else:
        return pick_n(dataset[:len(dataset) / 2], n - 2) + \
               pick_n(dataset[len(dataset) / 2:], n - 2)


def collect_old_files(file_list, today=None):
    """
    Get list of old files, which are designated for removal.

    Args:
        file_list (list): List of :class:`FileObj` from :func:`collect_files`.
        today (int, default None): Timestamp which will be used to compute
            diffs. If not set, `time.time()` is used.

    Returns:
        list: List :class:`FileObj` designated for removal.
    """
    if not today:
        today = time.time()

    month = 60 * 60 * 24 * 31
    prev_month = today - month
    prev_two_months = prev_month - month
    prev_three_months = prev_two_months - month

    def two_months_before(file_list):
        return [
            fo
            for fo in file_list
            if fo.timestamp < prev_month and fo.timestamp >= prev_two_months
        ]

    def three_months_before(file_list):
        return [
            fo
            for fo in file_list
            if (fo.timestamp < prev_two_months and
                fo.timestamp >= prev_three_months)
        ]

    def older_than_three_months(file_list):
        return [
            fo
            for fo in file_list
            if fo.timestamp < prev_three_months
        ]

    # sort the list - this is important for other pickers
    file_list = sorted(file_list, key=lambda x: x.timestamp)

    # collect list of two and three months old files
    two_months = two_months_before(file_list)
    three_months = three_months_before(file_list)

    # all older files are considered as old
    old_files = older_than_three_months(file_list)

    # pick files, which will be kept
    keep_twomonths = pick_n(two_months, 4)
    keep_threemonths = pick_n(three_months, 2)

    # collect all files which are not in keep_* lists
    old_files.extend([fo for fo in two_months if fo not in keep_twomonths])
    old_files.extend([fo for fo in three_months if fo not in keep_threemonths])

    return sorted(old_files, key=lambda x: x.timestamp)


def exists(client, path):
    """
    Check whether the `path` exists in ownCloud account.

    Args:
        client (obj): Instance of the logged in ownCloud handler.
        path (str): Path to the file / directory.

    Returns:
        bool: True, if the file exists.
    """
    path = os.path.abspath(path)

    dirname = os.path.dirname(path)
    filename = os.path.basename(path)

    listing = client.list(dirname)

    # I intentionally don't use set comprehension because of
    # support of prehistorical python2.6 suse servers
    return filename in set([
        os.path.basename(os.path.abspath(x.path))
        for x in listing
    ])


def upload_file(remote_path, path, add_date_string=True):
    """
    Upload file at `path` to `remote_path`.

    Args:
        remote_path (str): Path on the ownCloud account.
        path (str): Local path.
        add_date_string (bool, default True): Added prefix with current date?

    Returns:
        bool: True if successfull.
    """
    if add_date_string:
        filename = os.path.basename(os.path.abspath(path))
        remote_path = os.path.join(
            remote_path,
            time.strftime("%Y.%m.%d_") + filename,
        )

    return client.put_file(remote_path, path)


def get_config(args):
    """
    Merge local configuration files with arguments addedd from commandline.

    Args:
        args (obj): Argparse argument object.

    Returns:
        obj: :class:`ConfigParser.SafeConfigParser` instance.
    """
    config = ConfigParser.SafeConfigParser()
    config.read([
        "owncloud_backup.cfg",
        os.path.expanduser("~/.owncloud_backup.cfg"),
    ])

    # set configuration options
    if not config.has_section("Config"):
        config.add_section("Config")
    if not config.has_option("Config", "remote_path"):
        config.set("Config", "remote_path", args.remote_path)
    if not config.has_option("Config", "no_timestamp"):
        config.set(
            "Config",
            "no_timestamp",
            str(args.no_ts).lower(),
        )

    # set login options
    if not config.has_section("Login"):
        config.add_section("Login")
    if not config.has_option("Login", "url"):
        config.set("Login", "url", args.url)
    if args.username:
        config.set("Login", "user", args.username)
    if args.password:
        config.set("Login", "pass", args.password)

    return config


# Main program ================================================================
if __name__ == "__main__":
    default_url = "https://owncloud.cesnet.cz"

    parser = argparse.ArgumentParser(
        description="""This program may be used to perform database backups
            into ownCloud.

            Configuration file in ini format is expected in
            `owncloud_backup.cfg` or `~/.owncloud_backup.cfg` paths.
        """
    )
    parser.add_argument(
        "-u",
        "--username",
        help="Username of the ownCloud user."
    )
    parser.add_argument(
        "-p",
        "--password",
        help="Password of the ownCloud user."
    )
    parser.add_argument(
        "--url",
        default=default_url,
        help="URL of the ownCloud service. Default `%s`." % default_url
    )
    parser.add_argument(
        "-r",
        "--remote-path",
        default="backups",
        help="Path on the server. Default `/backups`."
    )
    parser.add_argument(
        "-n",
        "--no-timestamp",
        dest="no_ts",
        action="store_true",
        help="""By default, the script adds `%%Y.%%m.%%d_` prefix to each \
            uploaded file."""
    )
    parser.add_argument(
        "FILENAME",
        nargs=1,
        help="Upload FILENAME into the ownCloud."
    )

    args = parser.parse_args()
    config = get_config(args)

    client = owncloud.Client(config.get("Login", "url"))
    client.login(config.get("Login", "user"), config.get("Login", "pass"))

    # check whether the user was really logged in
    try:
        client.list("/")
    except owncloud.ResponseError as e:
        if e.status_code == 401:
            print >>sys.stderr, "Invalid username/password."
            sys.exit(1)

        print >>sys.stderr, e.message
        sys.exit(1)

    # try to create `remote_path` directory
    remote_path = config.get("Config", "remote_path")
    if not exists(client, remote_path):
        if not client.mkdir(remote_path):
            print >>sys.stderr, (
                "Can't create `%s`. Please create the directory and repeat."
                % remote_path
            )
            sys.exit(1)

    filename = args.FILENAME[0]
    if not os.path.exists(filename):
        print >>sys.stderr, "`%s` doesn't exists!" % filename
        sys.exit(1)

    no_ts = config.getboolean("Config", "no_timestamp")
    if not upload_file(remote_path, filename, not no_ts):
        print >>sys.stderr, "Couln't upload `%s`, sorry." % filename
        sys.exit(1)

    all_files = collect_files(
        remote_path,
        listdir=lambda path: [
            os.path.basename(os.path.abspath(x.path))
            for x in client.list(path)
        ],
    )
    old_files = collect_old_files(all_files)

    for file in old_files:
        client.delete(file.filename)
