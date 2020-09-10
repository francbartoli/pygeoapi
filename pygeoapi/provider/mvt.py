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
import requests
from urllib.parse import urlparse, urljoin

from pygeoapi.provider.tile import BaseTileProvider


LOGGER = logging.getLogger(__name__)


class MVTProvider(BaseTileProvider):
    """MVT Provider"""

    def __init__(self, provider_def):
        """
        Initialize object

        :param provider_def: provider definition

        :returns: pygeoapi.provider.MVT.MVTProvider
        """

        BaseTileProvider.__init__(self, provider_def)

        # if not os.path.exists(self.data):
        #     msg = 'Service does not exist: {}'.format(self.data)
        #     LOGGER.error(msg)
        #     raise ProviderConnectionError(msg)

    def __repr__(self):
        return '<MVTProvider> {}'.format(self.data)

    def get_layer(self):

        url = urlparse(self.data)

        return url.path.split("/{z}/{x}/{y}")[0][1:]

    def get_tiling_schemes(self):

        tile_matrix_set_links_list = [{
                'tileMatrixSet': 'WorldCRS84Quad',
                'tileMatrixSetURI': 'http://schemas.opengis.net/tms/1.0/json/examples/WorldCRS84Quad.json'  # noqa
            }, {
                'tileMatrixSet': 'WebMercatorQuad',
                'tileMatrixSetURI': 'http://schemas.opengis.net/tms/1.0/json/examples/WebMercatorQuad.json'  # noqa
            }]
        tile_matrix_set_links = [
            item for item in tile_matrix_set_links_list if item[
                'tileMatrixSet'] in self.schemes]

        return tile_matrix_set_links

    def get_tiles_service(self, baseurl=None, servicepath=None,
                          dirpath=None, tile_type=None):
        """
        Gets mvt service description

        :param baseurl: base URL of endpoint
        :param servicepath: base path of URL
        :param dirpath: directory basepath (equivalent of URL)
        :param tile_type: tile format type

        :returns: `dict` of item tile service
        """

        url = urlparse(self.data)
        baseurl = baseurl or '{}://{}'.format(url.scheme, url.netloc)
        # @TODO: support multiple types
        tile_type = tile_type or self.format_type
        servicepath = \
            servicepath or \
            '{}/tiles/{{{}}}/{{{}}}/{{{}}}/{{{}}}{}'.format(
                url.path.split('/{z}/{x}/{y}')[0],
                'tileMatrixSetId',
                'tileMatrix',
                'tileRow',
                'tileCol',
                tile_type)

        service_url = urljoin(baseurl, servicepath)
        service_metadata_url = urljoin(
            service_url.split('{tileMatrix}/{tileRow}/{tileCol}')[0],
            'metadata')

        links = {
            'links': [{
                'type': self.mimetype,
                'rel': 'item',
                'title': 'This collection as Mapbox vector tiles',
                'href': service_url,
                'templated': True
            }, {
                'type': 'application/json',
                'rel': 'describedby',
                'title': 'Metadata for this collection in the TileJSON format',
                'href': '{}?f=json'.format(service_metadata_url),
                'templated': True
            }]
        }

        return links

    def get_tiles(self, layer=None, tileset=None,
                  z=None, y=None, x=None, format_=None):
        """
        Gets tile

        :param layer: mvt tile layer
        :param tileset: mvt tileset
        :param z: z index
        :param y: y index
        :param x: x index
        :param format_: tile format

        :returns: an encoded mvt tile
        """
        if format_ == "mvt":
            format_ = self.format_type
        url = urlparse(self.data)
        base_url = '{}://{}'.format(url.scheme, url.netloc)
        with requests.Session() as session:
            session.get(base_url)
            resp = session.get('{base_url}/{lyr}/{z}/{y}/{x}.{f}'.format(
                base_url=base_url, lyr=layer,
                z=z, y=y, x=x, f=format_))
            resp.raise_for_status()
            return resp.content

    def get_metadata(self, tilejson=True):
        """
        Helper function to describe a vector tile service

        :returns: `dict` of JSON metadata
        """

        content = {
            "tilejson" : "3.0.0"
        }

        return content
