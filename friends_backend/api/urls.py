from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.views import FriendViewSet, UserViewSet
app_name = 'api'
router = DefaultRouter()

router.register('friends', FriendViewSet, basename='friends')
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]