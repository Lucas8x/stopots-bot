from stopots_bot.bot import BOT
from stopots_bot.webdriver import init_webdriver
from stopots_bot.dictionary import get_dictionary
from stopots_bot.utils import create_default_files, get_config_setting, cls, open_config_menu, is_a_valid_id, \
  is_a_valid_username

if __name__ == '__main__':
  create_default_files()
  avatar = get_config_setting('avatar')
  validator_type = get_config_setting('validator')
  auto_stop = get_config_setting('autoStop')
  auto_ready = get_config_setting('autoReady')
  use_equivalence = get_config_setting('useEquivalence')
  dictionary = get_dictionary()
  driver = init_webdriver()
  room_id = None

  while True:
    option = input('Opções:\n'
                   '1 - Entrada Rápida.\n'
                   '2 - Entrar no Jogo.\n'
                   '3 - Entrar com ID da Sala.\n'
                   '4 - Configurações.\n'
                   '5 - Sair.\n'
                   '> ')
    cls()

    if option == '1':
      username = get_config_setting('username')
      break

    elif option == '2':
      while True:
        username = input('Digite um nome: ')
        if is_a_valid_username(username):
          break
        else:
          print('Seu username/nick deve possuir entre 2 e 15 caracteres.')
      break

    elif option == '3':
      while True:
        room_input = input('ID: ').strip()
        if is_a_valid_id(room_input):
          room_id = int(room_input)
          break
        else:
          print('Número inválido.')
      username = get_config_setting('username')
      break

    elif option == '4':
      open_config_menu()

    elif option == '5':
      driver.quit()
      exit()
    else:
      print('Opção invalida.\n')

  bot = BOT(username, validator_type, auto_stop, auto_ready, use_equivalence, dictionary, driver)
  bot.join_game(room_id, avatar)
  bot.loop()
