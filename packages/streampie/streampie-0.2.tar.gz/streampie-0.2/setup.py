from distutils.core import setup

with open('requirements.txt') as f:
   required = f.read().splitlines()

setup(
   name = "streampie",
   py_modules = ["streampie"],
   version = '0.2',
   description = 'A simple, parallel stream processing library',
   author = 'Luka Malisa',
   author_email = 'luka.malisha@gmail.com',
   url = 'https://github.com/malisal/streampie',
   keywords = ['stream', 'parallel', 'distributed'],
   platforms=['any'],
   classifiers = [],
   install_requires=required,
)

