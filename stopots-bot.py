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

def cls():
  os.system('cls' if os.name == 'nt' else 'clear')

def defaultFiles():
  if not (os.path.exists('./config.json')):
    data = {
      "username": "",
      "validator": "check",
      "autoStop": False
    }
    with open('./config.json', 'a+') as x:
      json.dump(data, x, indent=2)

def jsonVariables():
  with open('config.json', 'r') as config:
    data = json.load(config)
    username = data['username']
    validator = data['validator']
    autoStop = data['autoStop']
  config.close()
  return username,validator,autoStop

def configJsonSettings():
  with open('config.json', 'r+') as j:
    data = json.load(j)
    while True:
      print("1 - Mudar username"
            "\n2 - Alterar o validador"
            "\n3 - Auto Stop [ Status:",data['autoStop'],"]"
            "\n0 - Voltar")
      optionToConfig = str(input(">"))
      cls()
      if optionToConfig == '1':
        username = str(input("Username:"))
        data['username'] = username
      elif optionToConfig == '2':
        print("1 - Rápido (apenas aperta em avaliar)"
              "\n2 - Negar - (invalidará todas as respostas inclusive as suas)"
              "\n3 - Avaliar - (avaliara as respostas com base no dicionario e negara as outras"
              "\n4 - Não fazer nada")
        tipo = int(input("> "))
        if tipo == 1:
          data['validator'] = 'quick'
        elif tipo == 2:
          data['validator'] = 'deny'
        elif tipo == 3:
          data['validator'] = 'check'
        elif tipo == 4:
          data['validator'] = 'null'
        else: pass
      elif optionToConfig == '3':
        if data['autoStop']:
          data['autoStop'] = False
          print("Auto Stop Desabilitado")
        elif not data['autoStop']:
          data['autoStop'] = True
          print("Auto Stop Habilitado")
      elif optionToConfig == '0':
        cls()
        break
      else:
        print("Opção invalida\n")
      j.seek(0)
      json.dump(data, j, indent=2)
      j.truncate()

def mydriver():
  global driver
  try:
    firefox_capabilities = DesiredCapabilities.FIREFOX
    firefox_capabilities['marionette'] = True
    driver = webdriver.Firefox(executable_path='./geckodriver.exe', capabilities=firefox_capabilities) #v23
  except:
    try:
      options = webdriver.ChromeOptions()
      options.add_argument("--log-level=3")
      options.add_argument("--silent")
      options.add_argument("--disable-extensions")
      options.add_argument('--disable-popup-blocking')
      driver = webdriver.Chrome('./chromedriver.exe', options=options) #v74
    except:
      print("Instale/Atualize o seu Firefox/Chrome")
      time.sleep(5)
      quit()
  return driver

def joinGame(username):
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
  # jogar button
  wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class="actions"]/button[@class="bt-yellow icon-exclamation"]')))
  time.sleep(1)
  driver.find_element_by_xpath('//*[@class="actions"]/button[@class="bt-yellow icon-exclamation"]/strong').click()
  print("Logado como:", username)

def find_letter():
  global letter
  try:
    letter = driver.find_element_by_xpath('//*[@id="letter"]/span').text
    print("Letra Atual:", letter)
  except: pass

def auto_complete():
  print("Auto Completando...")
  with open('./dicionario/'+letter.lower()+'.json', 'r', encoding='utf-8') as current_letter:
    data = json.load(current_letter)
  try:
    for x in range(1, 13):
      itemType = driver.find_element_by_xpath('//*[@class="ct answers" or @class="ct answers up-enter-done"]//label['+str(x)+']/span').text #TTema do campo
      if itemType.lower() == 'nome': itemType = random.choice(["NOME FEMININO","NOME MASCULINO"])
      for item in data:
        if item['category'].lower() == itemType.lower():
          campo = driver.find_element_by_xpath('//*[@class="ct answers" or @class="ct answers up-enter-done"]//label['+str(x)+']/input').get_attribute('value')
          if campo == '':
            if len(item['answer']) > 0:
              resposta = random.choice(item['answer'])
              driver.find_element_by_xpath('//*[@class="ct answers" or @class="ct answers up-enter-done"]//label['+str(x)+']/input').send_keys(resposta)
          break
  except:
    pass
  current_letter.close()

def matchInfo():
  # Rodadas
  try:
    rounds = driver.find_element_by_xpath('//*[@class="rounds"]/span').text
    total = driver.find_element_by_xpath('//*[@class="rounds"]/p[2]').text
    print("- Rodadas:", rounds + total,"-")
  except:
    pass

  #Jogadores
  print("- Jogadores -")
  for x in range(1, 15):
    try:
      nick = driver.find_element_by_xpath('//*[@id="users"]/li['+str(x)+']//*[@class="infos"]/*[@class="nick"]').text
      pts = driver.find_element_by_xpath('//*[@id="users"]/li['+str(x)+']//*[@class="infos"]/span').text
      if nick:
        global username
        if not nick == username:
          print(nick,"-", pts)
        else:
          print(">",nick,"-",pts)
    except:
      break

def roundEndRank():
  # Ranking da Rodada
  if driver.find_element_by_xpath('//*[@class="ct ranking" or @class="ct ranking up-enter-done"]//h3').text == 'RANKING DA RODADA':
    print("- Ranking da Rodada -")
    for x in range(1, 15):
      try:
        position = driver.find_element_by_xpath('//*[@class="ct ranking" or @class="ct ranking up-enter-done"]//*[@class="scrollElements"]//li['+str(x)+']//*[@class="position"]/span').text
        nick = driver.find_element_by_xpath('//*[@class="ct ranking" or @class="ct ranking up-enter-done"]//*[@class="scrollElements"]//li['+str(x)+']//*[@class="nick"]').text
        pts = driver.find_element_by_xpath('//*[@class="ct ranking" or @class="ct ranking up-enter-done"]//*[@class="scrollElements"]//li['+str(x)+']//*[@class="points"]').text
        if nick:
          if not nick == username:
            print(position+"º -",nick,"-",pts)
          else:
            print(">",position+"º -",nick,"-",pts)
      except:
        break

  # Rank Fim de Jogo (TOP 3)
  elif (driver.find_element_by_xpath('//*[@class="ct end" or @class="ct end up-enter-done"]//h3').text.upper() == 'FIM DE JOGO!') or (driver.find_element_by_xpath('//*[@class="ct end" or @class="ct end up-enter-done"]//h4').text.upper() == 'RANKING FINAL'):
    print("- Fim de Jogo -")
    for x in range(1,3):
      try:
        nick = driver.find_element_by_xpath('//*[@class="ct end" or @class="ct end up-enter-done"]//*[@class="positions"]/div['+str(x)+']/*[@class="nick"]/text()').text
        pts = driver.find_element_by_xpath('//*[@class="ct end" or @class="ct end up-enter-done"]//*[@class="positions"]/div['+str(x)+']/*[@class="points"]/text()').text
        print(str(x)+"º -", nick,"-",pts)
      except:
        break
  print("")

def validate(type):
  if driver.find_element_by_xpath('//*[@class="bt-yellow icon-exclamation" or @class="bt-yellow icon-exclamation shake"]'):
    # Modo Rápido
    if type == 'quick':
      driver.find_element_by_xpath('//*[@class="bt-yellow icon-exclamation" or @class="bt-yellow icon-exclamation shake"]').click()

    # Modo Negação
    elif type == 'deny':
      print("Negando todas as respostas...")
      for x in range(1, 15):
        if driver.find_element_by_xpath('//*[@class="ct validation up-enter-done"]//*[@class="scrollElements"]/label['+str(x)+']/span').text == 'VALIDADO!':
          driver.find_element_by_xpath('//*[@class="ct validation up-enter-done"]//*[@class="scrollElements"]/label['+str(x)+']/div').click()
      driver.find_element_by_xpath('//*[@class="bt-yellow icon-exclamation" or @class="bt-yellow icon-exclamation shake"]').click()

    # Modo Avaliador
    elif type == 'check':
      print("Verificando Respostas...")
      with open('./dicionario/'+letter.lower()+'.json', 'r', encoding='utf-8') as current_letter:
        data = json.load(current_letter)
      categoria = driver.find_element_by_xpath('//*[@class="ct validation up-enter-done"]/div/h3').text
      strCategoria = re.sub('TEMA: ', '', categoria)
      for x in range(1, 15):
        try:
          if driver.find_element_by_xpath('//*[@class="ct validation up-enter-done"]//*[@class="scrollElements"]/label['+str(x)+']/span').text == 'VALIDADO!':
            categoryAnswer = driver.find_element_by_xpath('//*[@class="ct validation up-enter-done"]//*[@class="scrollElements"]/label['+str(x)+']/div').text
            if not any(item['category'].lower() == strCategoria.lower() and categoryAnswer.lower() in item['answer'] for item in data):
              driver.find_element_by_xpath('//*[@class="ct validation up-enter-done"]//*[@class="scrollElements"]/label['+str(x)+']/div').click()
        except:
          continue
      driver.find_element_by_xpath('//*[@class="bt-yellow icon-exclamation" or @class="bt-yellow icon-exclamation shake"]').click()
      current_letter.close()

def playTheGame():
  validatorType = jsonVariables()[1]
  autoStop = jsonVariables()[2]
  try:
    while True:
      cls()
      try:
        button = driver.find_element_by_xpath('//*[@class= "bt-yellow icon-exclamation" or @class="bt-yellow icon-exclamation shake" or @class="bt-yellow icon-exclamation disable"]/strong').text.upper()
        # STOP !
        if button == 'STOP!':
          find_letter()
          auto_complete()
          if autoStop and driver.find_element_by_xpath('//*[@class= "bt-yellow icon-exclamation" or @class="bt-yellow icon-exclamation shake"]'):
            for x in range(1, 13):
              campo = driver.find_element_by_xpath('//*[@class="ct answers" or @class="ct answers up-enter-done"]//label['+str(x)+']/input').get_attribute('value')
              if len(campo) >= 2 and campo[0] == letter:
                continue
              else:
                break
            else:
              print("STOP! Pressionado")
              driver.find_element_by_xpath('//*[@class="bt-yellow icon-exclamation" or @class="bt-yellow icon-exclamation shake"]').click()

        # Avaliador
        if button == 'AVALIAR':
          if validatorType != 'null':
            validate(validatorType)
      except:
        pass

      # Rank Fim de Round
      try:
        if driver.find_element_by_xpath('//*[@class="active"]//*[@class="trophy"]'):
          roundEndRank()
      except:
        pass

      # Estou pronto:
      try:
        if driver.find_element_by_xpath('//*[@class="bt-yellow icon-exclamation" or @class="bt-yellow icon-exclamation shake"]/strong').text.upper() == 'ESTOU PRONTO':
          driver.find_element_by_xpath('//*[@class="bt-yellow icon-exclamation" or @class="bt-yellow icon-exclamation shake"]').click()
      except:
        pass

      # AFK Detector:
      try:
        if driver.find_element_by_xpath('//*[@class="alert"]//*[@class="buttons"]/button'):
          time.sleep(2)
          driver.find_element_by_xpath('//*[@class="alert"]//*[@class="buttons"]/button').click()
        elif driver.find_elements_by_xpath('//*[@class="popup-enter-done"]'):
          pass
      except:
        pass

      matchInfo()

      time.sleep(3)

  except KeyboardInterrupt:
    cls()
    print("Options:"
          "\n1 - Sair da Sala"
          "\n2 - Fechar o bot")
    while True:
      try:
        option = int(input("> "))
        if 1 <= option <= 2:
          break
        else:
          print("Opção invalida")
      except:
        print("Digite um número")

    if option == 1:
      if driver.find_element_by_xpath('//*[@class="exit"]'):
        driver.find_element_by_xpath('//*[@class="exit"]/.').click()
      print("Deseja entrar em outra sala? (s/n)")
      while True:
        option = input("> ")
        if option.lower() in "sn":
          break
        else:
          print("Opção invalida")

      if option == 's':
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class="actions"]/button[@class="bt-yellow icon-exclamation"]')))
        time.sleep(1)
        driver.find_element_by_xpath('//*[@class="actions"]/button[@class="bt-yellow icon-exclamation"]/strong').click()
        playTheGame()

      elif option == 'n':
        driver.quit()
        exit()

    elif option == 2:
      quit()

if __name__ == "__main__":
  defaultFiles()
  driver = mydriver()
  while True:
    print("Opções:"
          "\n1 - Entrada Rápida"
          "\n2 - Entrar no Jogo"
          "\n3 - Entrar com ID da Sala "
          "\n4 - Configs"
          "\n5 - Sair")
    option = input("> ")
    cls()

    if option == '1':
      driver.get("https://stopots.com.br/")
      username = jsonVariables()[0]
      if not 2 <= len(username) <= 15:
        username = ' '
      joinGame(username)
      playTheGame()

    elif option == '2':
      while True:
        username = input("Digite nome: ")
        if 2 <= len(username) <= 15:
          break
        else:
          print("Seu nick deve possuir entre 2 e 15 caracteres")
      driver.get("https://stopots.com.br/")
      joinGame(username)
      playTheGame()

    elif option == '3':
      id = str(input("ID:"))
      driver.get("https://stopots.com.br/" + id)
      joinGame(username)
      playTheGame()

    elif option == '4':
      configJsonSettings()

    elif option == '5':
      driver.quit()
      exit()
    else:
      print("Opção invalida")


'''
categorias = ["ADJETIVO","ANIMAL","APP OU SITE","ATOR","AVE","BANDA","BRINQUEDO",
              "CANTOR","CAPITAL","CARROCELEBRIDADE","CEP","CIDADE","COMIDA SAUDÁVEL",
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