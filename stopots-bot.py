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
from selenium.webdriver.support import expected_conditions as EC
import locale
locale.setlocale(locale.LC_ALL, '')

with open('dicionario.json', encoding='utf-8') as dicio:
  dictionary = json.load(dicio)


def cls():
  os.system('cls' if os.name == 'nt' else 'clear')


def default_files():
  if not (os.path.exists('./config.json')):
    data = {
      'username': '',
      'validator': 'check',
      'autoStop': False,
      'avatar': 0
    }
    with open('./config.json', 'a+') as x:
      json.dump(data, x, indent=2)


def get_json_setting(setting):
  with open('config.json') as config:
    data = json.load(config)
  return data[setting]


def config_json_settings():
  with open('config.json', 'r+') as j:
    data = json.load(j)
    while True:
      print(f"1 - Mudar username [Atual: {data['username']}]",
            f"\n2 - Alterar o validador [Atual: {data['validator']}]",
            f"\n3 - Auto Stop [Status: {data['autoStop']}]",
            f"\n4 - Mudar avatar [Atual: {data['avatar']}]",
            "\n0 - Voltar.")
      option_to_config = input(">")
      cls()
      if option_to_config == '1':
        print("0 - Voltar.")
        username = input("Username: ")
        if username != '0':
          if 2 <= len(username) <= 15:
            data['username'] = username
          else:
            print("Seu username/nick deve possuir entre 2 e 15 caracteres.")
      elif option_to_config == '2':
        print("1 - Rápido (Apenas confirma.)"
              "\n2 - Negar - (Invalidará todas as respostas inclusive as suas.)"
              "\n3 - Avaliar - (Avaliará as respostas com base no dicionario e negará as outras.)"
              "\n4 - Não fazer nada.")
        validator_change = int(input("> "))
        if validator_change == 1:
          data['validator'] = 'quick'
          print("Validador alterado para modo rápido.\n")
        elif validator_change == 2:
          data['validator'] = 'deny'
          print("Validador alterado para modo de negação.\n")
        elif validator_change == 3:
          data['validator'] = 'check'
          print("Validador alterado para modo de avaliação.\n")
        elif validator_change == 4:
          data['validator'] = 'null'
          print("Validador alterado para não fazer nada.\n")
        else:
          pass
      elif option_to_config == '3':
        if data['autoStop']:
          data['autoStop'] = False
          print("Auto Stop Desabilitado.\n")
        elif not data['autoStop']:
          data['autoStop'] = True
          print("Auto Stop Habilitado.\n")
      elif option_to_config == '4':
        while True:
          avatar_num = int(input("Número do Avatar: "))
          if 0 <= avatar_num <= 36:
            data['avatar'] = avatar_num
            break
          else: print("Min: 0 Max: 36")
      elif option_to_config == '0':
        cls()
        break
      else:
        print("Opção Invalida.\n")
      j.seek(0)
      json.dump(data, j, indent=2)
      j.truncate()


def my_driver():
  global driver
  try:
    firefox_capabilities = DesiredCapabilities.FIREFOX
    firefox_capabilities['marionette'] = True
    driver = webdriver.Firefox(executable_path='./geckodriver.exe', capabilities=firefox_capabilities)  # v23
  except:
    try:
      options = webdriver.ChromeOptions()
      options.add_argument('--log-level=3')
      options.add_argument('--silent')
      options.add_argument('--disable-extensions')
      options.add_argument('--disable-popup-blocking')
      driver = webdriver.Chrome('./chromedriver.exe', options=options)  # v78
    except:
      print("Instale/Atualize o seu Firefox/Chrome ou Geckodriver/Chromedriver.")
      time.sleep(5)
      quit()
  return driver


def join_game(username):
  print("Entrando...")
  wait = WebDriverWait(driver, 10)

  # entrar button
  wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class="login"]/button[@class="enter"]')))
  driver.find_element_by_xpath('//*[@class="login"]/button[@class="enter"]').click()
  wait.until(EC.invisibility_of_element_located((By.XPATH, '//*[@class="load"]')))

  # username field
  if username != ' ':
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class="perfil"]//input')))
    driver.find_element_by_xpath('//*[@class="perfil"]//input').clear()
    driver.find_element_by_xpath('//*[@class="perfil"]//input').send_keys(username)
  else: username = driver.find_element_by_xpath('//*[@class="perfil"]//input').get_attribute('value')

  # Avatar
  avatar_id = get_json_setting('avatar')
  if 1 <= avatar_id <= 36:
    time.sleep(2)
    # Botão edit => abre menu avatar
    wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@class="edit"]')))
    driver.find_element_by_xpath('//button[@class="edit"]').click()

    # Icone do Avatar
    if avatar_id > 14:
      driver.execute_script("arguments[0].scrollIntoView(true);",
                            driver.find_element_by_xpath('//*[@class="avatar avt'+str(avatar_id)+'"]'))
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="avatar avt'+str(avatar_id)+'"]')))
    driver.find_element_by_xpath('//*[@class="avatar avt'+str(avatar_id)+'"]').click()

    # Botão confirmar escolha
    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@class="buttons"]/button')))
    driver.find_element_by_xpath('//*[@class="buttons"]/button').click()

    # Esperar a animação
    wait.until(EC.invisibility_of_element_located((By.XPATH, '//*[@class="popup-enter-done" '
                                                             'or @class="popup-exit popup-exit-active"]')))
  time.sleep(2)

  # Botão Jogar => entra no jogo
  wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="actions"]/button[@class="bt-yellow icon-exclamation"]')))
  time.sleep(2)
  driver.find_element_by_xpath('//*[@class="actions"]/button[@class="bt-yellow icon-exclamation"]').click()
  print(f"Logado como: {username}")


def find_letter():
  try:
    letter = driver.find_element_by_xpath('//*[@id="letter"]/span').text.lower()
    print("Letra Atual:", letter)
    return letter
  except:
    pass


def get_answer(letter, category):
  try:
    return random.choice(dictionary[letter][category])
  except:
    return False


def auto_complete(letter):
  print("Auto Completando...")
  for x in range(1, 13):
    try:
      input_field = driver.find_element_by_xpath('//*[@class="ct answers"'
                                                 ' or @class="ct answers up-enter-done"]//label['+str(x)+']/input'
                                                 ).get_attribute('value')
      if len(input_field) == 0:
        field_category = driver.find_element_by_xpath('//*[@class="ct answers"'
                                                      ' or @class="ct answers up-enter-done"]//label['+str(x)+']/span'
                                                      ).text.lower()

        if field_category == 'nome':
          field_category = random.choice(['nome feminino', 'nome masculino'])

        elif field_category == 'comida' and len(dictionary[letter]['comida']) == 0:
          field_category = 'comida saudável'

        answer = get_answer(letter, field_category)
        if answer:
          driver.find_element_by_xpath('//*[@class="ct answers"'
                                       ' or @class="ct answers up-enter-done"]//label['+str(x)+']/input'
                                       ).send_keys(answer)
      else:
        continue
    except:
      continue


def match_info():
  # Rodadas
  try:
    rounds = driver.find_element_by_xpath('//*[@class="rounds"]/span').text
    total = driver.find_element_by_xpath('//*[@class="rounds"]/p[2]').text
    print(f"- Rodadas: {rounds}{total}")
  except:
    pass

  print("- Jogadores -")
  for x in range(1, 15):
    try:
      nick = driver.find_element_by_xpath('//*[@id="users"]/li['+str(x)+']//*[@class="infos"]/*[@class="nick"]').text
      pts = driver.find_element_by_xpath('//*[@id="users"]/li['+str(x)+']//*[@class="infos"]/span').text
      if nick:
        global username
        if nick != username:
          print(f"{nick} - {pts}")
        else:
          print(f">{nick} - {pts}")
    except:
      break


def round_end_rank():
  # Ranking da Rodada
  if driver.find_element_by_xpath('//*[@class="ct ranking"'
                                  ' or @class="ct ranking up-enter-done"]//h3'
                                  ).text.upper() == 'RANKING DA RODADA':
    print("- Ranking da Rodada -")
    for x in range(1, 15):
      try:
        position = driver.find_element_by_xpath('//*[@class="ct ranking" or @class="ct ranking up-enter-done"]'
                                                '//*[@class="scrollElements"]//li['+str(x)+']//*[@class="position"]/span'
                                                ).text
        nick = driver.find_element_by_xpath('//*[@class="ct ranking" or @class="ct ranking up-enter-done"]'
                                            '//*[@class="scrollElements"]//li['+str(x)+']//*[@class="nick"]'
                                            ).text
        pts = driver.find_element_by_xpath('//*[@class="ct ranking" or @class="ct ranking up-enter-done"]'
                                           '//*[@class="scrollElements"]//li['+str(x)+']//*[@class="points"]'
                                           ).text
        if nick:
          if nick != username:
            print(f"{position}º - {nick} - {pts}")
          else:
            print(f"{position}º - {nick} - {pts} <")
      except:
        break

  # Rank Fim de Jogo (TOP 3)
  elif driver.find_element_by_xpath('//*[@class="ct end"'
                                    ' or @class="ct end up-enter-done"]//h3'
                                    ).text.upper() == 'FIM DE JOGO!' or \
      driver.find_element_by_xpath('//*[@class="ct end"'
                                   ' or @class="ct end up-enter-done"]//h4'
                                   ).text.upper() == 'RANKING FINAL':
    print("- Fim de Jogo -")
    for x in range(1, 4):
      try:
        nick = driver.find_element_by_xpath('//*[@class="ct end" or @class="ct end up-enter-done"]'
                                            '//*[@class="positions"]/div['+str(x)+']/*[@class="nick"]'
                                            ).text
        pts = driver.find_element_by_xpath('//*[@class="ct end" or @class="ct end up-enter-done"]'
                                           '//*[@class="positions"]/div['+str(x)+']/*[@class="points"]/text()'
                                           ).text
        print(f"{x}º - {nick} - {pts}")
      except:
        break
  print("")
#rank final não esta aparecendo


def validate(validator_type, letter):
  if driver.find_element_by_xpath('//*[@class="bt-yellow icon-exclamation"'
                                  ' or @class="bt-yellow icon-exclamation shake"]'):
    if validator_type == 'quick':
      driver.find_element_by_xpath('//*[@class="bt-yellow icon-exclamation"'
                                   ' or @class="bt-yellow icon-exclamation shake"]').click()

    elif validator_type == 'deny':
      print("Negando todas as respostas...")
      for x in range(1, 15):
        if driver.find_element_by_xpath('//*[@class="ct validation up-enter-done"]'
                                        '//*[@class="scrollElements"]/label['+str(x)+']/span'
                                        ).text == 'VALIDADO!':
          driver.find_element_by_xpath('//*[@class="ct validation up-enter-done"]'
                                       '//*[@class="scrollElements"]/label['+str(x)+']/div'
                                       ).click()
      driver.find_element_by_xpath('//*[@class="bt-yellow icon-exclamation"'
                                   ' or @class="bt-yellow icon-exclamation shake"]'
                                   ).click()

    elif validator_type == 'check':
      print("Verificando Respostas...")

      category = driver.find_element_by_xpath('//*[@class="ct validation up-enter-done"]/div/h3').text
      category = re.sub('TEMA: ', '', category).lower()

      for x in range(1, 15):
        try:
          if driver.find_element_by_xpath('//*[@class="ct validation up-enter-done"]'
                                          '//*[@class="scrollElements"]/label['+str(x)+']/span'
                                          ).text == 'VALIDADO!':
            category_answer = driver.find_element_by_xpath('//*[@class="ct validation up-enter-done"]'
                                                           '//*[@class="scrollElements"]/label['+str(x)+']/div'
                                                           ).text.lower()
            if category != 'nome':
              if category_answer not in dictionary[letter][category]:
                driver.find_element_by_xpath('//*[@class="ct validation up-enter-done"]'
                                             '//*[@class="scrollElements"]/label['+str(x)+']/div'
                                             ).click()
            else:
              if category_answer not in dictionary[letter]['nome feminino'] \
                    or category_answer in dictionary[letter]['nome masculino']:
                driver.find_element_by_xpath('//*[@class="ct validation up-enter-done"]'
                                             '//*[@class="scrollElements"]/label['+str(x)+']/div'
                                             ).click()
        except:
          continue
      # Botão de Confirmar Avaliação
      driver.find_element_by_xpath('//*[@class="bt-yellow icon-exclamation"'
                                   ' or @class="bt-yellow icon-exclamation shake"]'
                                   ).click()

    # Mood Ganancioso
    elif validator_type == 'greedy':
      pass


def play_the_game():
  validator_type = get_json_setting('validator')
  auto_stop = get_json_setting('autoStop')

  try:
    while True:
      cls()
      try:
        button = driver.find_element_by_xpath('//*[@class= "bt-yellow icon-exclamation"'
                                              ' or @class="bt-yellow icon-exclamation shake"'
                                              ' or @class="bt-yellow icon-exclamation disable"]/strong'
                                              ).text.upper()
        # STOP !
        if button == 'STOP!':
          letter = find_letter()
          auto_complete(letter)
          if auto_stop and driver.find_element_by_xpath('//*[@class= "bt-yellow icon-exclamation"'
                                                        ' or @class="bt-yellow icon-exclamation shake"]'):
            for x in range(1, 13):
              input_field = driver.find_element_by_xpath('//*[@class="ct answers"'
                                                        ' or @class="ct answers up-enter-done"]//label['+str(x)+']/input'
                                                        ).get_attribute('value')
              if len(input_field) >= 2 and input_field[0] == letter:
                continue
              else:
                break
            else:
              print("STOP! Pressionado")
              driver.find_element_by_xpath('//*[@class="bt-yellow icon-exclamation"'
                                           ' or @class="bt-yellow icon-exclamation shake"]'
                                           ).click()
        # Avaliador
        elif button == 'AVALIAR' and validator_type != 'null':
          validate(validator_type, letter)
      except:
        pass

      # Estou pronto:
      try:
        if driver.find_element_by_xpath('//*[@class="bt-yellow icon-exclamation"'
                                        ' or @class="bt-yellow icon-exclamation shake"]/strong'
                                        ).text.upper() == 'ESTOU PRONTO':
          driver.find_element_by_xpath('//*[@class="bt-yellow icon-exclamation"'
                                       ' or @class="bt-yellow icon-exclamation shake"]'
                                       ).click()
      except:
        pass

      # Rank Fim de Round
      try:
        if driver.find_element_by_xpath('//*[@class="active"]//*[@class="trophy"]'):
          round_end_rank()
      except:
        pass

      # AFK Detector:
      try:
        if driver.find_element_by_xpath('//*[@class="alert"]//*[@class="buttons"]/button'):
          time.sleep(2)
          driver.find_element_by_xpath('//*[@class="alert"]//*[@class="buttons"]/button').click()
        elif driver.find_elements_by_xpath('//*[@class="popup-exit popup-exit-active"'
                                           ' or @class="class="popup-enter-done"]'):
          pass
      except:
        pass

      # Rodadas / Jogadores
      match_info()

      time.sleep(3)

  except KeyboardInterrupt:
    cls()
    print("Options:"
          "\n1 - Sair da Sala."
          "\n2 - Fechar o bot.")
    while True:
      try:
        option = int(input("> "))
        if 1 <= option <= 2:
          break
        else:
          print("Opção invalida.")
      except:
        print("Digite um número.")

    if option == 1:
      if driver.find_element_by_xpath('//*[@class="exit"]'):
        driver.find_element_by_xpath('//*[@class="exit"]/.').click()
      print("Deseja entrar em outra sala? (s/n)")
      while True:
        option = input("> ")
        if option.lower() in "sn":
          break
        else:
          print("Opção invalida.")

      if option == 's':
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class="actions"]/button[@class="bt-yellow icon-exclamation"]')))
        time.sleep(1)
        driver.find_element_by_xpath('//*[@class="actions"]/button[@class="bt-yellow icon-exclamation"]/strong').click()
        play_the_game()

      elif option == 'n':
        driver.quit()
        exit()

    elif option == 2:
      quit()


if __name__ == "__main__":
  default_files()
  driver = my_driver()
  while True:
    print("Opções:"
          "\n1 - Entrada Rápida."
          "\n2 - Entrar no Jogo."
          "\n3 - Entrar com ID da Sala."
          "\n4 - Configurações."
          "\n5 - Sair.")
    option = input("> ")
    cls()

    if option == '1':
      driver.get('https://stopots.com.br/')
      username = get_json_setting('username')
      if not 2 <= len(username) <= 15:
        username = ' '
      join_game(username)
      play_the_game()

    elif option == '2':
      while True:
        username = input("Digite um nome: ")
        if 2 <= len(username) <= 15:
          break
        else:
          print("Seu username/nick deve possuir entre 2 e 15 caracteres.")
      driver.get('https://stopots.com.br/')
      join_game(username)
      play_the_game()

    elif option == '3':
      room_id = str(input("ID:"))
      driver.get('https://stopots.com.br/' + room_id)
      join_game(username)
      play_the_game()

    elif option == '4':
      config_json_settings()

    elif option == '5':
      driver.quit()
      exit()
    else:
      print("Opção invalida\n")


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
