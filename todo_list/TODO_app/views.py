from django.shortcuts import render,redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Task
# Create your views here.

class userLogin(LoginView):
    template_name = 'TODO_app/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('task-list')
    
class registerView(FormView):
    template_name = 'TODO_app/register.html'
    form_class =UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('task-list')
    
    
    # register form save aavan vendeett.
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request,user) 
        return super(registerView,self).form_valid(form)
    
    # user login aanenkil register adkkumbol registereekk poovan paadilla.
    def get(self, *args,**kwargs):  
        if self.request.user.is_authenticated:
            return redirect('task-list')   
        return super(registerView,self).get( *args, **kwargs)

    
    

    
class taskList(LoginRequiredMixin,ListView):
    model = Task
    context_object_name = 'tasks'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = context['tasks'].filter(user=self.request.user)
        context["count"] = context['tasks'].filter(completed=False).count()
        
        # for search button 
        search_task = self.request.GET.get('search-area') or ''
        context['tasks'] = context['tasks'].filter(title__startswith = search_task)
        context['serch_task'] = search_task
        return context
        
    
class detailList(LoginRequiredMixin,DetailView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'TODO_app/task.html'
    
class createList(LoginRequiredMixin,CreateView):
    model = Task
    fields = ['title','description','completed']   
# reverse lazy is return the page
    success_url = reverse_lazy('task-list')  
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(createList,self).form_valid(form)
    
    
    
class updateList(UpdateView):
    model = Task
    fields = ['title','description','completed']   
    success_url = reverse_lazy('task-list')
    
class deleteList(DeleteView):
    model = Task
    context_object_name = 'task-delete'
    success_url = reverse_lazy('task-list')
    template_name = 'TODO_app/delete_confirm.html'
    
    
    
