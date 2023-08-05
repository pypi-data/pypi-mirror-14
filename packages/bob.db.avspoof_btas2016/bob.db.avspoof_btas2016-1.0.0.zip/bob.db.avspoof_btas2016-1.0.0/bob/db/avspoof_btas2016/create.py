#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Pavel Korshunov <pavel.korshunov@idiap.ch>
# Wed 19 Aug 13:43:50 2015

"""This script creates the AVSpoof database in a single pass.
"""

from __future__ import print_function

import fnmatch

from .models import *

# setup logging
import bob.core
logger = bob.core.log.setup("AVspoofLogger")


def add_clients(session, protodir, verbose):
    """Add clients to the avspoof database."""

    for client in open(os.path.join(protodir, 'clients-grandtest-allsupports.txt'), 'rt'):
        s = client.strip().split(' ', 2)
        if not s: continue  # empty line
        id = int(s[0][1:])
        set = s[1]
        if s[0][0] == 'f':
            gender = 'female'
        elif s[0][0] == 'm':
            gender = 'male'
        else:
            gender = 'unknown'
        logger.info("Adding client %d, %s into '%s' set...", id, gender, set)
        # if verbose:
            # print("Adding client %d, %s into '%s' set..." % (id, gender, set))
        session.add(Client(id, gender, set))
        session.flush()


def add_real_lists(session, protodir, verbose):
    """Adds all RCD filelists"""

    def add_real_list(session, filename):
        """Adds an RCD filelist and materializes RealAccess'es."""

        def parse_real_filename(f):
            """Parses the RCD filename and break it in the relevant chunks."""

            v = os.path.splitext(f)[0].split('/')
            # if this is a special randomize file then create an empty data entries for it
            if len(v) < 3:
                return [0, 'unknown', f, 'unknown', 'unknown', 'unknown']

            client_id = int(v[2][1:])
            path = f  # keep only the filename stem
            gender = v[1]
            sess = v[3]  # recording session
            device = v[4]
            speech = v[5]
            return [client_id, gender, path, device, sess, speech]

        logger.warn("Adding list %s", filename)
        # if verbose: print ("Adding list %s" % filename)
        for fname in open(filename, 'rt'):
            s = fname.strip()
            if not s: continue  # emtpy line
            # if verbose: print (s)
            logger.info(s)
            filefields = parse_real_filename(s)
            logger.info("Adding File %s in database", str(filefields))
            filefields[0] = session.query(Client).filter(Client.id == filefields[0]).one()
            #                                                    Client.gender == filefields[1]).one()
            file = File(*filefields)
            session.add(file)
            realfields = [file]
            session.add(RealAccess(*realfields))

    add_real_list(session, os.path.join(protodir, 'real-btas2016-allsupports-test.txt'))

#    add_real_list(session, os.path.join(protodir, 'real-physical_access-allsupports-train.txt'))
#    add_real_list(session, os.path.join(protodir, 'real-physical_access-allsupports-devel.txt'))
#    add_real_list(session, os.path.join(protodir, 'real-physical_access-allsupports-test.txt'))

    # add_real_list(session, os.path.join(protodir, 'real-grandtest-allsupports-train.txt'))
    # add_real_list(session, os.path.join(protodir, 'real-grandtest-allsupports-devel.txt'))
    # add_real_list(session, os.path.join(protodir, 'real-grandtest-allsupports-test.txt'))

    # add_real_list(session, os.path.join(protodir, 'real-smalltest-allsupports-train.txt'))
    # add_real_list(session, os.path.join(protodir, 'real-smalltest-allsupports-devel.txt'))
    # add_real_list(session, os.path.join(protodir, 'real-smalltest-allsupports-test.txt'))


def add_attack_lists(session, protodir, verbose):
    """Adds all RAD filelists"""

    def add_attack_list(session, filename):
        """Adds a filelist and materializes Attacks."""

        def parse_attack_filename(f):
            """Parses the filename and break it in the relevant chunks."""

            v = os.path.splitext(f)[0].split('/')
            # if this is a special randomize file then create an empty data entries for it
            if len(v) < 3:
                return [0, 'unknown', f, 'unknown', 'unknown', 'unknown'], ['unknown', 'unknown']

            # parse attacks first
            attack_parts = v[1].split('_')
            if attack_parts[0] == "replay":
                attack_support = attack_parts[0]  # replay attack
                attack_device = "_".join(attack_parts[1:])  # the rest of the attack
            else:
                attack_support = "_".join(attack_parts[0:2])  # attacks consisting of more than one word
                attack_device = "_".join(attack_parts[2:])

            client_id = int(v[3][1:])
            path = f  # keep only the filename stem
            gender = v[2]
            # speech synthesis is strangely generated, diff from all other files
            if attack_support == "speech_synthesis":
                sstr = v[4].split('_')
                if "Sess" in sstr[1]:  # the string is Session#
                    speech = "read"
                    sess = "sess" + sstr[1][-1]
                elif "Pass" in sstr[1]:
                    speech = "pass"
                    sess = "sess2"  # it's not specified in the file name, so assume 2
                else:
                    speech = "free"
                    sess = "sess2"
                device = "laptop"  # speech synthesis is from laptop data
            else:  # all the rest of the attacks
                sess = v[4]  # recording session
                device = v[5]
                speech = v[6]

            return [client_id, gender, path, device, sess, speech], [attack_support, attack_device]

        logger.warn("Adding list %s", filename)
        # if verbose: print ("Adding list %s" % filename)
        for fname in open(filename, 'rt'):
            s = fname.strip()
            if not s: continue  # emtpy line
            # if verbose: print (s)
            logger.info(s)
            filefields, attackfields = parse_attack_filename(s)
            logger.info("Adding File %s and Attack %s in database", str(filefields), str(attackfields))
            filefields[0] = session.query(Client).filter(
                Client.id == filefields[0] and \
                Client.gender == filefields[1]).one()
            file = File(*filefields)
            session.add(file)
            attackfields.insert(0, file)
            session.add(Attack(*attackfields))

    add_attack_list(session, os.path.join(protodir, 'attack-btas2016-allsupports-test.txt'))

#    add_attack_list(session, os.path.join(protodir, 'attack-physical_access-allsupports-train.txt'))
#    add_attack_list(session, os.path.join(protodir, 'attack-physical_access-allsupports-devel.txt'))
#    add_attack_list(session, os.path.join(protodir, 'attack-physical_access-allsupports-test.txt'))

    # add_attack_list(session,os.path.join(protodir, 'attack-smalltest-allsupports-train.txt'))
    # add_attack_list(session,os.path.join(protodir, 'attack-smalltest-allsupports-devel.txt'))
    # add_attack_list(session,os.path.join(protodir, 'attack-smalltest-allsupports-test.txt'))

    # add_attack_list(session, os.path.join(protodir, 'attack-grandtest-allsupports-train.txt'))
    # add_attack_list(session, os.path.join(protodir, 'attack-grandtest-allsupports-devel.txt'))
    # add_attack_list(session, os.path.join(protodir, 'attack-grandtest-allsupports-test.txt'))


def define_protocols(session, protodir, verbose):
    """Defines all available protocols"""

    # figures out which protocols to use
    valid = {}

    for fname in fnmatch.filter(os.listdir(protodir), 'attack-*-allsupports-train.txt'):
        s = fname.split('-', 4)

        consider = True
        files = {}

        for grp in ('train', 'devel', 'test'):

            # check attack file
            attack = os.path.join(protodir, 'attack-%s-allsupports-%s.txt' % (s[1], grp))
            if not os.path.exists(attack):
                logger.error("Not considering protocol %s as attack list '%s' was not found", s[1], attack)
                # if verbose:
                #     print("Not considering protocol %s as attack list '%s' was not found" % (s[1], attack))
                consider = False

            # check real file
            real = os.path.join(protodir, 'real-%s-allsupports-%s.txt' % (s[1], grp))
            if not os.path.exists(real):
                alt_real = os.path.join(protodir, 'real-%s.txt' % (grp,))
                if not os.path.exists(alt_real):
                    logger.error("Not considering protocol %s as real list '%s' or '%s' were not found",
                                 s[1], real, alt_real)
                    # if verbose:
                    #     print("Not considering protocol %s as real list '%s' or '%s' were not found" %
                    #           (s[1], real, alt_real))
                    consider = False
                else:
                    real = alt_real

            if consider: files[grp] = (attack, real)

        if consider: valid[s[1]] = files

    for protocol, groups in valid.items():
        logger.warn("Creating protocol '%s'...", protocol)
        # if verbose: print("Creating protocol '%s'..." % protocol)

        # create protocol on the protocol table
        obj = Protocol(name=protocol)

        for grp, flist in groups.items():

            counter = 0
            for fname in open(flist[0], 'rt'):
                s = os.path.splitext(fname.strip())[0]
                q = session.query(Attack).join(File).filter(File.path == s).one()
                q.protocols.append(obj)
                counter += 1
            logger.warn("  -> %5s/%-6s: %d files", grp, "attack", counter)
            # if verbose: print("  -> %5s/%-6s: %d files" % (grp, "attack", counter))

            counter = 0
            for fname in open(flist[1], 'rt'):
                s = os.path.splitext(fname.strip())[0]
                q = session.query(RealAccess).join(File).filter(File.path == s).one()
                q.protocols.append(obj)
                counter += 1
            logger.warn("  -> %5s/%-6s: %d files", grp, "real", counter)
            # if verbose: print("  -> %5s/%-6s: %d files" % (grp, "real", counter))

        session.add(obj)


def create_tables(args):
    """Creates all necessary tables (only to be used at the first time)"""

    from bob.db.base.utils import create_engine_try_nolock

    engine = create_engine_try_nolock(args.type, args.files[0], echo=(args.verbose > 2))
    Client.metadata.create_all(engine)
    RealAccess.metadata.create_all(engine)
    Attack.metadata.create_all(engine)
    Protocol.metadata.create_all(engine)


# Driver API
# ==========

def create(args):
    """Creates or re-creates this database"""

    # set verbosity level
    bob.core.log.set_verbosity_level(logger, args.verbose)

    from bob.db.base.utils import session_try_nolock

    dbfile = args.files[0]

    if args.recreate:
        if args.verbose and os.path.exists(dbfile):
            print('unlinking %s...' % dbfile)

        if os.path.exists(dbfile): os.unlink(dbfile)

    if not os.path.exists(os.path.dirname(dbfile)):
        os.makedirs(os.path.dirname(dbfile))

    # the real work...
    create_tables(args)
    s = session_try_nolock(args.type, args.files[0], echo=(args.verbose > 2))
    add_clients(s, args.protodir, args.verbose)
    add_real_lists(s, args.protodir, args.verbose)
    add_attack_lists(s, args.protodir, args.verbose)
    define_protocols(s, args.protodir, args.verbose)
    s.commit()
    s.close()

    return 0


def add_command(subparsers):
    """Add specific subcommands that the action "create" can use"""

    parser = subparsers.add_parser('create', help=create.__doc__)

    parser.add_argument('-R', '--recreate', action='store_true', default=False,
                        help="If set, I'll first erase the current database")
    # parser.add_argument('-v', '--verbose', action='count', default=0,
    #                     help="Do SQL operations in a verbose way")
    # pavel - for now, store protocols in the same package
    parser.add_argument('-D', '--protodir', action='store',
                        # default='/remote/idiap.svm/home.active/pkorshunov/src/bob.db.avspoof/bob/db/avspoof/protocols/',
                        default='/Users/pavelkor/Documents/pav/idiap/src/bob.db.avspoof_btas2016/bob/db/avspoof_btas2016/protocols/',
                        metavar='DIR',
                        help="Change the relative path to the directory containing the protocol definitions for avspoof attacks (defaults to %(default)s)")

    # add verbose option
    bob.core.log.add_command_line_option(parser)

    parser.set_defaults(func=create)  # action
