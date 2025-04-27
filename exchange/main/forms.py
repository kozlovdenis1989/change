from django.forms import ModelForm
from .models import Item, ExchangeProposal

class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description', 'image_url', 'category', 'condition']

class ExchangeProposalForm(ModelForm):
    class Meta:
        model = ExchangeProposal
        fields = ['comment']  

    def __init__(self, *args, **kwargs):
        self.item_sender = kwargs.pop('item_sender', None)
        self.item_receiver = kwargs.pop('item_receiver', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        proposal = super().save(commit=False)
        if self.item_sender:
            proposal.item_sender = self.item_sender
        if self.item_receiver:
            proposal.item_receiver = self.item_receiver
        if commit:
            proposal.save()
        return proposal


