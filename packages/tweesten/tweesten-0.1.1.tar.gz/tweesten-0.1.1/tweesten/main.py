# -*- coding: utf-8 -*-
# Copyright © 2015 Raúl Benito <erre.benito@gmail.com>
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

# Main class
'''Main class'''

# standard library imports
import configparser
import os
import sys

# external library imports
import tweepy

# tweesten imports
from tweesten.cliparser import CLIParser
from tweesten.confparser import ConfParser
from tweesten.imagefetcher import ImageFetcher


class Main(object):
    '''Main class'''
    def __init__(self):
        '''Constructor of the Main class'''
        # parse the command line
        cliargs = CLIParser()
        self.args = cliargs.arguments
        # read the configuration file
        cfgparse = ConfParser(self.args.pathtoconf)
        self.cfgvalues = cfgparse.confvalues

        # activate the twitter api
        self.auth = tweepy.OAuthHandler(self.cfgvalues['consumer_key'],
                                        self.cfgvalues['consumer_secret'])
        self.auth.secure = True
        self.auth.set_access_token(self.cfgvalues['access_token'],
                                   self.cfgvalues['access_token_secret'])
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True,
                              wait_on_rate_limit_notify=True)
        self.main()

    def main(self):
        '''Main of the Main class'''
        
        imageFetcher = ImageFetcher(self.cfgvalues)
        upload = self.api.media_upload(os.path.realpath('collage.png'))
        ids = [upload.media_id_string]
        result = self.api.update_status(status=self.cfgvalues['message'], media_ids=ids)
        os.remove('collage.png')
        sys.exit(0)
