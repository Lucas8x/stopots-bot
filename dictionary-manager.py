#!/usr/bin/env python
# -*- coding: utf-8 -*-
# coding: utf8

import os
import string
import json

letters = string.ascii_lowercase
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


def cls():
  os.system('cls' if os.name == 'nt' else 'clear')


def beautify_json():
  with open('dicionario.json', 'r', encoding='utf-8') as x:
    data = x.read()

  data = data.replace('"[', '[').replace(']"', ']').replace("'", '"')

  with open('dicionario.json', 'w', encoding='utf-8') as y:
    y.write(data)


def add_to_json(answer, category):
  letter = answer[0]
  with open('dicionario.json', encoding='utf-8') as dicio:
    dictionary = json.load(dicio)

  if answer not in dictionary[letter][category]:
    dictionary[letter][category].append(answer)
    print(f"Adicionado {answer} ao {category} da letra: {letter}")
  else:
    print("Essa resposta já existe no dicionário.")
    return

  for item in dictionary:
    for cat in dictionary[item]:
      dictionary[item][cat] = str(dictionary[item][cat.lower()])

  with open('dicionario.json', 'w', encoding='utf-8') as j:
    json.dump(dictionary, j, indent=2, separators=(',', ':'), ensure_ascii=False)

  beautify_json()


if __name__ == "__main__":
  while True:
    print("1 - Adicionar Respostas"
          "\n2 - Mostrar Ausentes"
          "\n3 - Sair")
    option = input("> ")
    cls()

    if option == '1':
      print("Digite: 0 para voltar")
      while True:
        category = input("Categoria: ").lower()
        if category.upper() in categories:
          while True:
            answer = input("Resposta: ").lower()
            if answer == '0':
              cls()
              break
            elif answer[0] in letters:
              if len(answer) <= 20:
                add_to_json(answer, category)
              else:
                print("Resposta muito grande max: 20 caracteres")
            else:
              print("Resposta Invalida.")
        elif category == '0':
          cls()
          break
        else:
          print("Essa categoria não existe.")

    elif option == '2':
      letter = input("Letra: ").lower()
      with open('dicionario.json', 'r', encoding='utf-8') as dicio:
        dictionary = json.load(dicio)

      for category in dictionary[letter]:
        if len(dictionary[letter][category]) == 0:
          print(f"Faltando: {category}")
      print("")

    elif option == '3':
      quit()
