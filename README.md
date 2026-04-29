# [Banco Safe]

## Equipe
- [Cipriano José Da Silva Neto] - GitHub: [@MCipris]
- [Gabriel Henrique Ferreira Bessa] - GitHub: [@Gabriel-Bessa2]
- [João Marcos Silva Fernandes de Freitas] - GitHub: [@Jomasii] 

---

## Stack de desenvolvimento
- Linguagem: Python
- Framework: Django
- Interface: Web
- Controle de Versão: GitLabFlow + GitHub

---

## Como Executar o Projeto

1. Clone o repositório
```
git clone https://github.com/MCipris/2026.1-DIM0517-SISTEMA-BANCARIO.git
```

2. Acesse a pasta
```
cd 2026.1-DIM0517-SISTEMA-BANCARIO
```

3. Crie e ative o ambiente virtual
    ### Windows
    ```
    python -m venv .venv
    .\.venv\Scripts\activate
    ```

    ### Linux e MacOS
    ```
    python -m venv .venv
    source .venv/bin/activate
    ```

4. Instale as dependências do projeto
```
pip install -r requirements.txt
```

5. Execute as migrações do projeto
```
python manage.py migrate
```

6. Copie o arquivo `.env.example` para `.env`

7. Execute o servidor
```
python manage.py runserver
```