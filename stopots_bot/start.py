from stopots_bot.command_line import command_line
from stopots_bot.bot import BOT
from stopots_bot.dictionary import get_dictionary
from stopots_bot.webdriver import init_webdriver


def start() -> None:
  args = command_line()
  dictionary = get_dictionary()
  driver = init_webdriver(args.webdriver)

  bot = BOT(args.username, args.validator, args.auto_stop, args.auto_ready, dictionary, driver)
  bot.join_game(args.room_id, args.avatar)
  bot.loop()
