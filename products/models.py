from django.db import models
from django.conf import settings
from django.shortcuts import reverse
import datetime

CATEGORY_CHOICES = {
    ('p', 'Pizza'),
    ('d', 'Deserts'),
    ('c', 'Cold Drinks')
}

LABEL_CHOICES = {
    ('p', 'primary'),
    ('s', 'secondary'),
    ('d', 'danger')
}


class Item(models.Model):
    title = models.CharField(max_length=128)
    price = models.FloatField()
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=1)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    description = models.TextField()
    slug = models.SlugField(default="test-product")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product', kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse('add_to_cart', kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse('remove_from_cart', kwargs={
            'slug': self.slug
        })


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, blank=True, null=True)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.quantity} of {self.item.title}'


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    order_date = models.DateTimeField(default=datetime.datetime.now())
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
