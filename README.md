# API de Banco de Dados Pokémon

Uma API desenvolvida em FastAPI para gerenciar a persistência de dados de treinadores Pokémon e seus Pokémon.
## 📋 Índice

    Visão Geral

    Relação com a API Principal

    Funcionalidades

    Instalação e Execução

    Execução com Docker

    Endpoints

    Estrutura do Projeto

    Tecnologias Utilizadas

## 🎯 Visão Geral

Esta API é responsável pelo gerenciamento da persistência de dados do sistema de treinadores Pokémon. Ela atua como uma camada de banco de dados, fornecendo operações CRUD (Create, Read, Update, Delete) para treinadores e seus Pokémon.
🔗 Relação com a API Principal

Esta API complementa a API principal de treinadores Pokémon, fornecendo os seguintes serviços:

    Persistência de Dados: Armazena informações de treinadores e Pokémon em um banco SQLite

    Operações de Banco: Implementa todas as operações de criação, leitura, atualização e exclusão

    Gerenciamento de Estado: Mantém o estado atual dos treinadores e suas localizações

    Estatísticas: Controla contadores como número de encontros Pokémon

A API principal (executando na porta 8000) faz chamadas HTTP para esta API (executando na porta 7000) para todas as operações de persistência.
## ⚡ Funcionalidades

    CRUD de Treinadores: Operações completas para gerenciar treinadores

    Captura de Pokémon: Registro de Pokémon capturados por treinadores

    Gerenciamento de Localização: Atualização da localização atual dos treinadores

    Estatísticas de Encontros: Contabilização de encontros Pokémon

    Operações em Lote: Listagem de todos os treinadores

## 🚀 Instalação e Execução
Pré-requisitos

    Python 3.11+

    pip (gerenciador de pacotes Python)

Instalação

    Clone o repositório:

bash

git clone <url-do-repositorio>
cd <diretorio-do-projeto>

    Instale as dependências:

bash

pip install -r requirements.txt

    Execute a aplicação:

bash

uvicorn main:app --reload --host 0.0.0.0 --port 7000

A API estará disponível em http://localhost:7000
## 🐳 Execução com Docker
Construir a imagem Docker
    bash

    docker build -t pokemon-db-api .

Executar o container
    bash

    docker run -p 7000:7000 pokemon-db-api

Dockerfile

O Dockerfile utilizado para containerizar a aplicação:

dockerfile

    Use official Python image
     
        FROM python:3.11

Set working directory
    
    WORKDIR /app

Copy requirements file

    COPY requirements.txt .

 Install dependencies
 
    RUN pip install --no-cache-dir -r requirements.txt

Copy application code

    COPY . .

Expose port (default for uvicorn)

    EXPOSE 7000

 Start the server with uvicorn
 
    CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7000", "--reload"]

Execução com Docker Compose

Para integrar com a API principal, use o docker-compose.yml fornecido na API principal.
## 📡 Endpoints
### 👤 Gerenciamento de Treinadores
Retorna informações de um treinador específico.

    GET /getTrainer/{trainer_name}

Cria um novo treinador.

    POST /createTrainer


Exclui um treinador.

    DELETE /deleteTrainer/{trainer_name}


Lista todos os treinadores cadastrados.

    GET /listAllTrainers/
    
### 🗺️ Gerenciamento de Localização
Atualiza a localização de um treinador.

    PATCH /updatePlayerLocation/


### 🐾 Gerenciamento de Pokémon

Registra a captura de um Pokémon.

     POST /capturePokemon/
Exclui um Pokémon de um treinador.

    DELETE /deletePokemon

Lista todos os Pokémons de um treinador.

    GET /listPokemon


Endpoint de health check simples.
## 🏗️ Estrutura do Projeto


    ├── main.py               # Arquivo principal da aplicação FastAPI
    ├── models/               # Modelos de dados do SQLAlchemy
    ├── schemes.py            # Esquemas Pydantic para validação de dados
    ├── requirements.txt      # Dependências do projeto
    ├── Dockerfile            # Configuração do container
    ├── test.db               # Banco de dados SQLite (gerado automaticamente)
    └── README.md             # Documentação do projeto

## 🛠️ Tecnologias Utilizadas

    FastAPI: Framework web moderno e rápido para construção de APIs

    SQLAlchemy: ORM para operações de banco de dados

    SQLite: Banco de dados leve para desenvolvimento

    Pydantic: Validação de dados e manipulação de esquemas

    Uvicorn: Servidor ASGI para executar a aplicação

    Docker: Containerização da aplicação

## 📝 Notas Adicionais

    Esta API utiliza SQLite como banco de dados, armazenado no arquivo test.db

    Todas as operações de banco de dados são realizadas através do ORM SQLAlchemy

    A API é projetada para ser consumida pela API principal de treinadores Pokémon

    O uso do padrão repository com injeção de dependência garante a testabilidade do código
