from env import *
import collections
import json
import time

connection = mysql_connector()
cursor = connection.cursor()


def insert_row_v5(data):
    insert_data_query = """
    INSERT INTO reddit_posts_v5 (epoch, post_type, score, comment_count, subreddit, post_id, author, post_data)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    # Execute the SQL query to insert the row
    cursor.execute(insert_data_query, data)

    # Commit the changes to the database
    connection.commit()


def create_table_v5():
    # NOTE: we are putting the majority of the post data into a JSON blob(score, url, and author)
    # NOTE: additionally, we are going to make the sub and date the primary key
    create_schema_query = """
    CREATE TABLE reddit_posts_v5 (
        epoch INT,
        post_type INT,
        score INT,
        comment_count INT,
        subreddit VARCHAR(255),
        post_id VARCHAR(10),
        author VARCHAR(50),
        post_data JSON
    )
    """

    # Execute the SQL query to create the schema
    cursor.execute(create_schema_query)

    # Commit the changes to the database
    connection.commit()

# create_table_v5()
def partition_table():
    cursor = connection.cursor()

    # Create the partitioned table
    partition_query = """
    ALTER TABLE reddit_posts_v3
     PARTITION BY RANGE COLUMNS(epoch) (
        PARTITION p200501 VALUES LESS THAN (UNIX_TIMESTAMP('2007-02-01')),
        PARTITION p200502 VALUES LESS THAN (UNIX_TIMESTAMP('2007-03-01')),
        PARTITION p200503 VALUES LESS THAN (UNIX_TIMESTAMP('2007-04-01')),
        PARTITION p200504 VALUES LESS THAN (UNIX_TIMESTAMP('2007-05-01')),
        PARTITION p200505 VALUES LESS THAN (UNIX_TIMESTAMP('2007-06-01')),
        PARTITION p200506 VALUES LESS THAN (UNIX_TIMESTAMP('2007-07-01')),
        PARTITION p200507 VALUES LESS THAN (UNIX_TIMESTAMP('2007-08-01')),
        PARTITION p200508 VALUES LESS THAN (UNIX_TIMESTAMP('2007-09-01')),
        PARTITION p200509 VALUES LESS THAN (UNIX_TIMESTAMP('2007-10-01')),
        PARTITION p200510 VALUES LESS THAN (UNIX_TIMESTAMP('2007-11-01')),
        PARTITION p200511 VALUES LESS THAN (UNIX_TIMESTAMP('2007-12-01')),
        PARTITION p200601 VALUES LESS THAN (UNIX_TIMESTAMP('2008-02-01')),
        PARTITION p200602 VALUES LESS THAN (UNIX_TIMESTAMP('2008-03-01')),
        PARTITION p200603 VALUES LESS THAN (UNIX_TIMESTAMP('2008-04-01')),
        PARTITION p200604 VALUES LESS THAN (UNIX_TIMESTAMP('2008-05-01')),
        PARTITION p200605 VALUES LESS THAN (UNIX_TIMESTAMP('2008-06-01')),
        PARTITION p200606 VALUES LESS THAN (UNIX_TIMESTAMP('2008-07-01')),
        PARTITION p200607 VALUES LESS THAN (UNIX_TIMESTAMP('2008-08-01')),
        PARTITION p200608 VALUES LESS THAN (UNIX_TIMESTAMP('2008-09-01')),
        PARTITION p200609 VALUES LESS THAN (UNIX_TIMESTAMP('2008-10-01')),
        PARTITION p200610 VALUES LESS THAN (UNIX_TIMESTAMP('2008-11-01')),
        PARTITION p200611 VALUES LESS THAN (UNIX_TIMESTAMP('2008-12-01'))
    )
    """
    cursor.execute(partition_query)

    # Commit the changes
    connection.commit()

    # Close the cursor and connection
    # cursor.close()
    # connection.close()


# partition_table()

def show_partitions():
    cursor = connection.cursor()

    table_name = 'reddit_posts_v4'

    # Query the information_schema database to retrieve partition information
    partition_query = f"""
        SELECT partition_name, subpartition_name, partition_method, subpartition_method, partition_expression
        FROM information_schema.partitions
        WHERE table_name = '{table_name}'
        ORDER BY partition_ordinal_position, subpartition_ordinal_position
    """

    # Execute the partition query
    cursor.execute(partition_query)

    # Fetch all the partition information
    partitions = cursor.fetchall()

    # Display the partition information
    for partition in partitions:
        print(partition)

    # Close the cursor and connection
    cursor.close()
    connection.close()

# show_partitions()

def show_post_from_date():
    cursor = connection.cursor()
    query = '''
    SELECT *
    FROM reddit_posts_v4
    WHERE (epoch >= 1119552233 AND epoch < 1196469538)
    AND score > 0 
    AND subreddit = 'politics';
    '''

    cursor.execute(query)
    partitions = cursor.fetchall()

    # Display the partition information
    count = 0
    for partition in partitions:
        count += 1
        print(partition)

    print(count)
# show_post_from_date()