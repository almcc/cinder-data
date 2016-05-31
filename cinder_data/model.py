from schematics.models import Model
from schematics.types import DateTimeType, IntType


class CinderModel(Model):
    """A basic model that assumes the model has an id attribute.

    Note:
        cinder-data makes use of schematics for it's models. Full documentation on Schematics
        can be found at: https://schematics.readthedocs.io/en/latest/

    Attributes:
        id (:class:`schematics.types.base.IntType`): The model id.
    """

    id = IntType(required=True)


class DjangoModel(CinderModel):
    """A subclass of :class:`.CinderModel` the includes user Django Admin attributes.

    Attributes:
        created_at (:class:`schematics.types.base.DateTimeType`): Django admin created_at
        updated_at (:class:`schematics.types.base.DateTimeType`): Django admin updated_at
    """

    created_at = DateTimeType()
    updated_at = DateTimeType()
