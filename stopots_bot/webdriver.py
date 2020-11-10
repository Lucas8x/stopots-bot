from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from stopots_bot.utils import cls


def init_chromedriver() -> webdriver:
  """
  Inicializa o chromedriver.
  :return: webdriver chrome
  """
  options = webdriver.ChromeOptions()
  options.add_experimental_option('excludeSwitches', ['enable-logging'])
  chrome_args = ['--log-level=3', '--silent', '--disable-extensions', '--disable-popup-blocking',
                 '--disable-blink-features', '--disable-blink-features=AutomationControlled']
  for arg in chrome_args:
    options.add_argument(arg)
  chromedriver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
  cls()
  return chromedriver


def init_geckodriver() -> webdriver:
  """
  Inicializa o geckodriver.
  :return: webdriver geckodriver
  """
  firefox_capabilities = DesiredCapabilities.FIREFOX
  firefox_capabilities['marionette'] = True
  geckodriver = webdriver.Firefox(executable_path=GeckoDriverManager().install(),
                                  capabilities=firefox_capabilities)
  cls()
  return geckodriver


def init_webdriver(name: str = 'chrome') -> webdriver:
  """
  Inicializa o webdriver (padrão = 'chrome')
  :param name: nome do webdriver
  :return: webdriver
  """
  try:
    return init_chromedriver() if name == 'chrome' else init_geckodriver()
  except Exception as e:
    print(f'Failed to initialize the webdriver\nError: {e}')
    quit()
