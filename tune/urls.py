from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('/', include('tune_admin.urls')),
#     path('api', include('bot_telegram.urls')),
    path('csv_check/', include('cost_models.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
