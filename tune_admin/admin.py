from pprint import pprint

from django.contrib import admin

from django.utils.safestring import mark_safe

from provider.models import ProviderProduct
from .models import Product, Category, SeriesCategory, BookingProduct, GuarantyModel, KitModel, StateModel

from django.db import models

@admin.register(StateModel)
class StateModelAdmin(admin.ModelAdmin):
    pass


@admin.register(KitModel)
class KitModelAdmin(admin.ModelAdmin):
    product_ = Product.objects.all()
    bookingproduct = ProviderProduct.objects.all()

    def save_model(self, request, obj, form, change):
        # for i in self.product_:
        #     if str(i.kit) == str(obj.kit):
        #         print(i.kit, obj.id)
        #         Product.objects.filter(id=i.id).update(kit=int(obj.id))
        # for i in self.bookingproduct:
        #     if str(i.kit) == str(obj.kit):
        #         ProviderProduct.objects.filter(id=i.id).update(kit=int(obj.id))
        super().save_model(request, obj, form, change)


@admin.register(GuarantyModel)
class GuarantyModelAdmin(admin.ModelAdmin):
    product_ = Product.objects.all()
    bookingproduct = ProviderProduct.objects.all()

    def save_model(self, request, obj, form, change):
        for i in self.product_:
            if str(i.guaranty) == str(obj.guaranty):
                print(i.guaranty, obj.id)
                Product.objects.filter(id=i.id).update(guaranty=obj.id)
        for i in self.bookingproduct:
            if str(i.guaranty) == str(obj.guaranty):
                ProviderProduct.objects.filter(id=i.id).update(guaranty=obj.id)
        super().save_model(request, obj, form, change)

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
    list_display = ['name', 'price', 'article', 'category',
                    'series', 'moderation', 'booking',
                    'sell', 'author', 'day_created', ]
    search_fields = ('name', 'article', 'provider_device', )
    exclude = ('name_tmp', 'up_price', 'author', )
    actions = [plus, plust, minus, minust,
               cost10, cost20, cost30, sell,
               'new_sale']

    admin.site.site_header = 'TuneApple'
    admin.site.site_title = 'TuneAppleAdmin'
    admin.site.index_title = 'TuneApple'

    # from django.forms import NullBooleanSelect, SelectMultiple,\
    #     CheckboxSelectMultiple, MultiWidget, Select, RadioSelect
    #
    # formfield_overrides = {
    #     models.ForeignKey: {'widget': CheckboxSelectMultiple(attrs={'size': 'auto'})},
    #
    # }


    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user
        super().save_model(request, obj, form, change)

    @staticmethod
    @admin.action(description='Обновить акции')
    def new_sale(modeladmin, request, queryset):
        all_pro = Product.objects.all()
        for i in all_pro:
            if i.sale == True:
                i.price = i.price + 2000
                i.save()
        Product.objects.update(sale=False)
        import random
        queryset_products = all_pro.filter(sell=False).filter(moderation=True).filter(booking=False)
        exit_list = []
        while len(exit_list) != 10:

            import datetime

            today = datetime.datetime.today()
            tomorrow = today + datetime.timedelta(days=5)
            random_index = random.randrange(len(queryset_products))
            sale_products = queryset_products[random_index]
            day_created = str(sale_products.day_created).split()[0]
            tomorrow = str(tomorrow).split()[0]
            if sale_products not in exit_list:
                if day_created < tomorrow:
                    sale_products.price = sale_products.price - 2000
                    sale_products.sale = True
                    sale_products.save()
                    exit_list.append(1)
















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
