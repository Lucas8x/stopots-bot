<p align="center">
 <img width="500" height="388" src="https://raw.githubusercontent.com/Lucas8x/stopots-bot/gh-pages/assets/answer.gif">
</p>

# stopots-bot
Automatizando sua jogabilidade de StopotS

## Requerimentos
* Python 3
* selenium
* webdriver-manager
* tabulate
* Navegador
  * [Chrome](https://www.google.com/chrome/)
  * [Firefox](https://www.mozilla.org/firefox/new/)
  
## Instalação
*Se você tiver o python e o git instalado.*
<pre><code>git clone https://github.com/Lucas8x/stopots-bot.git
cd stopots-bot
python setup.py install
</code></pre>
*Através do PIP.*
<pre><code>pip install stopots-bot
</code></pre>

### Manual
*Se você não tiver o python nem o git instalado.*
1. [Download](https://github.com/Lucas8x/stopots-bot/archive/master.zip).
2. Extrair.
3. Abrir `run.bat`.
4. ["Jogar"](#menu).

## Uso
Entrando com um nome:
<pre><code>stopots -u lucas</code></pre>

**NOTA:** Todas as opções são opcionais.
<pre><code>Opções:
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
</code></pre>

## Menu
1. Entrada Rápida - Ira entrar com o nome definido se não com um nome gerado pelo jogo ex:`Anonimo123`.
2. Entrar no Jogo - Sempre ira perguntar um nome.
3. Entrar com ID da Sala - Entra em uma sala específica.
4. [Configurações](#configurações).

## Configurações
1. Abrir `run.bat`.
2. Digite "4" para abrir as opções.

* Username/nick deve possuir entre 2 e 15 caracteres.
* Avaliadores:
  * Rápido - Apenas confirma as respostas sem verificar.
  * Aceitar - Confirma todas as respostas inclusive as erradas.
  * Negação - Invalidará todas as respostas inclusive as suas.
  * Avaliar - Avaliará as respostas com base no dicionario e negará as outras.
  * Nada - ...
* STOP! Automático - Irá apertar STOP! caso todas as respostas estejam preenchidas.
* Ready Automático - Irá apertar Estou Pronto ao mostrar o resultado da rodada.
* Avatar - Mínimo: 0 Máximo: 36.
 * <details><summary>Avatares</summary>
   a
  </details>

## Problemas
* Caso o navegador abra e feche :
  * Atualizar o navegador instalado chrome/firefox

Foi utilizado [StopAnswersAPI](https://github.com/nosliper/StopAnswersAPI) por [nosliper](https://github.com/nosliper) para formar um dicionário inicial.
