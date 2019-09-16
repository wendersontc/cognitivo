# Desafio

## Como executar
Clone o Projeto para um diretório qualquer em seu computador

```bash
git clone https://github.com/wendersontc/cognitivo
```

Depois navegue até o diretório criado
```bash
cd cognitivo
```

### Com Docker
É necessário instalar em sua maquina:
- [Docker](https://www.docker.com/) 

Execute o comando:
```bash
docker-compose up -d
```

## Como acessar
Uma vez que o projeo esteja rodando corretamente, abra seu navegador e acesso a url
```
1- http://localhost:9090/news/avaliations/

Identificação do dado da categoria News que tem o maior número de avaliações

2- http://localhost:9090/book/music/avaliations/

Identificação dos dados da categoria Music e Book que tem o maior número de avaliações maximo de registros = 10,
os mesmos são inseridos na base de dados.

3- http://localhost:9090/book/music/quotes

Identificação do dado com o maior número de citações


