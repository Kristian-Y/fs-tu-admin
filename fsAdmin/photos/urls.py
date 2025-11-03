from django.urls import path
from .views import AlbumsView, AlbumDetailView

urlpatterns = [
    # path('years/', YearListCreateView.as_view(), name='year-list'),
    # path('years/<int:pk>/', YearDetailView.as_view(), name='year-detail'),
    # path('team-photos/', TeamPhotoListCreateView.as_view(), name='teamphoto-list'),
    # path('team-photos/<int:pk>/', TeamPhotoDetailView.as_view(), name='teamphoto-detail'),
    # path('years-with-photos/', YearPhotosListView.as_view(), name='years-with-photos'),
    path('', AlbumsView.as_view(), name='albums'),
    path('<str:album_id>/', AlbumDetailView.as_view(), name='album-detail'),
]
