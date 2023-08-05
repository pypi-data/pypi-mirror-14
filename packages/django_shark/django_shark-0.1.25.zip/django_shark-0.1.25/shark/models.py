from django.db.models import *
from django import forms
from django.utils.timezone import now
from shark.widgets import MarkdownWidget


class SharkModel(Model):
    class Meta:
        abstract = True

    def __iter__(self):
        for field_name in self._meta.get_fields():
            yield field_name

    @classmethod
    def load(cls, pk):
        try:
            return cls.objects.get(pk=pk)
        except cls.DoesNotExist:
            return None

    primary_field_name = None
    def __str__(self):
        if self.__class__.primary_field_name is None:
            for primary_field in ['name']:
                if primary_field in dir(self):
                    self.__class__.primary_field_name = primary_field
                    break

        if self.__class__.primary_field_name:
            return self.__getattribute__(self.__class__.primary_field_name)
        else:
            return super().__str__()


class EditableText(SharkModel):
    name = CharField(max_length=128, primary_key=True, unique=True)
    content = TextField()
    handler_name = CharField(max_length=512)
    last_used = DateTimeField(default=now)


class MarkdownFormField(forms.CharField):
    def __init__(self, *args, **kwargs):
        # Django admin overrides the 'widget' value so this seems the only way
        # to scupper it!
        super(MarkdownFormField, self).__init__(*args, **kwargs)
        self.widget = MarkdownWidget()


class MarkdownField(TextField):
    def formfield(self, **kwargs):
        defaults = {'form_class': MarkdownFormField}
        defaults.update(kwargs)
        return super(MarkdownField, self).formfield(**defaults)


class StaticPage(SharkModel):
    url_name = CharField(max_length=128, primary_key=True, unique=True)
    title = CharField(max_length=512, null=True)
    description = CharField(max_length=512, null=True)
    body = MarkdownField(null=True)