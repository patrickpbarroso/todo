from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Task
from .forms import TaskForm

def taskList(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/list.html', {'tasks': tasks})

def taskView(request, id):
    task = get_object_or_404(Task, pk=id)
    return render(request,'tasks/task.html', {'task': task})

def helloWorld(request):
    return HttpResponse('Hello World!')

def newTask(request):
    form = TaskForm()
    return render(request, 'tasks/addtask.html', {'form': form})

def yourName(request, name):
    return render(request, 'tasks/yourName.html', {'name': name})