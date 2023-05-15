from env import AWS_sql_creds

mydb = AWS_sql_creds()

command = mydb.cursor()

command.execute("show databases")

