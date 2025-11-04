from datetime import datetime
import random

class Pagamento:
    def __init__(self, valor_total, metodo, status="pendente", data=None):
        self.id_pagamento = random.randint(100000, 999999)
        self.valor_total = float(valor_total)
        self.metodo = metodo  
        self.status = status
        self.data = data if data else datetime.now()

    def processar_pagamento(self):
        if self.status != "pendente":
            raise Exception("Pagamento já processado ou cancelado.")

        self.status = "pago"
        self.data = datetime.now()

        return {
            "status": "ok",
            "mensagem": (
                f"Pagamento de R$ {self.valor_total:.2f} via {self.metodo} realizado com sucesso! ✅<br>"
                f"ID para comprovação: {self.id_pagamento}"
            ),
            "id_pagamento": self.id_pagamento
        }

    def cancelar_pagamento(self):
        if self.status == "pago":
            raise Exception("Não é possível cancelar um pagamento já efetuado.")
        if self.status == "cancelado":
            raise Exception("O pagamento já foi cancelado.")
        self.status = "cancelado"
        return {"status": "cancelado", "mensagem": f"Pagamento {self.id_pagamento} cancelado com sucesso."}

    def aplicar_desconto(self, percentual):
        valor_desconto = self.valor_total * (percentual / 100)
        self.valor_total -= valor_desconto
        return valor_desconto
