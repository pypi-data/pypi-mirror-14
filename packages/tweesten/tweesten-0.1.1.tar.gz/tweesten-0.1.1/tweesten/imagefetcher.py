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

# Image fetching
'''Image fetching'''

import urllib.request


class ImageFetcher(object):
    '''ImageFetcher class'''
    def __init__(self, cfgvalues):
        '''Constructor for the ImageFetcher class'''
        self.cfgvalues = cfgvalues
        self.main()

    def main(self):
        '''main of ImageFetcher class'''
        self.baseurl = 'http://www.tapmusic.net/collage.php'
        self.baseurl += '?user='
        self.baseurl += self.cfgvalues['username']
        self.baseurl += '&type='
        self.baseurl += self.cfgvalues['fromlast']
        self.baseurl += '&size='
        self.baseurl += self.cfgvalues['size']
        self.baseurl += '&caption='
        self.baseurl += self.cfgvalues['caption']

        with open('collage.png', 'wb') as file:
            file.write(urllib.request.urlopen(self.baseurl).read())
            file.close()
        
    @property
    def url(self):
        return self.baseurl
