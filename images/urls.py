from django.urls import path
from .views import ImagesView, ImageDetailView


urlpatterns = [
    path('images/', ImagesView.as_view(), name='list_upload_images'),
    path('images/<int:image_id>/', ImageDetailView.as_view(), name='image_details')
]
