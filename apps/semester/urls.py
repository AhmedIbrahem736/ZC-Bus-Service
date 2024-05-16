from django.urls import path
from .views import SemesterListCreateAPIView, SemesterRetrieveUpdateDestroyAPIView
urlpatterns = [
    path('', SemesterListCreateAPIView.as_view(), name='semester-list-create'),
    path('<int:pk>/', SemesterRetrieveUpdateDestroyAPIView.as_view(), name='semester-retrieve-update-destroy'),

]
