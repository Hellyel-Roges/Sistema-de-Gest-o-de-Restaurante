$(document).ready(function () {
    let total = 0;
    let pedido = {};

   // Adicionar produtos ao carrinho pois o chefe nao quer homepage meu
    $('.adicionar-pedido').click(function () {
        const produto = $(this).data('produto');
        const preco = parseFloat($(this).data('preco'));

        if (pedido[produto]) {
            pedido[produto].quantidade += 1;
        } else {
            pedido[produto] = { preco: preco, quantidade: 1 };
        }

        total += preco;
        $('#total').text(total.toFixed(2));
        atualizarLista();
    });

    // Atualiza sa merda de lista de pedidos (Gustavo ou Guilherme nao mecha se nao vai quebra)
    function atualizarLista() {
        $('#lista-pedido').empty();
        for (const item in pedido) {
            $('#lista-pedido').append(
                `<li>${item} - R$ ${pedido[item].preco.toFixed(2)} (${pedido[item].quantidade}x)</li>`
            );
        }
    }

    // Finalizar pagamento fedelho
    $('#btn-pagar').click(function () {
        const metodo = $('#metodo-pagamento').val();
        $('#mensagem-pagamento').empty();

        if (total <= 0) {
            $('#mensagem-pagamento').html('<div class="alert alert-danger">Seu carrinho está vazio.</div>');
            return;
        }

        if (!metodo) {
            $('#mensagem-pagamento').html('<div class="alert alert-warning">Selecione um método de pagamento.</div>');
            return;
        }

    // Requisisão ajax jogando no peito do rota flask para jogar de cabeça pra classe
        $.ajax({
            url: '/api/pagamento',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                valor_total: total,
                metodo: metodo
            }),
            success: function (response) {
                if (response.status === 'ok') {
                    $('#mensagem-pagamento').html(
                        `<div class="alert alert-success">${response.mensagem}</div>`
                    );
                    total = 0;
                    pedido = {};
                    atualizarLista();
                    $('#total').text("0.00");
                } else {
                    $('#mensagem-pagamento').html(
                        `<div class="alert alert-danger">${response.mensagem}</div>`
                    );
                }
            },
            error: function () {
                $('#mensagem-pagamento').html(
                    '<div class="alert alert-danger">Erro ao processar pagamento.</div>'
                );
            }
        });
    });
});
