from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
# from .views import bot
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('/home', admin.site.urls),
#     path('/b', cache_page(100)(bot))

]
