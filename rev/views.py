import csv, io
from django.shortcuts import render,redirect
from django.contrib import messages
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn import metrics
import joblib
import os
from django.http import Http404
from .models import Parameters
from django.conf import settings

def index(request):
    return render(request, 'rev/index.html')

def aboutus(request):
    return render(request, 'rev/aboutus.html')

def upload(request):
    if request.POST:
        if len(request.FILES)<=0:
            messages.error(request, 'Please choose the file first')
            return redirect('upload')

        csv_file = request.FILES['csv']
        # let's check if it is a csv file
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'THIS IS NOT A CSV FILE')
            return redirect('upload')

        csv_data_set = csv_file.read().decode('UTF-8')

        tourism_data = pd.read_csv(io.StringIO(csv_data_set))
        dataset = tourism_data
        X = dataset.drop(columns=['Revenue Collected in million USD', 'Year'])
        y = tourism_data['Revenue Collected in million USD']
        # X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
        regressor = LinearRegression().fit(X, y)

        joblib.dump(regressor, csv_file.name.replace('.csv','.sav'))

        # setup a stream which is when we loop through each line we are able to handle a data in a stream
        io_string = io.StringIO(csv_data_set)

        next(io_string)
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            _, created = Parameters.objects.update_or_create(
                year = column[0],
                total_arrival = column[1],
                average_length_of_stay = column[2],
                total_foreign_exchange = column[3],
                holiday_pleasure = column[4],
                trekking_and_mountaineering = column[5],
                business = column[6],
                pilgrimage = column[7],
                revenue = column[8],
                model = csv_file.name.replace('.csv','.sav'),
            )
        messages.success(request, 'Files Uploaded successfully')
        return redirect('upload')

    files_sav = []
    for file in os.listdir(settings.BASE_DIR):
        if file.endswith(".sav"):
            files_sav.append(file)

    return render(request, 'rev/upload.html', {'files_sav' : files_sav})

def estimation(request,model_name=None):
    data = {}
    if not model_name==None:
        data['model_name'] = model_name

        if os.path.exists(model_name):
            loaded_model = joblib.load(model_name)
        else:
            messages.error(request,"File does not exist, please upload before estimation.")
            return redirect('upload')

    if request.POST:
        total_arrival = float(request.POST['total_arrival'])
        average_length_of_stay = float(request.POST['average_length_of_stay'])
        total_foreign_exchange = float(request.POST['total_foreign_exchange'])
        holiday_pleasure = float(request.POST['holiday_pleasure'])
        trekking_and_mountaineering = float(request.POST['trekking_and_mountaineering'])
        business = float(request.POST['business'])
        pilgrimage = float(request.POST['pilgrimage'])

        data['total_arrival'] = total_arrival
        data['average_length_of_stay'] = average_length_of_stay
        data['total_foreign_exchange'] = total_foreign_exchange
        data['holiday_pleasure'] = holiday_pleasure
        data['trekking_and_mountaineering'] = trekking_and_mountaineering
        data['business'] = business
        data['pilgrimage'] = pilgrimage

        result = loaded_model.predict([[total_arrival,average_length_of_stay,total_foreign_exchange,holiday_pleasure,trekking_and_mountaineering,business,pilgrimage]])
        data['result']=round(result[0],2)
        print(result)
        return render(request, 'rev/estimation.html',data)

    return render(request, 'rev/estimation.html',data)

def photos(request):
    return render(request, 'rev/photos.html')
