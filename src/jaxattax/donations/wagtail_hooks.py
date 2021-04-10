from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from . import models


@modeladmin_register
class CashDonationAdmin(ModelAdmin):
    model = models.CashDonation
    menu_label = 'Cash donations'
    menu_icon = 'fa-dollar'
    menu_order = 500
    add_to_settings_menu = False

    list_display = ('name', 'amount_dollars', 'date')
    search_fields = ('name',)

    ordering = ['-created']

    def amount_dollars(self, instance):
        return f"${instance.amount:.2f}"
    amount_dollars.short_description = "Amount"
    amount_dollars.admin_order_field = 'amount'
