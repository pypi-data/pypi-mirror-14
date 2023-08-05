import utils
from os import environ
from subprocess import call
from termcolor import colored
import fileinput

# list all items
def ls(path, args):
    with open(path) as todo:
        # ls acts as a refresh, so current todo file is reorganized before printing
        utils.reorganize_todo(path)
        for item in todo:
            i = utils.unpack(item)
            print colored(i['num'],'red') + '.' + colored(i['text'], 'white')


# add new item
def a(path, args):
    if len(args) == 1:
        # no specific number is given, append the item to end
        with open(path, 'a') as todo:
            text = args[0]
            todo.write(''.join([text,'\n']))

    elif len(args) == 2 and int(args[0]):
        # insert the item as the given numbered todo
        number, text = args
        index = int(number) - 1
        def insert_item(todo_file):
            contents = todo_file.readlines()
            contents.insert(index, ''.join([text, '\n']))
            return contents
        utils.read_then_write(path, insert_item)

    else:
        print 'not applicable to given arguments'

# edit the current todo file
def e(path, args):
    EDITOR = environ.get('EDITOR', 'vim')
    # add fail check below, invalid EDITOR will err
    call([EDITOR, path])

# delete an item
def d(path, args):
    number = int(args[0])
    if number:
        def delete_item(todo_file):
            contents = todo_file.readlines()
            contents = [l for l in contents if utils.unpack(l)['num'] != number]
            return contents
        utils.read_then_write(path, delete_item)
