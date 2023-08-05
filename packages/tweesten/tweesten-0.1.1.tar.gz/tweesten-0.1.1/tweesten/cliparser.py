# -*- coding: utf-8 -*-
# Copyright © 2016 Raúl Benito <erre.benito@gmail.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

# CLI argument parsing
'''CLI argument parsing'''

from argparse import ArgumentParser
import os.path
import sys


class CLIParser(object):
    '''CLIParser class'''
    def __init__(self):
        '''Constructor for the CLIParser class'''
        self.main()

    def main(self):
        '''main of CLIParser class'''
        tweestenepilog = 'Homepage: https://github.com/errebenito/tweesten'
        tweestendescription = 'tweets album covers of your last.fm scrobbles'
        parser = ArgumentParser(prog='tweesten',
                                description=tweestendescription,
                                epilog=tweestenepilog)
        parser.add_argument('pathtoconf', metavar='FILE', type=str,
                            help='the path to the tweesten configuration')
        args = parser.parse_args()
        if not os.path.exists(args.pathtoconf):
            print('the path you provided for the configuration does not exist')
            sys.exit(1)
        if not os.path.isfile(args.pathtoconf):
            print('the path you provided for the configuration is not a file')
            sys.exit(1)
        self.args = args

    @property
    def arguments(self):
        '''return the path to the config file'''
        return self.args
