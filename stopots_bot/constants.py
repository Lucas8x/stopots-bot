from typing import Union

EQUIVALENTS = {
  'msé': ['adjetivo'],
  'animal': ['ave', 'inseto', 'mamífero'],
  'presente': ['objeto', 'instrumento musical', 'vestuário', 'brinquedo'],
  'objeto': ['presente', 'instrumento musical', 'vestuário', 'brinquedo'],
  'flv': ['fruta'],
  'cep': ['capital', 'cidade', 'país'],
  'nome': ['nome feminino', 'nome masculino', 'ator', 'celebridade', 'vilão', 'sobrenome', 'cantor', 'esportista'],
  'comida': ['comida saudável', 'sobremesa', 'flv', 'fruta', 'doce'],
}

CATEGORIES = ['ADJETIVO', 'ANIMAL', 'APP OU SITE', 'ATOR', 'AVE', 'BANDA', 'BRINQUEDO',
              'CANTOR', 'CAPITAL', 'CARRO', 'CELEBRIDADE', 'CEP', 'CIDADE', 'COMIDA SAUDÁVEL',
              'COR', 'DESENHO ANIMADO', 'DOCE', 'DOENÇA', 'ELETRO ELETRÔNICO', 'ESPORTE',
              'ESPORTISTA', 'FANTASIA', 'FILME', 'FLOR', 'FLV', 'FRUTA', 'GAME', 'GENTÍLICO',
              'IDIOMA', 'INGREDIENTE', 'INSETO', 'INSTRUMENTO MUSICAL', 'JLR', 'LÍQUIDO',
              'MAMÍFERO', 'MARCA', 'MEIO DE TRANSPORTE', 'MSÉ', 'MÚSICA', 'NOME FEMININO',
              'NOME MASCULINO', 'OBJETO', 'PALAVRA EM ESPANHOL', 'PALAVRA EM INGLÊS', 'PAÍS',
              'PCH', 'PDA', 'PERSONAGEM FICTÍCIO', 'PRESENTE', 'PROFISSÃO', 'PROGRAMA DE TV',
              'RAÇA DE CACHORRO', 'REMÉDIO', 'SABOR DE PIZZA', 'SABOR DE SORVETE', 'SOBREMESA',
              'SOBRENOME', 'SUPER-HERÓI', 'SÉRIE', 'TIME ESPORTIVO', 'VERBO', 'VESTUÁRIO', 'VILÃO',
              'FLV']


class Constants:
  """Classe das constantes do jogo."""
  url = 'https://stopots.com.br/'
  enter_button = '//*[@class="login"]/button[@class="enter"]'
  loading_animation = '//*[@class="load"]'

  username_input = '//*[@class="perfil"]//input'
  avatar_edit_button = '//button[@class="edit"]'
  avatar_confirm_button = '//*[@class="buttons"]/button'
  fade_animation = '//*[@class="popup-enter-done" or @class="popup-exit popup-exit-active"]'
  play_button = '//*[@class="actions"]/button[@class="bt-yellow icon-exclamation"]'
  play_button_clickable = f'{play_button}/strong'

  play_button2 = '//*[@class="bt-yellow icon-exclamation"]'
  username_input2 = '//*[@class="infosUser"]//input'

  letter = '//*[@id="letter"]/span'
  trophy = '//*[@class="active"]//*[@class="trophy"]'
  exit = '//*[@class="exit"]'
  rounds = '//*[@class="rounds"]/span'
  rounds_total = '//*[@class="rounds"]/p[2]'
  yellow_button = '//*[@class= "bt-yellow icon-exclamation"or @class="bt-yellow icon-exclamation shake"' \
                  ' or @class="bt-yellow icon-exclamation disable"]/strong'
  yellow_button_clickable = '//*[@class="bt-yellow icon-exclamation"' \
                            ' or @class="bt-yellow icon-exclamation shake"]'
  ready_button = f'{yellow_button_clickable}/strong'
  afk_button_xpath = '//*[@class="alert"]//*[@class="buttons"]/button'
  afk_box = '//*[@class="popup-exit popup-exit-active" or @class="class="popup-enter-done"]'

  @staticmethod
  def avatar(avatar_id: Union[str, int]) -> str:
    """
    Retorna o xpath do icone de avatar.
    :param avatar_id: número inteiro ou string de um número inteiro.
    :return: xpath - exemplo: //*[@class="avatar avt1]'
    """
    return f'//*[@class="avatar avt{avatar_id}"]'

  class FormPanel:
    """Classe do painel de respostas a serem escritas."""
    label = '//*[@class="ct answers" or @class="ct answers up-enter-done"]//label'

    @classmethod
    def field_input(cls, x: Union[str, int]) -> str:
      """
      Retorna o xpath do campo a ser escrita a resposta.
      :param x: número inteiro ou string de um número inteiro.
      :return: xpath - exemplo: //*[@class="ct answers" or @class="ct answers up-enter-done"]//label[1]/input
      """
      return f'{cls.label}[{x}]/input'

    @classmethod
    def field_category(cls, x: Union[str, int]) -> str:
      """
      Retorna o xpath da categoria do campo a ser escrita a resposta.
      :param x: número inteiro ou string de um número inteiro.
      :return: xpath - exemplo: //*[@class="ct answers" or @class="ct answers up-enter-done"]//label[1]/span
      """
      return f'{cls.label}[{x}]/span'

  class AnswerPanel:
    """Classe do painel de respostas a serem avaliadas."""
    category = '//*[@class="ct validation up-enter-done"]/div/h3'
    label = '//*[@class="ct validation up-enter-done"]//*[@class="scrollElements"]/label'

    @classmethod
    def label_status(cls, x: Union[str, int]) -> str:
      """
      Retorna o xpath do estado da resposta.
      :param x: número inteiro ou string de um número inteiro.
      :return: xpath - exemplo: //*[@class="ct validation up-enter-done"]//*[@class="scrollElements"]/label[1]/span
      """
      return f'{cls.label}[{x}]/span'

    @classmethod
    def label_answer(cls, x: Union[str, int]) -> str:
      """
      Retorna o xpath da resposta escrita.
      :param x: número inteiro ou string de um número inteiro.
      :return: xpath - exemplo: //*[@class="ct validation up-enter-done"]//*[@class="scrollElements"]/label[1]/div
      """
      return f'{cls.label}[{x}]/div'

    @classmethod
    def label_report(cls, x: Union[str, int]) -> str:
      """
      Retorna o xpath do link de denunciar abaixo do item da resposta.
      :param x: número inteiro ou string de um número inteiro.
      :return: xpath - exemplo: //*[@class="ct validation up-enter-done"]//*[@class="scrollElements"]/label[1]/a
      """
      return f'{cls.label}[{x}]/a'

    @classmethod
    def label_clickable(cls, x: Union[str, int]) -> str:
      """
      Retorna o xpath do item clicável.
      :param x: número inteiro ou string de um número inteiro.
      :return: xpath - exemplo: //*[@class="ct validation up-enter-done"]//*[@class="scrollElements"]/label[1]/div
      """
      return f'{cls.label}[{x}]/div'

  class PlayerList:
    """Classe do painel de jogadores."""
    li = '//*[@id="users"]/li'

    @classmethod
    def nick(cls, x: Union[str, int]) -> str:
      """
      Retorna o xpath do nome do jogador.
      :param x: número inteiro ou string de um número inteiro.
      :return: xpath - exemplo: //*[@id="users"]/li[1]//*[@class="infos"]/*[@class="nick"]
      """
      return f'{cls.li}[{x}]//*[@class="infos"]/*[@class="nick"]'

    @classmethod
    def points(cls, x: Union[str, int]) -> str:
      """
      Retorna o xpath dos pontos do jogador.
      :param x: número inteiro ou string de um número inteiro.
      :return: xpath - exemplo: //*[@id="users"]/li[1]//*[@class="infos"]/span
      """
      return f'{cls.li}[{x}]//*[@class="infos"]/span'

  class ScorePanel:
    """Classe do painel de pontuação da rodada."""
    h3 = '//*[@class="ct ranking" or @class="ct ranking up-enter-done"]//h3'
    h4 = '//*[@class="ct end" or @class="ct end up-enter-done"]//h4'
    player_div = '//*[@class="ct end" or @class="ct end up-enter-done"]//*[@class="positions"]/div'

    @classmethod
    def nick(cls, x: Union[str, int]) -> str:
      """
      Retorna o xpath do nome do jogador na tabela de pontuação do final da rodada.
      :param x: número inteiro ou string de um número inteiro.
      :return: xpath - exemplo: //*[@class="ct end" or @class="ct end up-enter-done"]//*[@class="positions"]/div[1]/*[@class="nick"]
      """
      return f'{cls.player_div}[{x}]/*[@class="nick"]'

    @classmethod
    def points(cls, x: Union[str, int]) -> str:
      """
      Retorna o xpath dos pontos do jogador na tabela de pontuação do final da rodada.
      :param x: número inteiro ou string de um número inteiro.
      :return: xpath - exemplo: //*[@class="ct end" or @class="ct end up-enter-done"]//*[@class="positions"]/div[1]/*[@class="points"]/text()
      """
      return f'{cls.player_div}[{x}]/*[@class="points"]/text()'

  class RankPanel:
    """Classe do painel de pontuação do fim do jogo."""
    li = '//*[@class="ct ranking" or @class="ct ranking up-enter-done"]//*[@class="scrollElements"]//li'

    @classmethod
    def position(cls, x: Union[str, int]) -> str:
      """
      Retorna o xpath da posição do jogador na tabela de pontuação do final do jogo.
      :param x: número inteiro ou string de um número inteiro.
      :return: xpath - exemplo: //*[@class="ct ranking" or @class="ct ranking up-enter-done"]//*[@class="scrollElements"]//li[1]//*[@class="position"]/span
      """
      return f'{cls.li}[{x}]//*[@class="position"]/span'

    @classmethod
    def nick(cls, x: Union[str, int]) -> str:
      """
      Retorna o xpath do nome do jogador na tabela de pontuação do final do jogo.
      :param x: número inteiro ou string de um número inteiro.
      :return: xpath - exemplo: //*[@class="ct ranking" or @class="ct ranking up-enter-done"]//*[@class="scrollElements"]//li[1]//*[@class="nick"]
      """
      return f'{cls.li}[{x}]//*[@class="nick"]'

    @classmethod
    def points(cls, x: Union[str, int]) -> str:
      """
      Retorna o xpath dos pontos do jogador na tabela de pontuação do final do jogo.
      :param x: número inteiro ou string de um número inteiro.
      :return: xpath - exemplo: //*[@class="ct ranking" or @class="ct ranking up-enter-done"]//*[@class="scrollElements"]//li[1]//*[@class="points"]
      """
      return f'{cls.li}[{x}]//*[@class="points"]'
