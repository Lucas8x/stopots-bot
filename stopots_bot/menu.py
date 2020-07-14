from stopots_bot.bot import BOT, init_web_driver
from stopots_bot.dictionary import get_dictionary
from stopots_bot.utils import create_default_files, get_config_setting, cls, open_config_menu

if __name__ == "__main__":
  create_default_files()
  avatar = get_config_setting('avatar')
  validator_type = get_config_setting('validator')
  auto_stop = get_config_setting('autoStop')
  auto_ready = get_config_setting('autoReady')
  dictionary = get_dictionary()
  driver = init_web_driver()
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
        username = input('Digite um nome: ').strip()
        if 2 <= len(username) <= 15:
          break
        else:
          print('Seu username/nick deve possuir entre 2 e 15 caracteres.')

    elif option == '3':
      while True:
        try:
          room_input = input('ID: ').strip()
          if isinstance(int(room_input), int):
            room_id = int(room_input)
            break
        except Exception as e:
          print('Número invalido')
      username = get_config_setting('username')
      break

    elif option == '4':
      open_config_menu()

    elif option == '5':
      driver.quit()
      exit()
    else:
      print('Opção invalida\n')

  bot = BOT(username, validator_type, auto_stop, auto_ready, dictionary, driver)
  bot.join_game(room_id, avatar)
  bot.loop()
