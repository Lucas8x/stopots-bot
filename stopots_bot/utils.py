import json
import os
import random
from pathlib import Path
from typing import Any, Union, Optional


def cls() -> None:
  """limpa a tela."""
  os.system('cls' if os.name == 'nt' else 'clear')


def log_error(msg: str, exception: Exception):
  """
  Mostra mensagem de error com a exception
  :param msg: mensagem
  :param exception: Exception
  """
  print(f'\033[31m[ERROR]\033[m{msg} | {exception} | {exception.__class__.__name__}')


def is_a_valid_id(id_: Union[str, int]) -> bool:
  """
  Verifica se o número ou a string recebida é um número válido.
  :param id_: número inteiro ou string
  :return: bool
  """
  try:
    return isinstance(int(id_), int)
  except (ValueError, TypeError):
    return False


def is_a_valid_username(string: str) -> bool:
  """
  Verifica se a string recebida está na margem válida para um nome.
  :param string: nome
  :return: bool
  """
  return 2 <= len(string) <= 15


def random_from_list(arr: list[str]) -> Optional[str]:
  """
  Seleciona um item aleatório da lista.
  :param arr: lista de itens.
  :return: um item aleatório da lista | None
  """
  try:
    return random.choice(arr)
  except IndexError:
    return None
  except Exception as e:
    log_error('Random from list', e)
    return None


def create_default_files() -> None:
  """Criar o config.json padrão"""
  if not Path('config.json').exists():
    data = {
      "username": "",
      "validator": "check",
      "autoStop": False,
      "autoReady": True,
      "avatar": 0,
      "useEquivalence": True
    }
    with open('config.json', 'w') as config_file:
      json.dump(data, config_file, indent=2)


def get_config_setting(setting: str) -> Any:
  """
  Retorna o valor da chave recebida.
  :param setting: chave/nome
  :return: Any
  """
  try:
    with open('config.json') as config_file:
      data = json.load(config_file)
    return data[setting]
  except Exception as e:
    print(f'Failed get json setting. Error: {e}')


def invert_setting(data: dict, setting: str, msg: str) -> None:
  """
  Inverte uma configuração booleana
  :param data: python dictionary
  :param setting: chave/nome
  :param msg: mensagem/prefixo
  """
  data[setting] = not data[setting]
  print(msg, "Habilitado" if data[setting] else "Desabilitado")


def open_config_menu() -> None:
  """Abre um menu de configurações para o config.json"""
  with open('config.json', 'r+') as config_file:
    data = json.load(config_file)
    while True:
      print(f'1 - Mudar username [Atual: {data["username"]}]\n'
            f'2 - Alterar o validador [Atual: {data["validator"]}]\n'
            f'3 - Auto Stop [Status: {data["autoStop"]}]\n'
            f'4 - Auto Ready [Status: {data["autoReady"]}]\n'
            f'5 - Mudar avatar [Atual: {data["avatar"]}]\n'
            f'6 - Equivalência de categorias [Atual: {data["useEquivalence"]}]\n'
            '0 - Voltar')
      option_to_config = input('> ')
      cls()

      if option_to_config == '1':
        print('0 - Voltar.')
        username_input = input('Username: ')
        if username_input != '0':
          if 2 <= len(username_input) <= 15:
            data['username'] = username_input
          else:
            print('Seu username/nick deve possuir entre 2 e 15 caracteres.')

      elif option_to_config == '2':
        validator_change = int(input('1 - Rápido - Apenas confirma.\n'
                                     '2 - Negar - Invalidará todas as respostas inclusive as suas.\n'
                                     '3 - Aceitar - Validará todas as respostas inclusive as erradas.\n'
                                     '4 - Avaliar - Avaliará as respostas com base no dicionario e negará as outras.\n'
                                     '5 - Não fazer nada.\n'
                                     '> '))
        validators = {
          1: {'name': 'quick', 'desc': 'modo rápido'},
          2: {'name': 'deny', 'desc': 'modo de negação'},
          3: {'name': 'accept', 'desc': 'modo aceitação'},
          4: {'name': 'check', 'desc': 'modo avaliação'},
          5: {'name': 'null', 'desc': 'não fazer nada'},
        }

        data['validator'] = validators[validator_change]['name']
        print(f'Validador alterado para {validators[validator_change]["desc"]}\n')

      elif option_to_config in ['3', '4', '6']:
        settings = {
          3: {'setting': 'autoStop', 'msg': 'Auto Stop'},
          4: {'setting': 'autoReady', 'msg': 'Auto Ready'},
          6: {'setting': 'useEquivalence', 'msg': 'Equivalência'}
        }
        option_to_config = int(option_to_config)
        invert_setting(data, settings[option_to_config]['setting'], settings[option_to_config]['msg'])

      elif option_to_config == '5':
        while True:
          avatar_num = int(input('Número do Avatar: '))
          if 0 <= avatar_num <= 36:
            data['avatar'] = avatar_num
            break
          else:
            print('Min: 0 Max: 36')

      elif option_to_config == '0':
        cls()
        break

      else:
        print('Opção Invalida.\n')

      config_file.seek(0)
      json.dump(data, config_file, indent=2)
      config_file.truncate()
