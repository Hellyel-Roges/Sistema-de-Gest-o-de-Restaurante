from app import db
from app.models import Cliente, Mesa, ReservaMesa
from datetime import datetime


def criar_reserva(nome_cliente, numero_mesa, data_str, entrada_str, saida_str):
    """
    Realiza a criação da reserva com todas as validações de regras de negócio.
    Retorna um dict com 'status' e 'mensagem' para ser usado pela rota/API.
    """

    # Converter datas e horários
    try:
        horario_entrada = datetime.strptime(f"{data_str} {entrada_str}", "%Y-%m-%d %H:%M")
        horario_saida = datetime.strptime(f"{data_str} {saida_str}", "%Y-%m-%d %H:%M")
    except:
        return {"status": "erro", "mensagem": "Formato de data ou horário inválido."}

    # 🔥 Regra: não permitir horários invertidos
    if horario_entrada >= horario_saida:
        return {"status": "erro", "mensagem": "Horário de saída deve ser depois da entrada."}

    # 🔥 Regra: não pode reservar no passado
    agora = datetime.now()
    if horario_saida <= agora:
        return {"status": "erro", "mensagem": "Não é possível fazer reservas para horários ou dias passados."}

    # 🔥 Regra: intervalo permitido (11h às 23h)
    if not (11 <= horario_entrada.hour < 23) or not (11 < horario_saida.hour <= 23):
        return {"status": "erro", "mensagem": "Horário permitido para reservas: das 11:00 às 23:00."}

    # Validar mesa
    mesa = Mesa.query.filter_by(numero=numero_mesa).first()
    if not mesa:
        return {"status": "erro", "mensagem": f"Mesa {numero_mesa} não existe."}

    # Se o cliente não existir, criar
    cliente = Cliente.query.filter_by(nome=nome_cliente).first()
    if not cliente:
        cliente = Cliente(nome=nome_cliente)
        db.session.add(cliente)
        db.session.commit()

    # 🔥 Verificar conflito de horário
    conflito = ReservaMesa.query.filter(
        ReservaMesa.mesa_id == mesa.id,
        ReservaMesa.horario_de_entrada < horario_saida,
        ReservaMesa.horario_de_saida > horario_entrada
    ).first()

    if conflito:
        return {"status": "erro", "mensagem": f"Mesa {numero_mesa} já reservada neste horário."}

    # ✅ Criar reserva
    reserva = ReservaMesa(
        numero_mesa=numero_mesa,
        mesa_id=mesa.id,
        horario_de_entrada=horario_entrada,
        horario_de_saida=horario_saida,
        cliente_id=cliente.id
    )

    db.session.add(reserva)
    db.session.commit()

    return {"status": "ok", "mensagem": f"Reserva feita com sucesso para {cliente.nome} na mesa {numero_mesa}!"}
