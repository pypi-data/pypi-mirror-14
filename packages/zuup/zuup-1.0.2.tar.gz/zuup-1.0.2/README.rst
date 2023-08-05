====
zuup
====

.. image:: https://travis-ci.org/sileht/zuup.png?branch=master
   :target: https://travis-ci.org/sileht/zuup

.. image:: https://img.shields.io/pypi/v/zuup.svg
   :target: https://pypi.python.org/pypi/zuup/
   :alt: Latest Version

.. image:: https://img.shields.io/pypi/dm/zuup.svg
   :target: https://pypi.python.org/pypi/zuup/
   :alt: Downloads


Command line to consult Openstack zuul status

* Free software: Apache license
* Documentation: http://zuup.readthedocs.org
* Source: http://github.com/sileht/zuup
* Bugs: http://github.com/sileht/zuup/issues

Installation
------------

At the command line::

    $ pip install zuup

Or, if you have virtualenvwrapper installed::

    $ mkvirtualenv zuup
    $ pip install zuup

Usage
-----

To use zuup::

    $ zuup --help     
    usage: zuup [-h] [-D] [-d] [-w DELAY] [-e EXPIRATION] [-u USERNAME]
                [-p PROJECTS] [-c CHANGES] [-l] [-r] [-s] [-j JOB]

    optional arguments:
      -h, --help     show this help message and exit
      -D             Daemonize and exit if no more reviews
      -d             Daemonize
      -w DELAY       refresh delay
      -e EXPIRATION  review expiration in deamon mode
      -u USERNAME    Username
      -p PROJECTS    Projects
      -c CHANGES     changes
      -l             local changes
      -r             current repo changes
      -s             short output
      -j JOB         show log of a job of a change


Example
-------

Print jobs of projects::

    $ zuup -p openstack/ceilometer -p openstack/gnocchi

    [openstack/gnocchi] check[0]: https://review.openstack.org/235161
     TEST 01:22:14/00:00:00
     - SUCCESS --:--:-- gate-gnocchi-pep8 http://logs.openstack.org/61/235161/4/check/gate-gnocchi-pep8/ac6632a
     - SUCCESS --:--:-- gate-gnocchi-docs http://logs.openstack.org/61/235161/4/check/gate-gnocchi-docs/ff085e7
     - SUCCESS --:--:-- gate-gnocchi-python27 http://logs.openstack.org/61/235161/4/check/gate-gnocchi-python27/9e3fd5e
     - SUCCESS --:--:-- gate-gnocchi-python34 http://logs.openstack.org/61/235161/4/check/gate-gnocchi-python34/afcef87
     - SUCCESS --:--:-- gate-gnocchi-bashate http://logs.openstack.org/61/235161/4/check/gate-gnocchi-bashate/f7b10d4
     - SUCCESS --:--:-- gate-gnocchi-dsvm-functional-file-mysql http://logs.openstack.org/61/235161/4/check/gate-gnocchi-dsvm-functional-file-mysql/d016760
     - ======= 00:00:00 gate-gnocchi-dsvm-functional-swift-postgresql https://jenkins06.openstack.org/job/gate-gnocchi-dsvm-functional-swift-postgresql/263/
     - SUCCESS --:--:-- gate-gnocchi-dsvm-functional-ceph-mysql http://logs.openstack.org/61/235161/4/check/gate-gnocchi-dsvm-functional-ceph-mysql/2b54187
     - SUCCESS --:--:-- gate-ceilometer-dsvm-integration http://logs.openstack.org/61/235161/4/check/gate-ceilometer-dsvm-integration/a937fd5


    [openstack/ceilometer] check[0]: https://review.openstack.org/235202
     Merge tag '5.0.0' 01:02:46/00:09:20
     - SUCCESS --:--:-- gate-ceilometer-pep8 http://logs.openstack.org/02/235202/1/check/gate-ceilometer-pep8/bac67ce
     - SUCCESS --:--:-- gate-ceilometer-docs http://logs.openstack.org/02/235202/1/check/gate-ceilometer-docs/1d1eb96
     - FAILURE --:--:-- gate-ceilometer-python27 http://logs.openstack.org/02/235202/1/check/gate-ceilometer-python27/d993423
     - FAILURE --:--:-- gate-ceilometer-python34 http://logs.openstack.org/02/235202/1/check/gate-ceilometer-python34/5ee29b5
     - SUCCESS --:--:-- gate-tempest-dsvm-ceilometer-mongodb-full http://logs.openstack.org/02/235202/1/check/gate-tempest-dsvm-ceilometer-mongodb-full/a55e9e6
     - ======. 00:09:20 gate-tempest-dsvm-ceilometer-mysql-neutron-full https://jenkins06.openstack.org/job/gate-tempest-dsvm-ceilometer-mysql-neutron-full/114/
     - ======= 00:00:00 gate-tempest-dsvm-ceilometer-mysql-full https://jenkins03.openstack.org/job/gate-tempest-dsvm-ceilometer-mysql-full/36/
     - SUCCESS --:--:-- gate-tempest-dsvm-ceilometer-postgresql-full http://logs.openstack.org/02/235202/1/check/gate-tempest-dsvm-ceilometer-postgresql-full/a1eee16
     - ======= 00:00:00 gate-ceilometer-dsvm-functional-mongodb https://jenkins03.openstack.org/job/gate-ceilometer-dsvm-functional-mongodb/275/
     - ======= 00:00:00 gate-ceilometer-dsvm-functional-postgresql https://jenkins05.openstack.org/job/gate-ceilometer-dsvm-functional-postgresql/146/
     - SUCCESS --:--:-- gate-grenade-dsvm-ceilometer http://logs.openstack.org/02/235202/1/check/gate-grenade-dsvm-ceilometer/383ecfb
     - SUCCESS --:--:-- gate-ceilometer-dsvm-integration http://logs.openstack.org/02/235202/1/check/gate-ceilometer-dsvm-integration/6758820

    ...


Print jobs of an user::

    $ zuup -u sileht

    $ zuup -u sileht -d  # Run it in loop


Print jobs of a change-id::

    $ zuup -c 235161

    or

    $ zuup -c https://review.openstack.org/235207

Print jobs of change-ids on your local git branch::

    $ zuup -l

Print jobs resume ::

    $ zuup -c https://review.openstack.org/235207 -s

    [openstack/ceilometer] check[0]: https://review.openstack.org/235207 Switch to post-versioning 00:59:40/00:04:08 SSFSSSSPPSS
     - FAILURE --:--:-- gate-ceilometer-python27 http://logs.openstack.org/07/235207/1/check/gate-ceilometer-python27/546a067

Print running and failed jobs only ::

    $ zuup -c https://review.openstack.org/235207 -R

    [openstack/ceilometer] check[0]: https://review.openstack.org/235207
     Switch to post-versioning 01:00:18/00:03:30
     - FAILURE --:--:-- gate-ceilometer-python27 http://logs.openstack.org/07/235207/1/check/gate-ceilometer-python27/546a067
     - ======= 00:00:00 gate-ceilometer-dsvm-functional-mongodb https://jenkins03.openstack.org/job/gate-ceilometer-dsvm-functional-mongodb/276/
     - ======. 00:03:30 gate-ceilometer-dsvm-functional-postgresql https://jenkins04.openstack.org/job/gate-ceilometer-dsvm-functional-postgresql/140/
