from django.urls import path, include
from rest_framework.routers import DefaultRouter

from courses import views

router = DefaultRouter()
router.register('tags', views.TagView)

app_name = 'courses'

urlpatterns = [
    path('', include(router.urls))
]
