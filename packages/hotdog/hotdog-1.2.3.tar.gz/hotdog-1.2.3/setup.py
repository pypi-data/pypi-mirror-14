from distutils.core import setup
setup(
  name = 'hotdog',
  packages = ['hotdog'],
  version = '1.2.3',
  description = 'Appium/Selenium testing framework deriving from unittest',
  author = 'Matt Watson',
  author_email = 'Watson.Mattc@gmail.com',
  url = 'https://github.com/Mattwhooo/Hotdog',
  download_url = 'https://github.com/Mattwhooo/Hotdog/tarball/1.2.3',
  keywords = ['appium', 'selenium', 'testing'],
  classifiers=[],
  install_requires=['webium', 'testtools','beautifulsoup4','Appium-Python-Client', 'requests', 'sauceclient', 'timeout-decorator', 'appium_selector']
)