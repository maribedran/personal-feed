from django.conf.urls import include, url  # noqa
from django.contrib import admin
from django.views.generic import TemplateView

import django_js_reverse.views

from users.views import logout_view


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^jsreverse/$', django_js_reverse.views.urls_js, name='js_reverse'),

    url(r'^$', TemplateView.as_view(template_name='webapp/home.html'), name='home'),

    url(r'^social/', include('social_django.urls', namespace='social')),
    url(r'^logout/', logout_view, name='logout'),

    url(r'^api/twitter/', include('twitter.urls', namespace='twitter')),
]
