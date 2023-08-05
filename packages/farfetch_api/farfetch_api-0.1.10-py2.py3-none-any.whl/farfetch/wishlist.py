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

class WishlistApi(object):

    def get_wishlist(self, id):
        url = self.base_url + "wishlists/%s" % id
        contents = self.get(url)
        return contents

    def add_item_wishlist(self, id, item):
        url = self.base_url + "wishlists/%s/items" % id
        contents = self.post(url, data_j = item)
        return contents

    def update_item_wishlist(self, id, item_id, item_update):
        url = self.base_url + "wishlists/%s/items/%s" % (id, item_id)
        contents = self.patch(url, data_j = item_update)
        return contents

    def remove_item_wishlist(self, id, item_id):
        url = self.base_url + "wishlists/%s/items/%s" % (id, item_id)
        contents = self.delete(url)
        return contents

    def merge_wishlists(self, id, id_source):
        url = self.base_url + "wishlists/%s/merge/%s" % (id, id_source)
        contents = self.post(url)
        return contents
