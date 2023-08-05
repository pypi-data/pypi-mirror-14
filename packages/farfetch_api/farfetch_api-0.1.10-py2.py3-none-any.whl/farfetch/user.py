#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Farfetch API
# Copyright (c) 2008-2016 Hive Solutions Lda.
#
# This file is part of Hive Farfetch API.
#
# Hive Farfetch API is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Farfetch API is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Farfetch API. If not, see <http://www.apache.org/licenses/>.

__author__ = "Rui Castro <rui.castro@gmail.com>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2016 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

class UserApi(object):

    def create_user(self, user):
        url = self.base_url + "users"
        contents = self.post(url, data_j = user)
        return contents

    def get_user(self, id):
        url = self.base_url + "users/%s" % id
        contents = self.get(url)
        return contents

    def me_user(self):
        url = self.base_url + "users/Me"
        contents = self.get(url)
        return contents

    def update_user(self, id, user):
        url = self.base_url + "users/%s" % id
        contents = self.put(url, data_j = user)
        return contents

    def password_recovery_user(self, username, uri):
        url = self.base_url + "users/password-recovery"
        contents = self.post(url, data_j = dict(username = username, uri = uri))
        return contents

    def password_reset_user(self, username, password, token):
        url = self.base_url + "users/password-reset"
        contents = self.post(
            url,
            data_j = dict(
                username = username,
                password = password,
                token = token
            )
        )
        return contents

    def password_change_user(self, id, username, oldPassword, password):
        # changes the password (even though the api
        # asks for the previous password and the
        # username, it doesn't do anything with them)
        url = self.base_url + "users/%s/password-change" % id
        contents = self.post(
            url,
            data_j = dict(
                username = username,
                oldPassword = oldPassword,
                newPassword = password
            )
        )
        return contents

    def addresses_user(self, user_id):
        url = self.base_url + "users/%s/addresses" % user_id
        contents = self.get(url)
        return contents

    def address_user(self, user_id, address_id):
        url = self.base_url + "users/%s/addresses/%s" % (user_id, address_id)
        contents = self.get(url)
        return contents

    def shipping_address_user(self, user_id):
        url = self.base_url + "users/%s/addresses/shipping/current" % user_id
        contents = self.get(url)
        return contents

    def billing_address_user(self, user_id):
        url = self.base_url + "users/%s/addresses/billing/current" % user_id
        contents = self.get(url)
        return contents

    def update_shipping_address_user(self, user_id, address_id):
        url = self.base_url + "users/%s/addresses/shipping/%s" % (user_id, address_id)
        contents = self.put(url, data_j = dict())
        return contents

    def update_billing_address_user(self, user_id, address_id):
        url = self.base_url + "users/%s/addresses/billing/%s" % (user_id, address_id)
        contents = self.put(url, data_j = dict())
        return contents

    def create_address_user(self, user_id, address):
        url = self.base_url + "users/%s/addresses" % user_id
        contents = self.post(url, data_j = address)
        return contents

    def update_address_user(self, user_id, address_id, address):
        url = self.base_url + "users/%s/addresses/%s" % (user_id, address_id)
        contents = self.put(url, data_j = address)
        return contents

    def delete_address_user(self, user_id, address_id):
        url = self.base_url + "users/%s/addresses/%s" % (user_id, address_id)
        contents = self.delete(url)
        return contents

    def orders_user(self, user_id, page = None, page_size = None):
        url = self.base_url + "users/%s/orders" % user_id
        params = dict(
            page = page,
            pageSize = page_size
        )
        contents = self.get(url, params = params)
        return contents

    def payments_user(self, user_id):
        url = self.base_url + "users/%s/tokens" % user_id
        contents = self.get(url)
        return contents
