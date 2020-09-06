# =================================================================
#
# Authors: Francesco Bartoli <xbartolone@gmail.com>
#
# Copyright (c) 2020 Francesco Bartoli
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# =================================================================

import logging

from pygeoapi.provider.base import ProviderGenericError

LOGGER = logging.getLogger(__name__)


class BaseTileProvider:
    """generic Tile Provider ABC"""

    def __init__(self, provider_def):
        """
        Initialize object

        :param provider_def: provider definition

        :returns: pygeoapi.providers.tile.BaseTileProvider
        """

        self.name = provider_def['name']
        self.data = provider_def['data']
        self.format_type = provider_def['format']['name']
        self.mimetype = provider_def['mimetype']
        self.tiling_schemes = provider_def['schemes']
        self.fields = {}

    def get_fields(self):
        """
        Get provider field information (names, types)

        :returns: dict of fields
        """

        raise NotImplementedError()

    def get_tiling_schemes(self):
        """
        Get provider field information (names, types)

        :returns: dict of tiling schemes
        """

        raise NotImplementedError()

    def get_tile_services(self, baseurl, servicepath, tile_type):
        """
        Gets tile service description

        :param baseurl: base URL of endpoint
        :param servicepath: base path of URL
        :param tile_type: tile format type

        :returns: `dict` of file listing or `dict` of GeoJSON item or raw file
        """

        raise NotImplementedError()

    def get_tiles(self, layer, z, y, x, format):
        """
        Gets tiles data

        :param layer: tile layer
        :param z: z index
        :param y: y index
        :param x: x index

        :returns: `binary` of the tile
        """

        raise NotImplementedError()

    def get_metadata_services(self, baseurl, servicepath):
        """
        Gets tile service description

        :param baseurl: base URL of endpoint
        :param servicepath: base path of URL

        :returns: `dict` of the metadata description
        """

        raise NotImplementedError()


class ProviderTileQueryError(ProviderGenericError):
    """provider tile query error"""
    pass


class ProviderTilesetIdNotFoundError(ProviderTileQueryError):
    """provider tileset matrix query error"""
    pass
