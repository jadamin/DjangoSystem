from django.shortcuts import render,redirect
from django.contrib import messages
from datetime import datetime,timedelta
from .models import * 
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


#################################
#####       INDEX PAGE     #####
###############################



def index(request):
   return render(request, "home.html",{})
from django.shortcuts import render



#####################################
##    FUNCTION TO SHOW PROFILE    ##
###################################


def view_profile(request):
    appointments = Appointment.objects.filter(user=request.user)
    return render(request, 'profile.html', {'appointments': appointments})


#################################
#####   LOGIN FUNCTION     #####
###############################


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('Thefirstpage.html')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'login.html')
    


###############################################################
#####    FUNCTION TO REDIRECT USER TO HOME AFTER LOGIN    #####
##############################################################


def first_view(request):
    return redirect('the_first_page')


######################################################
#####   LOGOUT VIEW TO SHOW USER THE DOOR OUT   #####
####################################################


def logout_view(request):
    return redirect('home')


#############################################
#####  THE FIST PAGE SHOW FIRST PAGE   #####
###########################################

def the_first_page(request):
    return render(request, 'Thefirstpage.html')


########################################################
#####   FUNCTION TO SHOW FIRST PAGE BEFORE LOGIN   #####
#######################################################


def home_view(request):
    return render(request,'home.html')


#################################
#####   SIGNUP FUNCTION    #####
###############################


def signup_view(request):
    if request.method == 'POST':
        user_name = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']

        if password != password_confirm:
            return render(request, 'signin.html', {'error': 'Passwords do not match'})

        if len(password) < 8:
            return render(request, 'signin.html', {'error': 'Password must be at least 8 characters long'})

        if not any(char.isdigit() for char in password):
            return render(request, 'signin.html', {'error': 'Password must contain at least one digit'})

        if not any(char.isupper() for char in password):
            return render(request, 'signin.html', {'error': 'Password must contain at least one uppercase letter'})

        if not any(char.islower() for char in password):
            return render(request, 'signin.html', {'error': 'Password must contain at least one lowercase letter'})
        
        user = User.objects.create_user(username=user_name, email=email,first_name=first_name, last_name=last_name, password=password)        
        user.save()
        user = authenticate(username=user_name, password=password)
        login(request, user)
        return redirect('Thefirstpage.html')
    else:
        return render(request, 'signin.html')
    


##########################################
#####   BOOK YOUR APPOINTMENT FUNC   #####
#########################################


def booking(request):
    weekdays = validWeekday(30)
    validateWeekdays = isWeekdayValid(weekdays)

    time = [   "09:00  ","09:40  ","10:20  ","11:40  ","13:30  ","14:10  ","14:50  ","15:30  ","16:10  ","16:50  ",
    ]

    if request.method == 'POST':
        service = request.POST.get('service')
        day = request.POST.get('day')
        time = request.POST.get('time')
        
        if service is None:
            messages.success(request, "Please Select A Service!")
        elif day is None:
            messages.success(request, "Please Select A Day!")
        elif time is None:
            messages.success(request, "Please Select A Time!")
        else:
            user = request.user
            date = dayToWeekday(day)

            # Check if the selected day is within the next 21 days
            today = datetime.now()
            maxDate = today + timedelta(days=21)
            if day > maxDate.strftime('%Y-%m-%d'):
                messages.success(request, "The Selected Date Isn't In The Correct Time Period!")
            else:
                # Check if the selected date is a valid weekday
                if date not in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
                    messages.success(request, "The Selected Date Is Incorrect")
                else:
                    # Check if the selected time is available
                    if Appointment.objects.filter(day=day, time=time).count() >= 1:
                        messages.success(request, "The Selected Time Has Been Reserved Before!")
                    else:
                        # Check if the selected day is full
                        if Appointment.objects.filter(day=day).count() >= 11:
                            messages.success(request, "The Selected Day Is Full!")
                        else:
                            # Create new appointment
                            AppointmentForm = Appointment.objects.create(
                                user=user,
                                service=service,
                                day=day,
                                time=time,
                            )
                            messages.success(request, "Appointment Saved!")
                            return redirect('Thefirstpage.html')

    return render(request, 'booking.html', {
        'weekdays': weekdays,
        'validateWeekdays': validateWeekdays,
        'time': time,
    })


#################################
#####                      #####
###############################


def userPanel(request):
    user = request.user
    appointments = Appointment.objects.filter(user=user).order_by('day', 'time')
    return render(request, 'userPanel.html', {
        'user':user,
        'appointments':appointments,
    })


#################################
#####                      #####
###############################


def userUpdate(request, id):
    appointment = Appointment.objects.get(pk=id)
    userdatepicked = appointment.day
    #Copy  booking:
    today = datetime.today()
    minDate = today.strftime('%Y-%m-%d')

    #24h if statement in template:
    delta24 = (userdatepicked).strftime('%Y-%m-%d') >= (today + timedelta(days=1)).strftime('%Y-%m-%d')
    #Calling 'validWeekday' Function to Loop days you want in the next 21 days:
    weekdays = validWeekday(30)

    #Only show the days that are not full:
    validateWeekdays = isWeekdayValid(weekdays)
    

    if request.method == 'POST':
        service = request.POST.get('service')
        day = request.POST.get('day')

        #Store day and service in django session:
        request.session['day'] = day
        request.session['service'] = service

        return redirect('userUpdateSubmit', id=id)


    return render(request, 'userUpdate.html', {
            'weekdays':weekdays,
            'validateWeekdays':validateWeekdays,
            'delta24': delta24,
            'id': id,
        })


#################################
#####                      #####
###############################


def userUpdateSubmit(request, id):
    user = request.user
    time = [   "09:00  ","09:40  ","10:20  ","11:40  ","13:30  ","14:10  ","14:50  ","15:30  ","16:10  ","16:50  ",
    ]
    today = datetime.now()
    minDate = today.strftime('%Y-%m-%d')
    deltatime = today + timedelta(days=21)
    strdeltatime = deltatime.strftime('%Y-%m-%d')
    maxDate = strdeltatime

    day = request.session.get('day')
    service = request.session.get('service')
    
    #Only show the time of the day that has not been selected before and the time he is editing:
    hour = checkEditTime(time, day, id)
    appointment = Appointment.objects.get(pk=id)
    userSelectedTime = appointment.time
    if request.method == 'POST':
        time = request.POST.get("time")
        date = dayToWeekday(day)

        if service != None:
            if day <= maxDate and day >= minDate:
                if date == 'Monday' or date == 'Tuesday' or date == 'Wednesday' or date == 'Thursday' or date == 'Friday':
                    if Appointment.objects.filter(day=day).count() < 11:
                        if Appointment.objects.filter(day=day, time=time).count() < 1 or userSelectedTime == time:
                            AppointmentForm = Appointment.objects.filter(pk=id).update(
                                user = user,
                                service = service,
                                day = day,
                                time = time,
                            ) 
                            messages.success(request, "Appointment Edited!")
                            return redirect('index')
                        else:
                            messages.success(request, "The Selected Time Has Been Reserved Before!")
                    else:
                        messages.success(request, "The Selected Day Is Full!")
                else:
                    messages.success(request, "The Selected Date Is Incorrect")
            else:
                    messages.success(request, "The Selected Date Isn't In The Correct Time Period!")
        else:
            messages.success(request, "Please Select A Service!")
        return redirect('userPanel')


    return render(request, 'userUpdateSubmit.html', {
        'times':hour,
        'id': id,
    })
#################################
#####                      #####
###############################
def staffPanel(request):
    today = datetime.today()
    minDate = today.strftime('%Y-%m-%d')
    deltatime = today + timedelta(days=21)
    strdeltatime = deltatime.strftime('%Y-%m-%d')
    maxDate = strdeltatime
    #Only show the Appointments 21 days from today
    items = Appointment.objects.filter(day__range=[minDate, maxDate]).order_by('day', 'time')

    return render(request, 'staffPanel.html', {
        'items':items,
    })
#################################
#####                      #####
###############################
def dayToWeekday(x):
    z = datetime.strptime(x, "%Y-%m-%d")
    y = z.strftime('%A')
    return y
#################################
#####                      #####
###############################
def validWeekday(days):
    today = datetime.now()
    weekdays = []
    for i in range (0, days):
        x = today + timedelta(days=i)
        y = x.strftime('%A')
        if y == 'Monday' or y == 'Tuesday' or y == 'Wednesday' or y == 'Thursday' or y == 'Friday':
            weekdays.append(x.strftime('%Y-%m-%d'))
    return weekdays
#################################
#####                      #####
###############################  
def isWeekdayValid(x):
    validateWeekdays = []
    for j in x:
        if Appointment.objects.filter(day=j).count() < 10:
            validateWeekdays.append(j)
    return validateWeekdays
#################################
#####                      #####
###############################
def checkTime(times, day):
    x = []
    for k in times:
        if Appointment.objects.filter(day=day, time=k).count() < 1:
            x.append(k)
    return x
#################################
#####                      #####
###############################
def checkEditTime(times, day, id):
    #Only show the time of the day that has not been selected before:
    x = []
    appointment = Appointment.objects.get(pk=id)
    time = appointment.time
    for k in times:
        if Appointment.objects.filter(day=day, time=k).count() < 1 or time == k:
            x.append(k)
    return x