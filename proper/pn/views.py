from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import  Food, Unit, Purchases, Foods_in_stock, User
from .forms import UnitForm, FoodForm, PurchaseForm,FoodsInStockForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.forms import formset_factory
from django.utils import timezone
from django.db import transaction
from django.db.models import Sum
from django.http import JsonResponse
from datetime import datetime


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')  # Redirect to your home page
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('home')  # Redirect to your home page
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('home')  # Redirect to your home page

def home_view(request):
    return render(request, 'home.html')

def reference_tables(request):
    return render(request, 'reference_tables.html')

def display_table(request, model_name):
    models = {
        'food': Food.objects.all(),
        'unit': Unit.objects.all(),
    }

    paginator = Paginator(models[model_name], 10)  # 10 items per page
    page = request.GET.get('page')

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    context = {
        'model_name': model_name,
        'items': items,
        'fields': [field.name for field in models[model_name].model._meta.fields],
        'item_fields': [{field.name: getattr(item, field.name) for field in item._meta.fields} for item in items],
    }

    return render(request, 'display_table.html', context)

def delete_item_view(request, model_name, pk):
    models = {
        'unit': Unit.objects.all(),
        'food': Food.objects.all(),
    }

    model_class = models.get(model_name)
    item = get_object_or_404(model_class, pk=pk)

    if request.method == 'POST':
        item.delete()
        return redirect('display_table', model_name=model_name)

def add_item_view(request, model_name):
    form_classes = {
        'unit': UnitForm,
        'food': FoodForm,
    }

    form_class = form_classes.get(model_name)
    if form_class:
        form = form_class(request.POST or None)

        if form.is_valid():
            form.save()
            return redirect('display_table', model_name=model_name)

        template_name = 'add_item_template.html'
        return render(request, template_name, {'form': form, 'model_name': model_name})

    # Handle the case when an invalid table_name is provided
    return render(request, 'error.html', {'model_name': model_name})

def get_model_and_form(model_name):
    MODELS = {
        'unit': Unit,
        'food': Food,
    }

    FORM_CLASSES = {
        'unit': UnitForm,
        'food': FoodForm,
    }

    model_class = MODELS.get(model_name)
    form_class = FORM_CLASSES.get(model_name)

    if not (model_class and form_class):
        return None, None

    return model_class, form_class

def edit_item_view(request, model_name, pk):
    model_class, form_class = get_model_and_form(model_name)

    if model_class is None or form_class is None:
        return HttpResponseBadRequest("Invalid model name")

    item = get_object_or_404(model_class, pk=pk)
    form = form_class(instance=item)

    if request.method == 'POST':
        form = form_class(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('display_table', model_name=model_name)
    else:
        form = form_class(instance=item)

    return render(request, 'edit_item_template.html', {'form': form, 'model_name': model_name, 'item': item})

def display_documents(request):
    documents = Purchases.objects.all()

    paginator = Paginator(documents, 10)  # 10 items per page
    page = request.GET.get('page')

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    context = {
        'documents': items,
        'fields': [field.name for field in Purchases._meta.fields],
        'document_fields': [{field.name: getattr(document, field.name) for field in document._meta.fields} for document
                            in items],
    }

    return render(request, 'display_documents.html', context)

def add_document_view(request):
    FoodsInStockFormSet = formset_factory(FoodsInStockForm, extra=1, can_delete=True)

    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        formset = FoodsInStockFormSet(request.POST, prefix='foods_formset')

        foods_list = request.POST.getlist('food[]')
        quantity_list = request.POST.getlist('quantity[]')
        sum_list = request.POST.getlist('sum[]')

        if form.is_valid():
            document = form.save(commit=False)
            document.save()

            # Создаем списки для данных из таблицы
            foods_list = request.POST.getlist('food[]')
            quantity_list = request.POST.getlist('quantity[]')
            sum_list = request.POST.getlist('sum[]')

            # Получаем значения из объекта Document
            document = Purchases.objects.get(pk=document.id)

            # Обрабатываем данные из списков
            for food, quantity, sum_value in zip(foods_list, quantity_list, sum_list):
                # Преобразуем значения в нужные типы данных
                quantity = float(quantity)
                sum_value = float(sum_value)

                # Получаем или создаем объект Food по имени
                food_obj, created = Food.objects.get_or_create(name=food)

                # Получаем или создаем объект Unit по имени (предполагаем, что у Food есть поле unit)
                unit_obj, created = Unit.objects.get_or_create(name=food_obj.unit.name)

                # Создаем или обновляем объект Foods_in_stock
                foods_in_stock, created = Foods_in_stock.objects.get_or_create(
                    Document=document,
                    Food=food_obj,  # Получаем объект Food по имени
                    defaults={
                        'Date': document.Date,
                        'Unit': unit_obj,
                        'Quantity': quantity,
                        'Sum': sum_value
                    }
                )

                # Если объект уже существует, обновляем его поля
                if not created:
                    foods_in_stock.Date = document.Date
                    foods_in_stock.Unit = unit_obj
                    foods_in_stock.Quantity = quantity
                    foods_in_stock.Sum = sum_value
                    foods_in_stock.save()

            return redirect('display_documents')
        else:
            # Print errors to logs
            print(form.errors, formset.errors)
    else:
        form = PurchaseForm(initial={'Date': timezone.now().strftime('%Y-%m-%dT%H:%M')})
        formset = FoodsInStockFormSet(prefix='foods_formset')

    foods = Food.objects.all()

    if 'search' in request.GET:
        search_term = request.GET['search']
        foods = foods.filter(name__icontains=search_term)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = render(request, 'items/foods_table_ajax.html', {'foods': foods}).content
        return JsonResponse({'data': data.decode('utf-8')})

    foods_range = range(len(foods))

    context = {
        'form': form,
        'formset': formset,
        'foods': foods,
        'foods_range': foods_range,
    }

    return render(request, 'add_document.html', context)

def product_search(request):
    search_term = request.GET.get('search', '')
    products = Food.objects.filter(name__icontains=search_term).values_list('name', flat=True)
    return JsonResponse(list(products), safe=False)

def edit_document_view(request, pk=None):
    document = get_object_or_404(Purchases, pk=pk)
    foods_in_stock = Foods_in_stock.objects.filter(Document=document)
    form = PurchaseForm(instance=document)

    # Получаем все доступные варианты для выбора
    all_authors = User.objects.all()

    if request.method == 'POST':
        form = PurchaseForm(request.POST, instance=document)

        if form.is_valid():
            with transaction.atomic():  # Обеспечиваем атомарность операций
                document = form.save()  # Сохраняем документ

                # Обновляем связанные записи в табличной части
                foods_list = request.POST.getlist('food[]')
                quantity_list = request.POST.getlist('quantity[]')
                sum_list = request.POST.getlist('sum[]')

                # Обрабатываем данные из списков
                for food, quantity, sum_value in zip(foods_list, quantity_list, sum_list):
                    # Преобразуем значения в нужные типы данных
                    quantity = float(quantity)
                    sum_value = float(sum_value)

                    # Получаем или создаем объект Food по имени
                    food_obj, created = Food.objects.get_or_create(name=ffood)

                    # Получаем или создаем объект Unit по имени (предполагаем, что у food есть поле unit)
                    unit_obj, created = Unit.objects.get_or_create(name=food_obj.unit.name)

                    # Создаем или обновляем объект Foods_in_stock
                    foods_in_stock, created = Foods_in_stock.objects.get_or_create(
                        Document=document,
                        Food=food_obj,  # Получаем объект Food по имени
                        defaults={
                            'Date': document.Date,
                            'Unit': unit_obj,
                            'Quantity': quantity,
                            'Sum': sum_value
                        }
                    )

                    # Если объект уже существует, обновляем его поля
                    if not created:
                        foods_in_stock.Date = document.Date
                        foods_in_stock.Unit = unit_obj
                        foods_in_stock.Quantity = quantity
                        foods_in_stock.Sum = sum_value
                        foods_in_stock.save()

            return redirect('display_documents')

    context = {
        'form': form,
        'document': document,
        'all_authors': all_authors,
        'foods_in_stock': foods_in_stock,
    }

    return render(request, 'edit_document.html', context)

def delete_document_view(request, pk=None):
    document = get_object_or_404(Purchases, pk=pk)

    if request.method == 'POST':
        document.delete()
        return redirect('display_documents')

    context = {
        'document': document,
    }

    return render(request, 'delete_document.html', context)
