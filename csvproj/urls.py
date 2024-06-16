from django.contrib import admin
from django.urls import path
from csvapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.upload_file, name='upload_file'),
    path('analyze/', views.analyze_data, name='analyze_data'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
