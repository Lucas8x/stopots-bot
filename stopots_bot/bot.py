import itertools
import random
import re
import time
from typing import Dict, Optional

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from stopots_bot.constants import Constants, equivalents
from stopots_bot.utils import cls, is_a_valid_id, is_a_valid_username


class BOT:
  def __init__(self, username: str = None, validator_type: str = 'check', auto_stop: bool = False,
               auto_ready: bool = True, dictionary: Dict = None, driver: webdriver = None):
    self.username = username
    self.validator_type = validator_type
    self.auto_stop = auto_stop
    self.auto_ready = auto_ready
    self.dictionary = dictionary
    self.driver = driver

  def show_game_info(self) -> None:
    try:
      rounds = self.driver.find_element_by_xpath(Constants.rounds).text
      total = self.driver.find_element_by_xpath(Constants.rounds_total).text
      print(f'- Rodadas: {rounds}{total}')
    except NoSuchElementException:
      pass
    except Exception as e:
      print(f'[ERROR]Game Info: {e}')

    print('- Jogadores -')
    for x in range(1, 15):
      try:
        nick = self.driver.find_element_by_xpath(Constants.PlayerList.nick(x)).text
        points = self.driver.find_element_by_xpath(Constants.PlayerList.points(x)).text
        if nick:
          if nick != self.username:
            print(f'{nick} - {points}')
          else:
            print(f'{nick} - {points} < você')
      except NoSuchElementException:
        break
      except Exception as e:
        print(f'[ERROR]Player List: {e}')
        break

  def show_round_end_rank(self) -> None:
    h3_status = self.driver.find_element_by_xpath(Constants.ScorePanel.h3).text.upper()
    if h3_status == 'RANKING DA RODADA':
      print('- Ranking da Rodada -')
      for x in range(1, 15):
        try:
          position = self.driver.find_element_by_xpath(Constants.RankPanel.position(x)).text
          nick = self.driver.find_element_by_xpath(Constants.RankPanel.nick(x)).text
          points = self.driver.find_element_by_xpath(Constants.RankPanel.points(x)).text
          if nick:
            if nick != self.username:
              print(f'{position}º - {nick} - {points}')
            else:
              print(f'{position}º - {nick} - {points} < você')
        except NoSuchElementException:
          break
        except Exception as e:
          print(f'[ERROR]Round End: {e}')

    elif h3_status == 'FIM DE JOGO!' or self.driver.find_element_by_xpath(
            Constants.ScorePanel.h4).text.upper() == 'RANKING FINAL':
      print('- Fim de Jogo -')
      for x in range(1, 4):
        try:
          nick = self.driver.find_element_by_xpath(Constants.ScorePanel.nick(x)).text
          points = self.driver.find_element_by_xpath(Constants.ScorePanel.points(x)).text
          print(f'{x}º - {nick} - {points}')
        except NoSuchElementException:
          break
        except Exception as e:
          print(f'[ERROR]Game End: {e}')
          break
    print('')

  def join_game(self, room_id: Optional[int] = None, avatar_id: Optional[int] = 0) -> None:
    print('Entrando no jogo...')
    self.driver.get(f'{Constants.url}{room_id if room_id else ""}')
    wait = WebDriverWait(self.driver, 10)

    # entre anônimo
    wait.until(ec.presence_of_element_located((By.XPATH, Constants.enter_button)))
    # wait.until(ec.element_to_be_clickable((By.XPATH, Constants.enter_button)))
    self.driver.find_element_by_xpath(Constants.enter_button).click()
    wait.until(ec.invisibility_of_element_located((By.XPATH, Constants.loading_animation)))
    # wait.until(ec.NoSuchElementException((By.XPATH, Constants.loading_animation)))

    print(f'Entrando na sala {room_id if room_id else ""}...')
    # username
    user_input = Constants.username_input if not room_id else Constants.username_input2
    wait.until(ec.presence_of_element_located((By.XPATH, user_input)))
    if self.username is not None and is_a_valid_username(self.username):
      self.driver.find_element_by_xpath(user_input).clear()
      self.driver.find_element_by_xpath(user_input).send_keys(self.username)
    else:
      self.username = self.driver.find_element_by_xpath(user_input).get_attribute('value')

    # Avatar
    if 1 <= avatar_id <= 36:
      time.sleep(2)
      # Botão edit => abre menu avatar
      wait.until(ec.element_to_be_clickable((By.XPATH, Constants.avatar_edit_button)))
      self.driver.find_element_by_xpath(Constants.avatar_edit_button).click()

      # Icone do Avatar
      if avatar_id > 14:
        self.driver.execute_script('arguments[0].scrollIntoView(true);',
                                   self.driver.find_element_by_xpath(Constants.avatar(avatar_id)))
      wait.until(ec.element_to_be_clickable((By.XPATH, Constants.avatar(avatar_id))))
      self.driver.find_element_by_xpath(Constants.avatar(avatar_id)).click()

      # Botão confirmar escolha
      wait.until(ec.element_to_be_clickable((By.XPATH, Constants.avatar_confirm_button)))
      self.driver.find_element_by_xpath(Constants.avatar_confirm_button).click()

      # Esperar a animação
      wait.until(ec.invisibility_of_element_located((By.XPATH, Constants.fade_animation)))
    time.sleep(2)

    # Botão Jogar => entra no jogo
    play_button = Constants.play_button if not room_id else Constants.play_button2
    wait.until(ec.element_to_be_clickable((By.XPATH, play_button)))
    time.sleep(2)
    self.driver.find_element_by_xpath(play_button).click()

    print(f'Logado como: {self.username}')

  def find_letter(self) -> Optional[str]:
    try:
      letter = self.driver.find_element_by_xpath(Constants.letter).text.lower()
      print(f'Letra Atual: {letter if letter else "?"}')
      return letter
    except NoSuchElementException:
      return None
    except Exception as e:
      print(f'[ERROR]Find letter: {e}', e.__class__.__name__)
      return None

  def get_answer(self, letter: str, category: str) -> Optional[str]:
    try:
      return random.choice(self.dictionary[letter][category]).lower()
    except IndexError:
      return None
    except Exception as e:
      print(f'[ERROR]Get answer: {e}')
      return None

  def auto_complete(self, letter: str) -> None:
    print('Auto Completando...')
    for x in range(1, 13):
      try:
        field_input = self.driver.find_element_by_xpath(Constants.FormPanel.field_input(x)).get_attribute('value')
        if not field_input:
          field_category = self.driver.find_element_by_xpath(Constants.FormPanel.field_category(x)).text.lower()

          if field_category in equivalents:
            field_category = random.choice([field_category, *equivalents[field_category]] if field_category != 'nome'
                                           else [*equivalents[field_category]])

          answer = self.get_answer(letter, field_category)
          if answer:
            self.driver.find_element_by_xpath(Constants.FormPanel.field_input(x)).send_keys(answer)
      except NoSuchElementException:
        continue
      except Exception as e:
        print(f'[ERROR]Auto Complete: {e}', e.__class__.__name__)

  def validate(self, letter: str) -> None:
    if self.driver.find_element_by_xpath(Constants.yellow_button_clickable):
      if self.validator_type == 'quick':
        self.driver.find_element_by_xpath(Constants.yellow_button_clickable).click()

      elif self.validator_type == 'deny':
        print('Negando todas as respostas...')
        for x in range(1, 15):
          if self.driver.find_element_by_xpath(Constants.AnswerPanel.label_status(x)).text.upper() == 'VALIDADO!':
            self.driver.find_element_by_xpath(Constants.AnswerPanel.label_clickable(x)).click()
        self.driver.find_element_by_xpath(Constants.yellow_button_clickable).click()

      elif self.validator_type == 'accept':
        print('Confirmando todas as respostas...')
        for x in range(1, 15):
          if self.driver.find_element_by_xpath(Constants.AnswerPanel.label_report(x)).text.upper() == 'DENUNCIAR':
            Constants.AnswerPanel.label_clickable(x)
        self.driver.find_element_by_xpath(Constants.yellow_button_clickable).click()

      elif self.validator_type == 'check':
        print('Avaliando Respostas...')
        category = self.driver.find_element_by_xpath(Constants.AnswerPanel.category).text
        category = re.sub('TEMA: ', '', category).lower()
        for x in range(1, 15):
          try:
            if self.driver.find_element_by_xpath(Constants.AnswerPanel.label_status(x)).text.upper() == 'VALIDADO!':
              category_answer = self.driver.find_element_by_xpath(Constants.AnswerPanel.label_category(x)).text.lower()

              if category in equivalents:
                equivalent_answers = [self.dictionary[letter][category] if category != 'nome' else []] + \
                                     [self.dictionary[letter][cat] for cat in equivalents[category]]
                if category_answer not in list(itertools.chain(*equivalent_answers)):
                  self.driver.find_element_by_xpath(Constants.AnswerPanel.label_clickable(x)).click()
              elif category_answer not in self.dictionary[letter][category]:
                self.driver.find_element_by_xpath(Constants.AnswerPanel.label_clickable(x)).click()

          except Exception as e:
            continue
        self.driver.find_element_by_xpath(Constants.yellow_button_clickable).click()

      elif self.validator_type == 'greedy':
        pass

  def do_stop(self, letter: str) -> None:
    if self.driver.find_element_by_xpath(Constants.yellow_button_clickable):
      for x in range(1, 13):
        input_field = self.driver.find_element_by_xpath(Constants.FormPanel.field_input(x))\
          .get_attribute('value').lower()
        if not input_field[0] == letter and len(input_field) >= 2:
          break
      else:
        print('STOP! Pressionado.')
        self.driver.find_element_by_xpath(Constants.yellow_button_clickable).click()

  def loop(self) -> None:
    try:
      while True:
        cls()
        try:
          letter = self.find_letter()
          if letter:
            button = self.driver.find_element_by_xpath(Constants.yellow_button).text.upper()
            if button == 'STOP!':
              self.auto_complete(letter)
              if self.auto_stop:
                self.do_stop(letter)
            elif button == 'AVALIAR' and self.validator_type != 'null':
              self.validate(letter)
        except NoSuchElementException:
          pass
        except Exception as e:
          print(f'[ERROR]BLOCK1: {e}', e.__class__.__name__)

        try:
          if self.auto_ready and self.driver.find_element_by_xpath(Constants.ready_button).text.upper() == 'ESTOU PRONTO':
            self.driver.find_element_by_xpath(Constants.yellow_button_clickable).click()
        except NoSuchElementException as e:
          pass
        except Exception as e:
          print(f'[ERROR]BLOCK2: {e}', e.__class__.__name__)

        try:
          if self.driver.find_element_by_xpath(Constants.trophy):
            self.show_round_end_rank()
        except NoSuchElementException:
          pass
        except Exception as e:
          print(f'[ERROR]BLOCK3: {e}', e.__class__.__name__)

        try:
          if self.driver.find_element_by_xpath(Constants.afk_button_xpath):
            time.sleep(2)
            self.driver.find_element_by_xpath(Constants.afk_button_xpath).click()
          elif self.driver.find_elements_by_xpath(Constants.afk_box):
            pass
        except NoSuchElementException:
          pass
        except Exception as e:
          print(f'[ERROR]BLOCK4: {e}', e.__class__.__name__)

        self.show_game_info()
        time.sleep(3)

    except KeyboardInterrupt:
      cls()
      print('Options:\n'
            '1 - Sair da Sala.\n'
            '2 - Fechar o bot.')
      while True:
        end_option = input('> ').strip()
        if is_a_valid_id(end_option):
          end_option = int(end_option)
        else:
          print('Opção invalida.')
        break

      if end_option == 1:
        if self.driver.find_element_by_xpath(Constants.exit):
          self.driver.find_element_by_xpath(f'{Constants.exit}/.').click()
        print('Deseja entrar em outra sala? (s/n)')
        while True:
          rejoin_input = input('> ')
          if rejoin_input.strip().lower() in 'sn':
            break
          else:
            print('Opção invalida.')

        if rejoin_input == 's':
          wait = WebDriverWait(self.driver, 10)
          wait.until(ec.presence_of_element_located((By.XPATH, Constants.play_button)))
          time.sleep(1)
          self.driver.find_element_by_xpath(Constants.play_button_clickable).click()
          self.loop()

        elif rejoin_input == 'n':
          self.driver.quit()
          exit()

      elif end_option == 2:
        quit()
