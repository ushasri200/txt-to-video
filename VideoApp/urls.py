from django.urls import path
from VideoApp.views import *
urlpatterns=[
    path('call-to-video/',EnterTextAndDurationAPIView.as_view(),name='something')
]