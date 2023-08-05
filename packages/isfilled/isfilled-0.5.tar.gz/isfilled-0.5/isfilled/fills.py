from django.core.exceptions import ObjectDoesNotExist

from isfilled.models import Fill
from isfilled.util import import_string

class Filled(object):
    name = None
    fields = []
    exclude = []

    def __init__(self, instance=None):
        self.instance = instance

    def default_fields(self):
        if self.instance.fill:
            res = self.form().fields.keys()
        elif self.instance.form:
            res = self.get_form_fields(self.instance.using_form())
        else:
            res = self.get_model_fields(self.instance.model_model())
        return res

    def using_fields(self, keys, exclude=[]):
        return list(set(keys) - set(exclude))

    def is_field_filled(self, instance, field):
        # not all form fields are model fields; ignore
        if not hasattr(instance, field):
            return True
        return getattr(instance, field)

    def verify(self, instance, fields):
        return all(self.is_field_filled(instance, k) for k in fields)

    def registered_model_fills(self):
        return Fill.objects.filter(model=self.instance._meta.label)

    def as_fills(self, fills):
        return [import_string(fill.fill) if fill.fill else None for fill in fills]

    def get_model_fields(self, instance):
        return [k.name for k in instance._meta.get_fields()]

    def get_form_fields(self, form):
        return form().fields.keys()

    def str_as_list(self, fld):
        return filter(None, (fld or '').split(','))

class FillsMixin(object):
    """ Fills superpowers for Models """

    def check_fills(self, fills=[]):
        dummy = Filled(instance=self)
        registered_model_fills = fills or dummy.registered_model_fills()
        registered_fills = dummy.as_fills(registered_model_fills)
        def _fields(fill, instance):
            return fill.using_fields(keys=instance.str_as_list('fields') or fill.default_fields(),
                               exclude=instance.str_as_list('exclude'))
        def _verify(fill, instance):
            fill_instance = fill(instance=instance) if fill else Filled(instance=instance)
            flds = _fields(fill_instance, instance)
            return fill_instance.verify(self, flds)

        ctxs = {fill: _verify(fill, ins) for fill, ins in 
                    zip(registered_fills, registered_model_fills)}
        return type('Result', (object,), {'state': all(ctxs.values()), 'contexts': ctxs})

    def is_filled(self, form=None, fill=None):
        dummy = Filled(instance=self)
        if form is None and fill is None:
            fields = dummy.get_model_fields(self)
        elif form:
            fields = dummy.get_form_fields(form)
        elif fill:
            try:
                db = Fill.objects.get(name=fill.name,
                                      model=fill.form.Meta.model._meta.label)
            except ObjectDoesNotExist:
                db = None
            fields = dummy.using_fields(
                    (dummy.str_as_list(db.fields) if db else fill.fields) or dummy.get_form_fields(fill.form),
                    (dummy.str_as_list(db.exclude) if db else fill.exclude) or fill.exclude,)
        else:
            raise Exception("The impossible happened")

        return dummy.verify(self, fields)

        

