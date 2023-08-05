from functools import update_wrapper

from django.conf.urls import patterns, url
from django.contrib import admin

from .models import File
from .views import AssetListView


class FileAdmin(admin.ModelAdmin):
    list_display = ('name', 'preview',)
    fields = ('name', 'description', 'preview', 'file_original_name', 'file',
              'file_content_type',)
    readonly_fields = ('preview', 'file_content_type', 'file_original_name',)
    search_fields = ('name', 'description',)

    def get_urls(self):
        urls = super(FileAdmin, self).get_urls()

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        custom_urls = patterns(
            '',
            url(r'^list/$', wrap(AssetListView.as_view()),
                name='admin_assetmanager_list',),
        )

        return custom_urls + urls

admin.site.register(File, FileAdmin)
