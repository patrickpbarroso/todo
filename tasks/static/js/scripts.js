$(document).ready(function(){

    // Recebe o botão de deletar
    var deleteBtn = $('.delete-btn');

    // Quando é clicado no botão acima executa a função
    $(deleteBtn).on('click', function(evento){

        // Não deixa ser executada a ação do botão
        evento.preventDefault();

        // Link de deletar
        var delLink = $(this).attr('href');

        // Opção do usuário de deletar ou não
        var result = confirm('Quer deletar esta tarefa?')

        // Se o usuário clicou na opção deletar
        if(result){
            // O usuário é redirecionado para a deleção e o registro é excluído
            window.location.href = delLink;
        }
    })

});