# Sistema de Controle de Despesas Pessoais

## 1. Título

**Sistema de Controle de Despesas Pessoais e Renda**

---

## 2. Descrição do Projeto

O Sistema de Controle de Despesas Pessoais é uma aplicação desenvolvida em Python com o objetivo de auxiliar usuários no gerenciamento e acompanhamento de seus gastos.

O sistema permite cadastrar, consultar, editar, excluir e filtrar despesas, além de apresentar informações financeiras, como o valor total das despesas, o total gasto por categoria e a média das despesas cadastradas.

As informações são armazenadas em um arquivo no formato JSON, permitindo que os dados permaneçam salvos mesmo após o encerramento do programa.

O projeto foi desenvolvido utilizando conceitos de **Programação Orientada a Objetos (POO)**, organização modular de código, persistência de dados, validação de informações e testes automatizados.

---

## 3. Problema Identificado

Muitas pessoas possuem dificuldades para acompanhar seus gastos do dia a dia. Pequenas despesas realizadas ao longo do mês podem se acumular e dificultar o controle financeiro.

Quando não existe um registro organizado, o usuário pode ter dificuldade para responder perguntas como:

* Quanto estou gastando?
* Qual categoria possui mais despesas?
* Quanto gastei com alimentação?
* Quais despesas realizei em determinado período?
* Qual é o valor médio das minhas despesas?

O sistema foi desenvolvido para solucionar esse problema por meio de uma aplicação simples e organizada.

---

## 4. Justificativa

O desenvolvimento deste projeto é importante porque aborda uma situação presente no cotidiano de muitas pessoas: o controle financeiro pessoal.

Além de resolver um problema real, o projeto permite aplicar conhecimentos importantes da programação, como:

* Programação Orientada a Objetos;
* criação e utilização de classes;
* encapsulamento de responsabilidades;
* manipulação de arquivos;
* armazenamento de dados em JSON;
* validação de entradas;
* tratamento de erros;
* testes automatizados;
* organização de projetos Python;
* separação entre regras de negócio e interface.

Dessa forma, o projeto une uma necessidade prática com os conhecimentos técnicos estudados durante o curso.

---

## 5. Objetivo Geral

Desenvolver uma aplicação em Python capaz de auxiliar no controle e gerenciamento de despesas pessoais de forma simples, organizada e persistente.

---

## 6. Objetivos Específicos

O projeto possui os seguintes objetivos específicos:

1. Permitir o cadastro de despesas;
2. Permitir a visualização das despesas cadastradas;
3. Permitir a edição de despesas;
4. Permitir a exclusão de despesas;
5. Permitir a pesquisa por categoria;
6. Permitir a filtragem por período;
7. Calcular o valor total das despesas;
8. Calcular os gastos agrupados por categoria;
9. Calcular a média das despesas;
10. Armazenar os dados em um arquivo JSON;
11. Validar os dados inseridos pelo usuário;
12. Aplicar conceitos de Programação Orientada a Objetos;
13. Organizar o código em módulos;
14. Realizar testes automatizados das principais funcionalidades.

---

# 7. Funcionalidades

## 7.1 Cadastro de despesas

O usuário pode cadastrar uma nova despesa informando:

* descrição;
* valor;
* categoria;
* data.

Exemplo:

```text
Descrição: Almoço
Valor: R$ 35,00
Categoria: Alimentação
Data: 25/09/2026
```

Após o cadastro, a despesa recebe automaticamente um identificador único.

---

## 7.2 Listagem de despesas

O sistema permite visualizar todas as despesas cadastradas.

As informações apresentadas incluem:

* ID;
* descrição;
* valor;
* categoria;
* data.

---

## 7.3 Edição de despesas

O usuário pode selecionar uma despesa pelo seu ID e alterar seus dados.

Essa funcionalidade permite corrigir informações ou atualizar uma despesa já cadastrada.

---

## 7.4 Remoção de despesas

O sistema permite excluir uma despesa utilizando seu identificador.

Antes da remoção, o sistema verifica se a despesa informada realmente existe.

---

## 7.5 Filtro por categoria

É possível visualizar somente as despesas pertencentes a uma determinada categoria.

As categorias disponíveis são:

* Alimentação;
* Transporte;
* Moradia;
* Lazer;
* Saúde;
* Educação;
* Outros.

---

## 7.6 Filtro por período

O sistema permite informar uma data inicial e uma data final para visualizar somente as despesas realizadas naquele período.

Essa funcionalidade facilita a análise dos gastos de determinados dias, semanas ou meses.

---

## 7.7 Resumo financeiro

O sistema apresenta um resumo das informações cadastradas.

Entre os dados apresentados estão:

* quantidade de despesas;
* valor total;
* média das despesas;
* total gasto por categoria.

---

# 8. Temas de Programação Abordados

Durante o desenvolvimento foram utilizados diversos conceitos estudados em programação.

## 8.1 Programação Orientada a Objetos

O projeto utiliza classes para representar os principais elementos do sistema.

As principais classes são:

* `Despesa`;
* `DespesaRepository`;
* `ControleDespesas`.

Cada classe possui uma responsabilidade específica.

---

## 8.2 Classes e Objetos

A classe `Despesa` representa uma despesa individual.

Cada objeto criado a partir dessa classe possui informações como descrição, valor, categoria e data.

Exemplo conceitual:

```python
despesa = Despesa(
    id=1,
    descricao="Almoço",
    valor=35.00,
    categoria="Alimentação",
    data="25/09/2026"
)
```

---

## 8.3 Encapsulamento e Separação de Responsabilidades

O sistema separa as responsabilidades entre diferentes módulos.

A classe `Despesa` representa os dados de uma despesa.

A classe `DespesaRepository` é responsável pelo armazenamento e recuperação dos dados.

A classe `ControleDespesas` concentra as regras de negócio da aplicação.

Essa divisão facilita a manutenção e a compreensão do código.

---

## 8.4 Persistência de Dados

Os dados são armazenados em um arquivo JSON.

Dessa forma, as informações não são perdidas quando o programa é encerrado.

O arquivo utilizado é:

```text
data/despesas.json
```

---

## 8.5 Validação de Dados

O sistema realiza validações para evitar informações inválidas.

Entre as validações realizadas estão:

* descrição obrigatória;
* valor maior que zero;
* categoria válida;
* data em formato correto;
* ID válido;
* verificação da existência de despesas.

---

## 8.6 Tratamento de Erros

O sistema utiliza tratamento de exceções para evitar que entradas inválidas façam o programa ser encerrado inesperadamente.

Quando ocorre um erro de entrada, o usuário recebe uma mensagem explicando o problema e pode tentar novamente.

---

## 8.7 Testes Automatizados

Foram implementados testes automatizados utilizando a biblioteca `unittest`.

Os testes verificam funcionalida
