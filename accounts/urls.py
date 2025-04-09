from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = "accounts"

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='accounts:home'), name='logout'),
    path('register/', views.register, name='register'),
    path('create_event/', views.create_event, name='create_event'),
    path('rso/create/', views.create_rso, name='create_rso'),
    path('rso/<int:rso_id>/join/', views.join_rso, name='join_rso'),
    path('rso/<int:rso_id>/leave/', views.leave_rso, name='leave_rso'),
    path('add_comment/<int:event_id>/', views.add_comment, name='add_comment'),
    path('edit_comment/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
]
