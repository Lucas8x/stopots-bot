# -*- coding: utf-8 -*-
import json
import string
from pathlib import Path

from stopots_bot.utils import cls

alphabet = string.ascii_lowercase


def get_dictionary() -> dict:
  """
  Carrega o json do dicionário.
  :return: dicionário
  """
  try:
    dict_path = Path.joinpath(Path(__file__).parent, 'dictionary.json')
    with open(dict_path, encoding='utf-8') as dictionary_data:
      return json.load(dictionary_data)
  except Exception as e:
    print(f'Failed to initialize the dictionary, error: {e}')
    return {"error": f"failed to initialize the dictionary, error: {e}"}


class Dictionary:
  """Classe do dicionário."""
  def __init__(self, data: dict = None):
    self.data = data

  def load(self) -> None:
    """Carrega o dicionario no atributo data da classe."""
    data = get_dictionary()
    if 'error' in data:
      quit()
    self.data = data

  def save(self) -> None:
    """Salva o atributo data para o arqivo json."""
    with open('dictionary.json', 'w', encoding='utf-8') as dictionary_file:
      json.dump(self.data, dictionary_file, indent=2, separators=(',', ':'), ensure_ascii=False)

  def beautify_json(self) -> None:
    """Transforma os array em linhas."""
    for letter in self.data:
      for category in self.data[letter]:
        self.data[letter][category] = str(self.data[letter][category.lower()])
    self.save()
    with open('dictionary.json', encoding='utf-8') as x:
      data = x.read()
    with open('dictionary.json', 'w', encoding='utf-8') as y:
      data2 = data.replace('"[', '[').replace(']"', ']').replace("'", '"')
      y.write(data2)

  def category_exists(self, category: str) -> bool:
    """
    Verifica se a categoria existe em todas as letras.
    :param category: categoria
    :return: True/False
    """
    return all(category in self.data[letter] for letter in self.data)

  def add_answer(self, answer: str, category: str) -> None:
    """
    Adiciona uma resposta a uma categoria
    :param answer: resposta
    :param category: categoria
    """
    letter = answer[0]
    if answer in self.data[letter][category]:
      print('Essa resposta já existe.')
      return
    self.data[letter][category].append(answer)
    print(f'{answer} foi adicionado a {category} da letra: {letter}.')
    self.save()
    self.beautify_json()

  def delete_answer(self, answer: str, category: str = None) -> None:
    """
    Deleta uma resposta de uma categoria.
    :param answer: resposta
    :param category: categoria
    """
    letter = answer[0]
    if category:
      if answer in self.data[letter][category]:
        self.data[letter][category].remove(answer)
        print(f'{answer} foi removido de {category} da letra {letter}.')
      else:
        print(f'{answer} não existe em {category}.')
    else:
      for category in self.data[letter]:
        if answer in self.data[letter][category]:
          self.data[letter][category].remove(answer)
          print(f'{answer} foi removido de {category} da letra {letter}.')
    self.save()
    self.beautify_json()

  def add_category(self, category: str) -> None:
    """
    Adiciona uma categoria em todas as letras.
    :param category: categoria
    """
    for letter in self.data:
      if not self.data[letter].get(category):
        self.data[letter][category] = []
    print(f'Categoria: {category} adicionada ao dicionário.')
    self.save()
    self.beautify_json()

  def delete_category(self, category: str) -> None:
    """
    Deleta uma categoria e suas respostas.
    :param category: categoria
    """
    for letter in self.data:
      if category in self.data[letter]:
        self.data[letter].pop(category)
    print(f'Categoria: {category} apagada do dicionário.')
    self.save()
    self.beautify_json()

  def missing_answers(self, letter: str) -> None:
    """
    Mostra as categorias que estão sem respostas.
    :param letter: letra
    """
    for category in self.data[letter]:
      if not len(self.data[letter][category]):
        print(f'Faltando: {category}')
    print('')


def name_answer_genre() -> str:
  """
  Menu para definir a categoria de um nome, adicionando mais possibilidades ao bot.
  :return: categoria
  """
  while True:
    answer_genre = int(input('Esse nome é feminino ou masculino?\n'
                             '1 - Feminino\n'
                             '2 - Masculino\n'
                             '3 - Neutro (caso tenha adicionado categoria nome)\n'
                             '> '))
    if answer_genre not in range(1, 4):
      print('\033[31mDigite um número válido.\n\033[m')
      continue
    return {
      1: 'nome feminino',
      2: 'nome masculino',
      3: 'nome'
    }[answer_genre]


def dictionary_menu() -> None:
  """Abre o menu do dicionário"""
  dictionary = Dictionary()
  dictionary.load()
  while True:
    option = input('1 - Adicionar Resposta.\n'
                   '2 - Remover Resposta.\n'
                   '3 - Adicionar Categoria.\n'
                   '4 - Remover Categoria.\n'
                   '5 - Mostrar Ausentes.\n'
                   '6 - Sair.\n'
                   '> ')
    cls()
    print('Digite: 0 para voltar.\n')

    if option.isdigit():
      option = int(option)
      if option in range(1, 5):
        print(f'- {"Adicionando" if option in [1, 3] else "Removendo"} '
              f'{"Respostas" if option in [1, 2] else "Categoria"} -')
        while True:
          category = input('Categoria: ').strip().lower()
          if category != '0':
            if category == 'nome' and option == 1:
              category = name_answer_genre()
            if dictionary.category_exists(category):
              if option in [1, 2]:
                while True:
                  answer = input('Resposta: ').strip().lower()
                  if answer != '0':
                    if option == 1:
                      if len(answer) <= 20:
                        dictionary.add_answer(answer, category)
                      else:
                        print('\033[31mResposta muito grande max: 20 caracteres.\033[m')
                    elif option == 2:
                      dictionary.delete_answer(answer, category)
                  else:
                    cls()
                    break
              elif option == 4:
                dictionary.delete_category(category)
            elif option == 3:
              dictionary.add_category(category)
            else:
              print('\033[31mEssa categoria não existe.\033[m')
          else:
            cls()
            break
      elif option == 5:
        while True:
          letter = input('Letra: ').strip().lower()
          if letter in alphabet:
            dictionary.missing_answers(letter)
          break
      elif option == 6:
        exit()
      else:
        cls()
        print('\033[31mOpção inválida.\n\033[m')
    else:
      cls()
      print('\033[31mDigite um número.\n\033[m')


if __name__ == '__main__':
  dictionary_menu()
