#!/usr/bin/env python
# -*- coding: utf-8 -*-
# coding: utf8

import string
import json

letras = list(string.ascii_lowercase)
categorias = ["Adjetivo","Animal","App ou site","Ator","Banda","Cantor","Carro","Capital","Celebridade","CEP","Cidade",
              "Comida","Cor","Desenho animado","Eletro Eletrônico","Esporte","Esportista","Filme","Flor","FLV","Fruta",
              "Game","Gentílico","Inseto","Instrumento Musical","JLR","Líquido","Marca","Música","MSÉ","Nome Feminino",
              "Nome Masculino","Objeto","País","Palavra em inglês","PCH","PDA","Personagem Fictício","Profissão",
              "Programa de TV","Série","Sobremesa","Sobrenome","Time Esportivo","Verbo","Vestuário",
              "Nome","Gentílico","Super-Herói","Meio de Transporte","Idioma","Doce"]

def addtojson(answer,categoria):
  letter = answer[0]
  x = {
    "answer":answer.lower(),
    "category":categoria.lower()
  }
  with open('./dicionario/'+letter.lower()+'.json', 'r', encoding='utf-8') as j:
    data = json.load(j)
  with open('./dicionario/'+letter.lower()+'.json', 'w', encoding='utf-8') as j:
    data.append(x)
    j.seek(0)
    json.dump(data, j, indent=2, separators=(',', ':'), ensure_ascii=False)
    j.truncate()
  print("Adicionado a letra:", letter)

if __name__ == "__main__":
  option = str(input("> "))

  if option == '1':
    while True:
      categoria = input("Categoria:")
      answer = input("Answer:")
      if categoria == '0' or answer == '0': break
      addtojson(answer, categoria)

  if option == '2':
    pass


