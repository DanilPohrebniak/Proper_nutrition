from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import  Food, Unit
from .forms import UnitForm, FoodForm


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
