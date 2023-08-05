#!/usr/bin/env python3

import argparse
import tarfile
import os
import sys
import shutil
from fnmatch import fnmatch
from datetime import datetime
import colorama

parser = argparse.ArgumentParser(
    description=" let's compress any log what we need to ")

parser.add_argument('-s', '--src',
                    metavar='source_directory',
                    dest='source_directory',
                    required=True,
                    action='store',
                    help='source directory')

parser.add_argument('-d', '--desc',
                    metavar='des_directory',
                    dest='des_directory',
                    required=True,
                    action='store',
                    help='des directory')

parser.add_argument('-b', '--bak',
                    metavar='bak_directory',
                    dest='bak_directory',
                    required=False,
                    action='store',
                    help='bak directory',
                    default='/home/baakk')

parser.add_argument('-p', '--pattern',
                    metavar='log_pattern',
                    dest='log_pattern',
                    required=True,
                    action='store',
                    help='pattern log file name. accept *')

parser.add_argument('-t', '--time',
                    metavar='time_ago_log | days',
                    type=int,
                    dest='time_ago',
                    required=True,
                    action='store',
                    help='days. when log should be deal with')

args = parser.parse_args()

def main():
    current_time = datetime.timestamp(datetime.now())
    if not os.path.exists(args.bak_directory):
        os.makedirs(args.bak_directory)
    if not os.path.exists(args.source_directory):
        print("Error input source directory. please check again")
        sys.exit(1)
    for deal_root, deal_dirs, deal_files in os.walk(args.source_directory, followlinks=True):
        for deal_file in deal_files:
            try:
                single_file_path = os.path.join(deal_root, deal_file)
            except:
                print("Can not find file :  ", deal_file)
                sys.exit(1)
            create_file_time = os.stat(single_file_path).st_mtime
            if fnmatch(deal_file, args.log_pattern) \
                    and current_time - create_file_time >= 60 * 60 * 24 * int(args.time_ago) \
                    and not fnmatch(deal_file, '*.baakk') \
                    and not fnmatch(deal_file, '*.zip') \
                    and not fnmatch(deal_file, '*.tar') \
                    and not fnmatch(deal_file, '*.tar.gz') \
                    and not fnmatch(deal_file, '*.tar.bz2'):
                if not os.path.exists(args.des_directory):
                    os.makedirs(args.des_directory)
                os.chdir(deal_root)
                tarfile_name = deal_file + '.tar.bz2'
                print(tarfile_name)
                with tarfile.open(tarfile_name, mode='w:bz2') as f:
                    os.chdir(deal_root)
                    f.debug = 1
                    f.add(deal_file)
                shutil.move(os.path.join(deal_root, tarfile_name),
                            args.des_directory)
                bak_file = deal_file + '.baakk'
                os.rename(deal_file, bak_file)
                shutil.move(os.path.join(deal_root, bak_file), args.bak_directory)

if __name__ == '__main__':
    main()
