from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from accounts.models import User


# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=1000, unique=True, blank=True)
    slug = models.SlugField(max_length=1000, unique=True, blank=True)
    image = models.FileField(upload_to='photo/category', blank=True)
    description = models.TextField(max_length=1000, blank=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=True)
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return self.category_name


def pre_save_product_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.category_name)


pre_save.connect(pre_save_product_receiver, sender=Category)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, unique=True, blank=True)
    slug = models.SlugField(max_length=1000, unique=True, blank=True)
    stock_record = models.IntegerField(blank=True)
    description = models.TextField(max_length=1000, blank=True)
    image = models.FileField(upload_to='photo/products', blank=True)
    price = models.IntegerField(null = True, blank=True,default= 0)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=True)
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return self.title


def pre_save_product_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)


pre_save.connect(pre_save_product_receiver, sender=Product)


class Variant(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='variant')
    title = models.CharField(max_length=100, unique=True, blank=True)
    slug = models.SlugField(max_length=1000, unique=True, blank=True)
    stock_record = models.IntegerField(blank=True)
    description = models.TextField(max_length=1000, blank=True)
    image = models.FileField(upload_to='photo/variants', blank=True)
    price = models.IntegerField(blank=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=True)
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return self.title


def pre_save_product_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)


pre_save.connect(pre_save_product_receiver, sender=Variant)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='carts', null=True, blank=True, default=1)
    is_paid = models.BooleanField(default=False)


    def __str__(self):
        return self.user.first_name +" " + "cart"


class CartItem(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, blank=True, related_name='product')
    variant = models.ForeignKey(
        Variant, on_delete=models.CASCADE, null=True, blank=True, related_name='variants')
    price = models.IntegerField(null = True, blank=True,default= 0)
    quantity = models.IntegerField(default=1, null=True, blank=True)
    discount_amount = models.CharField(max_length=1000,null = True,blank = True)

    


class UserAddress(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null = True)
    address = models.TextField(null = True,blank = True)
    default_address = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'User Address'


    def __str__(self):
        return self.user.username

Percent = 1
fixed = 2
voucher_choice = (
    (Percent , 'percent'),
    (fixed , "Fixed")
)
class Voucher(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_type = models.IntegerField( choices=voucher_choice)
    discount_value = models.DecimalField(max_digits=12, decimal_places=2)
    min_spend = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    max_discount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)



    class Meta:
        verbose_name_plural = 'Voucher'

    def __str__(self):
        return self.code


