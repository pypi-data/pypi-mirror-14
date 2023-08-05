import django
from django.conf.urls import include, url
from django.contrib import admin

# Explicitly import to register the admins for the test models
import nested_admin.tests.admin


urlpatterns = [
    url(r'^_nesting/', include('nested_admin.urls')),
]

if django.VERSION < (1, 9):
    urlpatterns += [url(r'^admin/', include(admin.site.urls))]
else:
    urlpatterns += [url(r'^admin/', admin.site.urls)]

try:
    import grappelli
except ImportError:
    pass
else:
    urlpatterns += [url(r"^grappelli/", include("grappelli.urls"))]
