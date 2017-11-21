from django.conf.urls import url

from twitter.views import AddTwitterUserView


urlpatterns = [
    url(r'^add_user/', AddTwitterUserView.as_view(), name='add_user'),
]
