from django import template

from ..models import Order, OrderItem

register = template.Library()

@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        # qs = Order.objects.filter(user=user, ordered=False)
        # if qs.exists():
        #         print(qs[0])
        #         print(qs[0].items.count())
        #         return qs[0].items.count()
        qs = OrderItem.objects.filter(user=user)
        if qs.exists():
                total = 0
                for item in qs:
                       total += item.quantity
        return total
    return 0