from django.contrib import admin
from .models import ProviderProduct


@admin.register(ProviderProduct)
class ProviderProductAdmin(admin.ModelAdmin):
    list_display = ['name', ]
    exclude = ('author', 'booking', 'sell', 'count', 'moderation', 'up_price', 'day_next_publish', 'name_tmp')