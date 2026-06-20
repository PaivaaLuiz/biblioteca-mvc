# Relatório Técnico – Projeto Read Book

## Introdução

O projeto Read Book é um sistema web desenvolvido utilizando o padrão MVC. Seu objetivo é permitir a consulta de livros disponíveis em uma biblioteca, além de fornecer uma área administrativa para cadastro, edição e gerenciamento do catálogo. Durante o desenvolvimento foram utilizados conceitos importantes da Engenharia de Software, como Injeção de Dependência, ORM e banco de dados SQLite.

---

#  Injeção de Dependência (Dependency Injection)

## O que é?

A Injeção de Dependência (DI) é um mecanismo que permite fornecer objetos e serviços para uma classe sem que ela precise criá-los manualmente. No projeto Read Book, esse conceito é utilizado para permitir que os Controllers tenham acesso ao banco de dados sem criar conexões diretamente.

### Problema que ela resolve

Sem DI, cada Controller precisaria criar suas próprias conexões e dependências, aumentando o acoplamento e dificultando a manutenção do sistema. Com DI, o framework fornece automaticamente os serviços necessários, tornando o código mais organizado e reutilizável.

---

## Ciclos de Vida

### Transient

Uma nova instância é criada sempre que o serviço é solicitado. Utilizado para serviços simples e sem armazenamento de estado.

### Scoped

Uma instância é criada para cada requisição realizada pelo usuário. Esse é o ciclo ideal para acesso ao banco de dados, pois cada usuário trabalha com sua própria instância durante a navegação.

### Singleton

Existe apenas uma instância para toda a aplicação. Todos os usuários compartilham o mesmo objeto.

### Por que o banco de dados não deve ser Singleton?

No sistema Read Book vários administradores poderiam editar livros ao mesmo tempo. Se o contexto do banco fosse Singleton, diferentes usuários compartilhariam os mesmos dados temporários, podendo causar conflitos e inconsistências. Por esse motivo, o ciclo de vida recomendado para acesso ao banco é o Scoped.

---

# Entity Framework Core e ORM

## O que é um ORM?

ORM (Object Relational Mapping) é uma tecnologia que transforma classes em tabelas do banco de dados. No Read Book, a classe:

```csharp
public class Livro
{
    public int Id { get; set; }
    public string Titulo { get; set; }
    public string Autor { get; set; }
    public string Categoria { get; set; }
}
```

representa diretamente a tabela responsável por armazenar os livros da biblioteca.

### Vantagens

* Redução de código SQL manual.
* Maior produtividade.
* Facilidade de manutenção.
* Integração direta com as classes da aplicação.
* Menor chance de erros.

---

## O que é Code-First?

A abordagem Code-First consiste em criar primeiro as classes da aplicação e permitir que o banco seja gerado automaticamente a partir delas. No projeto Read Book, primeiro foi criada a entidade Livro e depois o banco foi gerado utilizando as ferramentas do framework. Isso permite desenvolver o sistema focando inicialmente nas regras de negócio.

---

## Como funcionam as Migrations?

As Migrations registram alterações feitas nas entidades da aplicação.

Por exemplo:

* Adicionar uma nova coluna.
* Criar uma nova tabela.
* Modificar um campo existente.

Quando o comando de atualização é executado, o Entity Framework compara as alterações registradas com a estrutura atual do banco e aplica apenas o que ainda não foi criado. Dessa forma, o banco acompanha automaticamente a evolução do projeto.

---

# SQLite

## Vantagens do SQLite

O Read Book utiliza SQLite durante o desenvolvimento.

As principais vantagens são:

* Simplicidade de configuração.
* Não exige instalação de servidor.
* Banco armazenado em um único arquivo.
* Baixo consumo de recursos.
* Ideal para testes e projetos acadêmicos.

Essas características permitiram desenvolver rapidamente o sistema sem necessidade de infraestrutura complexa.

---

## Limitação de Concorrência

O principal ponto fraco do SQLite é a concorrência. Como o banco é armazenado em um único arquivo, muitas operações de escrita simultâneas podem gerar bloqueios temporários. Se centenas ou milhares de usuários tentarem cadastrar ou alterar livros ao mesmo tempo, o desempenho poderá ser prejudicado.

---

## Quando migrar para PostgreSQL ou SQL Server?

A migração deve ocorrer quando o sistema começar a crescer significativamente.

Por exemplo:

* Grande aumento de usuários.
* Muitas operações simultâneas.
* Necessidade de alta disponibilidade.
* Maior volume de dados.

Se a Read Book evoluir para atender diversas bibliotecas ou milhares de usuários, bancos como PostgreSQL ou SQL Server serão mais adequados devido ao melhor suporte à concorrência e escalabilidade.

---

# Conclusão

Durante o desenvolvimento da Read Book foi possível compreender conceitos fundamentais do desenvolvimento web moderno. A Injeção de Dependência facilita a organização do código, o Entity Framework Core acelera o desenvolvimento através do ORM e do Code-First, enquanto o SQLite oferece uma solução simples e eficiente para ambientes de desenvolvimento. Essas tecnologias permitiram construir um sistema funcional de gerenciamento de biblioteca, aplicando conceitos amplamente utilizados no mercado de trabalho.
