from django.urls import path
from bank_account import views

urlpatterns = [
    path('credit_request', views.post_credit_request),
    path('link', views.link_redirect),
    path('unlink', views.post_unlink_redirect),
]
