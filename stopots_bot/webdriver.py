import time

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def init_webdriver():
  try:
    firefox_capabilities = DesiredCapabilities.FIREFOX
    firefox_capabilities['marionette'] = True
    geckodriver = webdriver.Firefox(executable_path='geckodriver.exe', capabilities=firefox_capabilities)  # v23
    return geckodriver
  except Exception as e:
    print(f'Falha ao iniciliazar o geckodriver: {e}Tentando com o chromedriver...')
    try:
      options = webdriver.ChromeOptions()
      options.add_experimental_option('excludeSwitches', ['enable-logging'])
      chrome_args = ['--log-level=3', '--silent', '--disable-extensions', '--disable-popup-blocking',
                     '--disable-blink-features', '--disable-blink-features=AutomationControlled']
      for arg in chrome_args:
        options.add_argument(arg)
      chromedriver = webdriver.Chrome('chromedriver.exe', options=options)  # v83.0.4103.39
      return chromedriver
    except Exception as e:
      print(f'Falha ao inicializar o chromedriver: {e}')
      print('Instale/Atualize o seu Firefox/Chrome e/ou Geckodriver/Chromedriver na pasta.')
      time.sleep(5)
      quit()
