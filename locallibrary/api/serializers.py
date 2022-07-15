# import serializer from rest_framework
import json
from rest_framework import serializers

# import model from models.py
from catalog.models import BookInstance, Language, Publisher, Genre, Book, Category
from django.contrib.auth.models import User


def author_serializer_casero(author):
    data = {}
    data['first_name'] = author.first_name
    data['last_name'] = author.last_name
    data['nationality'] = author.nationality
    return data


# Acá ya pasamos a utilizar clases, aunque no implementamos las clases abstractas
class BasicLanguageSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    country = serializers.CharField(max_length=100)


# Lo mismo pero implementando la clase "Meta"; esto es más orientado a objetos
class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ('name', 'website')


# A continuacion, un hack "propio" para combinar serializers (solo para vistas basadas en funciones)
# Este método recibe como argumento una lista de tuples, en la pos 0 espera un identificador (nombre) del modelo a
# representar, y luego el serializer del modelo
def combine_mult_serializers(lista_tuples):
    rta_json = '{'
    for mytuple in lista_tuples:
        name = mytuple[0]
        myjson = json.dumps(mytuple[1].data)
        rta_json += '"' + name + '":' + myjson + ', '
    rta_json = rta_json[:-2]
    rta_json += '}'
    return rta_json


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


# Create a model serializer
class BookInstanceSerializer(serializers.ModelSerializer):
    # specify model and fields
    class Meta:
        model = BookInstance
        fields = ('book', 'status', 'language', 'due_date', 'due_back')


class LanguageSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    country = serializers.CharField(max_length=100)

    # Lo siguiente sirve para des-serializar un objeto JSON en objeto de la clase original
    def restore_object(self, attrs, instance=None):
        if instance:
            # Update existing instance
            instance.name = attrs.get('name', instance.name)
            instance.country = attrs.get('country', instance.country)
            return instance
        return Language(**attrs)

    # Es necesario definir este método para poder utilizar el método post (recien se utilizará en la función
    # "genre_language_create()"
    def create(self, attrs):
        new_obj = Language(**attrs)
        new_obj.save()
        return new_obj


# La idea ahora es que un serializer traiga todos los libros y objetos relacionados por foreign keys
class BookRelatedSerializer(serializers.ModelSerializer):
    publisher = PublisherSerializer()
    genre = GenreSerializer(many=True)

    class Meta:
        model = Book
        fields = '__all__'


# Lo mismo pero desde uno de los objetos relacionados:
class GenreBookRelatedSerializer(serializers.ModelSerializer):
    book = BookRelatedSerializer(source='book_set', many=True)

    class Meta:
        model = Genre
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'

