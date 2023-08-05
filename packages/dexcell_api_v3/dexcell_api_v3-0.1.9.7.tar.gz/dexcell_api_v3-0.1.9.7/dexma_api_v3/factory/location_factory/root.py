__author__ = 'dcortes'

from schematics.models import Model
from schematics.types import StringType, IntType

from dexma_api_v3.factory.custom_types.unsigned_long import UnsignedLong
from dexma_api_v3.factory.base_entity import BaseEntity


class Root(BaseEntity):

    name = StringType(required=True)
    type = StringType(required=True)

