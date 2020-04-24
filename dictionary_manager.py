# -*- coding: utf-8 -*-
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


def dictionary_dump(data):
  with open('dictionary.json', 'w', encoding='utf-8') as dictionary_file:
    json.dump(data, dictionary_file, indent=2, separators=(',', ':'), ensure_ascii=False)


def read_dictionary_json():
  with open('dictionary.json', 'r', encoding='utf-8') as dictionary_file:
    return json.load(dictionary_file)


def beautify_json():
  dictionary = read_dictionary_json()
  for item in dictionary:
    for cat in dictionary[item]:
      dictionary[item][cat] = str(dictionary[item][cat.lower()])
  dictionary_dump(dictionary)

  with open('dictionary.json', 'r', encoding='utf-8') as x:
    data = x.read()
  with open('dictionary.json', 'w', encoding='utf-8') as y:
    data2 = data.replace('"[', '[').replace(']"', ']').replace("'", '"')
    y.write(data2)


def category_exists(category):
  dictionary = read_dictionary_json()
  if all(category in dictionary[letter] for letter in dictionary):
    return True


def append_answer(answer, category):
  letter = answer[0]
  dictionary = read_dictionary_json()

  if answer not in dictionary[letter][category]:
    dictionary[letter][category].append(answer)
    print(f'{answer} foi adicionado a {category} da letra: {letter}.')
  else:
    print('Essa resposta já existe.')
    return

  dictionary_dump(dictionary)
  beautify_json()


def delete_answer(answer, category=None):
  letter = answer[0]
  dictionary = read_dictionary_json()

  if category:
    if answer in dictionary[letter][category]:
      dictionary[letter][category].remove(answer)
      print(f'{answer} foi removido de {category} da letra {letter}.')
    else:
      print(f'{answer} não existe em {category}.')
  else:
    for category in dictionary[letter]:
      if answer in dictionary[letter][category]:
        dictionary[letter][category].remove(answer)
        print(f'{answer} foi removido de {category} da letra {letter}.')

  dictionary_dump(dictionary)
  beautify_json()


def append_category(category):
  dictionary = read_dictionary_json()
  if not category_exists(category):
    for letter in dictionary:
      dictionary[letter][category] = []
    dictionary_dump(dictionary)
    beautify_json()


def delete_category(category):
  dictionary = read_dictionary_json()
  for letter in dictionary:
    if category in dictionary[letter]:
      dictionary[letter].pop(category)
  dictionary_dump(dictionary)
  beautify_json()


def missing_answers(letter):
  dictionary = read_dictionary_json()
  for category in dictionary[letter]:
    if len(dictionary[letter][category]) == 0:
      print(f'Faltando: {category}')
  print('')


def main():
  while True:
    option = input('1 - Adicionar Respostas.\n'
                   '2 - Deletar Resposta.\n'
                   '3 - Adicionar Categoria.\n'
                   '4 - Remover Categoria.\n'
                   '5 - Mostrar Ausentes.\n'
                   '6 - Sair.\n'
                   '> ')
    cls()
    print('Digite: 0 para voltar.')

    if option not in ['5', '6']:
      print(f'- {"Adicionando" if option in ["1", "3"] else "Removendo"} '
            f'{"Respostas" if option in ["1", "2"] else "Categoria"} -')
      while True:
        category = input('Categoria: ').lower().strip()
        if category != '0':
          if category_exists(category):
            if option in ['1', '2']:
              while True:
                answer = input('Resposta: ').lower().strip()
                if answer != '0':
                  if option == '1' and len(answer) <= 20:
                    append_answer(answer, category)
                  elif option == '2':
                    delete_answer(answer, category)
                  else:
                    print('Resposta muito grande max: 20 caracteres.')
                else:
                  break
            elif option == '4':
              delete_category(category)
          elif option == '3':
            append_category(category)
          else:
            print('Essa categoria não existe.')
        else:
          break

    elif option == '5':
      while True:
        letter = input('Letra: ').lower().strip()
        if letter != '0':
          missing_answers(letter)
        break

    elif option == '6':
      exit()

    else:
      print('Opção invalida.\n')


if __name__ == "__main__":
  main()
