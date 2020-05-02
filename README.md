<p align="center">
 <img width="500" height="388" src="https://raw.githubusercontent.com/Lucas8x/stopots-bot/gh-pages/assets/answer.gif">
</p>

# stopots-bot
Auto Play StopotS Browser Game

## Requerimentos
* Navegador
  * [Chrome](https://www.google.com/chrome/)
  * [Firefox](https://www.mozilla.org/firefox/new/)
  
## Uso
### Windows
1. [Download](https://github.com/Lucas8x/stopots-bot/archive/master.zip).
2. Extrair.
3. Abrir `run.bat`.
4. ["Jogar"](#menu)

* Caso o navegador abra e feche :
  * Atualizar o navegador instalado chrome/firefox e
  * Atualizar [chromedriver](https://chromedriver.chromium.org/downloads)/[geckodriver](https://github.com/mozilla/geckodriver/releases).

## Menu
1. Entrada Rápida - Ira entrar com o nome definido se não com um nome gerado pelo jogo ex:`Anonimo123`.
2. Entrar no Jogo - Sempre ira perguntar um nome.
3. Entrar com ID da Sala - Entra em uma sala específica.
4. [Configurações](#configurações).

## Configurações
1. Abrir `run.bat`
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

### ~~Javascript~~
1. ~Copiar o [script](https://raw.githubusercontent.com/Lucas8x/stopots-bot/master/stopots-bot.js).~
2. ~Entrar no site do jogo.~
3. ~Colar no console do navegaodr (F12).~
4. ~Pressionar Enter.~

Foi utilizado [StopAnswersAPI](https://github.com/nosliper/StopAnswersAPI) por [nosliper](https://github.com/nosliper) para formar um dicionário inicial
