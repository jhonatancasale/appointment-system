# API REST para um sistema de agendamento


tl;dr
- [Objetivo](#objetivo)
- [Solução Proposta](#solução-proposta)
- [Disclaimer](#disclaimer)
- [Build](#how-to-build)
- [Run](#how-to-run)
- [Melhorias](#melhorias)


## Objetivo
Implementação de uma API REST usando os frameworks [Django](https://www.djangoproject.com) e [Django REST framework](http://www.django-rest-framework.org) com o objetivo de fornecer a funcionalidade de **agendamentos** onde cada agendamento é comporto por:

- Data (datetime.date)
- Horário de início (datetime.time)
- Horário final (datetime.time)
- Paciente (User:fk)
- Procedimento (TextField)

Em termos de comportamento, devido ao uso do [Django REST framework](http://www.django-rest-framework.org) foi bastante natural estender o comportamento para permitir

- Listagem de agendamentos
- Detalhes de um agendamento
- Cadastro de um agendamento
- Atualização de um agendamento
- Exclusão de um agendamento


## Solução proposta
#### _patients_ precisam ter email
Por decisão de projeto, o vinculo (__appointment__, __patient__) é criado buscando-se o __patient__ por seu email, dado que não estamos expondo o recurso __patient__ na API, não é trivial identificar a chave (id) do __patient__ no banco, logo, para fazer esse bind, foi escolhido usar como chave de busca o email do __patient__.

#### Horários de agendamento são `livres`
A única validação existente é a de que o horário inicial de um dado __appointment__ deve ser **menor** que seu final, porem, é possível que um mesmo __patient__ tenha 2+ __appointments__ para uma mesma janela de tempo, o motivo disso é que de fato, um __patient__ poderia fazer esse agendamento, como por exemplo em complexos em que existam mais de um médico em atendimento, para "otimizar" a espera, pode-se agendar consultas com sobreposição, ou mesmo devido à atrasos por parte do __patient__ e/ou __doctor__


## Disclaimer
Idealmente, o arquivo `src/scheduling_system/scheduling_system/.env` contem 2 importantes variáveis de ambiente

- SECRET_KEY
- DEBUG

Porém, por simplicidade, foi deixado hard-coded, onde a linha

`SECRET_KEY = config('SECRET_KEY', default=secret_key)`

Deveria ser

`SECRET_KEY = config('SECRET_KEY')`, 


## How to build
Clonado o  repositório, e já estando na pasta raiz do projeto, existem duas abordagens:
1. Configurando o próprio sistema
    1. Criar um `virtualenv` para proteger o Sistema Operacional é recomendado, para isso
        1. `virtualenv venv`
        ou
        1. `python3 -m venv venv` ou `python -m venv venv`
    1. Ativar o `venv`
        - `source venv/bin/activate`
    1. Instalar as dependências
        - `pip install -r requirements.txt`
    1. Criar o banco de dados
        - `python src/scheduling_system/manage.py makemigrations`
        - `python src/scheduling_system/manage.py migrate`
1. Usando o docker-compose
    1. `docker-compose build`


## How to run
Novamente, temos 2 opções
1.  `python src/scheduling_system/manage.py runserver` 
1. Usando o docker-compose
    1. `docker-compose up`


## Melhorias
### Adição da entidade `Doctor`
Na atual implementação, cada __appointment__ pertence tão e somente à um __patient__, no entanto, esse relacionamento poderia ser enriquecido com a adição (vinculo) de uma segunda entidade (User:Doctor), onde cada __appointment__ pertenceria tão e somente à um __doctor__ porem cada __doctor__ poderia ter um numero arbitrário de __appointments__, podendo este ser limitado por configuração posterior. O ponto importante seriam as possíveis análises que isso forneceria, como por exemplo:
- Quais médicos atendem mais?
- Qual a distribuição de __appointments__ ao longo da semana/mês/semestre/ano?
- Quais as especialidades mais solicitadas?
- Existe alguma correlação entre os __appointments__?


### Busca por __patient__ / __doctors__
De uma maneira geral, o sistema se beneficiaria do uso de `?search` que permitissem a busca e aquisição de, por exemplo:
- Dado um __patient__ retorne todos os seus __appointments__
- Dado um __patient__ retorne todos os seus __appointments__ em um dado intervalo de tempo
- Dado um __doctor__ retorne todos os seus __appointments__
- Dado um __doctor__ retorne todos os seus __appointments__ em um dado intervalo de tempo 


### Campos adicionais em __appointment__
Uma possível melhoria seria a inclusão de campos como:

#### Horário de chegada/saída (check in / check out) do __patient__ e  Horário efetivo de início e termino da consulta
Essas informações adicionais poderiam ajudar no melhor entendimento da demando/capacidade de processamento, ou seja, poderia se fazer um estudo de quanto tempo de fila estamos lidando, tempo médio de cada atendimento, quantas pessoas temos que acomodar em sala de espera (devido justamente as filas).

#### Uso de outro SGBG
Como por exemplo fazer uso do [PostgreSQL](https://www.postgresql.org)

#### Uso de uma Task Queue
Como por exemplo fazer uso do [Celery](http://www.celeryproject.org)

#### Uso de loggers
Nunca se sabe o que vai acontecer no mundo selvagem e perigoso da Web ...
