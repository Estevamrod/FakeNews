# VERACIDADE

Veracidade é um projeto de automatização do processo de busca e verificação de notícia independente da notícia. O projeto utiliza como base e essência a utilização de WebScraping e processos de tratamento de texto e dados.

### 📋 Pré-requisitos

Antes de tudo, para poder instalar as dependências, principalmente do python, deve ser aberto um ambiente virtual (virtual environment), além disso, deve se ter instalado na sua máquina o nodejs. Abaixo segue exemplo de como pode ser feito.

Windows e Linux
```
    python -m venv ./pasta-que-preferir
```

Após isso, basta apenas iniciar o ambiente virtual para Windows.
```
    cd ./pasta-que-preferir/Scripts/
    activate
```
Para linux o processo acaba sendo semelhante ao descrito acima.
```
    source ./pasta-que-preferir/bin/activate
```

Feito isso, aparecerá no terminal/cmd o nome do ambiente virtual dentro de parentesês. Agora basta clonar o projeto do github e depois instalar o gerenciador de pacote utilizado no backend e depois instalar as dependências do frontend.

### 🔧 Instalação

```
    git clone https://github.com/Estevamrod/FakeNews
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

### Iniciar projeto
Para iniciar os servidores backend e frontend, deve ser verificado primeiro se as dependências estão instaladas, se não estiver, verificar o tópico Instalação.

Backend

```
    cd server/
    flask --app app run --debug
```

Frontend
```
    npm run dev
```

Para testar os servidores do projeto, basta apenas copiar a url, tanto do backend quanto do frontend, e colar em um navegador que você preferir, o servidor frontend trabalha em localhost com a porta 5197, dessa forma, basta colocar em qualquer navegador "http://localhost:5197", por exemplo. Com isso, você terá em sua tela um retorno em json com uma mensagem (backend) e a tela principal do projeto (frontend).

## 🛠️ Construído com

Mencione as ferramentas que você usou para criar seu projeto

* [Python](https://www.python.org/) - Versão até 3.12
* [Flask](https://flask.palletsprojects.com/en/stable/) - Mais Recente
* [Spacy](https://spacy.io/) - Mais Recente
* [Beautiful Soup](https://beautiful-soup-4.readthedocs.io/en/latest/) - Mais Recente
* [grequests](https://pypi.org/project/grequests/) - Mais Recente
* [nltk](https://www.nltk.org/) - Mais Recente
* [React](https://react.dev/) - Mais Recente
* [Vite](https://vite.dev/) - Mais Recente
* [Nodejs](https://nodejs.org/en) - Mais Recente
* [pipenv](https://pipenv.pypa.io/en/latest/) - Mais Recente

## ✒️ Autores

* **Estevam Otavio** - *Desenvolvedor/Autor* - [Estevam Otavio](https://github.com/Estevamrod)
* **César Alexandre** - *Desenvolvedor/Autor* - [César Alexandre](https://github.com/CesarAlexandreTeodoro)
* **Sérgio Eduardo** - *Autor*
