
filename = 'code.sql'
lines = tuple(open(filename, 'r'))  # read the file line by line into array
sqlcode = ''
for line in lines:
    sqlcode += re.sub(r'--.*?\n', '', line + '\n')  # remove the in-line comments

orders = sqlcode.split(';') # split the text into commands

# Create the database and execute the commands
for order in orders:
    try:
        sql = strip_non_ascii(order) + ';'
        cursor.execute(sql)
    except:
        print('Error:\n', sql, '\n\n')
