from time import strftime
from os import path, listdir
from shutil import copyfile

def get_todo_path(directory):
    today = strftime('%Y%m%d')
    todo_path = directory + '/'+ today + '.md'

    # if today's todo.md does not exist, create the file
    if not path.isfile(todo_path):
        previous_todo_file = check_previous_todo(directory)

        if not previous_todo_file:
            # create an empty file
            open(todo_path, 'w')
        else:
            # copy previous days todos to todays todo.md
            copyfile(directory + '/' + previous_todo_file, todo_path)

    return todo_path

def check_previous_todo(directory):
    # get all todo.md's filtering all hidden files
    todos = [t for t in listdir(directory) if t[0] != '.']
    todos.sort()
    if(len(todos)):
        return todos[-1]
    else:
        return False

def reorganize_todo(file_path):
    def organize(todo_file):
        organized =[]
        current_line_number = 1
        for line in todo_file.readlines():
            # TODO: check is below is a nice way of doing this
            line_list = line.split('.',1)
            if len(line_list) == 2 and line_list[0].isdigit():
                [number,text] = line_list
                text = text.lstrip()
            else:
                text = ''.join(line_list)

            if not text.isspace():
                organized.append(''.join([str(current_line_number), '. ', text]))
                current_line_number = current_line_number + 1
        return organized
    read_then_write(file_path, organize)

def unpack(item):
    item_list = item.rstrip().split('.',1)
    res = {}
    res['num'] = int(item_list[0])
    res['text'] = item_list[1]
    return res

def read_then_write(path, fn_to_read):
    with open(path, 'r') as f:
        new_contents = fn_to_read(f)
        with open(path, 'w') as f_write:
            f_write.writelines(new_contents)

