from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Product, Category, SeriesCategory, BookingProduct

@admin.action(description='++ 1000 к цене')
def plus(modeladmin, request, queryset):
    for i in queryset:
        i.save(extra='+')
    pass

@admin.action(description='-- 1000 к цене')
def minus(modeladmin, request, queryset):
    for i in queryset:
        i.save(extra='-')
    pass

@admin.action(description='++ 4000 к цене')
def plust(modeladmin, request, queryset):
    for i in queryset:
        i.save(extra='ВРЕМЕННО+')
    pass

@admin.action(description='-- 4000 к цене')
def minust(modeladmin, request, queryset):
    for i in queryset:
        i.save(extra='ВРЕМЕННО-')
    pass

@admin.action(description='Отметить проданным')
def sell(modeladmin, request, queryset):
    for i in queryset:
        i.save(extra='Продажа')
    pass

@admin.action(description='+ 10 процентов')
def cost10(modeladmin, request, queryset):
    for i in queryset:
        i.save(extra='проц10')
    pass

@admin.action(description='+ 20 процентов')
def cost20(modeladmin, request, queryset):
    for i in queryset:
        i.save(extra='проц20')
    pass

@admin.action(description='+ 30 процентов')
def cost30(modeladmin, request, queryset):
    for i in queryset:
        i.save(extra='проц30')
    pass

@admin.register(Product)
class PostAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'article', 'category', 'series', 'moderation', 'booking', 'sell', 'author', 'day_created',]
    search_fields = ('name','article', 'provider_device')
    exclude = ('name_tmp', 'up_price', 'author')
    actions = [plus, plust, minus, minust, cost10, cost20, cost30, sell]

    admin.site.site_header = 'TuneApple'
    admin.site.site_title = 'TuneAppleAdmin'
    admin.site.index_title = 'TuneApple'
    # def image_show(self, obj):
    #     if obj.image_1:
    #         return mark_safe("<img src='{}' width='60' />".format(obj.image_1))
    #     return 'None'

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user
        super().save_model(request, obj, form, change)



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category', ]


@admin.register(SeriesCategory)
class SeriesCategoryAdmin(admin.ModelAdmin):
    list_display = ['category', ]


@admin.register(BookingProduct)
class BookingProductAdmin(admin.ModelAdmin):
    list_display = ['product_pka', 'booking_flag', 'sell_flag', 'name_user', 'phone']
    exclude = ('product_pka',)
    search_fields = ['product_pka__name', 'product_pka__article']
