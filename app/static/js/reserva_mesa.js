$(document).ready(function() {

    function atualizarLista(reservas) {
        $('#lista-reservas').empty();
        reservas.forEach(r => {
            $('#lista-reservas').append(
                `<li class="list-group-item">
                    Mesa ${r.numero_mesa} - ${r.cliente} em ${r.data} das ${r.horario_de_entrada} às ${r.horario_de_saida}
                </li>`
            );
        });
    }

    function mostrarMensagem(texto, tipo='info') {
        $('#mensagem').removeClass('d-none alert-info alert-success alert-danger')
                      .addClass(`alert alert-${tipo}`)
                      .text(texto);
        setTimeout(() => $('#mensagem').addClass('d-none'), 3000);
    }

    // Carrega reservas do backend
    function carregarReservas() {
        $.getJSON("/api/reservas", function(res) {
            if(res.status === "ok") {
                atualizarLista(res.reservas);
            }
        });
    }

    carregarReservas();

    $('#form-reserva').submit(function(e) {
        e.preventDefault();

        const nome = $('#nome').val();
        const mesa = parseInt($('#mesa').val());
        const data = $('#data').val();
        const entrada = $('#horario_entrada').val();
        const saida = $('#horario_saida').val();

        // Validação local
        if (entrada >= saida) {
            mostrarMensagem("Horário de saída deve ser depois da entrada!", 'danger');
            return;
        }

        $.ajax({
            url: "/api/reservas",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({ nome, mesa, data, entrada, saida }),
            success: function(res) {
                if(res.status === "ok") {
                    mostrarMensagem(res.mensagem, 'success');
                    $('#form-reserva')[0].reset();
                    carregarReservas();
                } else {
                    mostrarMensagem(res.mensagem, 'danger');
                }
            },
            error: function() {
                mostrarMensagem("Erro ao conectar com o servidor.", 'danger');
            }
        });
    });
});
