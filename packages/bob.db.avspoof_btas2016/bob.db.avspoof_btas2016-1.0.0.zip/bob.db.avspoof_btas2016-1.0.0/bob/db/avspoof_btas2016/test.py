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

import unittest
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


class AVSpoofDatabaseTest(unittest.TestCase):
    """Performs various tests on the AVspoof attack database."""

    @db_available
    def queryGroupsProtocolsTypes(self, protocol, cls, Ntrain, Ndevel, Ntest):

        db = Database()
        f = db.objects(cls=cls, protocol=protocol)

        self.assertEqual(len(f), Ntrain+Ndevel+Ntest)
        for k in f[:10]:  # only the 10 first...
            if cls == 'attack':
                k.get_attack()
                self.assertRaises(RuntimeError, k.get_realaccess)
            else:
                self.assertTrue(isinstance(k.get_realaccess(), RealAccess))

        train = db.objects(cls=cls, groups='train', protocol=protocol)
        self.assertEqual(len(train), Ntrain)

        dev = db.objects(cls=cls, groups='devel', protocol=protocol)
        self.assertEqual(len(dev), Ndevel)

        test = db.objects(cls=cls, groups='test', protocol=protocol)
        self.assertEqual(len(test), Ntest)

        # tests train, devel, and test files are distinct
        s = set(train + dev + test)
        self.assertEqual(len(s), Ntrain+Ndevel+Ntest)

    @db_available
    def test01_queryRealGrandtest(self):
        self.queryGroupsProtocolsTypes('btas2016',  'real', 0, 0, 5576)

    @db_available
    def test02_queryAttacksGrandtest(self):
        self.queryGroupsProtocolsTypes('btas2016', 'attack', 0, 0, 44920)


    @db_available
    def test03_queryClients(self):

        db = Database()
        f = db.clients()
        self.assertEqual(len(f), 47)  # 1 client
        self.assertTrue(db.has_client_id(0))
        self.assertTrue(db.has_client_id(-1))
        self.assertTrue(db.has_client_id(1))
        self.assertFalse(db.has_client_id(100))

        f = db.clients(gender='male')
        self.assertEqual(len(f), 31)  # 31 male clients
        clients = []
        for c in f:
            clients.append(c.id)
        self.assertIn(1, clients)
        self.assertNotIn(3, clients)
        self.assertIn(30, clients)
        self.assertNotIn(43, clients)

        f = db.clients(gender='female')
        self.assertEqual(len(f), 13)  # 13 female clients
        clients = []
        for c in f:
            clients.append(c.id)
        self.assertNotIn(1, clients)
        self.assertIn(3, clients)
        self.assertNotIn(30, clients)
        self.assertIn(43, clients)
        
        f = db.clients(gender='unknown')
        self.assertEqual(len(f), 3)  # 3 unknown clients

    @db_available
    def test04_queryAudioFile(self):

        db = Database()
        o = db.objects(clients=(0,))[0]
        o.audiofile()

    @db_available
    def test05_manage_files(self):

        from bob.db.base.script.dbmanage import main

        self.assertEqual(main('avspoof_btas2016 files'.split()), 0)

    @db_available
    def test06_manage_dumplist_1(self):

        from bob.db.base.script.dbmanage import main

        self.assertEqual(main('avspoof_btas2016 dumplist --self-test'.split()), 0)

    @db_available
    def test07_manage_dumplist_2(self):

        from bob.db.base.script.dbmanage import main

        self.assertEqual(main(
            'avspoof_btas2016 dumplist --class=attack --group=test --protocol=btas2016 --self-test'.split()), 0)

    @db_available
    def test08_manage_dumplist_client(self):

        from bob.db.base.script.dbmanage import main

        self.assertEqual(main('avspoof_btas2016 dumplist --client=0 --self-test'.split()), 0)

    @db_available
    def test09_manage_checkfiles(self):

        from bob.db.base.script.dbmanage import main

        self.assertEqual(main('avspoof_btas2016 checkfiles --self-test'.split()), 0)

    @db_available
    def queryAttackType(self, protocol, attack, device, N):

        db = Database()
        f = db.objects(cls='attack', support=attack, attackdevices=device, protocol=protocol)
        self.assertEqual(len(f), N)
        for k in f[:10]:  # only the 10 first...
            self.assertTrue(isinstance(k.get_attack(), Attack))


    @db_available
    def test10_queryReplayAttacks(self):
        self.queryAttackType('btas2016', 'unknown', None, 44920)

    @db_available
    def test11_queryReplayAttacksLogicalAccess(self):
        self.queryAttackType('btas2016', 'replay', None, 0)

    @db_available
    def test12_queryLogicalAttacksPhysicalAccess(self):
        self.queryAttackType('btas2016', None, 'logical_access', 0)
