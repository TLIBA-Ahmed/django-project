from django.urls import path
from . import views
urlpatterns = [
    path('home/<str:name>', views.home, name='home'), 
    path('list/', views.listConferences, name='list_conferences'),
    path('listC/', views.ConferenceListView.as_view(), name='conferences_listLV'),
    path('welcome/', views.welcome, name='welcome'),
    path('details/<int:pk>/', views.ConferenceDetailsView.as_view(), name='conference_details'),
    path('add/', views.ConferenceCreateView.as_view(), name='conference_create'),
    path('update/<int:pk>/', views.ConferenceUpdateView.as_view(), name='conference_update'),
    path('delete/<int:pk>/', views.ConferenceDeletesView.as_view(), name='conference_confirm_delete'),
    ]