from marshmallow import Schema, fields

from .base import WFSObject


class Collection(WFSObject):

    def __init__(self, collectionid, description, title):
        self.collectionid = collectionid
        self.description = description
        self.extent = self._get_bbox()
        self.title = title

    def __repr__(self):
        return '<Collection(name={self.description!r})>'.format(self=self)

#  see model https://github.com/opengeospatial/WFS_FES/blob/master/core/
#  standard/figures/PT1_FIG01.png


class CollectionSchema(Schema):

    collectionid = fields.Number()
    description = fields.Str()
    extent = fields.Str()
    title = fields.Str()
