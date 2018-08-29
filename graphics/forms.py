from django import forms
from django.db.models import Min, Max
from .models import Probeg, Filial, Loko
from django.core.exceptions import ValidationError
from django.forms import ModelForm


class UserEditForm(forms.ModelForm):

    serias = forms.CharField(label='Models', widget=forms.MultipleChoiceField)
    filials = forms.CharField(label='Filials', widget=forms.MultipleChoiceField)
    year = forms.IntegerField(label='Years', widget=forms.NumberInput)
    year2 = forms.IntegerField(label='Years', widget=forms.NumberInput)

    """
    class Meta:
        model = Probeg
        fields = ('serias', 'filials','year')

    def validate_year(self):
        cd = self.cleaned_data
        if cd['year'] < 1851:
            raise forms.ValidationError('Year incorrect')
        return cd['year']
    """





class SelectDataForm(forms.Form):
    """
    OPTIONS = (
        ("a", "A"),
        ("b", "B"),
        ("c", "C"),
        ("d", "D"),
        ("e", "E"),
        ("f", "F"),
    )
    """

    serias = forms.ModelMultipleChoiceField(label='serias', required=False, queryset=Loko.objects.all())
    year1 = forms.IntegerField(label='Years', widget=forms.NumberInput)
    year2 = forms.IntegerField(label='Years', widget=forms.NumberInput)
    filials = forms.ModelMultipleChoiceField(
        label="Filials",
        required=False,
        queryset=Filial.objects.all(),
        widget=forms.SelectMultiple()
    )
    serias.widget.attrs.update({'class': 'form-control select2', 'style': 'width: 100%;', 'multiple': 'multiple', 'data-placeholder': 'All' })
    year2.widget.attrs.update({'class': 'form-control-sm'})
    year1.widget.attrs.update({'class': 'form-control-sm'})
    #    class ="form-control select2" multiple="multiple" data-placeholder="Select a State" style = "width: 100%;"

    filials.widget.attrs.update({'class': 'form-control select2', 'style': 'width: 100%;', 'multiple': 'multiple', 'data-placeholder': 'All'})

    def clean_year1(self):
        cd = self.cleaned_data
        min_year = Probeg.objects.all().aggregate(Min('year'))['year__min']
        if int(cd.get('year1')) < min_year:
            return min_year
        return cd.get('year1')

    def clean_year2(self):
        cd = self.cleaned_data
        max_year = Probeg.objects.all().aggregate(Max('year'))['year__max']
        if int(cd.get('year2')) > max_year:
            return max_year
        return cd.get('year2')

class ProbegForm(ModelForm):
    class Meta:
        model = Probeg
        fields = ('filial', 'loko', 'year', 'km_count')


class FilialForm(ModelForm):
    class Meta:
        model = Filial
        fields = ('name',)


class LokoForm(ModelForm):
    class Meta:
        model = Loko
        fields = ('seria', 'stavka_za_km')