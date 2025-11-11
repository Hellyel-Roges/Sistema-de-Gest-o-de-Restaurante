$(document).ready(function () {
    let pedidoId = null;
    
    // Iniciar pedido
    $("#iniciar-pedido").click(function () {
        const cpf = $("#cpf").val().trim();

        if (!cpf) {
            alert("Digite seu CPF.");
            return;
        }

        $.ajax({
            url: "/api/pedido",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({ cpf: cpf }),
            success: function (response) {
                if (response.status === "ok") {
                    pedidoId = response.pedido_id;
                    $("#cpf").prop("disabled", true);
                    $("#iniciar-pedido").hide();
                    alert("Pedido iniciado com sucesso!");
                } else {
                    alert(response.mensagem);
                }
            }
        });
    });

    // Adicionar produto ao pedido
    $(".adicionar-pedido").click(function () {
        if (!pedidoId) {
            alert("Digite o CPF e clique em iniciar pedido primeiro.");
            return;
        }

        let produtoId = $(this).data("produto-id");

        $.ajax({
            url: `/api/pedido/${pedidoId}/item`,
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({ produto_id: produtoId }),
            success: function () {
                atualizarTotal();
            }
        });
    });

    // Atualizar valor total
    function atualizarTotal() {
        $.ajax({
            url: `/api/pedido/${pedidoId}/total`,
            type: "GET",
            success: function (response) {
                $("#total").text(response.total.toFixed(2));
            }
        });
    }

    // Finalizar pagamento
    $("#btn-pagar").click(function () {
        if (!pedidoId) {
            alert("Nenhum pedido iniciado.");
            return;
        }

        const metodo = $("#metodo-pagamento").val();

        if (!metodo) {
            alert("Selecione uma forma de pagamento.");
            return;
        }

        $.ajax({
            url: `/api/pedido/${pedidoId}/pagar`,
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({ forma_pagamento: metodo }),
            success: function (response) {
                if (response.status === "ok") {
                    alert("Pagamento iniciado. Confirme no painel do garçom ou caixa.");
                } else {
                    alert(response.mensagem);
                }
            }
        });
    });
});
