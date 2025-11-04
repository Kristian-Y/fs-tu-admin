from django.urls import path
from .views import AlbumsView, AlbumDetailView

urlpatterns = [
    path('albums/', AlbumsView.as_view(), name='albums-list'),
    path('albums/<int:album_id>/', AlbumDetailView.as_view(), name='album-detail'),
]
