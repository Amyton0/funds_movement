from django.shortcuts import render, get_object_or_404
from .forms import RecordForm, StatusForm, TypeForm, CategoryForm, SubCategoryForm, FilterForm
from django.http import HttpResponse, HttpResponsePermanentRedirect, JsonResponse
from .models import Record, Status, Type, Category, SubCategory


def main_page(request):
    records = Record.objects.all()
    if request.method == "POST":
        filterform = FilterForm(request.POST)
        if filterform.is_valid():
            filter_ = filterform.cleaned_data
            if filter_["first_date"]:
                records = records.filter(date__gte=filter_["first_date"])
            if filter_["last_date"]:
                records = records.filter(date__lte=filter_["last_date"])
            if filter_["status"]:
                records = records.filter(status=filter_["status"])
            if filter_["type"]:
                records = records.filter(record_type=filter_["type"])
            if filter_["category"]:
                records = records.filter(category=filter_["category"])
            if filter_["subcategory"]:
                records = records.filter(subcategory=filter_["subcategory"])
    return render(request, "index.html", context={'records': records, 'form': FilterForm()})


def create(request):
    if request.method == "POST":
        recordform = RecordForm(request.POST)
        if recordform.is_valid():
            record = recordform.cleaned_data
            print(record)
            Record(date=record["date"],
                   status=record['status'],
                   record_type=record['type'],
                   category=record['category'],
                   subcategory=record['subcategory'],
                   summ=record['summ'],
                   comment=record['comment']).save()
            return HttpResponsePermanentRedirect("/")
        else:
            return HttpResponse("Неправильно введены данные")
    else:
        recordform = RecordForm()
        data = {"header": "Создать запись", "form": recordform}

        return render(request, "record.html", context=data)


def directories(request):
    statuses = [(status.name, status.id) for status in Status.objects.all()]
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    types = [(type_.name, type_.id) for type_ in Type.objects.all()]
    folder_hierarchy = {}
    for type_ in types:
        folder_hierarchy[type_] = {}
        for category in categories.filter(category_type__id=type_[1]):
            folder_hierarchy[type_][(category.name, category.id)] = \
                [(subcategory.name, subcategory.id) for subcategory in subcategories.filter(category__id=category.id)]
    return render(request, "directories.html", context={"statuses": statuses, "folder_hierarchy": folder_hierarchy})


def create_status(request):
    if request.method == "POST":
        statusform = StatusForm(request.POST)
        if statusform.is_valid():
            status = statusform.cleaned_data
            Status(name=status["name"]).save()
            return HttpResponsePermanentRedirect("/directories")
        else:
            return HttpResponse("Неправильно введены данные")
    else:
        return render(request, "directory.html", context={"form": StatusForm(), "type": "Статус"})


def create_type(request):
    if request.method == "POST":
        typeform = TypeForm(request.POST)
        if typeform.is_valid():
            type_ = typeform.cleaned_data
            Type(name=type_["name"]).save()
            return HttpResponsePermanentRedirect("/directories")
        else:
            return HttpResponse("Неправильно введены данные")
    else:
        return render(request, "directory.html", context={"form": TypeForm(), "type": "Тип"})


def create_category(request, type_id):
    type_obj = get_object_or_404(Type, id=type_id)
    if request.method == "POST":
        categoryform = CategoryForm(request.POST)
        if categoryform.is_valid():
            category = categoryform.cleaned_data
            Category(name=category["name"], category_type=type_obj).save()
            return HttpResponsePermanentRedirect("/directories")
        else:
            return HttpResponse("Неправильно введены данные")
    else:
        return render(request, "directory.html", context={"form": CategoryForm(), "type": "Категория"})


def create_subcategory(request, category_id):
    category_obj = get_object_or_404(Category, id=category_id)
    if request.method == "POST":
        subcategoryform = SubCategoryForm(request.POST)
        if subcategoryform.is_valid():
            subcategory = subcategoryform.cleaned_data
            SubCategory(name=subcategory["name"], category=category_obj).save()
            return HttpResponsePermanentRedirect("/directories")
        else:
            return HttpResponse("Неправильно введены данные")
    else:
        return render(request, "directory.html", context={"form": SubCategoryForm(), "type": "Подкатегория"})


def delete_status(request, status_id):
    status_obj = get_object_or_404(Status, id=status_id)
    status_obj.delete()
    return HttpResponsePermanentRedirect("/directories")


def delete_type(request, type_id):
    type_obj = get_object_or_404(Type, id=type_id)
    type_obj.delete()
    return HttpResponsePermanentRedirect("/directories")


def delete_category(request, category_id):
    category_obj = get_object_or_404(Category, id=category_id)
    category_obj.delete()
    return HttpResponsePermanentRedirect("/directories")


def delete_subcategory(request, subcategory_id):
    subcategory_obj = get_object_or_404(SubCategory, id=subcategory_id)
    subcategory_obj.delete()
    return HttpResponsePermanentRedirect("/directories")


def delete_record(request, record_id):
    record_obj = get_object_or_404(Record, id=record_id)
    record_obj.delete()
    return HttpResponsePermanentRedirect("/")


def edit_status(request, status_id):
    status_obj = get_object_or_404(Status, id=status_id)
    if request.method == "POST":
        statusform = StatusForm(request.POST)
        if statusform.is_valid():
            status = statusform.cleaned_data
            status_obj.name = status["name"]
            status_obj.save()
            return HttpResponsePermanentRedirect("/directories")
        else:
            return HttpResponse("Неправильно введены данные")
    else:
        return render(request, "directory.html", context={"form": StatusForm(initial={"name": status_obj.name}), "type": "Статус"})


def edit_type(request, type_id):
    type_obj = get_object_or_404(Type, id=type_id)
    if request.method == "POST":
        typeform = TypeForm(request.POST)
        if typeform.is_valid():
            type_ = typeform.cleaned_data
            type_obj.name = type_["name"]
            type_obj.save()
            return HttpResponsePermanentRedirect("/directories")
        else:
            return HttpResponse("Неправильно введены данные")
    else:
        return render(request, "directory.html", context={"form": TypeForm(initial={"name": type_obj.name}), "type": "Тип"})


def edit_category(request, category_id):
    category_obj = get_object_or_404(Category, id=category_id)
    if request.method == "POST":
        categoryform = CategoryForm(request.POST)
        if categoryform.is_valid():
            category = categoryform.cleaned_data
            category_obj.name = category["name"]
            category_obj.save()
            return HttpResponsePermanentRedirect("/directories")
        else:
            return HttpResponse("Неправильно введены данные")
    else:
        return render(request, "directory.html", context={"form": CategoryForm(initial={"name": category_obj.name}), "type": "Категория"})


def edit_subcategory(request, subcategory_id):
    subcategory_obj = get_object_or_404(SubCategory, id=subcategory_id)
    if request.method == "POST":
        subcategoryform = SubCategoryForm(request.POST)
        if subcategoryform.is_valid():
            subcategory = subcategoryform.cleaned_data
            subcategory_obj.name = subcategory["name"]
            subcategory_obj.save()
            return HttpResponsePermanentRedirect("/directories")
        else:
            return HttpResponse("Неправильно введены данные")
    else:
        return render(request, "directory.html", context={"form": SubCategoryForm(initial={"name": subcategory_obj.name}), "type": "Подкатегория"})


def edit_record(request, record_id):
    record_obj = get_object_or_404(Record, id=record_id)
    if request.method == "POST":
        recordform = RecordForm(request.POST)
        if recordform.is_valid():
            record = recordform.cleaned_data
            record_obj.date = record["date"]
            record_obj.status = record['status']
            record_obj.record_type = record['type']
            record_obj.category = record['category']
            record_obj.subcategory = record['subcategory']
            record_obj.summ = record['summ']
            record_obj.comment = record['comment']
            record_obj.save()
            return HttpResponsePermanentRedirect("/")
        else:
            return HttpResponse("Неправильно введены данные")
    else:
        recordform = RecordForm(initial={
            "date": record_obj.date,
            "status": record_obj.status,
            "type": record_obj.record_type,
            "category": record_obj.category,
            "subcategory": record_obj.subcategory,
            "summ": record_obj.summ,
            "comment": record_obj.comment
        })
        data = {"header": "Редактировать запись", "form": recordform}

        return render(request, "record.html", context=data)


def index(request):
    return HttpResponsePermanentRedirect("/")


def load_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = SubCategory.objects.filter(category_id=category_id).values('id', 'name')
    return JsonResponse(list(subcategories), safe=False)


def load_categories(request):
    type_id = request.GET.get('type_id')
    categories = Category.objects.filter(category_type_id=type_id).values('id', 'name')
    return JsonResponse(list(categories), safe=False)
