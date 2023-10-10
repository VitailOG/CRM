from django.urls import path

from rest_framework.routers import DefaultRouter

from app.views import UserAPI
from app.views import ClientAPI
from app.views import CallbackAPI
from app.views import NotificationAPI
from app.views import RefreshTokenAPI
from app.views import HistoryMassagesAPI


router = DefaultRouter()
router.register('client', ClientAPI)
router.register('user', UserAPI)


urlpatterns = [
    path('callback/', CallbackAPI.as_view()),
    path('send/', NotificationAPI.as_view()),
    path('refresh/', RefreshTokenAPI.as_view()),
    path('history/', HistoryMassagesAPI.as_view()),
]

urlpatterns += router.urls
