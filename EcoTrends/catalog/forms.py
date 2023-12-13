# catalog/forms.py
from django import forms
from django.forms import formset_factory
from .models import Comment, Product,Category, SubCategory


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CommentForm, self).__init__(*args, **kwargs)
    def save(self, commit=True):
        instance = super(CommentForm, self).save(commit=False)
        instance.user = self.user
        if commit:
            instance.save()
        return instance
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'subcategory', 'image']
    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        subcategory = cleaned_data.get('subcategory')
        if subcategory and subcategory.category != category:
            raise forms.ValidationError("Subcategory does not belong to the selected category")
        return cleaned_data
class ProductSearchForm(forms.Form):
    search_query = forms.CharField(label='Search', max_length=100, required=False,
            widget=forms.TextInput(attrs={'placeholder': 'Enter search term'}))

        
ProductFormSet = formset_factory(ProductForm, extra=1)  # You can adjust 'extra' based on your needs


