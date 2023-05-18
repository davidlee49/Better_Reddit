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

def partition_and_sort():
    # Alter the existing table to become a partitioned table with sorting
    alter_table_query = """
    ALTER TABLE reddit_posts_v5
    PARTITION BY RANGE COLUMNS(epoch, subreddit) (
        PARTITION p200506 VALUES LESS THAN (UNIX_TIMESTAMP('2005-07-01'), 'subreddit_max_value') ENGINE = InnoDB,
        PARTITION p200507 VALUES LESS THAN (UNIX_TIMESTAMP('2005-08-01'), 'subreddit_max_value') ENGINE = InnoDB,
        PARTITION p200508 VALUES LESS THAN (UNIX_TIMESTAMP('2005-09-01'), 'subreddit_max_value') ENGINE = InnoDB,
        PARTITION p200509 VALUES LESS THAN (UNIX_TIMESTAMP('2005-10-01'), 'subreddit_max_value') ENGINE = InnoDB,
        PARTITION p200510 VALUES LESS THAN (UNIX_TIMESTAMP('2005-11-01'), 'subreddit_max_value') ENGINE = InnoDB,
        PARTITION p200511 VALUES LESS THAN (UNIX_TIMESTAMP('2005-12-01'), 'subreddit_max_value') ENGINE = InnoDB,
        PARTITION p200512 VALUES LESS THAN (UNIX_TIMESTAMP('2006-1-01'), 'subreddit_max_value') ENGINE = InnoDB,
        PARTITION p200601 VALUES LESS THAN (UNIX_TIMESTAMP('2006-2-01'), 'subreddit_max_value') ENGINE = InnoDB,
        PARTITION p200602 VALUES LESS THAN (UNIX_TIMESTAMP('2006-3-01'), 'subreddit_max_value') ENGINE = InnoDB,
        PARTITION p200603 VALUES LESS THAN (UNIX_TIMESTAMP('2006-4-01'), 'subreddit_max_value') ENGINE = InnoDB,
        PARTITION p200604 VALUES LESS THAN (UNIX_TIMESTAMP('2006-5-01'), 'subreddit_max_value') ENGINE = InnoDB,
        PARTITION p200605 VALUES LESS THAN (UNIX_TIMESTAMP('2006-6-01'), 'subreddit_max_value') ENGINE = InnoDB,
        PARTITION p200606 VALUES LESS THAN (UNIX_TIMESTAMP('2006-7-01'), 'subreddit_max_value') ENGINE = InnoDB,
        PARTITION p200607 VALUES LESS THAN (UNIX_TIMESTAMP('2006-8-01'), 'subreddit_max_value') ENGINE = InnoDB,
        PARTITION p200608 VALUES LESS THAN (UNIX_TIMESTAMP('2006-9-01'), 'subreddit_max_value') ENGINE = InnoDB,
        PARTITION p200609 VALUES LESS THAN (UNIX_TIMESTAMP('2006-10-01'), 'subreddit_max_value') ENGINE = InnoDB,
        PARTITION p200610 VALUES LESS THAN (UNIX_TIMESTAMP('2006-11-01'), 'subreddit_max_value') ENGINE = InnoDB,
        PARTITION p200611 VALUES LESS THAN (UNIX_TIMESTAMP('2006-12-01'), 'subreddit_max_value') ENGINE = InnoDB,
        PARTITION p200612 VALUES LESS THAN (UNIX_TIMESTAMP('2007-1-01'), 'subreddit_max_value') ENGINE = InnoDB,
        PARTITION p200701 VALUES LESS THAN (UNIX_TIMESTAMP('2007-2-01'), 'subreddit_max_value') ENGINE = InnoDB,
        PARTITION p200702 VALUES LESS THAN (UNIX_TIMESTAMP('2007-3-01'), 'subreddit_max_value') ENGINE = InnoDB,
        PARTITION p200703 VALUES LESS THAN (UNIX_TIMESTAMP('2007-4-01'), 'subreddit_max_value') ENGINE = InnoDB,
        PARTITION p200704 VALUES LESS THAN (UNIX_TIMESTAMP('2007-5-01'), 'subreddit_max_value') ENGINE = InnoDB,
        PARTITION p200705 VALUES LESS THAN (UNIX_TIMESTAMP('2007-6-01'), 'subreddit_max_value') ENGINE = InnoDB,
        PARTITION p200706 VALUES LESS THAN (UNIX_TIMESTAMP('2007-7-01'), 'subreddit_max_value') ENGINE = InnoDB,
        PARTITION p200707 VALUES LESS THAN (UNIX_TIMESTAMP('2007-8-01'), 'subreddit_max_value') ENGINE = InnoDB,
        PARTITION p200708 VALUES LESS THAN (UNIX_TIMESTAMP('2007-9-01'), 'subreddit_max_value') ENGINE = InnoDB,
        PARTITION p200709 VALUES LESS THAN (UNIX_TIMESTAMP('2007-10-01'), 'subreddit_max_value') ENGINE = InnoDB,
        PARTITION p200710 VALUES LESS THAN (UNIX_TIMESTAMP('2007-11-01'), 'subreddit_max_value') ENGINE = InnoDB,
        PARTITION p200711 VALUES LESS THAN (UNIX_TIMESTAMP('2007-12-01'), 'subreddit_max_value') ENGINE = InnoDB,
        PARTITION p200712 VALUES LESS THAN (UNIX_TIMESTAMP('2008-1-01'), 'subreddit_max_value') ENGINE = InnoDB,
        PARTITION p200801 VALUES LESS THAN (UNIX_TIMESTAMP('2008-2-01'), 'subreddit_max_value') ENGINE = InnoDB,
        PARTITION p200802 VALUES LESS THAN (UNIX_TIMESTAMP('2008-3-01'), 'subreddit_max_value') ENGINE = InnoDB,
        PARTITION p200803 VALUES LESS THAN (UNIX_TIMESTAMP('2008-4-01'), 'subreddit_max_value') ENGINE = InnoDB,
        PARTITION p200804 VALUES LESS THAN (UNIX_TIMESTAMP('2008-5-01'), 'subreddit_max_value') ENGINE = InnoDB,
        PARTITION p200805 VALUES LESS THAN (UNIX_TIMESTAMP('2008-6-01'), 'subreddit_max_value') ENGINE = InnoDB,
        PARTITION p200806 VALUES LESS THAN (UNIX_TIMESTAMP('2008-7-01'), 'subreddit_max_value') ENGINE = InnoDB,
        PARTITION p200807 VALUES LESS THAN (UNIX_TIMESTAMP('2008-8-01'), 'subreddit_max_value') ENGINE = InnoDB,
        PARTITION p200808 VALUES LESS THAN (UNIX_TIMESTAMP('2008-9-01'), 'subreddit_max_value') ENGINE = InnoDB,
        PARTITION p200809 VALUES LESS THAN (UNIX_TIMESTAMP('2008-10-01'), 'subreddit_max_value') ENGINE = InnoDB,
        PARTITION p200810 VALUES LESS THAN (UNIX_TIMESTAMP('2008-11-01'), 'subreddit_max_value') ENGINE = InnoDB,
        PARTITION p200811 VALUES LESS THAN (UNIX_TIMESTAMP('2008-12-01'), 'subreddit_max_value') ENGINE = InnoDB,
        PARTITION p200812 VALUES LESS THAN (UNIX_TIMESTAMP('2009-1-01'), 'subreddit_max_value') ENGINE = InnoDB,
        PARTITION p200901 VALUES LESS THAN (UNIX_TIMESTAMP('2009-2-01'), 'subreddit_max_value') ENGINE = InnoDB,
        PARTITION p200902 VALUES LESS THAN (UNIX_TIMESTAMP('2009-3-01'), 'subreddit_max_value') ENGINE = InnoDB,
        PARTITION p200903 VALUES LESS THAN (UNIX_TIMESTAMP('2009-4-01'), 'subreddit_max_value') ENGINE = InnoDB,
        PARTITION p200904 VALUES LESS THAN (UNIX_TIMESTAMP('2009-5-01'), 'subreddit_max_value') ENGINE = InnoDB,
        PARTITION p200905 VALUES LESS THAN (UNIX_TIMESTAMP('2009-6-01'), 'subreddit_max_value') ENGINE = InnoDB,
        PARTITION p200906 VALUES LESS THAN (UNIX_TIMESTAMP('2009-7-01'), 'subreddit_max_value') ENGINE = InnoDB,
        PARTITION p200907 VALUES LESS THAN (UNIX_TIMESTAMP('2009-8-01'), 'subreddit_max_value') ENGINE = InnoDB,
        PARTITION p200908 VALUES LESS THAN (UNIX_TIMESTAMP('2009-9-01'), 'subreddit_max_value') ENGINE = InnoDB,
        PARTITION p200909 VALUES LESS THAN (UNIX_TIMESTAMP('2009-10-01'), 'subreddit_max_value') ENGINE = InnoDB,
        PARTITION p200910 VALUES LESS THAN (UNIX_TIMESTAMP('2009-11-01'), 'subreddit_max_value') ENGINE = InnoDB,
        PARTITION p200911 VALUES LESS THAN (UNIX_TIMESTAMP('2009-12-01'), 'subreddit_max_value') ENGINE = InnoDB,
        PARTITION p200912 VALUES LESS THAN (UNIX_TIMESTAMP('2010-1-01'), 'subreddit_max_value') ENGINE = InnoDB,
        PARTITION pmax VALUES LESS THAN (MAXVALUE, 'subreddit_max_value') ENGINE = InnoDB
    )
    (
      PARTITION p200901_sorted ENGINE = InnoDB AS (
        SELECT * FROM reddit_posts_v5
        WHERE epoch >= UNIX_TIMESTAMP('2009-01-01') AND epoch < UNIX_TIMESTAMP('2009-02-01')
        ORDER BY score ASC, epoch DESC, subreddit ASC
  ));
    """

    # Execute the alter table query
    cursor.execute(alter_table_query)

    # Commit the changes to the database
    connection.commit()


# partition_and_sort()


def show_table_data():
    start_time = time.time()
    cursor.execute('''SELECT * 
                    FROM reddit_posts_v5
where date >= '2007-01-01' AND date <= '2007-01-31'
                    ''')

    # Fetch all the rows
    rows = cursor.fetchall()
    subreddits = collections.Counter()

    # Print the data
    count = 0
    for row in rows:
        print(row)
    print(len(rows))
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
    table_name = 'reddit_posts_v5'

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
    start_time = time.time()
    sub_query = 'AND subreddit = %s'
    if not subreddit:
        sub_query = ''
    cursor.nextset()

    # Define the SQL statement to retrieve data within the epoch range
    # subreddit = 'AND subreddit = ' + subreddit if subreddit else ''
    select_data_query = f'''
    SELECT *
    FROM reddit_posts_v5
    WHERE epoch BETWEEN %s AND %s {sub_query}
    ORDER BY score DESC
    LIMIT 100 '''

    # OFFSET 100


    # Execute the SQL query to retrieve data within the epoch range
    if subreddit:
        cursor.execute(select_data_query, (start_epoch, end_epoch, subreddit))
    else:
        cursor.execute(select_data_query, (start_epoch, end_epoch))

    # Fetch all the rows within the epoch range
    posts = cursor.fetchall()

    posts = [list(post) for post in posts]
    for i in range(len(posts)):
        print(posts[i][2], posts[i][7])
        posts[i][7] = json.loads(posts[i][7])


    # posts.sort(reverse=True, key=lambda posts: posts[2])

    print(len(posts))
    # print(posts)
    elapsed_time = time.time() - start_time
    print(elapsed_time)

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
# get_rows_by_time(1233513316, 1230834916, '')
