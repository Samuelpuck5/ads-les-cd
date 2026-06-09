# Aula Prática sobre Servidores de Integração Contínua

**Prof. Ricardo Job**

Este repositório descreve um roteiro prático para configuração e uso de um **Servidor de Integração Contínua**. 

O objetivo é proporcionar ao aluno um primeiro contato real com essa prática de desenvolvimento de software.

Se você ainda não sabe o que é **Integração Contínua** e também não entende o papel desempenhado por servidores de CI, recomendamos antes ler o [Capítulo 10](https://engsoftmoderna.info/cap10.html) do livro texto ([Engenharia de Software Moderna](https://engsoftmoderna.info/cap10.html)).


Apesar de existirem diversos servidores de integração contínua (Jenkins, circle CI, Travis CI), neste roteiro iremos usar um recurso nativo do GitHub, chamado **GitHub Actions**, para configurar um servidor de CI.

<p align="center">
    <img width="70%" src="https://user-images.githubusercontent.com/7620947/109080916-232f8200-76e0-11eb-8d02-9ca9f518cea2.png" />
</p>

O Github Actions permite executar programas externos assim que determinados eventos forem detectados em um repositório GitHub. Como nosso intuito é configurar um servidor CI, iremos usar o GitHub Actions para contruir o código (_build_) do projeto e executar seus testes de unidade quando um Pull Request (PR) for aberto no repositório.


## Programa de Exemplo

Para ilustrar o uso do servidor de CI, vamos usar um programa Python muito simples, que já foi criado e está disponível neste mesmo repositório ([calculator.py](https://github.com/ifpb-disciplinas-2026-1/ads-les-cd/blob/main/calculator.py)). Note que o a função que realiza a divisão não trata casos de divisão por zero:

```python
def soma(a,b): 
    return a+b
def subtracao(a,b): 
    return a-b
def multiplicacao(a,b): 
    return a*b
def divisao(a,b):
    return a/b
```

Quando chegar um PR no repositório, o servidor de CI vai automaticamente realizar um _build_ desse programa e rodar o seguinte teste de unidade (também já disponível no repositório, veja em [test_calculator.py](https://github.com/ifpb-disciplinas-2026-1/ads-les-cd/blob/main/test_calculator.py)):

```python
import pytest
from calculator import *

def test_soma():
    assert soma(2, 3) == 5

def test_subtracao():
    assert subtracao(10, 4) == 6

def test_multiplicacao():
    assert multiplicacao(3, 4) == 12

def test_divisao():
    assert divisao(8, 2) == 4
```

Caso você deseje executar os testes de unidade localmente, basta executar os seguintes comandos:

```bash
pip install -r requirements.txt
python -m pytest
```

## Tarefa #1: Configurar o GitHub Actions

#### Passo 1

Antes de mais nada realize um fork deste repositório. Para isso, basta clicar no botão **Fork** no canto superior direito desta página.

Ou seja, você irá configurar um servidor de CI na sua própria cópia do repositório.

#### Passo 2

Clone o repositório para sua máquina local, usando o seguinte comando (onde `<USER>` deve ser substituído pelo seu usuário no GitHub):

```bash
git clone https://github.com/<USER>/ads-les-cd.git
```

Em seguida, copie o código a seguir para um arquivo com o seguinte nome: `.github/workflows/ci.yaml`. 
Isto é, crie diretórios `.github` e depois `workflows` e salve o código abaixo no arquivo `ci.yaml`.

```yaml
name: CI Pipeline
# Configura servidor de CI para executar o pipeline de tarefas abaixo (jobs) quando 
# um push ou pull request for realizado tendo como alvo a branch main
on:
  push:
    branches:
      - main
      - develop
      - feature/**
      - release/**
      - hotfix/**
  pull_request:
    branches:
      - main
jobs:
  tests:
    runs-on: ubuntu-latest # Os comandos serão executados em um sistema operacional Linux
    steps:
    - name: Checkout
      uses: actions/checkout@v4 # Faz o checkout do código recebido
    - name: Setup Python
      uses: actions/setup-python@v5 # Configura o Python 3.12
      with:
        python-version: "3.12"
    - name: Install dependencies # Instala as dependências do código
      run: |
        pip install -r requirements.txt
    - name: Run Tests # Executada os testes de unidade
      run: |
        pytest
```

Esse arquivo ativa e configura o GitHub Actions para -- toda vez que ocorrer um evento `push` ou `pull_request` tendo como alvo a branch principal do repositório -- realizar três tarefas (jobs):

- realizar o checkout do código;
- realizar um build;
- rodar os testes de unidade.

#### Passo 3

Realize um `commit` e um `git push`, isto é:

```bash
git add --all
git commit -m "Configurando GitHub Actions"
git push origin main
```

#### Passo 4

Quando o `push` chegar no repositório principal, o GitHub Actions iniciará automaticamente o fluxo de tarefas configurado no arquivo `ci.yaml` (isto é, build + testes).

Você pode acompanhar o status dessa execução clicando na aba Actions do seu repositório.

<p align="center">
    <img width="80%" src="https://user-images.githubusercontent.com/7620947/110059807-b8b3bd00-7d43-11eb-9e57-e6ba1fa3457a.png" />
</p>

## Tarefa #2: Criando um PR com bug

Para finalizar, vamos introduzir um pequeno bug no programa de exemplo e enviar um PR, para mostrar que ele será "barrado" pelo processo de integração (isto, o nosso teste vai "detectar" o bug e falhar).

#### Passo 1

Introduza um novo método de testes no arquivo [test_calculator.py](https://github.com/ifpb-disciplinas-2026-1/ads-les-cd/blob/main/test_calculator.py).
Por exemplo, basta adicionar uma verificação de quando passamos como parametros os valores 10 e 0, como apresentado abaixo.

```python
def test_divisao_por_zero():
    with pytest.raises(ValueError):
        divisao(10, 0)
```

#### Passo 2

Após modificar o código, você deve criar um novo branch, realizar um `commit` e `push`:

```bash
git checkout -b bug
git add --all
git commit -m "Incluindo testes de unidade para divisões por zero"
git push origin bug
```

#### Passo 3

Em seguida, crie um Pull Request (PR) com sua modificação. Para isso, basta acessar a seguinte URL em seu navegador: `https://github.com/<USER>/ads-les-cd/compare/main...bug`, onde `<USER>` deve ser substituido pelo seu usuário no GitHub. Nessa janela, você pode conferir as modificações feitas e incluir uma pequena descrição no PR.

<p align="center">
    <img width="70%" src="https://user-images.githubusercontent.com/7620947/111704705-5b793a80-881e-11eb-8422-22d51bde6b19.png" />
</p>

Após finalizar a criação do Pull Request, será iniciada nossa pipeline, ou seja, o próprio GitHub vai fazer o build do sistema e rodar seus testes (como na tarefa #1). Porém, dessa vez os testes não vão passar, como mostrado abaixo:

<p align="center">
    <img width="70%" src="https://user-images.githubusercontent.com/7620947/111704932-a85d1100-881e-11eb-8d3b-31f34bafa986.png" />
</p>

**RESUMINDO**: O Servidor de CI conseguiu alertar, de forma automática, tanto o autor do PR como o integrador de que existe um problema no código submetido, o que impede que ele seja integrado no branch principal do repositório.


#### Passo 4

Adicione uma verificação à função `divisao`, de modo que seja possível capturar ocorrências de divisão por zero:

```python
def divisao(a, b):
    if b == 0:
        raise ValueError("Divisão por zero")
    return a / b
```
Após modificar o código, você deve realizar um `commit` e `push` na branch criada anteriormente (`git checkout -b bug`):

```bash
git add --all
git commit -m "Ajuste de cálculo de divisão por zero"
git push origin bug
```

**Repita o passo 3**: Realize uma nova PR e agora veja que o código realiza todo o processo de integração corretamente.

## Créditos

Este roteiro foi elaborado após ajustes e alterações do [roteiro original](https://github.com/aserg-ufmg/demo-ci) elaborado por **Rodrigo Brito**, aluno de mestrado do DCC/UFMG, como parte das suas atividades na disciplina Estágio em Docência, cursada em 2020/2, sob orientação do **Prof. Marco Tulio Valente**.

## Tarefa #3: Parte A - GitHub Flow

O objetivo é exercitarmos ao GitHub Flow com a `feature/potencia`.

#### Passo 1

Criar uma nova branch:

```bash
git checkout -b feature/potencia
```

Adicionar a função para calculadora e seu respectivo teste de unidade:

```python
# Adicionar a calculator.py
def potencia(a, b):
    return a ** b

# Adicionar ao teste: test_calculator.py
def test_potencia():
    assert potencia(2, 3) == 8
```

#### Passo 2

```bash
git add .
git commit -m "Adiciona operação potência"
git push origin feature/potencia
```

#### Passo 3

Em seguida, crie um Pull Request (PR) com sua modificação da branch `feature/potencia` para branch `main`.


## Tarefa #4: Parte B – Git Flow

Agora, seguindo o mesmo projeto usando Git Flow iremos adicionar duas novas funcionalidades: raiz e média.
Nessa parte, iremos realizar o direcionamento das modificações para a branch `develop`.

#### Passo 1

No primeiro passo, iremos criar a `branch` fazendo uma ramificação da branch principal e disponibilizá-la no repositório remoto.

```
git checkout main
git checkout -b develop
git push origin develop
```

#### Passo 2

Agora, para criarmos a nova feature de média, iremos realizar o checkout da branch `develop` e criar uma nova branch direcionada a essa funcionalidade.

```bash
git checkout develop
git checkout -b feature/media
```

Depois, adicionamos o seguinte código:

```python
# Adicionar a calculator.py
def media(a, b):
    return (a + b) / 2

# Adicionar ao teste: test_calculator.py
def test_media():
    assert media(4, 6) == 5
```

Realize o `commit` e `push` para o repositório remoto, depois abra o PR da branch `feature/media` para branch `develop`.

```bash
git add .
git commit -m "Adiciona operação potência"
git push origin feature/media
```

#### Passo 3

Por fim, iremos realizar uma nova release do projeto,  quando a branch `develop` estiver estável:

```bash
git checkout develop
git checkout -b release/1.0.0
#Correções finais.
git push origin release/1.0.0
```

Depois, crie uma nova PR dessa branch para a `main`:

```bash
#PR:
release/1.0.0 -> main
```

**Repita os passos de 1 a 3** para as novas funcionalidades: `raiz quadrada`, `módulo`, e `porcentagem`. 
Lembre-se que para cada funcionalidade deve seguir os passos anteriormente elencados.
