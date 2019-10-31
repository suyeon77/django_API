from rest_framework import viewsets , status
from rest_framework.response import Response
from .models import Essay , Album , Files
from .serializers import EssaySerializer , AlbumSerializer , FilesSerializer
from rest_framework.filters import SearchFilter
from rest_framework.parsers import MultiPartParser , FormParser




class PostViewSet(viewsets.ModelViewSet):
    # queryset
    # serializer_class
    queryset = Essay.objects.all()
    serializer_class = EssaySerializer

    filter_backends = [SearchFilter]
    search_fields = ('title' , 'body')

    def perform_create(self , serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_authenticated:
            qs = qs.filter(author = self.request.user)
        else : 
            qs = qs.none()
            
        return qs
        
class ImgViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    

class FileViewSet(viewsets.ModelViewSet):
    queryset = Files.objects.all()
    serializer_class = FilesSerializer

    parser_classes  = (MultiPartParser , FormParser)

    def post(self , req , *args , **kwargs):
        serializer = FilesSerializer(data = req.data)
        if serializer.is_valid:
            serializer.save()
            return Response(serialzer.data, status = HTTP_201_CREATED)
        else:
            return Response(serialzer.error , status = HTTP_400_BAD_REQUEST)


# Create your views here.
