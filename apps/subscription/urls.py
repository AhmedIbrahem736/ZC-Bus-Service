from django.urls import path
from .views import SubscriptionCreateAPIView, SubscribedUsersListView
urlpatterns = [
    path('', SubscriptionCreateAPIView.as_view(), name='subscription-create'),
    path('<int:semester_id>/', SubscribedUsersListView.as_view(), name='subscribed-users-list'),

]
