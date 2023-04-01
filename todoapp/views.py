from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from datetime import date
from .models import Task
from . forms import TodoForm
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView,DeleteView,CreateView
from django.urls import reverse_lazy

# Create your views here.
class TaskListView(ListView):
    model = Task
    template_name = 'home.html'
    context_object_name = 'tasks'
    fields = ('title','priority','date')

class TaskCreateView(CreateView):
    model = Task
    template_name = 'create.html'
    context_object_name = 'tasks'
    fields = ('title','priority','date')
    success_url = reverse_lazy('cbvhome')


class TaskDetailView(DetailView):
    model = Task
    template_name = 'detail.html'
    context_object_name = 'task'

class TaskUpdateView(UpdateView):
    model = Task
    template_name = 'update.html'
    context_object_name = 'task'
    fields = ('title','priority','date')

    def get_success_url(self):
        return reverse_lazy('cbvdetail',kwargs= {'pk': self.object.id})


class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'delete.html'
    success_url = reverse_lazy('cbvhome')

# @login_required
# def index(request):
#     user = request.user
#     tasks = Task.objects.all()
#     if request.method == 'POST':
#         form = TodoForm(request.POST)
#         if form.is_valid():
#             # Save the form data to the database
#             todo_item = form.save(commit=False)
#             todo_item.user = request.user
#             todo_item.save()
#             return redirect('/')
#         # title = request.POST.get('title','')
#         # priority = request.POST.get('priority','')
#         # date = request.POST.get('date','')
#         # todo_item.user = request.user
#         # task = Task(title= title,priority = priority,date=date)
#         # task.save()
#     return render(request,'index.html',{'tasks': tasks})
# @login_required(login_url='login')
# def index(request):
#     user = request.user
#     tasks = Task.objects.filter(user=user)
#     if request.method == 'POST':
#         # Save the form data to the database
#         title = request.POST.get('title','')
#         priority = request.POST.get('priority','')
#         date = request.POST.get('date','')
#         user = request.user
#         task = Task(title= title,priority = priority,date=date,user=user)
#         task.save()
#     return render(request,'index.html',{'tasks': tasks})

@login_required(login_url='account/login')
def index(request):
    user = request.user
    tasks = Task.objects.filter(user=user).order_by('priority')
    form = TodoForm()

    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo_item = form.save(commit=False)
            todo_item.user = request.user
            todo_item.save()
            return redirect('/')

    return render(request, 'index.html', {'tasks': tasks, 'form': form,'today':date.today().strftime('%Y-%m-%d')})

@login_required
def delete(request,taskid):
    task = Task.objects.get(id=taskid, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('/')
    return render(request,'delete.html')

@login_required
def update(request,id):
    task = Task.objects.get(id = id,user=request.user)
    form = TodoForm(request.POST or None, instance = task)
    print(task)
    if form.is_valid():
        form.save()
        return redirect('/')

    return render(request,'edit.html',{'form':form})
