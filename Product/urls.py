from django.urls import path

from castilloDeporte import views

urlpatterns = [
    path('<slug:slug>', views.ProductDetailView.as_view(), name='product'),
]