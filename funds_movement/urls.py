"""
URL configuration for funds_movement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from funds import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main_page),
    path('create', views.create),
    path('directories', views.directories),
    path('index', views.index),
    path('add/status', views.create_status),
    path('add/type', views.create_type),
    path('add/category/<int:type_id>', views.create_category),
    path('add/subcategory/<int:category_id>', views.create_subcategory),
    path('delete/status/<int:status_id>', views.delete_status),
    path('delete/type/<int:type_id>', views.delete_type),
    path('delete/category/<int:category_id>', views.delete_category),
    path('delete/subcategory/<int:subcategory_id>', views.delete_subcategory),
    path('delete/record/<int:record_id>', views.delete_record),
    path('edit/status/<int:status_id>', views.edit_status),
    path('edit/type/<int:type_id>', views.edit_type),
    path('edit/category/<int:category_id>', views.edit_category),
    path('edit/subcategory/<int:subcategory_id>', views.edit_subcategory),
    path('edit/record/<int:record_id>', views.edit_record),
    path('ajax/load-subcategories/', views.load_subcategories, name='ajax_load_subcategories'),
    path('ajax/load-categories/', views.load_categories, name='ajax_load_categories'),
]
