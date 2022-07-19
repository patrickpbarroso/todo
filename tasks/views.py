from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Task
from .forms import TaskForm

def taskList(request):
    tasks = Task.objects.all().order_by('-created_at')
    return render(request, 'tasks/list.html', {'tasks': tasks})

def taskView(request, id):
    task = get_object_or_404(Task, pk=id)
    return render(request,'tasks/task.html', {'task': task})

def helloWorld(request):
    return HttpResponse('Hello World!')

# Inserção dos dados (C do CRUD)
def newTask(request):
    # Se for post ele envia os dados para o banco
    if request.method == 'POST':
        form = TaskForm(request.POST)

        if form.is_valid():
            task = form.save(commit=False)
            task.done = 'fazendo'
            task.save()
            return redirect('/')

    # Senão ele chama o de adicionar nova task
    else:
        form = TaskForm()
        return render(request, 'tasks/addtask.html', {'form': form})

# Edição dos dados (U do CRUD)
def editTask(request, id):
    task = get_object_or_404(Task, pk=id)
    form = TaskForm(instance=task)

    # Depois de chamar o else para fazer as alterações, aqui as alterações são salvas no banco
    if(request.method == 'POST'):
        form = TaskForm(request.POST, instance=task)
        if(form.is_valid()):
            task.save()
            return redirect('/')
        else:
            return render(request, 'tasks/edittask.html', {'form': form, 'task': task})

    else:
        return render(request, 'tasks/edittask.html', {'form': form, 'task': task})

def yourName(request, name):
    return render(request, 'tasks/yourName.html', {'name': name})