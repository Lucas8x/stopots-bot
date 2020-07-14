import json
import os
from typing import Any


def cls() -> None:
  os.system('cls' if os.name == 'nt' else 'clear')


def create_default_files() -> None:
  if not (os.path.exists('config.json')):
    data = {
      "username": "",
      "validator": "check",
      "autoStop": False,
      "autoReady": True,
      "avatar": 0
    }
    with open('config.json', 'w') as config_file:
      json.dump(data, config_file, indent=2)


def get_config_setting(setting: str) -> Any:
  try:
    with open('config.json') as config_file:
      data = json.load(config_file)
    return data[setting]
  except Exception as e:
    print(f'Failed get json setting. Error: {e}')


def open_config_menu() -> None:
  with open('config.json', 'r+') as config_file:
    data = json.load(config_file)
    while True:
      print(f'1 - Mudar username [Atual: {data["username"]}]\n',
            f'2 - Alterar o validador [Atual: {data["validator"]}]\n',
            f'3 - Auto Stop [Status: {data["autoStop"]}]\n',
            f'4 - Auto Ready [Status: {data["autoReady"]}]\n',
            f'5 - Mudar avatar [Atual: {data["avatar"]}]\n',
            '0 - Voltar.')
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
        validator_change = int(input('1 - Rápido (Apenas confirma.)\n'
                                     '2 - Negar - (Invalidará todas as respostas inclusive as suas.)\n'
                                     '3 - Aceitar - (Validará todas as respostas inclusive as erradas.)\n'
                                     '4 - Avaliar - (Avaliará as respostas com base no dicionario e negará as outras.)\n'
                                     '5 - Não fazer nada.\n'
                                     '> '))

        if validator_change == 1:
          data['validator'] = 'quick'
          print('Validador alterado para modo rápido.\n')
        elif validator_change == 2:
          data['validator'] = 'deny'
          print('Validador alterado para modo de negação.\n')
        elif validator_change == 3:
          data['validator'] = 'accept'
          print('Validador alterado para modo de aceitação.\n')
        elif validator_change == 4:
          data['validator'] = 'check'
          print('Validador alterado para modo de avaliação.\n')
        elif validator_change == 5:
          data['validator'] = 'null'
          print('Validador alterado para não fazer nada.\n')

      elif option_to_config == '3':
        if data['autoStop']:
          data['autoStop'] = False
          print('Auto Stop Desabilitado.\n')
        else:
          data['autoStop'] = True
          print('Auto Stop Habilitado.\n')

      elif option_to_config == '4':
        if data['autoReady']:
          data['autoReady'] = False
          print('Auto Ready Desabilitado.\n')
        else:
          data['autoReady'] = True
          print('Auto Ready Habilitado.\n')

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
