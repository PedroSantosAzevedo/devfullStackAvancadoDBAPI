# Minha API

Este pequeno projeto faz parte do material diático da Disciplina **Desenvolvimento Full Stack Avancado** 

O objetivo aqui é ilutsrar o conteúdo apresentado ao longo das três aulas da disciplina.

---
## Como executar 


Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

```
python3 -m venv <myenvpath>
```

```
source venv/Scripts/activate
```

```
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

Para executar a API  basta executar:

```
(env)$  uvicorn main:app 
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
(env)$  uvicorn main:app --reload
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.

## Rotas Principais

1. POST /paciente
Adiciona novo paciente
Parâmetros (body):
```
{
  "first_name": "João",
  "last_name": "Silva",
  "cpf": "12345678901",
  "email": "joao@email.com",
  "phone_number": "11999998888",
  "address": "Rua A, 123"
}
```
Respostas:
```
200: Paciente criado com sucesso
409: CPF ou nome já existente
400: Erro na requisição
```
2. GET /pacientes
Lista todos os pacientes
Exemplo de resposta:
```
{
  "pacientes": [
    {
      "id": 1,
      "nome_completo": "João Silva",
      "cpf": "12345678901",
      "email": "joao@email.com",
      "telefone": "11999998888",
      "endereco": "Rua A, 123"
    }
  ]
}
```
4. POST /pacienteCompleto/
Busca paciente por CPF
Parâmetros (body)
```
{
  "cpf": "12345678901"
}
```
Respostas:
```
200: Dados completos do paciente
404: Paciente não encontrado
502: Erro no banco de dados
```
5. DELETE /delPaciente
Remove paciente por CPF
Parâmetros (query):
```
DELETE /delPaciente?cpf=12345678901
```
Respostas:

```
200: {"mesage": "Produto removido", "id": "12345678901"}
404: Paciente não encontrado
```
6. GET /
Redireciona para documentação
Acesso às opções de documentação interativa (Swagger/Redoc/RapiDoc)


## Modelo de Dados (Patient):

```
class Patient(Model):
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    cpf = Column(String, unique=True)
    email = Column(String)
    phone_number = Column(String)
    address = Column(String)
```

## Schemas (Esquemas de Validação):
```
PatientSchema: Valida dados para criação
PatientNameSearchSchema: Valida busca por nome
PatientFetchSchema: Valida busca por CPF
PatientDelSchema: Valida exclusão por CPF
```