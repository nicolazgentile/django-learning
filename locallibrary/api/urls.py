# POST from browser:    {"name": "terror", "city":"Neuquen"}
# POST from terminal:   curl -X POST http://localhost:8000/api/genre/ -d "name=Pensamiento lateral"
from django.urls import include, path

from rest_framework import routers

from .views import *

router = routers.DefaultRouter()
router.register(r'bookInstance', BookInstanceViewSet)

# specify URL Path for rest_framework
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('authors/<int:pk>', author_view, name='api-author-detail'),
    path('languages/', language_view, name='api-languages'),
    path('publishers/', publisher_view, name='api-publishers'),
    path('publishers&languages/', publisher_language_list_view, name='api-combinados1'),
    path('genres/', genre_list, name='api-genres'),
    path('genres/<int:pk>/detail/', genre_detail, name='api-genre-detail'),
    path('genres&languages/', genre_language_create, name='api-combinados2'),
    path('booksRelatedList/', BookRelatedList.as_view(), name='api-bookgrelated'),
    path('genresBooksList/', GenreBookRelatedList.as_view(), name='api-genrebookrelated'),
    path('categorys/detail/<int:pk>', CategoryDetailMix.as_view(), name='api-categoryDetailMix'),
    path('categorys/<int:pk>', CategoryDetail.as_view(), name='api-categoryDetail'),
    path('bookInstances/', BookInstanceList.as_view(), name='api-bookInstance1'),
]
