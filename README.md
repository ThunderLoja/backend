# Backend

## ➕ Dependências

Para rodar os programas recomenda-se a utilização de um ambiente virtual com o módulo [venv](https://docs.python.org/pt-br/3/library/venv.html#module-venv), onde serão instaladas as dependências e executados os programas.

Para instalar as dependências faça:

```bash
pip3 install -r requirements.txt
```

## 🚀 Para rodar a aplicação

Para rodar a aplicação, faça:

```bash
uvicorn app:app --reload
```

## 📝 Gerar documentação

Para gerar a documentação, faça:

```bash
python3 docs.py
```

## 📈 Gerenciar tabelas

É possível criar, apagar e prencher as tabelas com valores de testes utilizando o script `tables.py`. 

Para criar as tabelas, faça:

```bash
python3 tables.py create
```

Para apagar as tabelas, faça:

```bash
python3 tables.py drop
```

Por fim, para prencher as tabelas com valores de testes, faça:

```bash
python3 tables.py fill
```