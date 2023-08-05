#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Pavel Korshunov <pavel.korshunov@idiap.ch>
# Mon  18 Aug 23:12:22 CEST 2015
#
# Copyright (C) 2012-2015 Idiap Research Institute, Martigny, Switzerland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the ipyplotied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
The script generates text file lists for grandtest protocol using the file names and
the directory structure of the AVspoof database. These lists are later used to build an SQL-based
bob.db interface for AVspoof database.
"""
from __future__ import print_function

import os
import math
import argparse


def listFiles(rootdir="."):
    objs = []
    for root, dirs, files in os.walk(rootdir):
        _, path = root.split(rootdir)
        path = path.split(os.path.sep)
        gender = "male"  # female also ends with "male", so we cover both
        if gender in root:
            for sample in files:
                sample, ext = os.path.splitext(sample)
                if ext == ".wav":
                    subpath = path[1:]
                    subpath.append(sample)
                    start_id_indx = root.index(gender) + len(gender) + 1
                    id = root[start_id_indx:start_id_indx + 4]
                    objs.append((os.path.join(*subpath), id))
    return objs


def getIds(rootdir=".", gender="male", filter="genuine"):
    ids = []
    for root, dirs, files in os.walk(rootdir):
        curdir = os.path.basename(root)
        if curdir == gender and filter in root:
            ids = dirs
            break
    return ids


def getSubIds(ids, set="train"):
    subids = []

    if not ids:
        return subids

    #  indices=numpy.arange(len(ids))

    sublen = int(math.floor(len(ids) / 3))

    if set == "train":
        subids = ids[0:sublen]
    elif set == "devel":
        subids = ids[sublen:2 * sublen]
    elif set == "test":
        subids = ids[2 * sublen:]

    return subids


#  numpy.choice(ids)


def command_line_arguments(command_line_parameters):
    """Parse the program options"""

    # set up command line parser
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-d', '--database-directory', required=False,
                        help="The root directory of database data.")

    # parse arguments
    args = parser.parse_args(command_line_parameters)

    return args


def main(command_line_parameters=None):
    """Traverses the folder structure of AVspoof database and create file lists corresponding
    to train, devel, and test sets indicating genuine or spoofed samples."""

    args = command_line_arguments(command_line_parameters)

    rootdir = os.path.curdir
    if args.database_directory:
        rootdir = args.database_directory

    data_types = ["genuine", "attack"]
    sets = ["train", "devel", "test"]
    prefix = "-grandtest-allsupports"
    #    prefix = "-smalltest-allsupports"

    # fix ids split for the whole thing, so we are consistent across diff filters
    male_ids = getIds(rootdir, "male", data_types[0])
    female_ids = getIds(rootdir, "female", data_types[0])

    # traverse database and construct the whole list of files
    file_list = listFiles(rootdir)

    # write clients' Ids for train, devel, and test subsets into the file
    fid = open("clients%s.txt" % (prefix), "w")
    for set in sets:
        #   if not os.path.exists(set):
        #     os.makedirs(set)
        set_ids = getSubIds(male_ids, set)
        set_ids.extend(getSubIds(female_ids, set))
        print("set %s, set_ids: %s " % (set, " ".join(client_id for client_id in set_ids)))
        fid.write('\n'.join("%s %s" % (client_id, set) for client_id in set_ids))
        fid.write('\n')  # wrote all client Ids
        for data_type in data_types:
            # get ids for the specific set
            # set_ids = getSubIds(male_ids, set)
            # set_ids.extend(getSubIds(female_ids, set))
            # print "set %s, set_ids: %s " %(set, " ".join(id for id in set_ids))

            # construct the sublist for the current set and the current data_type
            list4set = []
            for item in file_list:
                if item[1] in set_ids and data_type in item[0]:
                    list4set.append(item[0])

            filename = ""
            if data_type == "genuine":
                filename = "real%s-%s.txt" % (prefix, set)
            if data_type == "attack":
                filename = "attack%s-%s.txt" % (prefix, set)
            # write file names either into real or attack file list
            with open(filename, "w") as f:
                f.write('\n'.join(stem for stem in list4set))
                f.close()

    fid.close()


if __name__ == '__main__':
    main()
