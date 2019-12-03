#!/usr/bin/env python
# -*- coding: utf-8 -*-
# coding: utf8

import string
import json

letters = list(string.ascii_lowercase)
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


def add_to_json(answer, category):
  letter = answer[0]
  with open('dicionario.json', encoding='utf-8') as dicio:
    dictionary = json.load(dicio)

  if answer not in dictionary[letter][category]:
    dictionary[letter][category].append(answer)
    print(f"Adicionado {answer} a {category} da letra: {letter}")
  else:
    print("Essa resposta já existe no dicionário")
    return

  for item in dictionary:
    for cat in dictionary[item]:
      dictionary[item][cat] = str(dictionary[item][cat.lower()])

  with open('dicionario.json', 'w', encoding='utf-8') as j:
    json.dump(dictionary, j, indent=2, separators=(',', ':'), ensure_ascii=False)

  with open('dicionario.json', 'r', encoding='utf-8') as x:
    data = x.read()

  data = data.replace('"[', '[')
  data = data.replace(']"', ']')
  data = data.replace("'", '"')

  with open('dicionario.json', 'w', encoding='utf-8') as y:
    y.write(data)


if __name__ == "__main__":
  print("1 - Adicionar Respostas"
        "\n2 - Mostrar Ausentes"
        "\n3 - Sair")
  option = str(input("> "))

  if option == '1':
    print("Digite: 0 para encerrar")
    while True:
      category = input("Categoria: ").lower()
      if category.upper() in categories:
        answer = input("Resposta: ").lower()
        if answer == '0':
          break
        elif answer[0] in letters:
          if len(answer) <= 20:
            add_to_json(answer, category)
          else:
            print("Resposta muito grande max: 20")
        else:
          print("Resposta Invalida")
      elif category == '0':
        break
      else:
        print("Essa categoria não existe")

  elif option == '2':
    letter = input("Letra: ").lower()
    print(f"Letra: {letter}")
    with open('dicionario.json', 'r', encoding='utf-8') as dicio:
      dictionary = json.load(dicio)

    for category in dictionary[letter]:
      if len(dictionary[letter][category]) == 0:
        print(f"Faltando: {category}")
  elif option == '3':
    quit()
