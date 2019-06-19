#!/usr/bin/env python
# -*- coding: utf-8 -*-
# coding: utf8

import string
import json

letras = list(string.ascii_lowercase)
categorias = ["ADJETIVO","ANIMAL","APP OU SITE","ATOR","AVE","BANDA","BRINQUEDO",
              "CANTOR","CAPITAL","CARRO","CELEBRIDADE","CEP","CIDADE","COMIDA SAUDÁVEL",
              "COR","DESENHO ANIMADO","DOCE","DOENÇA","ELETRO ELETRÔNICO","ESPORTE",
              "ESPORTISTA","FANTASIA","FILME","FLOR","FLV","FRUTA","GAME","GENTÍLICO",
              "IDIOMA","INGREDIENTE","INSETO","INSTRUMENTO MUSICAL","JLR","LÍQUIDO",
              "MAMÍFERO","MARCA","MEIO DE TRANSPORTE","MSÉ","MÚSICA","NOME FEMININO",
              "NOME MASCULINO","OBJETO","PALAVRA EM ESPANHOL","PALAVRA EM INGLÊS","PAÍS",
              "PCH","PDA","PERSONAGEM FICTÍCIO","PRESENTE","PROFISSÃO","PROGRAMA DE TV",
              "RAÇA DE CACHORRO","REMÉDIO","SABOR DE PIZZA","SABOR DE SORVETE","SOBREMESA",
              "SOBRENOME","SUPER-HERÓI","SÉRIE","TIME ESPORTIVO","VERBO","VESTUÁRIO","VILÃO",
              "FLV"]

def addtojson(answer, categoria):
  letter = answer[0]
  with open('dicionario.json', 'r', encoding='utf-8') as dicio:
    dicionario = json.load(dicio)

  for item in dicionario:
    if item['letter'] == letter:
      if not answer in item['categories'][categoria]:
        item['categories'][categoria].append(answer)
        print("Adicionado a letra:", letter)
        break
      else:
        print("Essa resposta já existe")
        return

  for item in dicionario:
    for cat in categorias:
      item['categories'][cat.lower()] = str(item['categories'][cat.lower()]) #lista para string

  with open('dicionario.json', 'w', encoding='utf-8') as j:
    json.dump(dicionario, j, indent=2, separators=(',', ':'), ensure_ascii=False)

  with open('dicionario.json', 'r', encoding='utf-8') as x:
    data = x.read()

  data = data.replace('"[', '[')
  data = data.replace(']"', ']')
  data = data.replace("'", '"')

  with open('dicionario.json', 'w', encoding='utf-8') as y:
    y.write(data)

if __name__ == "__main__":
  print("1 - Adicionar Respostas"
        "\n2 - Mostrar Ausentes")
  option = str(input("> "))

  if option == '1':
    print("Digite: 0 para encerrar")
    while True:
      categoria = input("Categoria:").lower()
      if categoria.upper() in categorias:
        answer = input("Resposta:").lower()
        if answer == '0':
          break
        elif answer[0] in letras:
          if len(answer) <= 20:
            addtojson(answer, categoria)
          else:
            print("Resposta muito grande max: 20")
        else:
          print("Resposta Invalida")
      elif categoria == '0':
        break
      else:
        print("Essa categoria não existe")

  elif option == '2':
    letter = input("letra:").lower()
    print("Letra:", letter)
    with open('dicionario.json', 'r', encoding='utf-8') as dicio:
      dicionario = json.load(dicio)
    for item in dicionario:
      if item['letter'] == letter:
        for cat in categorias:
          if len(item['categories'][cat.lower()]) == 0:
            print("Faltando:", cat)
        break
      else:
        continue
