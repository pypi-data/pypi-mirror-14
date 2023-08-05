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

class CheckoutOrderApi(object):

    def get_checkout_order(self, id):
        url = self.base_url + "checkoutOrders/%s" % id
        contents = self.get(url)
        return contents

    def update_checkout_order(self, id, checkout_order):
        url = self.base_url + "checkoutOrders/%s" % id
        contents = self.put(url, data_j = checkout_order)
        return contents

    def update_addresses_checkout_order(
        self,
        id,
        shipping_address = None,
        billing_address = None
    ):
        url = self.base_url + "checkoutOrders/%s" % id
        checkout_order = dict()
        if shipping_address: checkout_order["shippingAddress"] = shipping_address
        if billing_address: checkout_order["billingAddress"] = billing_address
        contents = self.patch(url, data_j = checkout_order)
        return contents

    def shipping_options_checkout_order(self, id):
        url = self.base_url + "checkoutOrders/%s/shippingOptions" % id
        contents = self.get(url)
        return contents

    def update_shipping_options_checkout_order(self, id, shipping_options):
        url = self.base_url + "checkoutOrders/%s/shippingOptions" % id
        contents = self.put(url, data_j = shipping_options)
        return contents

    def create_promocode_checkout_order(self, id, code):
        url = self.base_url + "checkoutOrders/%s/Promocode" % id
        params = dict(
            code = code
        )
        contents = self.post(url, params = params)
        return contents
