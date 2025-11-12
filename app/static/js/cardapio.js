$(document).ready(function () {
    const container = $('#cardapio-container');

    // Carregar produtos da API
    $.ajax({
        url: "/api/produtos",
        method: "GET",
        success: function (produtos) {

            if (!produtos || produtos.length === 0) {
                container.html('<p class="text-muted">Nenhum item no cardápio no momento.</p>');
                return;
            }

            // Limpa o "Carregando..."
            container.empty();

            // Itera sobre os produtos e cria o HTML
            produtos.forEach(p => {
                const itemHtml = `
                <div class="col-md-10 col-lg-8 mx-auto">
                    <div class="menu-item">
                        <div class="menu-item-header">
                            <span class="menu-item-nome">${p.nome}</span>
                            <span class="menu-item-preco">R$ ${p.preco.toFixed(2)}</span>
                        </div>
                        <p class="menu-item-descricao">
                            ${p.descricao || 'Prato especial da casa.'}
                        </p>
                    </div>
                </div>
                `;
                container.append(itemHtml);
            });
        },
        error: function () {
            container.html('<p class="text-danger">Erro ao carregar o cardápio. Tente novamente.</p>');
        }
    });
});