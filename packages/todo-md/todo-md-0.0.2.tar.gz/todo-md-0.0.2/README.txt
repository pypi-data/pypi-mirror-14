todo manager, backed with actual text files.

installation:
`pip install todo-md`

details:
creates daily todo text files in the preferred directory. naming convention of
the todo files is 'YYYYMMDD.md'. if todays file does not exist, copies most
recent file as today

current todo text file is renumbered after every operation, thus you can mess
with the file without renumbering yourself.



usage:
`todo ls` - list current todos
`todo a <num> <text>` - add new todo to <num>, append to end by default
`todo e` - open current todo text file in your preferred editor
`todo d <num>` - delete <num> todo

