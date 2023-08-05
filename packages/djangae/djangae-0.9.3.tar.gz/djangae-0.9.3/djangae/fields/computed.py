from django.db import models

class ComputedFieldMixin(object):
    def __init__(self, func, *args, **kwargs):
        self.computer = func

        kwargs["editable"] = False

        super(ComputedFieldMixin, self).__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        value = self.computer(model_instance)
        setattr(model_instance, self.attname, value)
        return value

    def deconstruct(self):
        name, path, args, kwargs = super(ComputedFieldMixin, self).deconstruct()
        args = [self.computer] + args
        del kwargs["editable"]
        return name, path, args, kwargs

class ComputedCharField(ComputedFieldMixin, models.CharField):
    __metaclass__ = models.SubfieldBase


class ComputedIntegerField(ComputedFieldMixin, models.IntegerField):
    __metaclass__ = models.SubfieldBase


class ComputedTextField(ComputedFieldMixin, models.TextField):
    __metaclass__ = models.SubfieldBase


class ComputedPositiveIntegerField(ComputedFieldMixin, models.PositiveIntegerField):
    __metaclass__ = models.SubfieldBase


class ComputedBooleanField(ComputedFieldMixin, models.BooleanField):
    __metaclass__ = models.SubfieldBase
