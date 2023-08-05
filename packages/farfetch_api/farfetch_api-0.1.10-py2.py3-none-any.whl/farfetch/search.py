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

class SearchApi(object):

    def search_products(
        self,
        q = None,
        page = None,
        page_size = None,
        sort = None,
        filters = None
    ):
        url = self.base_url + "search/products"
        params = dict(
            q = q,
            page = page,
            pageSize = page_size,
            sort = sort
        )
        if filters: params.update(filters)
        contents = self.get(url, params = params)
        return contents

    def facets_product(self):
        url = self.base_url + "search/products/facets"
        contents = self.get(url)
        return contents

    def search_suggestions(self, search_terms, gender = None):
        url = self.base_url + "search/suggestions"
        params = dict(
            search_terms = search_terms
        )
        if gender: params["gender"] = gender
        contents = self.get(url, params = params)
        return contents

    def search_stopwords(self, search_terms, gender = None):
        url = self.base_url + "search/stopwords"
        params = dict(
            search_terms = search_terms
        )
        if gender: params["gender"] = gender
        contents = self.get(url, params = params)
        return contents
