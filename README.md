# Catálogo de Filmes — UC32

Sistema web CRUD feito com Python, Flask, SQLite, HTML e Jinja2.

## Funcionalidades
- Cadastrar filmes com título, gênero, ano e nota de 1 a 10.
- Listar os filmes cadastrados.
- Editar filmes.
- Excluir filmes.
- Criar a tabela SQLite automaticamente ao iniciar o app.

## Executar localmente (Windows)
1. Abra esta pasta no VS Code.
2. Abra o terminal.
3. Crie um ambiente virtual:
   ```bash
   python -m venv .venv
   ```
4. Ative o ambiente:
   ```bash
   .venv\Scripts\activate
   ```
5. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
6. Inicie:
   ```bash
   python app.py
   ```
7. Acesse http://127.0.0.1:5000

O arquivo `filmes.db` é criado automaticamente e está no `.gitignore`.

## Publicar
Suba os arquivos para um repositório GitHub. No Render, crie um **Web Service** conectado ao repositório e use:
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app`

Observação: o disco local de um serviço gratuito no Render pode não ser persistente. Para manter dados entre reinicializações, será necessário configurar armazenamento persistente ou outro banco de dados.
