from typing import Union


class Constants:
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
    return f'//*[@class="avatar avt{avatar_id}"]'

  class FormPanel:
    label = '//*[@class="ct answers" or @class="ct answers up-enter-done"]//label'

    @classmethod
    def field_input(cls, x: Union[str, int]) -> str:
      return f'{cls.label}[{x}]/input'

    @classmethod
    def field_category(cls, x: Union[str, int]) -> str:
      return f'{cls.label}[{x}]/span'

  class AnswerPanel:
    category = '//*[@class="ct validation up-enter-done"]/div/h3'
    label = '//*[@class="ct validation up-enter-done"]//*[@class="scrollElements"]/label'

    @classmethod
    def label_status(cls, x: Union[str, int]) -> str:
      return f'{cls.label}[{x}]/span'

    @classmethod
    def label_category(cls, x: Union[str, int]) -> str:
      return f'{cls.label}[{x}]/div'

    @classmethod
    def label_report(cls, x: Union[str, int]) -> str:
      return f'{cls.label}[{x}]/a'

    @classmethod
    def label_clickable(cls, x: Union[str, int]) -> str:
      return f'{cls.label}[{x}]/div'

  class PlayerList:
    li = '//*[@id="users"]/li'

    @classmethod
    def nick(cls, x: Union[str, int]) -> str:
      return f'{cls.li}[{x}]//*[@class="infos"]/*[@class="nick"]'

    @classmethod
    def points(cls, x: Union[str, int]) -> str:
      return f'{cls.li}[{x}]//*[@class="infos"]/span'

  class ScorePanel:
    h3 = '//*[@class="ct ranking" or @class="ct ranking up-enter-done"]//h3'
    h4 = '//*[@class="ct end" or @class="ct end up-enter-done"]//h4'
    player_div = '//*[@class="ct end" or @class="ct end up-enter-done"]//*[@class="positions"]/div'

    @classmethod
    def nick(cls, x: Union[str, int]) -> str:
      return f'{cls.player_div}[{x}]/*[@class="nick"]'

    @classmethod
    def points(cls, x: Union[str, int]) -> str:
      return f'{cls.player_div}[{x}]/*[@class="points"]/text()'

  class RankPanel:
    li = '//*[@class="ct ranking" or @class="ct ranking up-enter-done"]//*[@class="scrollElements"]//li'

    @classmethod
    def position(cls, x: Union[str, int]) -> str:
      return f'{cls.li}[{x}]//*[@class="position"]/span'

    @classmethod
    def nick(cls, x: Union[str, int]) -> str:
      return f'{cls.li}[{x}]//*[@class="nick"]'

    @classmethod
    def points(cls, x: Union[str, int]) -> str:
      return f'{cls.li}[{x}]//*[@class="points"]'


equivalents = {
  'msé': ['adjetivo'],
  'animal': ['ave', 'inseto', 'mamífero'],
  'presente': ['objeto', 'instrumento musical', 'vestuário', 'brinquedo'],
  'objeto': ['presente', 'instrumento musical', 'vestuário', 'brinquedo'],
  'flv': ['fruta'],
  'cep': ['capital', 'cidade', 'país'],
  'fantasia': ['animal', 'ave', 'inseto', 'mamífero'],
  'nome': ['nome feminino', 'nome masculino', 'ator', 'celebridade', 'vilão', 'sobrenome'],
  'comida': ['comida saudável', 'sobremesa', 'flv', 'fruta', 'doce'],
}

categories = ['ADJETIVO', 'ANIMAL', 'APP OU SITE', 'ATOR', 'AVE', 'BANDA', 'BRINQUEDO',
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
