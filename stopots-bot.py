#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import random
import re
import json
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import locale
locale.setlocale(locale.LC_ALL, '')


class Game:
  enter_button = '//*[@class="login"]/button[@class="enter"]'
  loading_animation = '//*[@class="load"]'
  username_input = '//*[@class="perfil"]//input'
  avatar_edit_button = '//button[@class="edit"]'
  avatar_confirm_button = '//*[@class="buttons"]/button'
  fade_animation = '//*[@class="popup-enter-done" or @class="popup-exit popup-exit-active"]'
  play_button = '//*[@class="actions"]/button[@class="bt-yellow icon-exclamation"]'
  play_button_clickable = f'{play_button}/strong'
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
  def avatar(avatar_id):
    return f'//*[@class="avatar avt{avatar_id}"]'

  class FormPanel:
    label = '//*[@class="ct answers" or @class="ct answers up-enter-done"]//label'

    @staticmethod
    def field_input(x):
      return f'{Game.FormPanel.label}[{x}]/input'

    @staticmethod
    def field_category(x):
      return f'{Game.FormPanel.label}[{x}]/span'

  class AnswerPanel:
    category = '//*[@class="ct validation up-enter-done"]/div/h3'
    label = '//*[@class="ct validation up-enter-done"]//*[@class="scrollElements"]/label'

    @staticmethod
    def label_status(x):
      return f'{Game.AnswerPanel.label}[{x}]/span'

    @staticmethod
    def label_category(x):
      return f'{Game.AnswerPanel.label}[{x}]/div'

    @staticmethod
    def label_report(x):
      return f'{Game.AnswerPanel.label}[{x}]/a'

    @staticmethod
    def label_click(x):
      driver.find_element_by_xpath(f'{Game.AnswerPanel.label}[{x}]/div').click()
      '''return f'{Game.AnswerPanel.label}[{x}]/div'''

  class PlayerList:
    li = '//*[@id="users"]/li'

    @staticmethod
    def nick(x):
      return f'{Game.PlayerList.li}[{x}]//*[@class="infos"]/*[@class="nick"]'

    @staticmethod
    def points(x):
      return f'{Game.PlayerList.li}[{x}]//*[@class="infos"]/span'

  class ScorePanel:
    h3 = '//*[@class="ct ranking" or @class="ct ranking up-enter-done"]//h3'
    h4 = '//*[@class="ct end" or @class="ct end up-enter-done"]//h4'
    player_div = '//*[@class="ct end" or @class="ct end up-enter-done"]//*[@class="positions"]/div'

    @staticmethod
    def nick(x):
      return f'{Game.ScorePanel.player_div}[{x}]/*[@class="nick"]'

    @staticmethod
    def points(x):
      return f'{Game.ScorePanel.player_div}[{x}]/*[@class="points"]/text()'

  class RankPanel:
    li = '//*[@class="ct ranking" or @class="ct ranking up-enter-done"]//*[@class="scrollElements"]//li'

    @staticmethod
    def position(x):
      return f'{Game.RankPanel.li}[{x}]//*[@class="position"]/span'

    @staticmethod
    def nick(x):
      return f'{Game.RankPanel.li}[{x}]//*[@class="nick"]'

    @staticmethod
    def points(x):
      return f'{Game.RankPanel.li}[{x}]//*[@class="points"]'


def init_dictionary():
  try:
    with open('dictionary.json', encoding='utf-8') as dictionary_data:
      return json.load(dictionary_data)
  except Exception as e:
    print(f'Failed initialize dictionary, error: {e}')


def cls():
  os.system('cls' if os.name == 'nt' else 'clear')


def create_default_files():
  if not (os.path.exists('./config.json')):
    data = {
      "username": "",
      "validator": "check",
      "autoStop": False,
      "autoReady": True,
      "avatar": 0
    }
    with open('./config.json', 'a+') as config_file:
      json.dump(data, config_file, indent=2)


def get_config_setting(setting):
  try:
    with open('config.json') as config_file:
      data = json.load(config_file)
    return data[setting]
  except Exception as e:
    print(f'Failed get json setting. Error: {e}')


def open_config_menu():
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


def init_web_driver():
  try:
    firefox_capabilities = DesiredCapabilities.FIREFOX
    firefox_capabilities['marionette'] = True
    web_driver = webdriver.Firefox(executable_path='./geckodriver.exe', capabilities=firefox_capabilities)  # v23
    return web_driver
  except Exception as e:
    print(f'Failed to initialize Geckodriver: {e}')
    try:
      options = webdriver.ChromeOptions()
      options.add_argument('--log-level=3')
      options.add_argument('--silent')
      options.add_argument('--disable-extensions')
      options.add_argument('--disable-popup-blocking')
      web_driver = webdriver.Chrome('./chromedriver.exe', options=options)  # v80
      return web_driver
    except Exception as e:
      print(f'Failed to initialize Chromedriver: {e}')
      print('Instale/Atualize o seu Firefox/Chrome ou Geckodriver/Chromedriver.')
      time.sleep(5)
      quit()


def join_game(username):
  print('Entrando...')
  wait = WebDriverWait(driver, 10)

  # entrar button
  wait.until(ec.presence_of_element_located((By.XPATH, Game.enter_button)))
  driver.find_element_by_xpath(Game.enter_button).click()
  wait.until(ec.invisibility_of_element_located((By.XPATH, Game.loading_animation)))

  # username field
  if username != ' ' and 2 <= len(username) <= 15:
    wait.until(ec.presence_of_element_located((By.XPATH, Game.username_input)))
    driver.find_element_by_xpath(Game.username_input).clear()
    driver.find_element_by_xpath(Game.username_input).send_keys(username)
  else:
    username = driver.find_element_by_xpath(Game.username_input).get_attribute('value')

  # Avatar
  avatar_id = get_config_setting('avatar')
  if 1 <= avatar_id <= 36:
    time.sleep(2)
    # Botão edit => abre menu avatar
    wait.until(ec.element_to_be_clickable((By.XPATH, Game.avatar_edit_button)))
    driver.find_element_by_xpath(Game.avatar_edit_button).click()

    # Icone do Avatar
    if avatar_id > 14:
      driver.execute_script('arguments[0].scrollIntoView(true);', driver.find_element_by_xpath(Game.avatar(avatar_id)))
    wait.until(ec.element_to_be_clickable((By.XPATH, Game.avatar(avatar_id))))
    driver.find_element_by_xpath(Game.avatar(avatar_id)).click()

    # Botão confirmar escolha
    wait.until(ec.element_to_be_clickable((By.XPATH, Game.avatar_confirm_button)))
    driver.find_element_by_xpath(Game.avatar_confirm_button).click()

    # Esperar a animação
    wait.until(ec.invisibility_of_element_located((By.XPATH, Game.fade_animation)))
  time.sleep(2)

  # Botão Jogar => entra no jogo
  wait.until(ec.element_to_be_clickable((By.XPATH, Game.play_button)))
  time.sleep(2)
  driver.find_element_by_xpath(Game.play_button).click()
  print(f'Logado como: {username}')


def find_letter():
  try:
    letter = driver.find_element_by_xpath(Game.letter).text.lower()
    print(f'Letra Atual: {letter}')
    return letter
  except Exception as e:
    pass


def get_answer(letter, category):
  try:
    return random.choice(dictionary[letter][category])
  except IndexError:
    return False
  except Exception as e:
    print(f'Get answer error: {e}')
    return False


def auto_complete(letter):
  print('Auto Completando...')
  for x in range(1, 13):
    try:
      field_input = driver.find_element_by_xpath(Game.FormPanel.field_input(x)).get_attribute('value')
      if not field_input:
        field_category = driver.find_element_by_xpath(Game.FormPanel.field_category(x)).text.lower()

        if field_category == 'nome':
          field_category = random.choice(['nome feminino', 'nome masculino'])

        elif field_category == 'comida' and not dictionary[letter]['comida']:
          field_category = random.choice(['comida saudável', 'sobremesa', 'flv', 'fruta'])

        answer = get_answer(letter, field_category)
        if answer:
          driver.find_element_by_xpath(Game.FormPanel.field_input(x)).send_keys(answer)
      else:
        continue
    except Exception:
      print('')
      continue


def show_game_info():
  try:
    rounds = driver.find_element_by_xpath(Game.rounds).text
    total = driver.find_element_by_xpath(Game.rounds_total).text
    print(f'- Rodadas: {rounds}{total}')
  except Exception as e:
    pass

  print('- Jogadores -')
  for x in range(1, 15):
    try:
      nick = driver.find_element_by_xpath(Game.PlayerList.nick(x)).text
      points = driver.find_element_by_xpath(Game.PlayerList.points(x)).text
      if nick:
        if nick != username:
          print(f'{nick} - {points}')
        else:
          print(f'{nick} - {points} < você')
    except Exception as e:
      break


def show_round_end_rank():
  h3_status = driver.find_element_by_xpath(Game.ScorePanel.h3).text.upper()
  if h3_status == 'RANKING DA RODADA':
    print('- Ranking da Rodada -')
    for x in range(1, 15):
      try:
        position = driver.find_element_by_xpath(Game.RankPanel.position(x)).text
        nick = driver.find_element_by_xpath(Game.RankPanel.nick(x)).text
        points = driver.find_element_by_xpath(Game.RankPanel.points(x)).text
        if nick:
          if nick != username:
            print(f'{position}º - {nick} - {points}')
          else:
            print(f'{position}º - {nick} - {points} < você')
      except Exception as e:
        break

  elif h3_status == 'FIM DE JOGO!' or driver.find_element_by_xpath(Game.ScorePanel.h4).text.upper() == 'RANKING FINAL':
    print('- Fim de Jogo -')
    for x in range(1, 4):
      try:
        nick = driver.find_element_by_xpath(Game.ScorePanel.nick(x)).text
        points = driver.find_element_by_xpath(Game.ScorePanel.points(x)).text
        print(f'{x}º - {nick} - {points}')
      except Exception as e:
        break
  print('')


def validate(validator_type, letter):
  if driver.find_element_by_xpath(Game.yellow_button_clickable):
    if validator_type == 'quick':
      driver.find_element_by_xpath(Game.yellow_button_clickable).click()

    elif validator_type == 'deny':
      print('Negando todas as respostas...')
      for x in range(1, 15):
        if driver.find_element_by_xpath(Game.AnswerPanel.label_status(x)).text.upper() == 'VALIDADO!':
          Game.AnswerPanel.label_click(x)
      driver.find_element_by_xpath(Game.yellow_button_clickable).click()

    elif validator_type == 'accept':
      print('Confirmando todas as respostas...')
      for x in range(1, 15):
        if driver.find_element_by_xpath(Game.AnswerPanel.label_report(x)).text.upper() == 'DENUNCIAR':
          Game.AnswerPanel.label_click(x)
      driver.find_element_by_xpath(Game.yellow_button_clickable).click()

    elif validator_type == 'check':
      print('Verificando Respostas...')

      category = driver.find_element_by_xpath(Game.AnswerPanel.category).text
      category = re.sub('TEMA: ', '', category).lower()

      for x in range(1, 15):
        try:
          if driver.find_element_by_xpath(Game.AnswerPanel.label_status(x)).text.upper() == 'VALIDADO!':
            category_answer = driver.find_element_by_xpath(Game.AnswerPanel.label_category(x)).text.lower()
            if category not in ['nome', 'msé', 'comida']:
              if category_answer not in dictionary[letter][category]:
                Game.AnswerPanel.label_click(x)
            elif category == 'msé':
              if category_answer not in zip(dictionary[letter]['msé'],
                                            dictionary[letter]['adjetivo']):
                Game.AnswerPanel.label_click(x)
            elif category == 'nome':
              if category_answer not in zip(dictionary[letter]['nome feminino'],
                                            dictionary[letter]['nome masculino']):
                Game.AnswerPanel.label_click(x)
              elif category == 'comida':
                if category_answer not in zip(dictionary[letter]['comida'],
                                              dictionary[letter]['comida saudável'],
                                              dictionary[letter]['sobremesa'],
                                              dictionary[letter]['flv'],
                                              dictionary[letter]['fruta']):
                  Game.AnswerPanel.label_click(x)
        except Exception as e:
          continue
      driver.find_element_by_xpath(Game.yellow_button_clickable).click()

    elif validator_type == 'greedy':
      pass


def do_stop(letter):
  if driver.find_element_by_xpath(Game.yellow_button_clickable):
    for x in range(1, 13):
      input_field = driver.find_element_by_xpath(Game.FormPanel.field_input(x)).get_attribute('value')
      if input_field[0] == letter and len(input_field) >= 2:
        continue
      else:
        break
    else:
      print('STOP! Pressionado')
      driver.find_element_by_xpath(Game.yellow_button_clickable).click()


def play_the_game():
  validator_type = get_config_setting('validator')
  auto_stop = get_config_setting('autoStop')
  auto_ready = get_config_setting('autoReady')

  try:
    while True:
      cls()
      try:
        button = driver.find_element_by_xpath(Game.yellow_button).text.upper()
        letter = find_letter()
        if button == 'STOP!':
          auto_complete(letter)
          if auto_stop:
            do_stop(letter)
        elif button == 'AVALIAR' and validator_type != 'null':
          validate(validator_type, letter)
      except Exception as e:
        pass

      try:
        if auto_ready and driver.find_element_by_xpath(Game.ready_button).text.upper() == 'ESTOU PRONTO':
          driver.find_element_by_xpath(Game.yellow_button_clickable).click()
      except Exception as e:
        pass

      try:
        if driver.find_element_by_xpath(Game.trophy):
          show_round_end_rank()
      except Exception as e:
        pass

      try:
        if driver.find_element_by_xpath(Game.afk_button_xpath):
          time.sleep(2)
          driver.find_element_by_xpath(Game.afk_button_xpath).click()
        elif driver.find_elements_by_xpath(Game.afk_box):
          pass
      except Exception as e:
        pass

      show_game_info()
      time.sleep(3)

  except KeyboardInterrupt:
    cls()
    print('Options:\n'
          '1 - Sair da Sala.\n'
          '2 - Fechar o bot.')
    while True:
      try:
        option1 = int(input('> '))
        if 1 <= option1 <= 2:
          break
        else:
          print('Opção invalida.')
      except Exception as e:
        print('Digite um número.')

    if option1 == 1:
      if driver.find_element_by_xpath(Game.exit):
        driver.find_element_by_xpath(f'{Game.exit}/.').click()
      print('Deseja entrar em outra sala? (s/n)')
      while True:
        option2 = input('> ')
        if option2.lower() in 'sn':
          break
        else:
          print('Opção invalida.')

      if option2 == 's':
        wait = WebDriverWait(driver, 10)
        wait.until(ec.presence_of_element_located((By.XPATH, Game.play_button)))
        time.sleep(1)
        driver.find_element_by_xpath(Game.play_button_clickable).click()
        play_the_game()

      elif option2 == 'n':
        driver.quit()
        exit()

    elif option1 == 2:
      quit()


if __name__ == "__main__":
  create_default_files()
  driver = init_web_driver()
  dictionary = init_dictionary()
  while True:
    option = input('Opções:\n'
                   '1 - Entrada Rápida.\n'
                   '2 - Entrar no Jogo.\n'
                   '3 - Entrar com ID da Sala.\n'
                   '4 - Configurações.\n'
                   '5 - Sair.\n'
                   '> ')
    cls()

    if option == '1':
      driver.get('https://stopots.com.br/')
      username = get_config_setting('username')
      join_game(username)
      play_the_game()

    elif option == '2':
      while True:
        username = input('Digite um nome: ')
        if 2 <= len(username) <= 15:
          break
        else:
          print('Seu username/nick deve possuir entre 2 e 15 caracteres.')
      driver.get('https://stopots.com.br/')
      join_game(username)
      play_the_game()

    elif option == '3':
      room_id = input('ID: ')
      driver.get(f'https://stopots.com.br/{room_id}')
      username = get_config_setting('username')
      join_game(username)
      play_the_game()

    elif option == '4':
      open_config_menu()

    elif option == '5':
      driver.quit()
      exit()
    else:
      print('Opção invalida\n')

'''
categorias = ["ADJETIVO","ANIMAL","APP OU SITE","ATOR","AVE","BANDA","BRINQUEDO",
              "CANTOR","CAPITAL","CARRO", "CELEBRIDADE","CEP","CIDADE","COMIDA SAUDÁVEL",
              "COR","DESENHO ANIMADO","DOCE","DOENÇA","ELETRO ELETRÔNICO","ESPORTE",
              "ESPORTISTA","FANTASIA","FILME","FLOR","FLV","FRUTA","GAME","GENTÍLICO",
              "IDIOMA","INGREDIENTE","INSETO","INSTRUMENTO MUSICAL","JLR","LÍQUIDO",
              "MAMÍFERO","MARCA","MEIO DE TRANSPORTE","MSÉ","MÚSICA","NOME FEMININO",
              "NOME MASCULINO","OBJETO","PALAVRA EM ESPANHOL","PALAVRA EM INGLÊS","PAÍS",
              "PCH","PDA","PERSONAGEM FICTÍCIO","PRESENTE","PROFISSÃO","PROGRAMA DE TV",
              "RAÇA DE CACHORRO","REMÉDIO","SABOR DE PIZZA","SABOR DE SORVETE","SOBREMESA",
              "SOBRENOME","SUPER-HERÓI","SÉRIE","TIME ESPORTIVO","VERBO","VESTUÁRIO","VILÃO",
              "FLV"]
'''
