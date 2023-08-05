from django.contrib.admin.options import IS_POPUP_VAR
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.db.models import Q

from .forms import SearchForm
from .models import File
from .settings import PAGE_SIZE, IMAGE_CONTENT_TYPES


class AssetListView(ListView):

    model = File
    paginate_by = PAGE_SIZE
    context_object_name = 'assets'
    template_name = 'asset_list.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AssetListView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AssetListView, self).get_context_data(**kwargs)
        context['form'] = SearchForm(self.request.GET)
        context['is_popup'] = IS_POPUP_VAR in self.request.GET or IS_POPUP_VAR in self.request.POST
        return context

    def get_queryset(self, *args, **kwargs):
        q = self.request.GET.get('q')
        images_only = bool(self.request.GET.get('images_only'))

        object_list = self.model.objects
        if q:
            object_list = object_list.filter(
                Q(name__search=q) | Q(description__search=q)
            )
        if images_only:
            object_list = object_list.filter(
                file_content_type__in=IMAGE_CONTENT_TYPES
            )
        else:
            object_list = object_list.all()

        return object_list
