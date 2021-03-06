from django.shortcuts import render,render_to_response #imports a render method which is userd to load the template
from django.http import HttpResponse #Used to return the Http Response
from django.db import connection #Used to Connect with The Database
from django.contrib.auth.models import User #Used to store the login Information
from django.contrib.auth import authenticate, login, logout #authenticate is used to confirm the logging user details
from django.contrib.auth.decorators import login_required
from .models import SignUp,Appointment
import MySQLdb
# Create your views here.


def home(request):
    '''
        Home page..
    '''
    return HttpResponse(render(request, "patient/home.html"))



def login_user(request):
    '''
        Acccepts the Login Details And checks wether the user is authenticated
    '''
    if(request.method == "POST"):
        username = request.POST.get('un')
        password = request.POST.get('pwd')
        #Authenticating The User Details
        user = authenticate(username = username, password = password)

        if(user):
            login(request, user)
            # If Registered Then Proceed
            return HttpResponse(render(request, "patient/login_success.html"))

        else:
            #if Not Registered Then ask to signup
            context = {"stop":True}
            return HttpResponse(render(request, "patient/login.html", context))

    else:
        #If the method is "GET"
        return HttpResponse(render(request, "patient/login.html"))




def signup(request):
    '''
        SignUp Page Accepts the signup Details.....
    '''
    if(request.method == "POST"):
        ID = SignUp.objects.count()
        ID += 1000
        name = request.POST.get('Full_name')
        address = request.POST.get('Address')
        contact = int(request.POST.get('Contact'))
        gender = request.POST.get('Gender')
        pemail = request.POST.get('email')
        password = request.POST.get('Password')
        Cpassword = request.POST.get('CPassword')
        dnames = name.split()


        if(password!=Cpassword):
            context = {"stop": True}
            return HttpResponse(render(request, "patient/signup.html", context))


        try:
            #Inserting the values into User table(Builtin) Which is checked for User Authentication The None feild is for email
            user = User.objects.create_user(name, email = pemail, password = password, id=ID, first_name = dnames[0], last_name = dnames[-1], is_staff=0)
            #Establish The Connection
            c = connection.cursor()
            #Executing The Query
            c.execute("INSERT INTO hospital_signup(patient_id,Name,Address,Contact,Gender,Password,Email) VALUES ('%d','%s', '%s', '%d', '%s', '%s', '%s')" % (ID, name, address, contact, gender, password, pemail))
            return HttpResponse(render(request, "patient/signsuccess.html"))
        except Exception as e:
            print(e)

    else:
        #If the method is "GET"
        return HttpResponse(render(request, "patient/signup.html"))


@login_required
def appointment(request):
    '''
        The Appointment page Creates an Appointment with the Doctor
    '''
    if(request.method == 'POST'):
        pid = int(request.POST.get('pid'))
        Pname = request.POST.get('pname')
        docname = request.POST.get('docName')
        appointment_date = request.POST.get('date')
        appointment_time = request.POST.get('time')
        disease = request.POST.get('ill')
        ID = Appointment.objects.count()
        ID+=1

        try:
            c = connection.cursor()
            c.execute("Select * from hospital_appointment where AppointmentDate='%s' and AppointmentTime='%s' and Doctor_Name='%s'" % (appointment_date, appointment_time, docname))
            free = c.fetchone()

            if(free):
                context = {"stop" : True}
                return HttpResponse(render(request, "patient/appointment.html", context))

            else:
                c.execute("INSERT INTO hospital_appointment(ID,pid,Patient_Name,Doctor_Name,AppointmentDate,AppointmentTime,Disease) VALUES (%d,%d,'%s', '%s', '%s', '%s', '%s')" % (
                    ID, pid, Pname, docname, appointment_date, appointment_time, disease))
                c.execute("Select * from hospital_appointment")
                appointments = c.fetchall()
                context = {"appointments" : appointments}
                return HttpResponse(render(request, "patient/appointment_success.html", context))

        except Exception as e:
            print(e)
            
    else:
        #If the method is "GET"
        return HttpResponse(render(request, "patient/appointment.html"))



def forgetpassword(request):
    '''
        Gives the link to password reset if Forgot....
    '''
    return HttpResponse(render(request, "patient/forgetpassword.html"))



def signsuccess(request):
    '''
        Used to Redirect To the Login Page
    '''
    return HttpResponse(render(request, "patient/signsuccess.html")) 

