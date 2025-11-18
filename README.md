# 🍝 La Forchetta
### Sistema de Gestão de Restaurante de Massas – Delivery e Presencial

> “Um sistema no ponto certo, como uma boa massa: **eficiente, saboroso e equilibrado.**”

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12%2B-blue?logo=python&logoColor=white" alt="Python 3.12+">
  <img src="https://img.shields.io/badge/Flask-black?logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/SQLAlchemy-darkred?logo=sqlalchemy&logoColor=white" alt="SQLAlchemy">
  <img src="https://img.shields.io/badge/JavaScript-ES6%2B-yellow?logo=javascript&logoColor=black" alt="JavaScript">
  <img src="https://img.shields.io/badge/jQuery-blue?logo=jquery&logoColor=white" alt="jQuery">
  <img src="https://img.shields.io/badge/HTML5-orange?logo=html5&logoColor=white" alt="HTML5">
  <img src="https://img.shields.io/badge/CSS3-blue?logo=css3&logoColor=white" alt="CSS3">
  <img src="https://img.shields.io/badge/Bootstrap-purple?logo=bootstrap&logoColor=white" alt="Bootstrap">
</p>

---

## 📍 Índice

* [Sobre o Projeto](#sobre)
* [Funcionalidades](#funcionalidades)
* [Arquitetura da Aplicação](#arquitetura)
* [Frontend & IHC](#frontend)
* [Estrutura de Pastas](#estrutura)
* [Tecnologias Utilizadas](#tecnologias)
* [Como Instalar e Executar](#instalacao)
* [Objetivo Acadêmico](#objetivo)
* [Equipe](#equipe)
* [Contato](#contato)

---

## <a id="sobre"></a>🧩 Sobre o Projeto

**La Forchetta** é um sistema web *full-stack* para gestão de restaurante, desenvolvido em **Python** com o framework **Flask**. O projeto simula o funcionamento completo de um restaurante de massas italianas, integrando o atendimento presencial (reservas) e o serviço de delivery.

O que começou como um projeto acadêmico focado em POO (Programação Orientada a Objetos) evoluiu para uma aplicação web robusta e moderna. A arquitetura atual abandona a POO simples e adota uma estrutura de 3 camadas profissional:

1.  **Models (ORM):** Classes Python que representam as tabelas do banco de dados (via Flask-SQLAlchemy).
2.  **Services:** Módulos Python que contêm toda a "lógica de negócios" (o "cérebro").
3.  **Routes (Controllers):** Endpoints Flask que conectam o frontend às lógicas de *Services* e *Models*.

O frontend foi desenvolvido com foco total em **IHC (Interação Homem-Computador)**, garantindo uma interface limpa, responsiva, com tema escuro consistente e interatividade dinâmica usando JavaScript(JQuery) e AJAX.

---

## <a id="funcionalidades"></a>🍽️ Funcionalidades

### 🔸 Requisitos Gerais
* 💳 **Sistema de Formas de Pagamento**
* 📜 **Gerenciamento de Cardápio (Pratos, Bebidas, Sobremesas)**
* 👤 **Sistema de Clientes**
* 🍝 **Sistema de Produtos**

### 🏛️ Presencial
* 🪑 **Reserva de Mesas** (com formulário dinâmico via AJAX)
* 🚗 **Gerenciamento de Estacionamento por Cliente**
* 🎫 **Controle de Catraca para Entrada e Saída de Clientes**

### 🚚 Delivery
* 🛵 **Gestão de Entrega**
* 🧾 **Criação e Rastreamento de Pedidos Online** (com carrinho de compras interativo via AJAX)
* ✉️ **Contato para Suporte e duvidas**

---

## <a id="arquitetura"></a>🏛️ Arquitetura da Aplicação

O backend é organizado em três camadas claras para garantir a separação de responsabilidades (Separation of Concerns).

1.  **Models (`app/models/`)**
    * Define a estrutura do banco de dados usando classes que herdam de `db.Model` (SQLAlchemy).
    * *Ex: `Produto`, `Pedido`, `ReservaMesa`, `Pagamento`.*

2.  **Services (`app/services/`)**
    * Contém a "lógica de negócios" (o "cérebro"). É aqui que os métodos (ex: `calcular_total`, `realizar_pagamento`, `criar_reserva`) são implementados.
    * *Ex: `pedido_services.py`, `pagamento_services.py`, `reserva_services.py`.*

3.  **Routes (`app/routes/`)**
    * Define as URLs (endpoints) do site e atua como a camada de "Controller".
    * **`paginas_routes.py`**: Retorna as páginas HTML (templates) para o usuário (ex: a Home, a página de Contato).
    * **`pedido_api.py`**, **`produto_api.py`**, **`reserva_api.py`**: Definem as APIs RESTful que retornam dados (JSON) para o JavaScript (AJAX).

---

## <a id="frontend"></a>🎨 Frontend & IHC (Interação Homem-Computador)

O frontend foi estruturado para ser modular, atraente e amigável:

* **Herança de Templates:** Um `base.html` centraliza o `navbar` e o `footer`, garantindo consistência visual e fácil manutenção em todas as páginas.
* **Dinamismo (AJAX):** As páginas de Reserva e Delivery usam JavaScript(jquery) para se comunicar com as APIs do Flask sem recarregar a página, criando uma experiência de usuário fluida.
* **CSS Modular:** Cada página carrega um CSS específico (ex: `delivery.css`) que herda as variáveis de tema do `home.css`, mantendo o tema escuro (preto e dourado) consistente.
* **Anti-FOUC:** O `home.js` aplica uma animação `.fade-in` (via CSS) para evitar o "flash de conteúdo não estilizado", melhorando a percepção visual do usuário.
* **Acessibilidade:** Ícones decorativos e emojis são escondidos de leitores de tela com `aria-hidden="true"` para uma navegação mais limpa e direta.

---

## <a id="estrutura"></a>🗂️ Estrutura de Pastas

Sistema-de-Gest-o-de-Restaurante/
<br>├── app/
<br>│   ├── models/
<br>│   │   ├── cliente.py
<br>│   │   ├── database.py
<br>│   │   ├── mesa.py
<br>│   │   ├── pagamento.py
<br>│   │   ├── pedido.py
<br>│   │   ├── pedido_produto.py
<br>│   │   ├── produto.py
<br>│   │   ├── reserva_mesa.py
<br>│   │   └── init.py
<br>│   ├── routes/
<br>│   │   ├── paginas_routes.py
<br>│   │   ├── pedido_api.py
<br>│   │   ├── produto_api.py
<br>│   │   └── reserva_api.py
<br>│   ├── services/
<br>│   │   ├── pagamento_services.py
<br>│   │   ├── pedido_services.py
<br>│   │   └── reserva_services.py
<br>│   ├── static/
<br>│   │   ├── css/
<br>│   │   │   ├── cardapio.css
<br>│   │   │   ├── contato.css
<br>│   │   │   ├── delivery.css
<br>│   │   │   ├── home.css
<br>│   │   │   ├── reserva_mesa.css
<br>│   │   │   └── style.css
<br>│   │   ├── img/
<br>│   │   │   ├── italian-bg.png
<br>│   │   │   ├── mesas.png
<br>│   │   │   └── prato_massa.png
<br>│   │   ├── js/
<br>│   │   │   ├── cardapio.js
<br>│   │   │   ├── delivery.js
<br>│   │   │   ├── home.js
<br>│   │   │   └── reserva_mesa.js
<br>│   │   └── vendor/
<br>│   │       ├── bootstrap/ (css/ e js/)
<br>│   │       └── jquery/ (jquery.min.js)
<br>│   ├── templates/
<br>│   │   ├── base.html
<br>│   │   ├── cardapio.html
<br>│   │   ├── contato.html
<br>│   │   ├── delivery.html
<br>│   │   ├── index.html
<br>│   │   └── reserva_mesa.html
<br>│   └── init.py
<br>├── instance/
<br>│   └── database.db
<br>├── .gitignore
<br>├── app.py
<br>├── README.md
<br>└── requirements.txt


---

## <a id="tecnologias"></a>🧑‍💻 Tecnologias Utilizadas

### Backend
* 🐍 **Python 3.12+**
* **Flask** (Servidor web e roteamento)
* **Flask-SQLAlchemy** (Mapeamento Objeto-Relacional - ORM)
* **Jinja2** (Sistema de templates)

### Frontend (IHC)
* **HTML5**
* **CSS3** (com Tema Escuro modularizado por página)
* **JavaScript (ES6+)**
* **jQuery** (Para requisições AJAX e manipulação do DOM)
* **Bootstrap 5** (Para o sistema de grid e componentes base)

### Banco de Dados
* **SQLite** (Armazenado em `instance/database.db`)

---

## <a id="instalacao"></a>🚀 Como Instalar e Executar

Siga os passos abaixo para executar o projeto localmente.

### 1. Pré-requisitos
* Tenha o **Python 3.12** ou superior instalado.
* Tenha o **Git** instalado (para clonar o repositório).

### 2. Fork e Clone
1.  **Faça um Fork** do repositório clicando no botão "Fork" no canto superior direito desta página.
2.  Vá para o **seu** perfil no GitHub, abra o Fork que você acabou de criar e copie a URL (botão verde "Code").
3.  Clone para sua máquina:
    ```bash
    # Substitua a URL abaixo pela que você copiou do seu Fork
    git clone https://github.com/SEU-USUARIO/Sistema-de-Gest-o-de-Restaurante.git
    
    cd Sistema-de-Gest-o-de-Restaurante
    ```

### 3. Criar e Ativar o Ambiente Virtual (venv)
Um ambiente virtual (`venv`) isola as dependências do seu projeto e é uma boa prática.

**No Windows (CMD ou PowerShell):**
```bash
# Criar o venv
py -m venv venv

# Ativar o venv
.\venv\Scripts\activate
```

**No Linux ou Mac (Bash/Zsh):**
```bash
# Criar o venv
python3 -m venv venv

# Ativar o venv
source venv/bin/activate
```

### 4. Instalar as Dependências
Com o ambiente virtual ativo, instale todas as bibliotecas Python listadas no `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 5. Executar a Aplicação
O Flask irá criar o banco de dados (`database.db`) na pasta `instance/` automaticamente na primeira vez que for executado.
# Rodar o servidor de desenvolvimento
```bash
py app.py
```
O site estará disponível no seu navegador em: http://127.0.0.1:5000

---

## <a id="objetivo"></a>🎓 Objetivo Acadêmico

Este projeto foi desenvolvido para fins educacionais nas disciplinas de **Programação Orientada a Objetos e Interação Homem-Computador (IHC)**. O foco foi aplicar conceitos teóricos em um **sistema de gestão realista**, escalável e com foco na usabilidade, evoluindo de uma estrutura de POO simples para uma arquitetura de aplicação web completa.

---

## <a id="equipe"></a>🍕 Equipe de Desenvolvimento

👨‍💻 **Integrantes:**  
- Guilherme Silva Souza
- Gustavo Freitas Sampaio
- Hellyel Roges dos Passos Ambrozio Pereira 

📅 **Curso:** Ciência da Computação – Universidade Católica de Santos  
📘 **Disciplina:** Programação Orientada a Objetos + Interação Homem Computador

---

## <a id="contato"></a>💬 Contato

📧 helleyl.pereira.dev@gmail.com
💡 Projeto acadêmico open-source – contribuições são bem-vindas!  

---

⭐ **Dê uma estrela se gostou do projeto!**  
> Feito com dedicação, lógica e um toque de molho italiano 🍅

