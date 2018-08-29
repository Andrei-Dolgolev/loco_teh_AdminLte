from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseBadRequest, JsonResponse
from .forms import SelectDataForm, ProbegForm
from .models import Probeg
import json
# Create your views here.
"""
def profit_by_year(request):
    filials = request.GET.get('filial')
    seria = request.GET.get('models')
    if filials and seria:
        pass
    return HttpResponseBadRequest('unrecognised request')
"""

def profit_by_year_all(request):
    if request.method == 'POST':
        data = Probeg.objects.all().select_related('filial').select_related('loko')
        response_data = {}
        for probeg_object in data:
            if response_data.get(probeg_object.year):
                response_data[probeg_object.year] += int(probeg_object.km_count * probeg_object.loko.stavka_za_km)
            else:
                response_data[probeg_object.year] = int(probeg_object.km_count * probeg_object.loko.stavka_za_km)
        return JsonResponse(response_data)

def profit_by_year(request):
    if request.method == 'POST':
        form = SelectDataForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            #filials = form.cleaned_data.get('filials')
            #loko = form.cleaned_data.get('filials')
            data = Probeg.objects.all().select_related('filial').select_related('loko')
            if form.cleaned_data.get('filials'):
                data = data.filter(filial__in=form.cleaned_data.get('filials'))
            if form.cleaned_data.get('serias'):
                data = data.filter(loko__in=form.cleaned_data.get('serias'))

            # if form.cleaned_data.get('year1') and form.cleaned_data.get('year2'):
            #     year_range = range(form.cleaned_data.get('year1'),form.cleaned_data.get('year2'))
            #     data = Probeg.objects.filter(filia)

            if form.cleaned_data.get('year1'):
                data = data.filter(year__gte=form.cleaned_data.get('year1'))

            if form.cleaned_data.get('year2'):
                data = data.filter(year__lte=form.cleaned_data.get('year2'))

            response_data = {}
            for probeg_object in data:
                if response_data.get(probeg_object.year):
                    response_data[probeg_object.year] += int(probeg_object.km_count * probeg_object.loko.stavka_za_km)
                else:
                    response_data[probeg_object.year] = int(probeg_object.km_count * probeg_object.loko.stavka_za_km)
            return JsonResponse(response_data)       #json.dumps([list(response_data.keys()),list(response_data.values())]))
        print(form.errors)
        return HttpResponse(json.dumps({'status': 'bad'}))
    form = SelectDataForm()

    return render(request, 'graphics/profit_by_year/graphics.html', {'forms': form})
