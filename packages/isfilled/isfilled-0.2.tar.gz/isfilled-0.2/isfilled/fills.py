from isfilled.models import Fill
from isfilled.util import import_string

class Filled(object):
    def __init__(self, instance=None):
        self.instance = instance

    def default_fields(self):
        if self.instance and self.instance.model:
            res = [k.name for k in self.instance.model_model()._meta.get_fields()]
        elif self.instance.fill:
            res = self.form().fields.keys()
        else:
            raise Exception("Something is wrong")
        return res

    def fields(self, keys, exclude=[]):
        return list(set(keys) - set(exclude))

    def is_filled(self):
        return True

    def is_field_filled(self, instance, field):
        # not all form fields are model fields; ignore
        if not hasattr(instance, field):
            return True
        return getattr(instance, field)

    def verify(self, instance, fields):
        return all(self.is_field_filled(instance, k) for k in fields)

class FillsMixin(object):
    """ Fills superpowers for Models """

    def registered_model_fills(self):
        return Fill.objects.filter(model=self._meta.label)

    def as_fills(self, fills):
        return [import_string(fill.fill) if fill.fill else None for fill in fills]

    def check_fills(self, fills=[]):
        registered_model_fills = fills or self.registered_model_fills()
        registered_fills = self.as_fills(registered_model_fills)
        def _fields(fill, instance):
            return fill.fields(keys=instance.fields or fill.default_fields(),
                        exclude=instance.exclude or [],)
        def _verify(fill, instance):
            fill_instance = fill(instance=instance) if fill else Filled(instance=instance)
            flds = _fields(fill_instance, instance)
            return fill_instance.verify(self, flds)

        ctxs = {fill: _verify(fill, ins) for fill, ins in 
                    zip(registered_fills, registered_model_fills)}
        return (all(ctxs.values()), ctxs)

    def check_fill(self, fill):
        self.check_fills([fill])

