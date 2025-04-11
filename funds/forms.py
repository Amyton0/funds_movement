from django import forms
import datetime
from django.forms import DateInput
from .models import Status, Type, Category, SubCategory


class RecordForm(forms.Form):
    date = forms.DateField(label="Дата создания", initial=datetime.date.today(), widget=DateInput(attrs={
            'type': 'date',
            'format': '%d.%m.%Y'
        }),
        input_formats=['%d.%m.%Y', '%d-%m-%Y', '%Y-%m-%d'])
    status = forms.ModelChoiceField(label="Статус", queryset=Status.objects.all())
    type = forms.ModelChoiceField(label="Тип", queryset=Type.objects.all())
    category = forms.ModelChoiceField(label="Категория", queryset=Category.objects.none())
    subcategory = forms.ModelChoiceField(label="Подкатегория", queryset=SubCategory.objects.none())
    summ = forms.IntegerField(label="Сумма", min_value=0)
    comment = forms.CharField(label="Комментарий", required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'type' in self.data:
            try:
                type_id = int(self.data.get('type'))
                self.fields['category'].queryset = Category.objects.filter(category_type_id=type_id)
            except (ValueError, TypeError):
                pass
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = SubCategory.objects.filter(category_id=category_id)
            except (ValueError, TypeError):
                pass


class StatusForm(forms.Form):
    name = forms.CharField(label="Введите новый статус")


class TypeForm(forms.Form):
    name = forms.CharField(label="Введите новый тип")


class CategoryForm(forms.Form):
    name = forms.CharField(label="Введите новую категорию")


class SubCategoryForm(forms.Form):
    name = forms.CharField(label="Введите новую подкатегорию")


class FilterForm(forms.Form):
    first_date = forms.DateField(label="От", widget=DateInput(attrs={
        'type': 'date',
        'format': '%d.%m.%Y'
    }),
                           input_formats=['%d.%m.%Y', '%d-%m-%Y', '%Y-%m-%d'], required=False)
    last_date = forms.DateField(label="До", widget=DateInput(attrs={
        'type': 'date',
        'format': '%d.%m.%Y'
    }),
                           input_formats=['%d.%m.%Y', '%d-%m-%Y', '%Y-%m-%d'], required=False)
    status = forms.ModelChoiceField(label="Статус", queryset=Status.objects.all(), required=False)
    type = forms.ModelChoiceField(label="Тип", queryset=Type.objects.all(), required=False)
    category = forms.ModelChoiceField(label="Категория", queryset=Category.objects.all(), required=False)
    subcategory = forms.ModelChoiceField(label="Подкатегория", queryset=SubCategory.objects.all(), required=False)
