from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.http import HttpResponse
from .models import Acao
from .forms import AcaoForm
from django.contrib import messages

# Create your views here.

# Visualização dos dados (R do CRUD)
def acoesList(request):

    # Pega o conteúdo pesquisado
    search = request.GET.get('search')

    # Se o usuário digitar na barra de pesquisa
    if search:

        # Filtra as tasks pelo o que foi digitado pelo usuário
        acoes = Acao.objects.filter(codigo__icontains=search)

    # Se o usuário não digitar nada na busca, mostra todas as tasks (tarefas) ordenadas pela data de criação 
    else:
        # Obtém todas as tasks e as ordena pela data de criação
        acoes_list = Acao.objects.all().order_by('-codigo')

        #Paginação das tarefas de 3 em 3
        paginator = Paginator(acoes_list, 3)

        # Página atual
        page = request.GET.get('page')

        #Pegando as tasks da página atual
        acoes = paginator.get_page(page)

    # Envia as tasks selecionadas para serem renderizadas no código html
    return render(request, 'acoes/list.html', {'acoes': acoes})

# Visualização de uma task específica, selecionada pelo id
def acoesView(request, id):
    acao = get_object_or_404(Acao, pk=id)
    return render(request,'acoes/acao.html', {'acao': acao})

# Inserção dos dados (C do CRUD)
def newAcao(request):
    # Se o formulário já tiver preenchido ele envia os dados para o banco
    if request.method == 'POST':
        form = AcaoForm(request.POST)

        # Verifica se os dados no formulário são válidos
        if form.is_valid():
            task = form.save(commit=False)
            task.save()

            # Redireciona para a página inicial
            return redirect('/')
        
        else:
            # Redireciona para a página inicial
            return redirect('/acoes/newacao/')

    # Senão ele chama o formulário para adicionar nova tarefa
    else:
        form = AcaoForm()

        # Chama a página de adicionar nova tarefa
        return render(request, 'acoes/addacao.html', {'form': form})
    
# Edição dos dados (U do CRUD)
def editAcao(request, id):
    # Obtém a tarefa de acordo com a chave primária id
    acao = get_object_or_404(Acao, pk=id)
    # Cria um forms com os dados obtidos acima
    form = AcaoForm(instance=acao)

    # Após fazer as alterações e o formulário for válido , elas são salvas no banco
    if(request.method == 'POST'):
        form = AcaoForm(request.POST, instance=acao)
        if(form.is_valid()):
            acao.save()
            return redirect('/acoes/')
        else:
            return render(request, 'acoes/editacao.html', {'form': form, 'acao': acao})

    # Caso ocorra algum outro tipo de requisição, a página de editar task é chamada novamente
    else:
        return render(request, 'acoes/editacao.html', {'form': form, 'acao': acao})
    
def deleteAcao(request, id):
    # Obtém a task com o id passado
    acao = get_object_or_404(Acao, pk=id)
    # Deleta a task encontrada acima
    acao.delete()

    # Mostra a mensagem na tela
    messages.info(request, 'Ação deletada com sucesso')

    # Redireciona de volta para a página inicial
    return redirect('/')
    
