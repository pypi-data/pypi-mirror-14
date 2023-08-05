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

__author__ = "Rui Castro <rui.castro@gmail.com> & João Magalhães <joamag@hive.pt>"
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

class MerchantLocationApi(object):

    def list_merchant_locations(self, merchant_id = None):
        if merchant_id: url = self.base_url + "merchantsLocations/" + str(merchant_id)
        else: url = self.base_url + "merchantsLocations"
        contents = self.get(url)
        return contents

    def list_merchant_locations_near_me(self, latitude, longitude, page = None, page_size = None):
        url = self.base_url + "merchantsLocations/nearMe"
        params = dict(
            lat = latitude,
            lon = longitude
        )
        if not page == None: params["page"] = page
        if not page_size == None: params["pageSize"] = page_size
        contents = self.get(url, params = params)
        return contents
