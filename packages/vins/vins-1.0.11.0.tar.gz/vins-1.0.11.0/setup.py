from setuptools import setup, find_packages

setup(name='vins',
      version='1.0.11.0',
      description='Voice INterfaces Service CLI',
      author='Evgeny Volkov',
      author_email='wolf510@inbox.ru',
      packages = find_packages(),
      install_requires=['click', 'requests'],
      entry_points='''
          [console_scripts]
          vins=vins_cli:cli
      '''
)

