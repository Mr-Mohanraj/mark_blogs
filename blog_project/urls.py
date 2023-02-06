from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('pages.urls', namespace="pages")),
    path('', include('authentication.urls', namespace='auth')),
    path('article/',include('article.urls', namespace="blog")),
]


urlpatterns += staticfiles_urlpatterns()
