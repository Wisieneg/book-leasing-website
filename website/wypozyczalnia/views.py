from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from django.utils import timezone
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import book,lease


def index(request):
    template=loader.get_template('wypozyczalnia/index.html')
    cat=request.GET.get('cat','')
    dexists=False
    recomendations=[]
    books_lista={}
    if request.POST.get('title') is not None:
        x=request.POST.get('title')
        try:
            books_lista=book.objects.filter(title__icontains=x)
            if cat=='':
                o=0
            else:
                books_lista=books_lista.filter(category=cat)
        except book.DoesNotExist:
            dexists=True

    else:
        if cat=='':
            books_lista=book.objects.all().order_by('title')
        else:
            try:
                books_lista=book.objects.filter(category=cat)
            except book.DoesNotExist:
                books_lista={}

    if request.user.id is None:
        recomendations=book.objects.all().order_by('pub_date')[:4]
    else:
        l=lease.objects.filter(client=request.user)
        if len(l)>0:
            cat=l[len(l)-1].book.category
            recomendations=book.objects.filter(category=cat)[:4]
        else:
            recomendations=book.objects.all().order_by('pub_date')[:4]
    context={'books':books_lista,'recomendations':recomendations,}
    return HttpResponse(template.render(context,request))


def book_view(request,book_id):
    book1=book.objects.get(pk=book_id)
    available=False
    lensed=None
    if book1.amount>0:
        available=True
    leases=lease.objects.filter(client=request.user)
    for l in leases:
        if l.book==book1:
            lensed=True

    message=request.GET.get("message","a")
    template=loader.get_template('wypozyczalnia/book_view.html')
    context={'book':book1,'available':available,'message':message,'lensed':lensed,}
    return HttpResponse(template.render(context,request))

@login_required(login_url='/wypozyczalnia/login/')
def account(request):
    leases=lease.objects.filter(client=request.user)
    books=[]
    for l in leases:
        if l.client==request.user:
            books.append(l.book)
    template=loader.get_template('wypozyczalnia/account.html')
    context={'books':books,}
    return HttpResponse(template.render(context,request))

@login_required(login_url='/wypozyczalnia/login/')
def checkout(request,book_id):
    book1=book.objects.get(pk=book_id)
    leases=lease.objects.filter(client=request.user)
    for x in leases:
        if x.book==book1:
            message="Wypożyczyłeś już tę książkę!"
            link='/wypozyczalnia/book/'+str(book_id)
            link+='?message='+message
            return HttpResponseRedirect(link)

    if len(leases)==4:
        message="Osiągnąłeś limit wypożyczonych książek (4)"
        link='/wypozyczalnia/book/'+str(book_id)
        link+='?message='+message
        return HttpResponseRedirect(link)

    if book1.amount==0:
        message="Ta książka jest obecnie niedostępna"
        link='/wypozyczalnia/book/'+str(book_id)
        link+='?message='+message
        return HttpResponseRedirect(link)
    else:
        book1.amount=book1.amount-1
        book1.save()
    lease_instance=lease.objects.create(client=request.user,book=book1)
    return HttpResponseRedirect('/wypozyczalnia/account')

@login_required(login_url='/wypozyczalnia/login/')
def giveback(request,book_id):
    book1=book.objects.get(pk=book_id)
    lease.objects.filter(client=request.user,book=book1).delete()
    book1.amount+=1
    book1.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def login_view(request):
    exist=False
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        template=loader.get_template("wypozyczalnia/login.html")

        if user is not None:
            login(request,user)
            return HttpResponseRedirect(reverse('wypozyczalnia:index'))

        else:
            exist=True
            return render(request, 'wypozyczalnia/login.html', {'exist': exist})

    else:
        return render(request, 'wypozyczalnia/login.html', {'exist': exist})

@login_required(login_url='/wypozyczalnia/login/')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('wypozyczalnia:index'))
