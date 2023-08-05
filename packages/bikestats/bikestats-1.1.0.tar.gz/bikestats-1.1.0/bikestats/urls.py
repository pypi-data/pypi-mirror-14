from django.contrib import admin
from django.contrib.auth.views import logout
from django.conf.urls import url


admin.autodiscover()


urlpatterns = [
    url(r'^admin/', admin.site.urls),
]
