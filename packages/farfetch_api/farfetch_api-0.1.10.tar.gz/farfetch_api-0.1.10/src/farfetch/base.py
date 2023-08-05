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

__author__ = "João Magalhães <joamag@hive.pt> & Rui Castro <rui.castro@gmail.com>"
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

import time

import appier

from . import bag
from . import city
from . import user
from . import brand
from . import state
from . import order
from . import search
from . import country
from . import payment
from . import product
from . import returns
from . import category
from . import currency
from . import merchant
from . import wishlist
from . import continent
from . import guest_user
from . import address_schema
from . import checkout_order
from . import merchant_location

BASE_URL = "https://publicapi.farfetch.com/v1/"
""" The default base url to be used when no other
base url value is provided to the constructor """

AUTH_URL = "https://publicapi.farfetch.com/authentication"
""" The complete url for the authentication process
and retrieval of (authentication) token """

CLIENT_ID = None
""" The default value to be used for the client id
in case no client id is provided to the api client """

CLIENT_SECRET = None
""" The secret value to be used for situations where
no client secret has been provided to the client """

class Api(
    appier.Api,
    bag.BagApi,
    city.CityApi,
    user.UserApi,
    brand.BrandApi,
    state.StateApi,
    order.OrderApi,
    search.SearchApi,
    country.CountryApi,
    payment.PaymentApi,
    product.ProductApi,
    returns.ReturnApi,
    category.CategoryApi,
    currency.CurrencyApi,
    merchant.MerchantApi,
    wishlist.WishlistApi,
    continent.ContinentApi,
    guest_user.GuestUserApi,
    address_schema.AddressSchemaApi,
    checkout_order.CheckoutOrderApi,
    merchant_location.MerchantLocationApi
):

    def __init__(self, *args, **kwargs):
        appier.Api.__init__(self, *args, **kwargs)
        self.base_url = appier.conf("FF_BASE_URL", BASE_URL)
        self.auth_url = appier.conf("FF_AUTH_URL", AUTH_URL)
        self.client_id = appier.conf("FF_CLIENT_ID", None)
        self.client_secret = appier.conf("FF_CLIENT_SECRET", None)
        self.country = appier.conf("FF_COUNTRY", "US")
        self.currency = appier.conf("FF_CURRENCY", "USD")
        self.language = appier.conf("FF_LANGUAGE", "en-US")
        self.base_url = kwargs.get("base_url", self.base_url)
        self.auth_url = kwargs.get("auth_url", self.auth_url)
        self.client_id = kwargs.get("client_id", self.client_id)
        self.client_secret = kwargs.get("client_secret", self.client_secret)
        self.country = kwargs.get("country", self.country)
        self.currency = kwargs.get("currency", self.currency)
        self.language = kwargs.get("language", self.language)
        self.username = kwargs.get("username", None)
        self.password = kwargs.get("password", None)
        self.token = kwargs.get("token", None)
        self.expires_in = kwargs.get("expires_in", None)

    def build(
        self,
        method,
        url,
        data = None,
        data_j = None,
        data_m = None,
        headers = None,
        params = None,
        mime = None,
        kwargs = None
    ):
        auth = kwargs.pop("auth", True)
        if auth: headers["Authorization"] = self.get_token()
        headers["FF-Country"] = kwargs.pop("country", self.country)
        headers["FF-Currency"] = kwargs.pop("currency", self.currency)
        headers["Accept-Language"] = kwargs.pop("language", self.language)
        self.logger.debug(
            "build(...) %s %s headers=%s kwargs=%s data_j=%s" %\
            (method, url, headers, kwargs, data_j)
        )

    def auth_callback(self, params, headers):
        headers["Authorization"] = self.get_token(force = True)

    def get_token(self, force = False):
        not_expired = self.expires_in and self.expires_in > time.time()
        if self.token and not_expired and not force: return self.token
        grant_type, scope = self.get_grant_type()
        contents = self.post(
            self.auth_url,
            callback = False,
            auth = False,
            grant_type = grant_type,
            scope = scope,
            client_id = self.client_id,
            client_secret = self.client_secret,
            username = self.username,
            password = self.password
        )
        self.expires_in = time.time() + contents["expires_in"]
        token_type = contents["token_type"]
        access_token = contents["access_token"]
        self.token = "%s %s" % (token_type, access_token)
        self.trigger("token", self.token, self.expires_in)
        return self.token

    def get_grant_type(self):
        if self.username and self.password:
            grant_type = "password"
            scope = "openid api offline_access"
        else:
            grant_type = "client_credentials"
            scope = "api"
        return grant_type, scope
