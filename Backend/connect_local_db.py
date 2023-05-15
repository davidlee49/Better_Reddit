from env import *
import collections
import json
import time


connection = mysql_connector()
cursor = connection.cursor()


def show_databases():
    # Execute the SQL query to show databases
    cursor.execute("SHOW DATABASES")
    # Fetch all the rows
    databases = cursor.fetchall()

    # Print the list of databases
    for database in databases:
        print(database[0])

def create_table_v1():
    # Define the SQL statement to create the schema
    create_schema_query = """
    CREATE TABLE reddit_posts (
        score INT,
        url_id VARCHAR(255) PRIMARY KEY,
        epoch INT,
        author VARCHAR(255),
        subreddit VARCHAR(255)
    )
    """

    # Execute the SQL query to create the schema
    cursor.execute(create_schema_query)

    # Commit the changes to the database
    connection.commit()

def create_table_v3():
    # NOTE: we are putting the majority of the post data into a JSON blob(score, url, and author)
    # NOTE: additionally, we are going to make the sub and date the primary key
    create_schema_query = """
    CREATE TABLE reddit_posts_v3 (
        epoch INT,
        subreddit VARCHAR(255),
        post_data JSON
    )
    """

    # Execute the SQL query to create the schema
    cursor.execute(create_schema_query)

    # Commit the changes to the database
    connection.commit()

def create_database():
    # Define the SQL statement to create the database
    create_database_query = "CREATE DATABASE reddit_posts"

    # Execute the SQL query to create the database
    cursor.execute(create_database_query)


def show_tables():
    # Execute the SQL query to show tables
    cursor.execute("SHOW TABLES")

    # Fetch all the rows
    tables = cursor.fetchall()

    # Print the list of tables
    for table in tables:
        print(table[0])

def show_table_data():
    start_time = time.time()
    cursor.execute("SELECT * FROM reddit_posts_v5")

    # Fetch all the rows
    rows = cursor.fetchall()
    subreddits = collections.Counter()

    # Print the data
    count = 0
    for row in rows:
        count += 1
        subreddits[row[1]] += 1
        print(row)
    elapsed_time = time.time() - start_time
    # print(subreddits)
    print(elapsed_time, count)


def insert_data(data):
    insert_data_query = """
    INSERT INTO reddit_posts (score, url_id, epoch, author, subreddit)
    VALUES (%s, %s, %s, %s, %s)
    """

    cursor.executemany(insert_data_query, data)
    connection.commit()



def insert_row(data):
    insert_data_query = """
    INSERT INTO reddit_posts (score, url_id, epoch, author, subreddit)
    VALUES (%s, %s, %s, %s, %s)
    """

    # Execute the SQL query to insert the row
    cursor.execute(insert_data_query, data)

    # Commit the changes to the database
    connection.commit()

def insert_row_v3(data):
    insert_data_query = """
    INSERT INTO reddit_posts_v3 (epoch, subreddit, post_data)
    VALUES (%s, %s, %s)
    """

    # Execute the SQL query to insert the row
    cursor.execute(insert_data_query, data)

    # Commit the changes to the database
    connection.commit()


# data = [1234, 'test', '{post: [author, url, 10]}']
# insert_row_v2(data)


def delete_data():
    delete_data_query = """
    DELETE FROM reddit_posts
    WHERE subreddit = 'science'
    """

    # Execute the SQL query to delete the data
    cursor.execute(delete_data_query)

    # Commit the changes to the database
    connection.commit()

def read_row():
    # Define the ID of the row you want to read
    row_id = '203'

    # Define the SQL statement to read the row by ID
    select_data_query = f"SELECT * FROM reddit_posts WHERE url_id = '{row_id}'"

    # Execute the SQL query to read the row
    cursor.execute(select_data_query)

    # Fetch the row
    row = cursor.fetchone()

    # Print the row
    print(row)

def read_columns():
    # Define the column you want to read
    number_of_subreddits = collections.Counter()
    column_name = 'subreddit'

    # Define the SQL statement to read the column for every row
    select_column_query = f"SELECT {column_name} FROM reddit_posts"

    # Execute the SQL query to read the column
    cursor.execute(select_column_query)

    # Fetch all the rows for the selected column
    column_data = cursor.fetchall()

    # Print the column data


    for data in column_data:
        # print(data[0])
        number_of_subreddits[data[0]] += 1
    print(number_of_subreddits)

def clear_table():
    table_name = 'reddit_posts_v4'

    # Define the SQL statement to clear the table
    truncate_table_query = f"TRUNCATE TABLE {table_name}"

    # Execute the SQL query to clear the table
    cursor.execute(truncate_table_query)

    # Commit the changes to the database
    connection.commit()


def print_last_row():
    select_last_row_query = """
    SELECT *
    FROM reddit_posts
    WHERE url_id = LAST_INSERT_ID()
    """

    # Execute the SQL query to get the last row
    cursor.execute(select_last_row_query)

    # Fetch the last row
    last_row = cursor.fetchone()

    # Print the last row
    print(last_row)

def get_rows_by_time(end_epoch, start_epoch, subreddit):
    cursor.nextset()

    # Define the SQL statement to retrieve data within the epoch range
    # subreddit = 'AND subreddit = ' + subreddit if subreddit else ''
    select_data_query = f"""
    SELECT *
    FROM reddit_posts_v3
    WHERE epoch BETWEEN %s AND %s AND 
    subreddit = %s
    """

    # Execute the SQL query to retrieve data within the epoch range
    cursor.execute(select_data_query, (start_epoch, end_epoch, subreddit))

    # Fetch all the rows within the epoch range
    posts = cursor.fetchall()

    # print(posts)

    # Convert rows_list to a JSON object
    # json_data = json.dumps(rows_list)

    # Print the JSON object
    # print(json_data)

    # print(len(posts))

    posts = [list(post) for post in posts]
    for i in range(len(posts)):
        # print(posts[i][2])
        posts[i][2] = json.loads(posts[i][2])


    posts.sort(reverse=True, key=lambda posts: posts[2]['score'])


    # print(posts)


    return {'posts': posts}


def delete_table():
    sql = "DROP TABLE IF EXISTS reddit_posts_v"

    # Execute the SQL statement
    cursor.execute(sql)

    # Commit the changes
    connection.commit()

# delete_table()
# print_last_row()
# create_database()
# create_table_v1()
# create_table_v3()
# show_databases()
# show_tables()
# delete_data()
show_table_data()
# read_row()
# read_columns()
# clear_table()
# get_rows_by_time(1122879600, 1120201200, 'reddit.com')
