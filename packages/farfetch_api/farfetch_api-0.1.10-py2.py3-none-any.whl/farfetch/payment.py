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

import uuid

class PaymentApi(object):

    def payment_methods(self):
        url = self.base_url + "payments/methods"
        contents = self.get(url)
        return contents

    def create_payment(
        self,
        order_id,
        payment_method_id,
        credit_card = None,
        transaction_id = None,
        redirect_url = None,
        cancel_url = None
    ):
        if not transaction_id:
            transaction_id = str(uuid.uuid4())
            transaction_id = transaction_id.replace("-", "")
        transaction_id = transaction_id[:20]
        payment = dict(
            checkoutOrderId = order_id,
            paymentMethodId = payment_method_id
        )
        if credit_card: payment["creditCard"] = credit_card
        if redirect_url: payment["redirectUrl"] = redirect_url
        if cancel_url: payment["cancelUrl"] = cancel_url
        url = self.base_url + "payments/%s" % transaction_id
        contents = self.put(url, data_j = payment)
        return contents

    def confirm_payment(self, id, parameters = {}):
        url = self.base_url + "payments/%s" % id
        contents = self.patch(
            url,
            data_j = dict(
                confirmationParameters = parameters
            )
        )
        return contents
