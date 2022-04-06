from dataclasses import field, fields
import email
from re import search, template
from urllib import request
from django.conf import settings
from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,DeleteView,UpdateView,FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView

from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Task
from .form import ContactForm
# from django.conf import settings
from django.core.mail import send_mail,BadHeaderError
from django.http import HttpResponse





class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields ='__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')

class RegisterPage(FormView):
    template_name ='base/register.html'
    form_class =UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request,user)
        return super(RegisterPage,self).form_valid(form)

    def get(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage,self).get(*args,**kwargs)


    
# class ContactUS(LoginRequiredMixin,FormView):
#     model=Contact
#     context_object_name='contactus'
#     template_name='base/contactus.html'
   
    
    
def contact_form(request):
    form=ContactForm()
    if request.method=="POST":
        form=ContactForm(request.POST)
        if form.is_valid():
            # print('Form is valid')
            subject = f'Message from {form.cleaned_data["name"]}'
            message =form.cleaned_data["message"]
            sender =form.cleaned_data["email"]
            recipients =['anirudhmaurya08@gmial.com']
            try:
                send_mail(subject,message,sender,recipients,fail_silently=True)
            except BadHeaderError:
                return HttpResponse('Invalid header found')
            return render(request,'base/success.html')
    return render(request,'base/contact.html',{'form':form})
    # 
    #     contact=Contact()
    #     name=request.POST.get('name')
    #     email=request.POST.get('email')
    #     subject=request.POST.get('subject')
    #     contact.name=name
    #     contact.email=email
    #     contact.subject=subject
    #     contact.save()
    #     return render(request,'contactus/success.html',{'name':name})
    # else:
    #     return render(request,'contactus')

    # def form_valid(self, form):
    #     return super(ContactUS,self).form_valid(form)
    
    # def get(self,*args,**kwargs):
    #     if self.request:
    #         return render(request,'contactus.html')
    #     return (ContactUS,self).get(*args,**kwargs)
    

        
        
 



class TaskList(LoginRequiredMixin,ListView):
    model = Task 
    context_object_name ='tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        search_input =self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] =context['tasks'].filter(title__startswith=search_input)
        
        context['search_input']= search_input

        return context

class TaskDetail(LoginRequiredMixin,DetailView):
    model = Task
    context_object_name ='task'
    template_name ='base/task.html'

class TaskCreate(LoginRequiredMixin,CreateView):
    model= Task
    fields = ['title','description','complete']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user =self.request.user
        return super(TaskCreate,self).form_valid(form)

class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task
    fields = ['title','description','complete']
    success_url = reverse_lazy('tasks')

class TaskDelete(LoginRequiredMixin,DeleteView):
    model = Task
    context_object_name ='task'
    success_url = reverse_lazy('tasks')

