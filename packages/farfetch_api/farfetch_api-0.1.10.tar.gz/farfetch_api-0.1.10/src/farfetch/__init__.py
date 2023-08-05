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

from . import address_schema
from . import bag
from . import base
from . import brand
from . import category
from . import checkout_order
from . import city
from . import continent
from . import country
from . import currency
from . import guest_user
from . import merchant_location
from . import merchant
from . import order
from . import payment
from . import product
from . import returns
from . import search
from . import state
from . import user
from . import wishlist

from .address_schema import AddressSchemaApi
from .bag import BagApi
from .base import BASE_URL, AUTH_URL, Api
from .brand import BrandApi
from .category import CategoryApi
from .checkout_order import CheckoutOrderApi
from .city import CityApi
from .continent import ContinentApi
from .country import CountryApi
from .currency import CurrencyApi
from .guest_user import GuestUserApi
from .merchant_location import MerchantLocationApi
from .merchant import MerchantApi
from .order import OrderApi
from .payment import PaymentApi
from .product import ProductApi
from .returns import ReturnApi
from .search import SearchApi
from .state import StateApi
from .user import UserApi
from .wishlist import WishlistApi
