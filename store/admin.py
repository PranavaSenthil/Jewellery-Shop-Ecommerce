from django.contrib import admin
from store.models import *
from django.contrib.auth.models import User
# Register your models here.
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user','phoneno', 'gender', 'address_line_1', 'city', 'state', 'country')
    search_fields = ('user__username', 'city', 'state', 'country','phoneno')
    list_filter = ('gender', 'city', 'state', 'country')

class customeProductAdmin(admin.ModelAdmin):
    list_display = ('name','category', 'price', 'stock')
    search_fields = ('name', 'category', 'price', 'stock')
    list_filter = ('category', 'price', 'stock')

class customerReviewAdmin(admin.ModelAdmin):
    list_display = ('product','user', 'rating', 'comment')
    search_fields = ('product', 'user', 'rating', 'comment')
    list_filter = ('product', 'rating')

class CartdetailsAdmin(admin.ModelAdmin):
    list_display = ('user','product', 'quantity')
    search_fields = ('user', 'product', 'quantity')
    list_filter = ('user', 'product', 'quantity')

class orderAdmin(admin.ModelAdmin):
    list_display = ('user','product', 'quantity', 'status','shipping_address')
    search_fields = ('user', 'product', 'quantity')
    list_filter = ('user', 'product', 'quantity')

class queriesAdmin(admin.ModelAdmin):
    list_display = ('user','email','message')
    search_fields = ('user','email','message')
    list_filter = ('user','email','message')

admin.site.register(Category)
admin.site.register(Product, customeProductAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Review, customerReviewAdmin)
admin.site.register(Cart, CartdetailsAdmin)
admin.site.register(Order, orderAdmin)
admin.site.register(Queries, queriesAdmin)
