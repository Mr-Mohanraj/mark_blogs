from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('pages.urls', namespace="pages")),
    path('', include('authentication.urls', namespace='auth')),
    path('', include('user_profile.urls', namespace="profile")),
    path('article/',include('article.urls', namespace="blog")),
    # path('summernote/', include('django_summernote.urls')),
]

if settings.DEBUG:
    print("Mode => DEBUG=TRUE")
    settings.EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)