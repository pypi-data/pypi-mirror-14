#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Pavel Korshunov <pavel.korshunov@idiap.ch>
# Wed 19 Aug 13:43:50 2015
#
# Copyright (C) 2011-2012 Idiap Research Institute, Martigny, Switzerland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""A few checks at the avspoof attack database.
"""

from __future__ import print_function

from .query import Database
from .models import *


def db_available(test):
    """Decorator for detecting if OpenCV/Python bindings are available"""
    from bob.io.base.test_utils import datafile
    from nose.plugins.skip import SkipTest
    import functools

    @functools.wraps(test)
    def wrapper(*args, **kwargs):
        dbfile = datafile("db.sql3", __name__, None)
        if os.path.exists(dbfile):
            return test(*args, **kwargs)
        else:
            raise SkipTest(
                "The database file '%s' is not available; did you forget to run 'bob_dbmanage.py %s create' ?" % (
                dbfile, 'avspoof_btas2016'))

    return wrapper


# class AVSpoofDatabaseTest(unittest.TestCase):
class AVSpoofDatabaseTest():
    """Performs various tests on the avspoof attack database."""

    @db_available
    def queryAttackType(self, protocol, N, devices=None, support=None, attackdevices=None):
        db = Database()
        f = db.objects(cls='real', protocol=protocol, devices=devices, clients=N)
        print ("Real set %s" % str(f))
        f = db.objects(cls='attack', protocol=protocol, support=support, devices=devices,
                       attackdevices=attackdevices, clients=N)
        print ("Attack set %s " % str(f))

    #        train = db.objects(cls='attack', groups='train', protocol=protocol)
    #        dev = db.objects(cls='attack', groups='devel', protocol=protocol)
    #        test = db.objects(cls='attack', groups='test', protocol=protocol)

    @db_available
    def test01_queryAttacks(self):
        print ("test01_queryAttacks, btas2016")
        self.queryAttackType('btas2016', N=1)

    @db_available
    def test02_queryReplayAttacks(self):
        print ("test02_queryReplayAttacks, unknown")
        self.queryAttackType(support='unknown', N=1)

    @db_available
    def test03_queryPhone2AndReplayAttacks(self):
        print ("test03_queryPhone2AndReplayAttacks, replay")
        self.queryAttackType(support='replay', N=60)

    @db_available
    def test04_queryPhone2ReplayAttacks(self):
        print ("test04_queryPhone2ReplayAttacks, replay, phone2 only")
        self.queryAttackType(support='replay', attackdevices='phone2', N=1)

    @db_available
    def test05_queryReplayLaptopAttacks(self):
        print ("test05_queryReplayLaptopAttacks, replay, laptop only")
        self.queryAttackType(support='replay', N=60, devices=None, attackdevices='laptop')


def main():
    test = AVSpoofDatabaseTest()
    test.test01_queryAttacks()
    test.test02_queryReplayAttacks()
    test.test03_queryPhone2AndReplayAttacks()
    test.test04_queryPhone2ReplayAttacks()
    test.test05_queryReplayLaptopAttacks()


if __name__ == '__main__':
    main()
