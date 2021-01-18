import argparse
from typing import Optional

from stopots_bot.dictionary import dictionary_menu
from stopots_bot.utils import is_a_valid_username, is_a_valid_id


def command_line() -> Optional[argparse.Namespace]:
  """
  Define a interface da linha de comando.
  :return: argumentos enviados
  """
  parser = argparse.ArgumentParser(prog='Stopots Bot', description='auto play stopots')

  # user args
  parser.add_argument('--user', '-u', dest='username', action='store', default=None, help='seu username')
  parser.add_argument('--avatar', '-a', dest='avatar', action='store', type=int, default=0, help='número do avatar')
  parser.add_argument('--room', '-r', dest='room_id', action='store', type=int, help='número da sala')

  # bot args
  parser.add_argument('--auto-stop', dest='auto_stop', action='store_true', default=False,
                      help='habilita stop automático')
  parser.add_argument('--auto-ready', dest='auto_ready', action='store_true', default=True,
                      help='habilita ready automático')
  parser.add_argument('--validator', dest='validator', action='store', default='check',
                      choices=['quick', 'deny', 'accept', 'check', 'null'], help='tipo do avaliador')
  parser.add_argument('--use-equiv', dest='use_equivalence', action='store_true', default=True,
                      help='habilita respostas equivalentes')

  # driver
  parser.add_argument('--driver', dest='webdriver', action='store', default='chrome',
                      choices=['chrome', 'firefox'], help='seu navegador')

  # dictionary
  parser.add_argument('--dict', dest='open_dictionary', action='store_true', default=False,
                      help='abre o menu do dicionário')

  args = parser.parse_args()

  if args.open_dictionary:
    dictionary_menu()
    return

  if args.username and not is_a_valid_username(args.username):
    print('Seu username/nick deve possuir entre 2 e 15 caracteres.')
    quit()

  if args.room_id and not is_a_valid_id(args.room_id):
    print('Esse número da sala não é válido.')
    quit()

  if not 0 <= args.avatar <= 36:
    print('Avatar não válido.\nMin: 0 Max: 36')
    quit()

  return args


if __name__ == '__main__':
  command_line()
