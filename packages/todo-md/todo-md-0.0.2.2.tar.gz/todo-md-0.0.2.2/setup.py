from distutils.core import setup

setup(
    name = 'todo-md',
    version = '0.0.2.2',
    author = 'onur satici',
    author_email = 'onursatici@gmail.com',
    packages = ['todo_md'],
    install_requires = [
        'termcolor'
    ],
    scripts = ['todo'],
    description = 'txt file backed todo manager',
    long_description = open('README.txt').read()
)
