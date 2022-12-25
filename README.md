# RELDS

## Liste produtos de um site de forma fácil e rápida!

Relds é uma api de web scraping operando em lojas online e marketplaces, focada na obtenção de informações produtos, como preço, link, imagem, titulo. Surgiu de uma curiosidade sobre o mundo da obtenção de dados da web e também sobre os preços dos produtos mostrados nas lojas.

## Recursos

- Listagem de produtos

## Lojas - Drivers

| Loja  | Status |
| ----- | ------ |
| Kabum | Ativo  |

## Modo de usar

- **Configuração do env.json**

  - `string: string de conexão do mongodb atlas`
  - `dbname: nome do banco de dados`
  - `user: usuário do banco de dados`
  - `pass: senha do usuário do banco de dados`

- **Inicialização**

  - `pip install -r requirements.txt`
  - `python main.py`

- **Scrap**

  - **Request (POST)**
    - `url: http://127.0.0.1:5000/products/scrap`
  - **Body**
    - `loja: nome da loja`
    - `produtos: lista com os objetos de configuração de cada produto a ser buscado`
  - **Response**
    - `_res: status`
    - `data: x produtos atualizados`

- **Rotas para os produtos no DB**

  - **Listar todos os produtos do banco**

    - **Request (GET)**
      - `url: http://127.0.0.1:5000/products/list`

  - **Pegar produto pelo seu id**
    - **Request (GET)**
      - `url: http://127.0.0.1:5000/products/getproduct/id`

## Dicas

- **Constantes**
  - `constants.py`
- Em **constants.py** tem exemplos do objeto do produto a ser buscado

## Contribuição

- Exemplos

  - **Drivers**
    - `drivers.py`

- Para que a API seja mais robusta e ampla são precisos diversos drivers. Caso tenha interesse, faça um fork e mande um drive novo ou correção de algum existente.
