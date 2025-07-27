# Projeto-FBD

Este README guiará você na configuração e execução deste projeto.

## Pré-requisitos

Antes de iniciar, certifique-se de que você tenha o Python 3 instalado.

1.  **Configuração do Banco de Dados:**
    *   Execute o script localizado em `banco.sql` em seu sistema de gerenciamento de banco de dados para criar as tabelas necessárias.

2.  **Variáveis de Ambiente:**
    *   Crie um arquivo chamado `.env` na raiz do projeto.
    *   Neste arquivo, você precisará definir as credenciais de acesso ao seu banco de dados. Altere os valores de exemplo abaixo para os seus próprios:
      ```env
      DB_HOST=localhost
      DB_USER=seu_usuario
      DB_PASSWORD=sua_senha
      DB_NAME=nome_do_banco
      ```

## Instalação e Execução

Siga os passos abaixo no seu terminal para rodar a aplicação.

1.  **Crie e ative um ambiente virtual:**
    ```bash
    # Cria o ambiente virtual
    python3 -m venv venv

    # Ativa o ambiente no Windows
    venv\Scripts\activate
    ```
    *Observação: Se você estiver usando Linux ou macOS, o comando de ativação é `source venv/bin/activate`.*

2.  **Instale as dependências:**
    Com o ambiente ativado, instale as bibliotecas necessárias a partir do arquivo `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

3.  **Inicie a aplicação:**
    Execute o comando abaixo para iniciar o servidor do Panel.
    ```bash
    panel serve app.py
    ```

Após executar o último comando, a aplicação estará rodando e acessível no endereço local