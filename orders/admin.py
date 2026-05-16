from django.contrib import admin
from django.db.models import Sum

from brfn.admin_actions import AdminActionSelectLabelMixin

from .models import Order, OrderItem


@admin.register(OrderItem)
class OrderItemAdmin(AdminActionSelectLabelMixin, admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "product",
        "quantity",
        "price",
        "gross_amount",
        "commission_amount",
        "producer_amount",
    )
    list_filter = ("order__created_at", "product__producer")
    search_fields = ("order__id", "product__name", "product__producer__username")


@admin.register(Order)
class OrderAdmin(AdminActionSelectLabelMixin, admin.ModelAdmin):
    list_display = ("id", "user", "created_at", "status", "total", "platform_fee_total", "producer_total")
    list_filter = ("status", "created_at")
    search_fields = ("id", "user__username", "user__email")

    def platform_fee_total(self, obj: Order):
        val = obj.orderitem_set.aggregate(s=Sum("commission_amount"))["s"] or 0
        return val

    def producer_total(self, obj: Order):
        val = obj.orderitem_set.aggregate(s=Sum("producer_amount"))["s"] or 0
        return val

    platform_fee_total.short_description = "Platform fee"
    producer_total.short_description = "Producer total"
