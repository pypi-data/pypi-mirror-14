import json

from django import forms
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import connection, models
from django.db.models import signals
from django.template.loader import render_to_string
from django.utils.module_loading import import_string
from django.utils.safestring import mark_safe
from jsonfield.fields import TypedJSONField
from jsonfield.forms import JSONFormField
import common.models

from .settings import IMAGE_CONTENT_TYPES, STORAGE

if STORAGE:
    _storage_klass = import_string(STORAGE[0])
    _storage = _storage_klass(*STORAGE[1], **STORAGE[2])


class SearchQuerySet(models.query.QuerySet):
    def __init__(self, model=None, fields=None):
        super(SearchQuerySet, self).__init__(model)
        self._search_fields = fields

    def search(self, query):
        meta = self.model._meta

        columns = [meta.get_field(name, many_to_many=False).column for name in self._search_fields]
        full_names = ["%s.%s" %
                      (connection.ops.quote_name(meta.db_table),
                       connection.ops.quote_name.quote_name(column))
                      for column in columns]

        # Create the MATCH...AGAINST expressions
        fulltext_columns = ", ".join(full_names)
        match_expr = ("MATCH(%s) AGAINST (%%s)" % fulltext_columns)

        # Add the extra SELECT and WHERE options
        return self.extra(select={'relevance': match_expr}, where=[match_expr], params=[query, query])


class FileManager(models.Manager):
     def __init__(self, fields):
         super(FileManager, self).__init__()
         self._search_fields = fields

     def get_query_set(self):
         return SearchQuerySet(self.model, self._search_fields)

     def search(self, query):
         return self.get_query_set().search(query)


class AssetManagerFileFieldWidget(forms.Widget):
    template_name = 'asset_widget.html'

    class Media(object):
        css = {
            'all': ('assetmanager/admin/css/asset_list.css',
                    'assetmanager/admin/css/fontello/css/fontello.css',)
        }

    def render(self, name, value, attrs=None):
        url_params = '_popup'
        if self.attrs.get('images_only'):
            url_params += '&images_only=1'
        '''
        If we don't do this for the value then it will submit '{}' as empty
        value in form and even though it's required it won't throw an error
        '''
        value_as_json = '' if not value else json.dumps(value)

        context = {
            'name': name,
            'value': value,
            'value_as_json': value_as_json,
            'images_only': self.attrs['images_only'],
            'template_url': '/admin/assetmanager/file/list/',
            'is_required': self.is_required,
            'url_params': url_params,
        }

        return mark_safe(render_to_string(self.template_name, context))


#TODO Move to fields.py
class AssetManagerFileFormField(JSONFormField):
    widget = AssetManagerFileFieldWidget

    def __init__(self, images_only=False, *args, **kwargs):
        self.images_only = images_only
        kwargs['widget'] = self.widget
        super(AssetManagerFileFormField, self).__init__(*args, **kwargs)

    def widget_attrs(self, widget):
        attrs = super(AssetManagerFileFormField, self).widget_attrs(widget)
        if self.images_only is not None:
            attrs.update({'images_only': self.images_only})
        return attrs


class AssetManagerFileField(TypedJSONField):

    def __init__(self, *args, **kwargs):
        self.images_only = kwargs.pop('images_only', False)
        # Safeguard to make sure we're passing the id and url
        kwargs['required_fields'] = {
            'id': models.PositiveIntegerField(),
            'url': models.URLField(),
            'name': models.CharField(null=True, max_length=255, blank=True),
            'file_original_name': models.CharField(max_length=255)
        }

        super(AssetManagerFileField, self).__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name, virtual_only=False):
        super(AssetManagerFileField, self).contribute_to_class(cls, name)

        setattr(cls, self.name, self)

        signals.post_save.connect(self._save_attachment, cls, True)
        signals.post_delete.connect(self._delete_attachment, cls, True)

    def _save_attachment(self, **kwargs):
        instance = kwargs['instance']
        file_ = getattr(instance, self.name)
        content_type = ContentType.objects.get_for_model(instance)

        Attachment.objects.filter(content_type=content_type,
                                  object_id=instance.id,
                                  object_field=self.name,
                                  file_id=file_['id']).delete()
        if file_:
            attachment = Attachment.objects.create(content_type=content_type,
                                                   object_id=instance.id,
                                                   object_field=self.name,
                                                   file_id=file_['id'])
            attachment.save()

    def _delete_attachment(self, **kwargs):
        instance = kwargs['instance']
        file_ = getattr(instance, self.name)
        content_type = ContentType.objects.get_for_model(instance)

        Attachment.objects.filter(content_type=content_type,
                                  object_id=instance.id,
                                  object_field=self.name,
                                  file_id=file_['id']).delete()

    def formfield(self, **kwargs):
        defaults = {'form_class': AssetManagerFileFormField,
                    'images_only': self.images_only}
        defaults.update(kwargs)
        return super(AssetManagerFileField, self).formfield(**defaults)


class File(common.models.DateTimeModelMixin):

    name = models.CharField(null=True, max_length=255, blank=True)
    description = models.TextField(null=True, blank=True)
    file = models.FileField(storage=_storage)
    file_original_name = models.CharField(max_length=255)
    file_content_type = models.CharField(max_length=50, db_index=True)

    objects = FileManager(fields=('name', 'description', 'file_original_name',))

    def __unicode__(self):
        return self.name or self.file.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        file_original_name = self.file.name
        if self.pk:
            file = File.objects.get(pk=self.pk)
            if self.file.name == file.file.name:
                file_original_name = file.file_original_name
        else:
            file_original_name = self.file.name

        self.file_original_name = file_original_name

        if hasattr(self.file.file, 'content_type'):
            self.file_content_type = self.file.file.content_type

        super(File, self).save(force_insert, force_update, using, update_fields)

        '''
        Look up any object+fields this file has been attached to
        and update the id/name/url
        '''
        for attachment in self.attachments.all():
            setattr(attachment.content_object,
                    attachment.object_field,
                    {'id': self.pk, 'name': self.name, 'url': self.file.url,
                     'file_original_name': self.file_original_name})
            attachment.content_object.save()

    def preview(self):
        html = ''
        if self.pk:
            url = self.file.url
            if self.is_image:
                html = '<img src="{}" width="200" />'.format(url)
            else:
                content_type_icons = {
                    'application/pdf': 'fontello-icon-file-pdf',
                    'application/msword': 'fontello-icon-file-word',
                    'application/msexcel': 'fontello-icon-file-excel',
                }
                icon = content_type_icons.get(self.file_content_type,
                                              'fontello-icon-doc')
                html = '<div class="icon {}"></div>'.format(icon)

            if self.name:
                html += '<div class="name">{}</div>'.format(self.name)

            html += '<a href="{}" class="fontello-icon fontello-icon-popup"></a>'.format(url)

        return html
    preview.allow_tags = True
    preview.short_description = 'Preview'

    @property
    def is_image(self):
        return self.file_content_type in IMAGE_CONTENT_TYPES


class Attachment(common.models.DateTimeModelMixin):

    content_type = models.ForeignKey(ContentType, related_name='attachments')
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    object_field = models.CharField(max_length=100)
    file = models.ForeignKey(File, related_name='attachments')
