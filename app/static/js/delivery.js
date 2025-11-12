$(document).ready(function () {

    let pedidoId = null;
    let carrinho = {}; // { produto_id: {nome, preco, qtd} }

    // -------------------- UTIL --------------------
    function mostrarMensagem(texto, tipo = "success") {
        // Sua função original. Vai funcionar com o CSS novo.
        $("#mensagem")
            .html(`<div class="alert alert-${tipo} alert-dismissible fade show" role="alert">
                      ${texto}
                      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                   </div>`);
    }

    function atualizarCarrinho() {
        let html = "";
        let total = 0;

        if (Object.keys(carrinho).length === 0) {
            // Usa a classe 'text-muted' que o CSS vai estilizar
            html = '<li class="list-group-item text-muted">Seu carrinho está vazio.</li>';
        } else {
            for (let id in carrinho) {
                let item = carrinho[id];
                total += item.preco * item.qtd;

                // !!!! MUDANÇA AQUI (CORRIGE O TEXTO CINZA) !!!!
                // Este é o novo HTML para o item do carrinho
                html += `
                <li class="list-group-item d-flex justify-content-between align-items-center">
                    <div>
                        <strong class="text-gold">${item.nome}</strong>
                        <small class="d-block text-light"> 
                            R$ ${item.preco.toFixed(2)} x ${item.qtd}
                        </small>
                    </div>
                    <div>
                        <span class="fw-bold me-3 text-light">R$ ${(item.preco * item.qtd).toFixed(2)}</span>
                        
                        <button class="btn btn-sm btn-outline-danger btn-remover" data-id="${id}">
                            <i class="bi bi-trash"></i>
                        </button>
                    </div>
                </li>`;
            }
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
                
                // !!!! MUDANÇA AQUI (DEIXA O CARD BONITO) !!!!
                // Este é o novo HTML para o card do produto
                html += `
                <div class="col-md-6 mb-4">
                    <div class="produto-card">
                        <img src="${p.imagem || '/static/img/prato_massa.png'}" class="produto-card-img" alt="${p.nome}">
                        <div class="produto-card-body">
                            <h5 class="produto-card-title">${p.nome}</h5>
                            <p class="produto-card-text">${p.descricao || 'Descrição não disponível.'}</p>
                            <p class="produto-card-price">R$ ${p.preco.toFixed(2)}</p>

                            <button class="btn btn-gold w-100 btn-add" data-id="${p.id}" data-nome="${p.nome}" data-preco="${p.preco}">
                                Adicionar <i class="bi bi-plus-lg"></i>
                            </button>
                        </div>
                    </div>
                </div>`;
            });
            $("#produtos").html(html);
        }
    });

    // ----------------------------------------------------
    // O RESTO DO SEU ARQUIVO (LÓGICA DE API)
    // NÃO MUDA NADA DAQUI PARA BAIXO
    // ----------------------------------------------------

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
            },
            error: function() {
                mostrarMensagem("Erro ao criar pedido. Tente novamente.", "danger");
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
                },
                error: function() {
                    mostrarMensagem("Erro ao adicionar item.", "danger");
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
            },
            error: function() {
                mostrarMensagem("Erro ao remover item.", "danger");
            }
        });
    });

    // -------------------- FINALIZAR E PAGAR --------------------
    $("#btn-finalizar").click(function () {
        if (!pedidoId || Object.keys(carrinho).length === 0) {
            mostrarMensagem("Seu carrinho está vazio!", "danger");
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
                $("#metodo").val(""); // Limpa o select
            },
            error: function(jqXHR) {
                let erro = jqXHR.responseJSON ? jqXHR.responseJSON.mensagem : "Erro ao finalizar pagamento.";
                mostrarMensagem(erro, "danger");
            }
        });
    });

});