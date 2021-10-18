<p align="center">
 <img width="500" height="388" src="https://raw.githubusercontent.com/Lucas8x/stopots-bot/gh-pages/assets/answer.gif" alt="">
</p>

<p align="center">
 <img alt="GitHub" src="https://img.shields.io/github/license/lucas8x/stopots-bot?style=flat-square">
 <img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/lucas8x/stopots-bot?style=flat-square">
</p>

<p align="center">
 <a href="#-requerimentos">Requerimentos</a> •
 <a href="#-instalação">Instalação</a> •
 <a href="#-uso">Como usar</a> •
 <a href="#menu">Menu</a> •
 <a href="#-licença">Licença</a>
</p>

# stopots-bot

Automatizando sua jogabilidade de StopotS

## 💻 Requerimentos

- [Python 3](https://www.python.org/)
- selenium
- webdriver-manager
- tabulate
- Navegador
  - [Chrome](https://www.google.com/chrome/)
  - [Firefox](https://www.mozilla.org/firefox/new/)

## 🚀 Instalação
Se você já possui o python e o git instalado:
```Shell
# Clone o repositório
git clone https://github.com/Lucas8x/stopots-bot.git

# Entre na pasta
cd stopots-bot

# Instale as dependências
python setup.py install
```
Se você possui apenas o python:
```Shell
pip install stopots-bot
```

### Manual

_Se você não possuir o python nem o git instalado._

1. [Download](https://github.com/Lucas8x/stopots-bot/archive/master.zip).
2. Extrair.
3. Abrir `run.bat`.
4. ["Jogar"](#menu).

## 🔨 Uso

```bash
# Entrando com um nome
stopots -u lucas
```

**NOTA:** Todas as opções são opcionais.

```
Opções:
  -h, --help            mostra esta mensagem de ajuda
  --user USERNAME, -u USERNAME
                        seu username
  --avatar AVATAR, -a AVATAR
                        número do avatar
  --room ROOM_ID, -r ROOM_ID
                        número da sala
  --auto-stop           habilita stop automático
  --auto-ready          habilita ready automático
  --validator {quick,deny,accept,check,null}
                        tipo do avaliador
  --driver {chrome,firefox}
                        seu navegador
  --dict                abre o menu do dicionário
```

### Menu

1. Entrada Rápida - Ira entrar com o nome definido se não com um nome gerado pelo jogo ex:`Anonimo123`.
2. Entrar no Jogo - Sempre ira perguntar um nome.
3. Entrar com ID da Sala - Entra em uma sala específica.
4. [Configurações](#configurações).

## ⚙️ Configurações

1. Abrir `run.bat`.
2. Digite "4" para abrir as opções.

- Username/nick deve possuir entre 2 e 15 caracteres.
- Avaliadores:
  - Rápido - Apenas confirma as respostas sem verificar.
  - Aceitar - Confirma todas as respostas inclusive as erradas.
  - Negação - Invalidará todas as respostas inclusive as suas.
  - Avaliar - Avaliará as respostas com base no dicionario e negará as outras.
  - Nada - ...
- STOP! Automático - Irá apertar STOP! caso todas as respostas estejam preenchidas.
- Ready Automático - Irá apertar Estou Pronto ao mostrar o resultado da rodada.
- Avatar - Mínimo: 0 Máximo: 36.
<!-- - <details>
    <summary>Avatares</summary>
    a
  </details> -->

## ⚠️ Problemas

- Caso o navegador abra e feche :
  - Atualizar o navegador instalado chrome/firefox

## 📝 Licença

Este projeto esta sob a licença [MIT](./LICENSE).

## 💜 Menção Honrosa

Foi utilizado [StopAnswersAPI](https://github.com/nosliper/StopAnswersAPI) por [nosliper](https://github.com/nosliper) para formar um dicionário inicial.
