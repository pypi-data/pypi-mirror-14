#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import datetime

import pytest

import owncloud_backup


# Variables ===================================================================
TODAY = 1455104624
TMP_DIR = None


# Fixtures ====================================================================
@pytest.fixture
def files():
    day = 60 * 60 * 24

    out = []
    date = TODAY
    for i in range(95):
        ts_date = datetime.datetime.fromtimestamp(date)
        date_str = ts_date.strftime("%Y.%m.%d.txt")
        out.append(owncloud_backup.FileObj(date, date_str))
        date -= day

    return out


# Tests =======================================================================
def test_collect_files():
    owncloud_backup.collect_files(".", lambda x: [])


def test_pick_n():
    assert owncloud_backup.pick_n(range(10), 4) == [0, 2, 5, 7]
    assert owncloud_backup.pick_n(range(10), 3) == [0, 5, 9]

    assert owncloud_backup.pick_n(range(9), 4) == [0, 2, 4, 6]
    assert owncloud_backup.pick_n(range(9), 3) == [0, 4, 8]

    assert owncloud_backup.pick_n(range(12), 4) == [0, 3, 6, 9]
    assert owncloud_backup.pick_n(range(12), 3) == [0, 6, 11]

    assert owncloud_backup.pick_n(range(15), 3) == [0, 7, 14]


def test_old_files_detection(files):
    shred = owncloud_backup.collect_old_files(files, today=TODAY)

    assert shred
    assert len(shred) == 57

    keeped = set(files) - set(shred)
    assert keeped == {
        owncloud_backup.FileObj(
            timestamp=1447069424,
            filename='2015.11.09.txt'
        ),
        owncloud_backup.FileObj(
            timestamp=1448365424,
            filename='2015.11.24.txt'
        ),
        owncloud_backup.FileObj(
            timestamp=1449747824,
            filename='2015.12.10.txt'
        ),
        owncloud_backup.FileObj(
            timestamp=1450352624,
            filename='2015.12.17.txt'
        ),
        owncloud_backup.FileObj(
            timestamp=1451043824,
            filename='2015.12.25.txt'
        ),
        owncloud_backup.FileObj(
            timestamp=1451735024,
            filename='2016.01.02.txt'
        ),
        owncloud_backup.FileObj(
            timestamp=1452426224,
            filename='2016.01.10.txt'
        ),
        owncloud_backup.FileObj(
            timestamp=1452512624,
            filename='2016.01.11.txt'
        ),
        owncloud_backup.FileObj(
            timestamp=1452599024,
            filename='2016.01.12.txt'
        ),
        owncloud_backup.FileObj(
            timestamp=1452685424,
            filename='2016.01.13.txt'
        ),
        owncloud_backup.FileObj(
            timestamp=1452771824,
            filename='2016.01.14.txt'
        ),
        owncloud_backup.FileObj(
            timestamp=1452858224,
            filename='2016.01.15.txt'
        ),
        owncloud_backup.FileObj(
            timestamp=1452944624,
            filename='2016.01.16.txt'
        ),
        owncloud_backup.FileObj(
            timestamp=1453031024,
            filename='2016.01.17.txt'
        ),
        owncloud_backup.FileObj(
            timestamp=1453117424,
            filename='2016.01.18.txt'
        ),
        owncloud_backup.FileObj(
            timestamp=1453203824,
            filename='2016.01.19.txt'
        ),
        owncloud_backup.FileObj(
            timestamp=1453290224,
            filename='2016.01.20.txt'
        ),
        owncloud_backup.FileObj(
            timestamp=1453376624,
            filename='2016.01.21.txt'
        ),
        owncloud_backup.FileObj(
            timestamp=1453463024,
            filename='2016.01.22.txt'
        ),
        owncloud_backup.FileObj(
            timestamp=1453549424,
            filename='2016.01.23.txt'
        ),
        owncloud_backup.FileObj(
            timestamp=1453635824,
            filename='2016.01.24.txt'
        ),
        owncloud_backup.FileObj(
            timestamp=1453722224,
            filename='2016.01.25.txt'
        ),
        owncloud_backup.FileObj(
            timestamp=1453808624,
            filename='2016.01.26.txt'
        ),
        owncloud_backup.FileObj(
            timestamp=1453895024,
            filename='2016.01.27.txt'
        ),
        owncloud_backup.FileObj(
            timestamp=1453981424,
            filename='2016.01.28.txt'
        ),
        owncloud_backup.FileObj(
            timestamp=1454067824,
            filename='2016.01.29.txt'
        ),
        owncloud_backup.FileObj(
            timestamp=1454154224,
            filename='2016.01.30.txt'
        ),
        owncloud_backup.FileObj(
            timestamp=1454240624,
            filename='2016.01.31.txt'
        ),
        owncloud_backup.FileObj(
            timestamp=1454327024,
            filename='2016.02.01.txt'
        ),
        owncloud_backup.FileObj(
            timestamp=1454413424,
            filename='2016.02.02.txt'
        ),
        owncloud_backup.FileObj(
            timestamp=1454499824,
            filename='2016.02.03.txt'
        ),
        owncloud_backup.FileObj(
            timestamp=1454586224,
            filename='2016.02.04.txt'
        ),
        owncloud_backup.FileObj(
            timestamp=1454672624,
            filename='2016.02.05.txt'
        ),
        owncloud_backup.FileObj(
            timestamp=1454759024,
            filename='2016.02.06.txt'
        ),
        owncloud_backup.FileObj(
            timestamp=1454845424,
            filename='2016.02.07.txt'
        ),
        owncloud_backup.FileObj(
            timestamp=1454931824,
            filename='2016.02.08.txt'
        ),
        owncloud_backup.FileObj(
            timestamp=1455018224,
            filename='2016.02.09.txt'
        ),
        owncloud_backup.FileObj(
            timestamp=1455104624,
            filename='2016.02.10.txt'
        ),
    }
