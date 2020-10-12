from django.shortcuts import render, redirect
from django.forms import modelformset_factory, TextInput, NumberInput
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers
from .forms import EmpForm, ContactModelForm
from .models import Office, Employee, Jobs, Contact, Product
from .serializers import JobsSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
from django.contrib.auth.models import User
from django.views.generic import View, TemplateView, ListView
from validate_email import validate_email
from django.core.mail import send_mail
from django.conf import settings


class UsernameValidationView(View):
    def post(self, request):
            data = json.loads(request.body)
            name = data['username']

            if not str(name).isalnum():
                return JsonResponse({'username_error': 'username should only contain alphanumeric character'}, status=400)
            if User.objects.filter(username=name).exists():
                return JsonResponse({'username_error': 'sorry this user already exists, try another name'}, status=409)
            return JsonResponse({'username_valid': True})

class EmailValidationView(View):
    def post(self, request):
            data = json.loads(request.body)
            email = data['email']

            if not validate_email(email):
                return JsonResponse({'email_error': 'Incorrect email, please provide valid email'}, status=400)
            if User.objects.filter(email=email).exists():
                return JsonResponse({'email_error': 'sorry this email already taken, try another one'}, status=409)
            return JsonResponse({'email_valid': True})

class RegistrationView(TemplateView):
    template_name = 'modelform/signup.html'

    def post(self, request):

        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        send_mail(
            name,
            password,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

        User.objects.create(
            username=name,
            email=email,
            password=password
        )
        return HttpResponse('')


# Create your views here.
def home(request):
    form = EmpForm()
    formset = modelformset_factory(Office, fields=('name','branch','code','city','employee'),widgets={'name':TextInput(attrs={'class':'form-control'}),
                                                                                                            'branch':TextInput(attrs={'class':'form-control'}),
                                                                                                            'code':NumberInput(attrs={'class':'form-control'}),
                                                                                                            'city':TextInput(attrs={'class':'form-control'}),
                                                                                                            'employee':TextInput(attrs={'class':'form-control'})})
    return render(request, 'modelform/home.html', {'form': form, 'formset': formset})

def job_list(request):
    list  = Jobs.objects.all()
    return render(request, 'modelform/jobs.html', {'list': list})


@api_view(['GET'])
def get_jobs(request):
    location = request.query_params.get('location', None)
    job_type = request.query_params.get('job_type', None)
    sort_jobs = request.query_params.get('sort_jobs', None)
    jobs = Jobs.objects.all()
    if location:
        jobs = jobs.filter(location=location)
    if job_type:
        jobs = jobs.filter(job_type=job_type)
    if sort_jobs:
        if sort_jobs == 'ascending':
            jobs = jobs.all().order_by('-posted_on')
        elif sort_jobs == 'descending':
            jobs = jobs.all().order_by('posted_on')
    if jobs:
        serialized = JobsSerializer(jobs, many=True)
        return Response(serialized.data)
    else:
        return Response({})

def employee(request):
    emp = Employee.objects.all()
    return render(request, 'modelform/employee.html', {'emp': emp})

def office(request):
    off = Office.objects.all()
    return render(request, 'modelform/office.html', {'off': off})

def city(request):
    return render(request, 'modelform/city.html')

def postEmp(request):
    # request should be ajax and method should be POST.
    if request.is_ajax and request.method == 'POST':
        # get the form data
        form = EmpForm(request.POST)
        # save the data and after fetch the object in instance
        if form.is_valid():
            instance = form.save()
            # serialize in new friend object in json
            ser_instance = serializers.serialize('json', [instance, ])
            # send to client side.
            return JsonResponse({'instance': ser_instance}, status=200)
        else:
            # some form errors occured.
            return JsonResponse({'error': form.errors}, status=400)

    # some error occured
    return JsonResponse({'error': ''}, status=400)

def getEmpName(request):
    # request should be ajax and method should be GET.
    if request.is_ajax and request.method == "GET":
        # get the employee name from the client side.
        name = request.GET.get('name', None)
        if Employee.objects.filter(name=name).exists():
            # if name found return not valid new friend
            return JsonResponse({"valid": False}, status=200)
        else:
            # if name not found, then user can create a new friend.
            return JsonResponse({'valid': True}, status=200)
    return JsonResponse({}, status=400)

def postOff(request):
    return JsonResponse({'errors': ''}, status=400)

def contactPost(request):
    myForm = ContactModelForm()
    # if request.method == 'POST':
    #     myForm = ContactModelForm(request.POST)
    #     if myForm.is_valid():
    #         myForm.save()
    #         return redirect('contact')
    if request.is_ajax:
        myForm = ContactModelForm(request.POST)
        if myForm.is_valid():
            myForm.save()
            return JsonResponse({'msg':'Success'})

    return render(request, 'modelform/contact.html', {'myForm': myForm})

def checkName(request):
    if request.is_ajax and request.method == 'GET':
        name = request.GET['username']
        check = Contact.objects.filter(name=name)
        if len(check) == 1:
            return JsonResponse({'msg': 'Exists'})
        else:
            return JsonResponse({'msg': 'Not Exists'})


class CrudView(ListView):
    model = Product
    template_name = 'modelform/crud.html'
    context_object_name = 'things'


class CreateCrudView(View):
    def get(self, request):
        name1 = request.GET.get('name', None)
        category1 = request.GET.get('category', None)
        price1 = request.GET.get('price', None)

        obj = Product.objects.create(
            productname=name1,
            category=category1,
            price=price1
        )

        thing = {'id':obj.id,'name':obj.productname,'category':obj.category,'price':obj.price}

        data = {
            'thing': thing
        }
        return JsonResponse(data)


class UpdateCrudView(View):
    def get(self, request):
        id1 = request.GET.get('id', None)
        name1 = request.GET.get('name', None)
        category1 = request.GET.get('category', None)
        price1 = request.GET.get('price', None)

        obj = Product.objects.get(id=id1)
        obj.productname = name1
        obj.category = category1
        obj.price = price1
        obj.save()

        thing = {'id':obj.id,'name':obj.productname,'category':obj.category,'price':obj.price}

        data = {
            'thing': thing
        }
        return JsonResponse(data)


class DeleteCrudView(View):
    def get(self, request):
        id1 = request.GET.get('id', None)
        Product.objects.get(id=id1).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)


