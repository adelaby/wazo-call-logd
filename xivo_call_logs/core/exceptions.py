# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+


class DatabaseServiceUnavailable(Exception):

    def __init__(self):
        super(DatabaseServiceUnavailable, self).__init__('Postgresql is unavailable')