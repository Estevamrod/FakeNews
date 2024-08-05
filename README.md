# VERACIDADE

Veracidade é um projeto de automatização do processo de busca e verificação de notícia independente da notícia. O projeto utiliza como base e essência a utilização de WebScraping e processos de tratamento de texto e dados.

## 🚀 Começando

precisa ser feito

### 📋 Pré-requisitos

Antes de tudo, para poder instalar as dependências, principalmente do python, deve ser aberto um ambiente virtual (virtual environment), além deve ter instalado na sua máquina o nodejs. Abaixo segue exemplo de como pode ser feito.

Windows
```
    python -m venv ./pasta-que-preferir
```

Após isso, basta apenas iniciar o ambiente.
```
    cd ./pasta-que-preferir/Scripts/activate
```
Feito isso, aparecerá no terminal/cmd o nome do ambiente virtual dentro de parentesês. Agora basta clonar o projeto do github e depois instalar o gerenciador de pacote utilizado no backend e depois instalar as dependências do frontend.
```
    git clone precisa colocar o link aqui
    cd FakeNews/
```
Dependencias backend
```
    cd server/
    pip install pipenv
    pipenv install Pipfile
    Python -m spacy download pt_core_news_lg
```
Dependencias frontend
```
    cd client/
    npm i ou npm install
```

### 🔧 Instalação

Para iniciar os servidores backend e frontend, deve ser verificado primeiro se as dependências estão instaladas, se não estiver, verificar o tópico Pré-requisitos.

Backend (teste)

```
    cd server/
    flask --app app run --debug
```

Frontend
```
    npm run dev
```

Para testar os servidores do projeto, basta apenas copiar a url, tanto do backend quanto do frontend, e colar em um navegador que você preferir. Com isso, você terá em sua tela um returno em json com uma mensagem (backend) e a tela principal do projeto (frontend).

## ⚙️ Executando os testes

Explicar como executar os testes automatizados para este sistema.

### 🔩 Analise os testes de ponta a ponta

Explique que eles verificam esses testes e porquê.

```
Dar exemplos
```

### ⌨️ E testes de estilo de codificação

Explique que eles verificam esses testes e porquê.

```
Dar exemplos
```

## 📦 Implantação

Adicione notas adicionais sobre como implantar isso em um sistema ativo

## 🛠️ Construído com

Mencione as ferramentas que você usou para criar seu projeto

* [Python](http://www.dropwizard.io/1.0.2/docs/) - O framework web usado
* [Flask](https://maven.apache.org/) - Gerente de Dependência
* [Spacy](https://rometools.github.io/rome/) - Usada para gerar RSS
* [Beautiful Soup](https://rometools.github.io/rome/) - Usada para gerar RSS
* [grequests](https://rometools.github.io/rome/) - Usada para gerar RSS
* [nltk](https://rometools.github.io/rome/) - Usada para gerar RSS
* [React](https://rometools.github.io/rome/) - Usada para gerar RSS
* [Vite](https://rometools.github.io/rome/) - Usada para gerar RSS
* [Nodejs](https://rometools.github.io/rome/) - Usada para gerar RSS
* [pipenv](https://rometools.github.io/rome/) - Usada para gerar RSS

## 🖇️ Colaborando

Por favor, leia o [COLABORACAO.md](https://gist.github.com/usuario/linkParaInfoSobreContribuicoes) para obter detalhes sobre o nosso código de conduta e o processo para nos enviar pedidos de solicitação.

## 📌 Versão

Nós usamos [SemVer](http://semver.org/) para controle de versão. Para as versões disponíveis, observe as [tags neste repositório](https://github.com/suas/tags/do/projeto). 

## ✒️ Autores

Mencione todos aqueles que ajudaram a levantar o projeto desde o seu início

* **Um desenvolvedor** - *Trabalho Inicial* - [umdesenvolvedor](https://github.com/linkParaPerfil)
* **Fulano De Tal** - *Documentação* - [fulanodetal](https://github.com/linkParaPerfil)

Você também pode ver a lista de todos os [colaboradores](https://github.com/usuario/projeto/colaboradores) que participaram deste projeto.

## 📄 Licença

Este projeto está sob a licença (sua licença) - veja o arquivo [LICENSE.md](https://github.com/usuario/projeto/licenca) para detalhes.

## 🎁 Expressões de gratidão

* Conte a outras pessoas sobre este projeto 📢;
* Convide alguém da equipe para uma cerveja 🍺;
* Um agradecimento publicamente 🫂;
* etc.
