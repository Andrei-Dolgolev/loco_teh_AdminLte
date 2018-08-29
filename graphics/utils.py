from .forms import ProbegForm, LokoForm, FilialForm
from .models import Loko, Filial
import openpyxl


def write_filials(wb):
    # запись филиалов
    table_filials = wb['Филиал']

    data = table_filials.columns
    print(data)
    error_data = []
    for filial in list(data)[0]:
        print(filial.value)
        form = FilialForm({'name': filial.value})
        if form.is_valid():
            form.save()
        else:
            error_data.append([filial.value])

    return {'status': 'Correct', 'error': error_data}


def write_loko(wb):

    table_loko = wb['Ставка за км']

    data = table_loko.rows

    title_row = next(data)
    error_data = []
    if title_row[0].value == 'Серия' and title_row[1].value == 'Ставка':
        for data_row in data:
            model = data_row[0].value
            stavka = data_row[1].value
            form = LokoForm({'seria': model, 'stavka_za_km': stavka})
            if form.is_valid():
                form.save()
            else:
                error_data.append([model,stavka])
        return {'status': 'Correct', 'error': error_data}
    else:
        return {'status':'false'}


def write_probeg(wb):

    table_probeg = wb['Пробег']

    data = table_probeg.columns

    filials_column = next(data)

    if filials_column[0].value == 'Филиал':
        filials = list(map(lambda x: x.value, filials_column[1:]))
    else:
        print('false')  # test
        return {'status': 'In probeg table column filial not found'}

    models_column = next(data)

    if models_column[0].value == 'Серия':
        models = list(map(lambda x: x.value, models_column[1:]))
    else:
        print ('false')  # test
        return {'status': 'In probeg table column seria not found'}

    error_data = []

    for year_column in data:
        year = year_column[0].value
        for i, probeg in enumerate(year_column[1:]):
            print(i)
            try:
                filial = Filial.objects.get(name = filials[i])
                loko = Loko.objects.get(seria = models[i])
            except StopIteration:
                continue
            data_forms = {'filial': filial.id, 'loko': loko.id, 'year': year, 'km_count': probeg.value}
            print (data_forms)
            form = ProbegForm(data_forms)
            print(form.errors)
            print(form.cleaned_data)
            if form.is_valid():
                form.save()
            else:
                error_data.append([year, probeg.value])

    return {'status':'Correct', 'error': error_data}


def from_lxml_to_db():

    wb = openpyxl.load_workbook('test_LT.xlsx')
    #  data about save operation
    data = {}

    data['filials'] = write_filials(wb)

    data['loko'] = write_loko(wb)

    data['probeg'] = write_probeg(wb)

    print(data)

    return data