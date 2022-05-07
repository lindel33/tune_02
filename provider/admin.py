from django.contrib import admin
from .models import ProviderProduct


@admin.register(ProviderProduct)
class ProviderProductAdmin(admin.ModelAdmin):
    list_display = ['name', ]
    exclude = ('author', 'booking',
               'moderation', 'up_price',
               'day_next_publish', 'name_tmp',
               'provider_device')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        ss = ProviderProduct.objects.filter(author=request.user)
        return ss