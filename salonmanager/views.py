from datetime import date, timedelta
from decimal import Decimal
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import StaffMember,Customer,Service,Branch,Appointment

from .utils import timeslot_gen_tf,calculate_end_time

# Create your views here.
def manager_signup(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your password and confirm password are not Same!!")
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('manager_login')
    return render (request,'manager_signup.html')

def manager_login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            
            return redirect('manager_dashboard')
        else:
            return redirect('manager_login')
    return render (request,'manager_login.html')
@login_required(login_url='/salonmanager/login/')
def manager_dashboard(request):
    return render(request,'base.html')

def appointment_booking(request):
    time_slot_tf = timeslot_gen_tf('10:00 AM','10:00 PM')
    appointment_list=[]
    staff_members_list= StaffMember.objects.all()
    
    branches  = Branch.objects.all()
    if request.method =='POST':
        selected_date = request.POST.get('selected_date')
        selected_time = request.POST.get('selected_time')
        selected_staff = request.POST.get('selected_staff')
        selected_branch = request.POST.get('selected_branch')
        selected_services = request.POST.getlist('service-name')
        selected_customer = request.POST.get('customer')
        customer = get_object_or_404(Customer,id=  selected_customer)
        staff = get_object_or_404(StaffMember, name= selected_staff)
        branch = get_object_or_404(Branch,name = selected_branch)
        
        total_duration = timedelta()
        total_prices=[]
        services_list = []
        for services in selected_services:
            service_objs = Service.objects.get(name = services)
            duration = service_objs.duration
            total_prices.append(service_objs.price)
            total_duration = total_duration+duration
            services_list.append(service_objs)
            
        end_time = calculate_end_time(selected_time,total_duration)
        total_price = sum([Decimal(str(price.amount)) for price in total_prices])
        print(selected_time,end_time,total_price)
        appointment_details= Appointment.objects.create(
             customer=customer,
            staff_member=staff,
            start_time=selected_time,
            end_time=end_time,
            date=selected_date,
            total_price = total_price,
            status = 'booked',
            branch = branch,
        )
        appointment_details.services.set(services_list)
    else:
        
        if Appointment.objects.exists:
            today = date.today()
            appointment_list_today = Appointment.objects.filter(date=today)
        for appointment in appointment_list_today:
            customer_id = appointment.customer_id
            customer  = get_object_or_404(Customer,id = customer_id)
            staff_member_id = appointment.staff_member_id
            staff_member = get_object_or_404(StaffMember,id = staff_member_id)
            branch_id = appointment.branch_id
            branch = get_object_or_404(Branch,id=branch_id)
            start_time_str = appointment.start_time.strftime("%H:%M:%S")
            services = appointment.services.all()
            appointment_dict={
                'customer':customer,
                'staff_member':staff_member.name,
                'start_time':start_time_str,
                'end_time':appointment.end_time,
                'date':appointment.date,
                'total_price':appointment.total_price,
                'status':appointment.status,
                'branch':branch,
                'services': services,
                'id':appointment.pk
            }
            print(type(appointment_dict['start_time']))
            appointment_list.append(appointment_dict)
        print(appointment_list)
    return render(request,'appointment_booking.html',{'time_slots':time_slot_tf,'staff_members':staff_members_list,'branches':branches,'appointment_details_list':appointment_list})
def save_appointment(request):
    existing_customer=  Customer.objects.all
    staff_members = StaffMember.objects.all
    services = Service.objects.all
    categories = Service.objects.values_list('category', flat=True).distinct()
    branches = Branch.objects.all()
    
    
    global selected_date, selected_time, selected_staff
    if request.method == 'POST':
        selected_staff = request.POST.get('staff-name')
        selected_time = request.POST.get('start-time')
        selected_date = request.POST.get('date')
        selected_branch = request.POST.get('branch')
    
    
    context={
        'existing_customers':existing_customer,'selected_staff':selected_staff,'selected_time':selected_time,'selected_date':selected_date,
        'selected_branch': selected_branch,'services':services,'categories':categories,'staff_members':staff_members,'branches':branches    }
        
    return render(request, 'save_appointment.html',context)