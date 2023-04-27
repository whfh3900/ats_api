from django.urls import include, path
from apps.api.views import AddSchedule

urlpatterns = [
   path('cf', AddSchedule.as_view()),
]