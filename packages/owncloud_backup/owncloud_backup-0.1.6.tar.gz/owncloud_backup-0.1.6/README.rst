ownCloud backup
===============

This project is used for uploading the backups to the ownCloud and managing old backups.

How it works
------------

By default, script expects one *file* argument, which will be uploaded to ownCloud with ``%Y.%m.%d_`` time prefix into `remote_path` directory.

When the file is uploaded, scripts requests listing of all other files in selected `remote_path`, then reads time informations from names and then removes old files.

Process of removing of old files is defined to keep following files:

- all files from last month
- one file per week for two-months-before
- one file per two weeks for three-months-before

and to remove all older files.

Configuration
-------------

There is possibility of configuration of following variables using `conf` files ``owncloud_backup.cfg`` or ``~/.owncloud_backup.cfg``::

    [Login]
    user=login@owncloud.tld
    pass=password
    url=https://owncloud.cesnet.cz

    [Config]
    remote_path=/backups
    no_timestamp=false

All values in `Config` section and `url` variable from `Login` section is optional (defaults are shown in this example).

`no_timestamp` will instruct the script to stop putting the timestamp prefix to uploaded files. In that case, it is expected that such files will contain the timestamp added manually, or they will be ignored in process of elimination of old files.

Commandline arguments
---------------------

All variables defined in configuration file may be also added using commandline arguments::

    usage: owncloud_backup.py [-h] [-u USERNAME] [-p PASSWORD] [--url URL]
                              [-r REMOTE_PATH] [-n]
                              FILENAME

    This program may be used to perform database backups into ownCloud.
    Configuration file in ini format is expected in `owncloud_backup.cfg` or
    `~/.owncloud_backup.cfg` paths.

    positional arguments:
      FILENAME              Upload FILENAME into the ownCloud.

    optional arguments:
      -h, --help            show this help message and exit
      -u USERNAME, --username USERNAME
                            Username of the ownCloud user.
      -p PASSWORD, --password PASSWORD
                            Password of the ownCloud user.
      --url URL             URL of the ownCloud service. Default
                            `https://owncloud.cesnet.cz`.
      -r REMOTE_PATH, --remote-path REMOTE_PATH
                            Path on the server. Default `/backups`.
      -n, --no-timestamp    By default, the script adds `%Y.%m.%d_` prefix to each
                            uploaded file.

Installation
------------

Module is hosted at `PYPI <https://pypi.python.org/pypi/owncloud_backup>`_, and
can be installed using `PIP`_::

    sudo pip install owncloud_backup

.. _PIP: http://en.wikipedia.org/wiki/Pip_%28package_manager%29

Installation on SuSe
--------------------

In case that you are using ancient Suse installation with old python versions and no PIP, you may install it with following commands::

  wget --no-check-certificate https://pypi.python.org/packages/source/s/setuptools/setuptools-20.0.zip
  unzip setuptools-20.0.zip
  cd setuptools-20.0/
  python setup.py install
  easy_install pip==1.2
  pip install -U owncloud_backup


Source code
+++++++++++

Project is released under the MIT license. Source code can be found at GitHub:

- https://github.com/NLCR/owncloud_backup

Unittests
+++++++++

Almost every feature of the project is tested by unittests. You can run those
tests using provided ``run_tests.sh`` script, which can be found in the root
of the project.

If you have any trouble, just add ``--pdb`` switch at the end of your ``run_tests.sh`` command like this: ``./run_tests.sh --pdb``. This will drop you to `PDB`_ shell.

.. _PDB: https://docs.python.org/2/library/pdb.html

Requirements
^^^^^^^^^^^^

This script expects that packages pytest_ is installed. In case you don't have it yet, it can be easily installed using following command::

    pip install --user pytest

or for all users::

    sudo pip install pytest

.. _pytest: http://pytest.org/


Example
^^^^^^^
::

    ./run_tests.sh 
    ============================= test session starts ==============================
    platform linux2 -- Python 2.7.6, pytest-2.8.2, py-1.4.30, pluggy-0.3.1
    rootdir: /home/bystrousak/Plocha/Dropbox/c0d3z/prace/owncloud_backup, inifile: 
    plugins: cov-1.8.1
    collected 3 items 

    tests/test_backup.py ...

    =========================== 3 passed in 0.47 seconds ===========================
