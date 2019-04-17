#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import string
import random
import re
import json
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def cls():
  os.system('cls' if os.name == 'nt' else 'clear')

options = Options()
options.headless = False
firefox_capabilities = DesiredCapabilities.FIREFOX
firefox_capabilities['marionette'] = True
driver = webdriver.Firefox(options=options, executable_path='./geckodriver.exe', capabilities=firefox_capabilities)

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

def joinGame(username):
  print("Entrando...")
  wait = WebDriverWait(driver, 10)
  # entrar button
  wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class="login"]/form/button')))
  driver.find_element_by_xpath('//*[@class="login"]/form/button').click()
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

def auto_complete(letter):
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
  except: pass
  current_letter.close()

def matchInfo():
  try:
    rounds = driver.find_element_by_xpath('//*[@class="rounds"]/span').text
    total = driver.find_element_by_xpath('//*[@class="rounds"]/p[2]').text
    print("- Rodadas:", rounds + total,"-")
  except: pass
  print("- Current Players -")
  for x in range(1, 15):
    try:
      nick = driver.find_element_by_xpath('//*[@id="users"]/li['+str(x)+']//*[@class="infos"]/*[@class="nick"]').text
      pts = driver.find_element_by_xpath('//*[@id="users"]/li['+str(x)+']//*[@class="infos"]/span').text
      if nick:
        if not nick == username: print(nick,"-", pts)
        else: print(">",nick,"-",pts)
    except: break

def roundEndRank():
  if driver.find_element_by_xpath('//*[@class="ct ranking" or @class="ct ranking up-enter-done"]//h3').text == 'RANKING DA RODADA':
    print("- Ranking da Rodada -")
    for x in range(1, 15):
      try:
        position = driver.find_element_by_xpath('//*[@class="ct ranking" or @class="ct ranking up-enter-done"]//*[@class="scrollElements"]//li['+str(x)+']//*[@class="position"]/span').text
        nick = driver.find_element_by_xpath('//*[@class="ct ranking" or @class="ct ranking up-enter-done"]//*[@class="scrollElements"]//li['+str(x)+']//*[@class="nick"]').text
        pts = driver.find_element_by_xpath('//*[@class="ct ranking" or @class="ct ranking up-enter-done"]//*[@class="scrollElements"]//li['+str(x)+']//*[@class="points"]').text
        if nick: print(position+"º -",nick,"-",pts)
      except: break
  elif driver.find_element_by_xpath('//*[@class="ct end" or @class="ct end up-enter-done"]//h3').text == 'FIM DE JOGO!' or driver.find_element_by_xpath('//*[@class="ct end" or @class="ct end up-enter-done"]//h4').text == 'RANKING FINAL':
    print("- Fim de Jogo -")
    for x in range(1,3):
      try:
        nick = driver.find_element_by_xpath('//*[@class="ct end" or @class="ct end up-enter-done"]//*[@class="positions"]/div['+str(x)+']/*[@class="nick"]').text
        pts = driver.find_element_by_xpath('//*[@class="ct end" or @class="ct end up-enter-done"]//*[@class="positions"]/div['+str(x)+']/*[@class="points"]').text
        print(str(x)+"º -", nick,"-",pts)
      except: break
  print("")

def validate(type):
  if driver.find_element_by_xpath('//*[@class="bt-yellow icon-exclamation" or @class="bt-yellow icon-exclamation shake"]'):
    if type == 'quick':
      driver.find_element_by_xpath('//*[@class="bt-yellow icon-exclamation" or @class="bt-yellow icon-exclamation shake"]').click()
    elif type == 'deny':
      print("Negando todas as respostas...")
      for x in range(1, 15):
        if driver.find_element_by_xpath('//*[@class="ct validation up-enter-done"]//*[@class="scrollElements"]/label['+str(x)+']/span').text == 'VALIDADO!':
          driver.find_element_by_xpath('//*[@class="ct validation up-enter-done"]//*[@class="scrollElements"]/label['+str(x)+']/div').click()
      driver.find_element_by_xpath('//*[@class="bt-yellow icon-exclamation" or @class="bt-yellow icon-exclamation shake"]').click()
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
        except: continue
      driver.find_element_by_xpath('//*[@class="bt-yellow icon-exclamation" or @class="bt-yellow icon-exclamation shake"]').click()
      current_letter.close()

def playTheGame():
  while True:
    cls()
    try:
      button = driver.find_element_by_xpath('//*[@class= "bt-yellow icon-exclamation" or @class="bt-yellow icon-exclamation shake" or @class="bt-yellow icon-exclamation disable"]/strong').text
      if button == 'STOP!':
        find_letter()
        auto_complete(letter)
      # Avaliador
      if button == 'AVALIAR':
        validate('check')
      # Rank fim de Round
      if driver.find_element_by_xpath('//*[@class="active"]//*[@class="trophy"]'):
        roundEndRank()
      # Estou pronto:
      if driver.find_element_by_xpath('//*[@class="bt-yellow icon-exclamation" or @class="bt-yellow icon-exclamation shake"]'):
        driver.find_element_by_xpath('//*[@class="bt-yellow icon-exclamation" or @class="bt-yellow icon-exclamation shake"]').click()
      # AFK Detector:
      if driver.find_element_by_xpath('//*[@class="alert"]//*[@class="buttons"]/button'):
        time.sleep(2)
        driver.find_element_by_xpath('//*[@class="alert"]//*[@class="buttons"]/button').click()
      elif driver.find_elements_by_xpath('//*[@class="popup-enter-done"]'):
        pass
    except: pass
    matchInfo()
    time.sleep(3)

    '''
    try:
      end = driver.find_element_by_class_name('ct end')
      if end: break
    except: pass
    '''

if __name__ == "__main__":
  print("Options:",
        "\n1 - Entrada Rápida"
        "\n2 - Entrar no Jogo"
        "\n3 - Entrar com ID da Sala "
        "\n4 - Configs"
        "\n5 - Sair")
  option = str(input("> "))

  if option == '1':
    driver.get("https://stopots.com.br/")
    joinGame(username=' ')
    playTheGame()

  elif option == '2':
    username = input("Digite nome: ")
    driver.get("https://stopots.com.br/")
    joinGame(username)
    playTheGame()

  elif option == '3':
    id = str(input("ID:"))
    driver.get("https://stopots.com.br/"+id)
    time.sleep(5)
    playTheGame()

  elif option == '4':
    pass

  elif option == '5':
    exit()

  else: print("Opção invalida")
