from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.http import HttpResponse
from .models import Task
from .forms import TaskForm
from django.contrib import messages

# Visualização dos dados (R do CRUD)
def taskList(request):

    # Pega o conteúdo pesquisado
    search = request.GET.get('search')

    if search:

        tasks = Task.objects.filter(title__icontains=search)

    else:
        # Obtém todas as tasks e as ordena pela data de criação
        tasks_list = Task.objects.all().order_by('-created_at')

        #Paginação das tarefas de 3 em 3
        paginator = Paginator(tasks_list, 3)

        # Página atual
        page = request.GET.get('page')

        #Pegando as tasks da página atual
        tasks = paginator.get_page(page)

    return render(request, 'tasks/list.html', {'tasks': tasks})

# Visualização de uma task específica, selecionada pelo id
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

def deleteTask(request, id):
    # Obtém a task com o id passado
    task = get_object_or_404(Task, pk=id)
    # Deleta a task encontrada acima
    task.delete()

    # Mostra a mensagem na tela
    messages.info(request, 'Tarefa deletada com sucesso')

    # Redireciona de volta para a página inicial
    return redirect('/')

def yourName(request, name):
    return render(request, 'tasks/yourName.html', {'name': name})