from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Album

class AlbumsView(APIView):
    def get(self, request):
        albums = []
        for album in Album.objects.all().order_by('-created_at'):
            if album.photos.exists():
                albums.append({
                    "id": album.id,
                    "name": album.name,
                    "cover": album.photos.first().image.url,
                    "count": album.photos.count()
                })
        return Response({"albums": albums})


class AlbumDetailView(APIView):
    def get(self, request, album_id):
        album = Album.objects.get(pk=album_id)
        photos = [{
            # "name": photo.image.name,
            "url": photo.image.url
        } for photo in album.photos.all()]
        return Response({"album": album.name, "images": photos})
