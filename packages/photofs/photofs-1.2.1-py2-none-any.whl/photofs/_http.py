# coding: utf-8
# photofs
# Copyright (C) 2012-2016 Moses Palmér
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.

import urllib3


#: The connection pool
__http = urllib3.PoolManager()


def request(method, *args, **kwargs):
    """Initiates an HTTP request.

    This function is shorthand for
    ``urllib3.PoolManager().request(method, *args, **kwargs)´´.

    :param str method: The HTTP verb.
    """
    return __http.request(method, *args, **kwargs)
