# POST from browser:    {"name": "terror", "city":"Neuquen"}
# POST from terminal:   curl -X POST http://localhost:8000/api/languaje/ -d "name=Pensamiento lateral"

import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.views import APIView
from django.contrib.auth.models import User

from .serializers import author_serializer_casero, BasicLanguageSerializer, PublisherSerializer, BookRelatedSerializer, \
    GenreBookRelatedSerializer, CategorySerializer
from .serializers import combine_mult_serializers, GenreSerializer, BookInstanceSerializer, LanguageSerializer
from catalog.models import BookInstance, Author, Language, Publisher, Genre, Book, Category


# Inicialmente creamos una vista, y serializamos los datos (para parsearlos a json) manualmente
# (basicamente armo un diccionario, y lo parseo a JSON)
def author_view(request, pk):
    author = Author.objects.get(pk=pk)
    data = author_serializer_casero(author)
    return HttpResponse(json.dumps(data), content_type="application/json")


# Ahora vamos a un paso intermedio, utilizando un serializer (basado en clases) como tata cheese manda....
def language_view(request):
    languages = Language.objects.all()
    my_serializer = BasicLanguageSerializer(languages, many=True)
    return HttpResponse(json.dumps(my_serializer.data), content_type="application/json")


# Lo mismo pero pero el serializer implementa la clase "Meta"; esto es más orientado a objetos
# Además, en primera instancia utilizo "json.dumps", pero luego defino mi parseador
def publisher_view(request):
    publishers = Publisher.objects.all()
    my_serializer = PublisherSerializer(publishers, many=True)
    return HttpResponse(json.dumps(my_serializer.data), content_type="application/json")


# Ahora, una pausa en los serializers; combinamos múltiples serializers (modelos/datos) en una vista:
def publisher_language_list_view(request):
    lista_serials = []
    publishers = Publisher.objects.all()
    my1_serializer = PublisherSerializer(publishers, many=True)
    lista_serials.append(('Publimen', my1_serializer))

    languages = Language.objects.all()
    my2_serializer = BasicLanguageSerializer(languages, many=True)
    lista_serials.append(('Lenguado', my2_serializer))

    genres = Genre.objects.all()
    my2_serializer = GenreSerializer(genres, many=True)
    lista_serials.append(('Inclusioooon!!!', my2_serializer))

    json_all = combine_mult_serializers(lista_serials)
    return HttpResponse(json_all, content_type="application/json")


# Ahora pasamos a enfocarnos en la vista (serializer simple con implementación de la clase Meta)
# El decorador permite la utilización del método "Response()", y permitir los protocolos GET y POST (retrieve/create)
@api_view(['GET', 'POST'])
def genre_list(request):
    """
    List all snippets, or create a new snippet.
    """
    if request.method == 'GET':
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = GenreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Lo mismo, pero para retrieve/update/delete, y vista en detalle (requiere parámetro pk)
@api_view(['GET', 'PUT', 'DELETE'])
def genre_detail(request, pk):
    """
    Retrieve, update or delete a snippet instance.
    """
    try:
        genre = Genre.objects.get(pk=pk)
    except Genre.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = GenreSerializer(genre)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = GenreSerializer(genre, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        genre.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Ahora utilizaremos POST (create), para ingresar dos nuevos records a sus dos respectivos modelos, a través
# de una lista con dos diccionarios
# Ejemplo browser: [{"name": "Adults"}, {"name": "Japones", "country": "Japon"}]
# curl --request POST --url http://localhost:8000/api/genre\&language/
# --header 'content-type: application/json' -d '[{"name":"Software"},{"name":"Quaqorino","country":"Ecuador"}]'
@api_view(['POST'])
def genre_language_create(request):
    serializer1 = GenreSerializer(data=request.data[0])
    serializer2 = LanguageSerializer(data=request.data[1])

    if serializer1.is_valid():
        serializer1.save()
        if not serializer2.is_valid():
            return Response(serializer1.data, status=status.HTTP_201_CREATED)

    if serializer2.is_valid():
        serializer2.save()
        return Response(status=status.HTTP_201_CREATED)

    return Response(status=status.HTTP_400_BAD_REQUEST)


#Ahora entramos con un pie a las vistas basadas en clases....
class BookInstanceList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = BookInstance.objects.all()
    serializer_class = BookInstanceSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

# Vuelta a laburar con los serializers
class BookRelatedList(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookRelatedSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


# Vuelta a laburar con los serializers
class GenreBookRelatedList(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreBookRelatedSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


# A probar los mixin para acciones de detalle
class CategoryListMix(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    generics.GenericAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class CategoryDetailMix(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# Más resumido y especifico, REST_framework define dos vistas genericas ya combinadas
class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# Seteando el atributo "permission_classes" a "DjangoModelPermissions", obtenemos una autenticación basada en
# sesiones, y una gestión de permisos basadas en los default de django (can_add_ENTIDAD, can_change..., etc
class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [DjangoModelPermissions]

    # def get(self, request, format=None):
    #     content = {
    #         'user': str(request.user),  # `django.contrib.auth.User` instance.
    #         'auth': str(request.auth),  # None
    #     }
    #     return Response(content)



# Create your views here.
class BookInstanceViewSet(viewsets.ModelViewSet):
    queryset = BookInstance.objects.all()

    serializer_class = BookInstanceSerializer


# @detail_route(methods=['get'])
# def fetch_report(self, request, *args, **kwargs):
#     import base64
#     short_report = open("somePdfFile", 'rb')
#     report_encoded = base64.b64encode(short_report.read())
#     return Response({'detail': 'this works',
#         'report': report_encoded})