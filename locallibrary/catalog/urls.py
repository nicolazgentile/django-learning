from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('books/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('books/<str:publi>', views.PublisherBookList.as_view(), name='books_by_publisher'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('authors/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('authors/dead/', views.AuthorBlackListView.as_view(), name='authors_dead'),
    path('publishers/', views.PublisherListView.as_view(), name='publishers'),
    path('publisher/<int:pk>', views.PublisherDetailView.as_view(), name='publisher-detail'),
    path('clients/', views.client_listView, name='clients'),
    path('clients/<int:pk>', views.client_detailView, name='client-detail'),
    path('clients/add/', views.client_createView, name='client-add'),
    path('clients/<int:pk>/update/', views.client_updateView, name='client-update'),
    path('clients/<int:pk>/delete/', views.client_deleteView, name='client-delete'),
    path('employees/', views.EmployeeListView.as_view(), name='employees'),
    path('employees/<int:pk>', views.EmployeeDetailView.as_view(), name='employee-detail'),
    path('employees/add/', views.EmployeeDetailView.as_view(), name='employee-add'),
    path('employee/<int:pk>/update/', views.EmployeeUpdateView.as_view(), name='employee-update'),
]
