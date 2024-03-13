from setuptools import setup, find_namespace_packages

setup(name='console_bot',
      version='1.0.0',
      description='Turn your terminal into a powerful assistant with console_bot!',
      url='https://github.com/Swingyboy/goitneo-python-hw-3-group-2',
      author='UnicornLabs',
      author_email='support@unicornlabs.com',
      license='MIT',
      packages=find_namespace_packages(),
      install_requires=[
          'prettytable==3.10.0',
          'wcwidth==0.2.13',
      ]
)
