from django.urls import re_path, path
from . import views

app_name = 'payments'

urlpatterns = [
    re_path(r'^$', views.create_order, name='payment'),
    re_path(r'^notification/', views.payment_notification, name='notification'),
    ]