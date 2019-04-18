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
  folder = "./dicionario/"
  with open(folder + letter.lower() + '.json', 'r', encoding='utf-8') as current_letter:
    data = json.load(current_letter)

  for item in data:
    if item['category'].lower() == categoria.lower():
      if not answer.lower() in item['answer']:
        item['answer'].append(answer.lower())
        print("Adicionado a letra:", letter)
      else:
        print("Essa resposta já existe")
        return
  for item in data:
    item['answer'] = str(item['answer']) #lista para string

  with open(folder + letter.lower() + '.json', 'w', encoding='utf-8') as j:
    json.dump(data, j, indent=2, separators=(',', ':'), ensure_ascii=False)

  with open(folder + letter.lower() + '.json', 'r', encoding='utf-8') as x:
    data = x.read()

  data = data.replace('"[', '[')
  data = data.replace(']"', ']')
  data = data.replace("'", '"')

  with open(folder + letter.lower() + '.json', 'w', encoding='utf-8') as y:
    y.write(data)

if __name__ == "__main__":
  print("1 - Adicionar Respostas"
        "\n2 - Mostrar Ausentes")
  option = str(input("> "))

  if option == '1':
    print("Digite: 0 para encerrar")
    while True:
      categoria = input("Categoria:")
      if categoria.upper() in categorias:
        answer = input("Resposta:")
        if answer == '0': break
        addtojson(answer, categoria)
      elif categoria == '0': break
      else: print("Essa categoria não existe")

  elif option == '2':
    letter = input("letra:")
    print("Letra:", letter)
    with open('./dicionario/' + letter.lower() + '.json', 'r', encoding='utf-8') as current_letter:
      data = json.load(current_letter)
    for item in data:
      if len(item['answer']) == 0:
        print("Faltando:", item['category'])
