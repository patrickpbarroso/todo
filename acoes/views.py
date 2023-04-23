from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.http import HttpResponse
from .models import Acao
from .forms import AcaoForm
from django.contrib import messages
import yfinance as yf
import pandas as pd
import numpy as np

# Create your views here.

# Visualização dos dados (R do CRUD)
def acoesList(request):

    # Pega o conteúdo pesquisado
    search = request.GET.get('search')

    # Se o usuário digitar na barra de pesquisa
    if search:

        # Filtra as ações pelo o que foi digitado pelo usuário
        acoes_list = Acao.objects.filter(codigo__icontains=search)

    # Se o usuário não digitar nada na busca, mostra todas as tasks (tarefas) ordenadas pela data de criação 
    else:
        # Populando a base de dados
        # Obtém o ticket de uma ação
        msft = yf.Ticker("PETR4.SA")

        # Obtém todas as informações da ação
        acao_info = msft.info
        
        # Obtém dados históricos de mercado para a ação
        hist = msft.history(period="max")
        hist = hist.head(25)

        # Cria duas colunas no dataframe para guardar código e descrição da ação
        hist['Code'] = acao_info['symbol']
        hist['Description'] = acao_info['longName']

        #Verifica se a base de dados já foi populada. Se sim, continua. Se não, preenche com os dados do yfinance


        if not Acao.objects.filter(codigo__icontains=hist.iloc[1].Code):
            for date, row in hist.iterrows():
                new_stock = Acao.objects.create(
                    codigo = row.Code,
                    descricao = row.Description,
                    data = date,
                    open = row.Open,
                    close = row.Close,
                    high = row.High,
                    low = row.Low,
                    volume = row.Volume
                )
                new_stock.save()
        
        # Obtém todas as ações da base de dados
        acoes_list = Acao.objects.all()


    # Envia as tasks selecionadas para serem renderizadas no código html
    return render(request, 'acoes/list.html', {'acoes': acoes_list})

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
    
