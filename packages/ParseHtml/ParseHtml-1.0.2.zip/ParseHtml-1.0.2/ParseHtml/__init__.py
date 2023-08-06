#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# email: 2647078704@qq.com

from __future__ import unicode_literals, division, absolute_import, \
                        print_function

import re
import BeautifulSoup


def parse_text(contents_string):
    Newlines = re.compile(r'[\r\n]\s+')
    bs = BeautifulSoup.BeautifulSoup(contents_string, convertEntities=BeautifulSoup.BeautifulSoup.HTML_ENTITIES)
    txt = bs.getText('\n')
    return Newlines.sub('\n', txt)
