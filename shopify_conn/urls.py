from django.urls import path
from .views import index, redirected

app_name = 'shopify_conn'

urlpatterns = [
    path('', index, name=''),
    path('redirected', redirected, name='redirected'),
]