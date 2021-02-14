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
from .models import Parameters, Account
from django.conf import settings

def index(request):
    return render(request, 'rev/index.html')

def aboutus(request):
    return render(request, 'rev/aboutus.html')

def upload(request):
    if 'username' not in request.session:
        return redirect('index')

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
    if 'username' not in request.session:
        return redirect('index')

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
    if 'username' not in request.session:
        return redirect('index')

    return render(request, 'rev/photos.html')

def login(request):
    if 'username' in request.session:
        return redirect('index')

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        if len(username) <= 0:
            messages.error(request, 'Please enter first name')
            return redirect('login')

        if len(password) <= 0:
            messages.error(request, 'Please enter password')
            return redirect('login')


        ex_user = Account.objects.filter(username=username,password=password).exists()

        if ex_user:
            messages.success(request, "Login Successful")
            request.session['username'] = username
        else:
            messages.error(request, 'username and password does not exist')
            return redirect('login')

        return redirect('index')
    else:
        return render(request, 'rev/user_logIn.html')

def signup(request):
    if request.method == "POST":
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        username = request.POST['username']
        password = request.POST['pass']
        repassword = request.POST['repass']
        email = request.POST['email']

        if len(first_name)<=0:
            messages.error(request, 'Please enter first name')
            return redirect('signup')

        if len(last_name) <= 0:
            messages.error(request, 'Please enter last name')
            return redirect('signup')


        if len(email) <= 0:
            messages.error(request, 'Please enter email')
            return redirect('signup')

        if len(username) <= 0:
            messages.error(request, 'Please enter username')
            return redirect('signup')

        if len(password)<=0:
            messages.error(request, 'Please enter password')
            return redirect('signup')

        if len(repassword) <= 0:
            messages.error(request, 'Please reenter password ')
            return redirect('signup')


        if password != repassword:
            messages.error(request, "Password doesn't match")
            return redirect('signup')

        ex_user = Account.objects.filter(username=username).exists()

        if ex_user:
            messages.error(request, "Username already exist")
            return redirect('signup')

        ex_email = Account.objects.filter(email=email).exists()


        if ex_email:
            messages.error(request, "Email already exist")
            return redirect('signup')

        create_acc = Account.objects.create(
            first_name= first_name,
            last_name = last_name,
            username = username,
            password = password,
            email = email
        )
        return redirect('login')
    else:
        return render(request, 'rev/signup.html')

def log_out(request):
    del request.session['username']
    return redirect('index')