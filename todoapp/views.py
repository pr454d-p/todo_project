from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from datetime import date
from .models import Task
from . forms import TodoForm



@login_required(login_url='account:login')
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

    return render(request,'update.html',{'form':form})
