from django.conf.urls import include, url

from rest_framework import routers

from twitter.views import AddTwitterUserView, TweetReadOnlyViewSet, TwitterUserReadOnlyViewSet


router = routers.SimpleRouter()
router.register(r'tweets', TweetReadOnlyViewSet, base_name='tweets')
router.register(r'users', TwitterUserReadOnlyViewSet, base_name='users')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^add_user/', AddTwitterUserView.as_view(), name='add_user'),
]
