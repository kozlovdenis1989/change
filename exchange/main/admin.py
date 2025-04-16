from django.contrib import admin
from .models import Item, ExchangeProposal

class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'condition', 'created_at')
    search_fields = ('title', 'description')

class ExchangeProposalAdmin(admin.ModelAdmin):
    list_display = ('item_sender', 'item_receiver', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('comment',)

admin.site.register(Item, ItemAdmin)
admin.site.register(ExchangeProposal, ExchangeProposalAdmin)