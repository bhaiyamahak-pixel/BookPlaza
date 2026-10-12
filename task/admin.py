from django.contrib import admin
from .models import Book, Customer, Order


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'title',
        'author',
        'price',
        'category',
        'stock',
    )
   
    list_editable = (
        'stock',
    )
   
    search_fields = (
        'title',
        'author',
    )

    list_filter = (
        'category',
    )

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'phone',
        'email',
    )

    search_fields = (
        'name',
        'phone',
        'email',
    )

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'customer_name',
        'phone',
        'book',
        'quantity',
        'order_date',
    )

    search_fields = (
        'customer_name',
        'phone',
        'address',
        'city',
        'pin_code',
        'book__title',
    )

    list_filter = (
        'order_date',
        'city',
    )
