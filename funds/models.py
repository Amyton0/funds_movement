from django.db import models

# Create your models here.


class Status(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Type(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=20)
    category_type = models.ForeignKey(
        Type,
        on_delete=models.CASCADE,
        related_name='category_types',
        verbose_name='Тип'
    )

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=20)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='subcategories',
        verbose_name='Категория'
    )

    def __str__(self):
        return self.name


class Record(models.Model):
    id = models.BigAutoField(primary_key=True)
    date = models.DateField()
    status = models.ForeignKey(
        Status,
        on_delete=models.CASCADE,
        related_name='statuses',
        verbose_name='Статус'
    )
    record_type = models.ForeignKey(
        Type,
        on_delete=models.CASCADE,
        related_name='record_types',
        verbose_name='Тип'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='categories',
        verbose_name='Категория'
    )
    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.CASCADE,
        related_name='subcategories',
        verbose_name='Подкатегория'
    )
    summ = models.IntegerField()
    comment = models.TextField()
