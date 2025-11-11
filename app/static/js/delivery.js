$(document).ready(function () {

    let pedidoId = null;
    let carrinho = {}; // { produto_id: {nome, preco, qtd} }

    // -------------------- UTIL --------------------
    function mostrarMensagem(texto, tipo = "success") {
        $("#mensagem")
            .html(`<div class="alert alert-${tipo}">${texto}</div>`);
        setTimeout(() => $("#mensagem").html(""), 3000);
    }

    function atualizarCarrinho() {
        let html = "";
        let total = 0;

        for (let id in carrinho) {
            let item = carrinho[id];
            total += item.preco * item.qtd;
            html += `
                <li>
                    ${item.nome} (x${item.qtd}) - R$ ${(item.preco * item.qtd).toFixed(2)}
                    <button class="btn btn-sm btn-danger btn-remover" data-id="${id}">X</button>
                </li>`;
        }

        $("#lista-pedido").html(html);
        $("#total").text(total.toFixed(2));
    }

    // -------------------- CARREGA PRODUTOS VIA AJAX --------------------
    $.ajax({
        url: "/api/produtos",
        method: "GET",
        success: function (produtos) {
            let html = "";
            produtos.forEach(p => {
                html += `
                <div class="col-md-4 mb-4">
                    <div class="card p-3 shadow">
                        <h4>${p.nome}</h4>
                        <p>${p.descricao}</p>
                        <b>R$ ${p.preco.toFixed(2)}</b>
                        <button class="btn btn-primary btn-add mt-2" data-id="${p.id}" data-nome="${p.nome}" data-preco="${p.preco}">
                            Adicionar
                        </button>
                    </div>
                </div>`;
            });
            $("#produtos").html(html);
        }
    });

    // -------------------- CRIAR PEDIDO AUTOMATICAMENTE AO ADICIONAR ITEM --------------------
    function criarPedidoSeNaoExistir(callback) {
        if (pedidoId) {
            callback();
            return;
        }
        $.ajax({
            url: "/api/pedido",
            method: "POST",
            contentType: "application/json",
            data: JSON.stringify({}),
            success: function (res) {
                pedidoId = res.id;
                mostrarMensagem("Pedido iniciado.");
                callback();
            }
        });
    }

    // -------------------- ADICIONAR ITEM --------------------
    $(document).on("click", ".btn-add", function () {
        let id = $(this).data("id");
        let nome = $(this).data("nome");
        let preco = parseFloat($(this).data("preco"));

        criarPedidoSeNaoExistir(() => {
            $.ajax({
                url: `/api/pedido/${pedidoId}/item`,
                method: "POST",
                contentType: "application/json",
                data: JSON.stringify({ produto_id: id, quantidade: 1 }),
                success: function () {
                    if (!carrinho[id]) carrinho[id] = { nome, preco, qtd: 0 };
                    carrinho[id].qtd++;
                    atualizarCarrinho();
                }
            });
        });
    });

    // -------------------- REMOVER ITEM --------------------
    $(document).on("click", ".btn-remover", function () {
        let id = $(this).data("id");

        $.ajax({
            url: `/api/pedido/${pedidoId}/item`,
            method: "DELETE",
            contentType: "application/json",
            data: JSON.stringify({ produto_id: id, quantidade: 1 }),
            success: function () {
                carrinho[id].qtd--;
                if (carrinho[id].qtd <= 0) delete carrinho[id];
                atualizarCarrinho();
            }
        });
    });

    // -------------------- FINALIZAR E PAGAR --------------------
    $("#btn-finalizar").click(function () {
        if (!pedidoId) {
            mostrarMensagem("Você não adicionou itens!", "danger");
            return;
        }

        let metodo = $("#metodo").val();
        if (!metodo) {
            mostrarMensagem("Escolha a forma de pagamento.", "danger");
            return;
        }

        $.ajax({
            url: `/api/pedido/${pedidoId}/pagar`,
            method: "POST",
            contentType: "application/json",
            data: JSON.stringify({ forma_pagamento: metodo }),
            success: function (res) {
                mostrarMensagem(`Pagamento realizado! Total R$ ${res.total.toFixed(2)}`);
                carrinho = {};
                pedidoId = null;
                atualizarCarrinho();
            }
        });
    });

});
