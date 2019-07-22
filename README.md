# stopots-bot
Auto Play StopotS Game

## Requerimentos
* Python 3
* selenium
  * geckodriver
  * chromedriver

## Uso
### Windows
1. [Download](https://github.com/Lucas8x/stopots-bot/archive/master.zip).
2. Extrair.
3. Abrir `run.bat`.

* Caso o navegador não abra:
  * Atualizar o navegador instalado chrome/firefox.
  * Atualizar chromedriver/geckodriver.

## Configurações
1. Abrir `run.bat`
2. Digite "4" para abrir o menu.

* Username/nick deve possuir entre 2 e 15 caracteres.
* Avaliadores:
  * Rápido - Apenas confirma.
  * Negação - Invalidará todas as respostas inclusive as suas.
  * Avaliar - Avaliará as respostas com base no dicionario e negará as outras.
  * Nada - ...
* STOP! Automático - Ira apertar STOP! caso todas as respostas estejam preenchidas.
* Avatar - Mínimo: 0 Máximo: 36.

## Menu
1. Entrada Rápida - Ira entrar com o nome definido se não com um nome gerado pelo jgoo `Anonimo123`.
2. Entrar no Jogo - Sempre ira perguntar um nome.
3. ~Entrar com ID da Sala - Entra em uma sala específica.~
4. Configurações.


Foi utilizado [StopAnswersAPI](https://github.com/nosliper/StopAnswersAPI) por [nosliper](https://github.com/nosliper) para formar um dicionário inicial
