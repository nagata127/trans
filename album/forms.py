from django import forms
from .models import *

class ImageForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['photo']

class LangChoiceForm(forms.Form):
	lang = (
		('ja', '日本'),
		('en', '英語'),
        ("fr", "フランス"),
        ("de", "ドイツ"),
        ("es", "スペイン"),
        ("he", "ヘブライ"),
	)
	select = forms.fields.ChoiceField(
        required = False,
        widget = forms.widgets.Select,
        choices = lang
    )

LangChoiceFormSet = forms.formset_factory(
        form = LangChoiceForm,
        extra = 1,
        max_num = 2,
    )
