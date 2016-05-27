from schematics.models import Model
from schematics.types import IntType, DateTimeType


class CinderModel(Model):
    id = IntType(required=True)


class DjangoModel(CinderModel):
    created_at = DateTimeType()
    updated_at = DateTimeType()
