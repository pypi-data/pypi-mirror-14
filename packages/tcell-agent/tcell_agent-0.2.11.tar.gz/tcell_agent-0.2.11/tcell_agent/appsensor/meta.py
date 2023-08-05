# -*- coding: utf-8 -*-
# Copyright (C) 2015 tCell.io, Inc. - All Rights Reserved

from __future__ import unicode_literals
from __future__ import print_function

class AppSensorMeta(object):
    def __init__(self, remote_address, method, location, route_id, session_id=None, user_id=None, transaction_id=None):
        self.remote_address = remote_address
        self.method = method
        self.location = location
        self.route_id = route_id
        self.session_id = session_id
        self.user_id = user_id
        self.transaction_id = transaction_id