from django.shortcuts import render,redirect
from . models import Task
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

def index(request):
    tasks = Task.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title','')
        priority = request.POST.get('priority','')
        date = request.POST.get('date','')
        task = Task(title= title,priority = priority,date=date)
        task.save()
    return render(request,'index.html',{'tasks': tasks})


def delete(request,taskid):
    task = Task.objects.get(id=taskid)
    if request.method == 'POST':
        task.delete()
        return redirect('/')
    return render(request,'delete.html')

def update(request,id):
    task = Task.objects.get(id = id)
    form = TodoForm(request.POST or None, instance = task)
    if form.is_valid():
        form.save()
        return redirect('/')

    return render(request,'edit.html',{'form':form})