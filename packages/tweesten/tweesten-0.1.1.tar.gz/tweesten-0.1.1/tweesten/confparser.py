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
# along with this program.  If not, see <http://www.gnu.org/licenses/

# Get values of the configuration file
'''Get values of the configuration file'''

# standard library imports
import configparser
import sys


class ConfParser(object):
    '''ConfParser class'''
    def __init__(self, pathtoconf):
        self.consumer_key = ''
        self.consumer_secret = ''
        self.access_token = ''
        self.access_token_secret = ''
        self.pathtoconf = pathtoconf
        self.size = ''
        self.fromlast = ''
        self.username = ''
        self.message = ''
        self.main()

    def main(self):
        '''Main of the ConfParser class'''
        # read the configuration file
        conf = configparser.ConfigParser()
        try:
            with open(self.pathtoconf) as conffile:
                conf.read_file(conffile)
                if conf.has_section('main'):
                    self.consumer_key = conf.get('main', 'consumer_key')
                    self.consumer_secret = conf.get('main',
                                                    'consumer_secret')
                    self.access_token = conf.get('main', 'access_token')
                    self.access_token_secret = conf.get('main',
                                                        'access_token_secret')
                    self.size = conf.get('main', 'size')
                    self.fromlast = conf.get('main', 'fromlast')
                    self.username = conf.get('main', 'username')
                    self.caption = conf.get('main', 'caption')
                    self.message = conf.get('main', 'message')
        except (configparser.Error, IOError, OSError) as err:
            print(err)
            sys.exit(1)

    @property
    def confvalues(self):
        '''get the values of the configuration file'''
        return {'consumer_key': self.consumer_key,
                'consumer_secret': self.consumer_secret,
                'access_token': self.access_token,
                'access_token_secret': self.access_token_secret,
                'size': self.size,
                'fromlast': self.fromlast,
                'username': self.username,
                'caption': self.caption,
                'message': self.message}
