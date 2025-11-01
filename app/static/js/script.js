$(document).ready(function () {
    let total = 0;
    let pedido = {}; // Armazena os produtos e quantidades

    $('.adicionar-pedido').click(function () {
        const produto = $(this).data('produto');
        const preco = parseFloat($(this).data('preco'));

        // Verifica se o produto já está no pedido
        if (pedido[produto]) {
            pedido[produto].quantidade += 1;
        } else {
            pedido[produto] = { preco: preco, quantidade: 1 };
        }

        // Atualiza o total
        total += preco;
        $('#total').text(total.toFixed(2));

        // Atualiza a lista do pedido
        $('#lista-pedido').empty();
        for (const item in pedido) {
            $('#lista-pedido').append(
                `<li>${item} - R$ ${pedido[item].preco.toFixed(2)} (${pedido[item].quantidade}x)</li>`
            );
        }
    });
});
