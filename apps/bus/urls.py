from django.urls import path
from .views import BusRouteListCreateAPIView, BusRouteRetrieveUpdateAPIView, BusRouteDeleteAPIView

urlpatterns = [
    path('bus-routes/', BusRouteListCreateAPIView.as_view(), name='bus-route-list-create'),
    path('bus-routes/<int:pk>/', BusRouteRetrieveUpdateAPIView.as_view(), name='bus-route-retrieve-update'),
    path('bus-routes/<int:pk>/delete/', BusRouteDeleteAPIView.as_view(), name='bus-route-delete'),
]
