from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import Book, Author, BookInstance, Genre, Publisher, Client, Employee
from .forms import ClientForm
from django.views import generic
from datetime import date
import requests

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()
    filtro_books = 'Profe'
    filtro_genres = 'Ror'
    num_books_filter = Book.objects.filter(title__icontains=filtro_books).count()
    num_genres_filter = Genre.objects.filter(name__icontains=filtro_genres).count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'filtro_books' : filtro_books,
        'num_books_filter': num_books_filter,
        'filtro_genres': filtro_genres,
        'num_genres_filter': num_genres_filter,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    paginate_by = 10


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10


class AuthorDetailView(generic.DetailView):
    model = Author


class PublisherListView(generic.ListView):
    model = Publisher


class PublisherDetailView(generic.DetailView):
    model = Publisher

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PublisherDetailView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['book_list'] = self.object.book_set.all()
        return context


class AuthorBlackListView(generic.ListView):
    template_name = 'catalog/author_black_list.html'
    context_object_name = 'dead_authors'

    queryset = Author.objects.filter(date_of_death__lte=date.today())


class PublisherBookList(generic.ListView):
    template_name = 'catalog/books_by_publisher.html'
    context_object_name = 'booksByPublisher'

    def get_queryset(self):
        self.publisher = Publisher.objects.get(name=self.kwargs['publi'])
        return Book.objects.filter(publisher=self.publisher)


def client_listView(request):
    context = {}

    context["dataset"] = Client.objects.all()

    return render(request, "catalog/client_list.html", context)


def client_detailView(request, pk):
    context = {}

    context["cliente"] = Client.objects.get(pk=pk)

    return render(request, "catalog/client_detail.html", context)


def client_createView(request):
    context = {}

    form = ClientForm(request.POST or None)
    if form.is_valid():
        form.save()

        return HttpResponseRedirect("/catalog/clients/")

    context['form'] = form
    return render(request, "catalog/client_form.html", context)


def client_updateView(request, pk):
    context = {}
    objeto_cliente = get_object_or_404(Client, pk=pk)

    objeto_formulario = ClientForm(request.POST or None, instance=objeto_cliente)

    if request.method == 'GET':
        form = ClientForm(None)  # Solo para probar el método GET, cuando presionamos update, pide la planilla vacía
        context['form'] = form
        return render(request, 'catalog/client_form.html', context)

    if request.method == 'POST':
        if objeto_formulario.is_valid():
            objeto_formulario.save()
            return HttpResponseRedirect("/catalog/clients/{}".format(pk))
        else:
            return render(request, 'catalog/client_form.html', {'form': objeto_formulario})


def client_deleteView(request, pk):
    objeto_cliente = get_object_or_404(Client, pk=pk)

    if request.method == 'POST':
        objeto_cliente.delete()
        return HttpResponseRedirect("/catalog/clients/")

    else:
        return render(request, 'catalog/client_delete.html', {'cliente': objeto_cliente})


class EmployeeListView(generic.ListView):
    model = Employee
    context_object_name = 'employees'


class EmployeeDetailView(generic.DetailView):
    model = Employee
    context_object_name = 'tipejo'

    def get_context_data(self, *args, **kwargs):
        context = super(EmployeeDetailView, self).get_context_data(**kwargs)
        # add extra field
        context["clave"] = f'{self.object.last_name}{self.object.identification}'
        return context


class EmployeeUpdateView(generic.UpdateView):
    model = Employee

    fields = ['last_name', 'category', 'user']

    # Para consumir APIs desde acá....posiblemente tira un error porque el puerto de llamada es el mismo que el target
    # api_response = requests.get('http://localhost:8000/api/genres')
    # print(api_response)

    success_url = f'/catalog/employees/'
