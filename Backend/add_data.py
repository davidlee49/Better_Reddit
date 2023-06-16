from praw_reddit import *
from db_methods import *
from console_helper_methods import *
import heapq
import time


# Specify the directory path
directory = r'C:\Users\ryu28\OneDrive\Desktop\Reddit Json Dump'


def process_directory(directory):
    updated_posts_year = {}
    for filename in os.listdir(directory):
        item_path = os.path.join(directory, filename)

        if os.path.isfile(item_path):
            # Perform operations on the file
            process_file(item_path, updated_posts_year)

        # Recursively process the subdirectory
        elif os.path.isdir(item_path):
            print('Processing directory:', item_path)
            process_directory(item_path)


def process_file(item_path, updated_posts_year):
    print('Processing file:', item_path)
    posts_m = {day+1: [] for day in range(get_days_in_month(item_path))}

    # file containing JSON objects for all a month
    file = open(item_path)

    # extracts the all "fullnames" from the file for reddit's api
    get_all_fullnames_and_sort_by_time(file, posts_m)
    update_scores_from_praw(item_path, posts_m, updated_posts_year)
    print('Processing complete')


def get_all_fullnames_and_sort_by_time(file, posts):
    for line_num, line in enumerate(file):
        line = json.loads(line)
        day = int(get_date(line['created_utc']).split('-')[2])
        posts[day].append(f"t3_{line['id']}")

    return


def update_posts_and_subreddits(updated_posts, updated_posts_week, updated_posts_month, updated_posts_year,
                                updated_post, posts_day, item_path, subreddit):

    # handle new subreddits for time ranges
    if subreddit not in updated_posts:
        updated_posts[subreddit] = {day + 1: [] for day in range(get_days_in_month(item_path))}
    if subreddit not in updated_posts_week:
        updated_posts_week[subreddit] = {0: [], 1: [], 2: [], 3: []}
    if subreddit not in updated_posts_month:
        updated_posts_month[subreddit] = []
    if subreddit not in updated_posts_year:
        updated_posts_year[subreddit] = []

    # handle adding posts for 1 day
    if len(updated_posts[subreddit][posts_day]) < 50:
        heapq.heappush(updated_posts[subreddit][posts_day], updated_post)
    else:
        heapq.heappushpop(updated_posts[subreddit][posts_day], updated_post)

    # handle adding posts for 1 week
    week = posts_day // 7 if posts_day < 28 else 3
    if len(updated_posts_week[subreddit][week]) < 75:
        heapq.heappush(updated_posts_week[subreddit][week], updated_post)
    else:
        heapq.heappushpop(updated_posts_week[subreddit][week], updated_post)

    # handle adding posts for 1 month
    if len(updated_posts_month[subreddit]) < 100:
        heapq.heappush(updated_posts_month[subreddit], updated_post)
    else:
        heapq.heappushpop(updated_posts_month[subreddit], updated_post)

    # handle adding post for 1 year
    if len(updated_posts_year[subreddit]) < 200:
        heapq.heappush(updated_posts_year[subreddit], updated_post)
    else:
        heapq.heappushpop(updated_posts_year[subreddit], updated_post)


def save_top_to_db(day, year_and_month, updated_posts):
    for subreddit in updated_posts:
        updated_posts[subreddit][day] = [trimmed_post[2] for trimmed_post in updated_posts[subreddit][day]]
        updated_posts[subreddit][day].sort(reverse=True, key=lambda x: x['score'])
        insert_row_v5(year_and_month + "-" + str(day), 'day', subreddit, json.dumps(updated_posts[subreddit][day]))


def save_top_week_to_db(year_and_month, updated_posts_week):
    for week in range(4):
        for subreddit in updated_posts_week:
            updated_posts_week[subreddit][week] = [trimmed_post[2] for trimmed_post in
                                                   updated_posts_week[subreddit][week]]
            updated_posts_week[subreddit][week].sort(reverse=True, key=lambda x: x['score'])
            insert_row_v5(year_and_month + "-" + str(f'week{week}'), 'week', subreddit,
                          json.dumps(updated_posts_week[subreddit][week]))


def save_top_month_to_db(year_and_month, updated_posts_month):
    for subreddit in updated_posts_month:
        updated_posts_month[subreddit] = [trimmed_post[2] for trimmed_post in updated_posts_month[subreddit]]
        updated_posts_month[subreddit].sort(reverse=True, key=lambda x: x['score'])
        insert_row_v5(year_and_month, 'month', subreddit, json.dumps(updated_posts_month[subreddit]))

    print('completed month')


def save_top_year_to_db(year, updated_posts_year):
    for subreddit in updated_posts_year:
        updated_posts_year[subreddit] = [trimmed_post[2] for trimmed_post in updated_posts_year[subreddit]]
        updated_posts_year[subreddit].sort(reverse=True, key=lambda x: x['score'])
        insert_row_v5(year, 'year', subreddit, json.dumps(updated_posts_year[subreddit]))


def update_scores_from_praw(item_path, posts_m, updated_posts_year):
    updated_posts, updated_posts_week, updated_posts_month = {}, {}, {}
    year_and_month = item_path.split('_')[-1]
    for day in posts_m:
        total_count, retry_count = 0, 0
        while total_count < len(posts_m[day]):
            praw_generator = praw_fetch_batch_post(posts_m[day][total_count:])
            try:
                for post in praw_generator:
                    post_info = {'created_utc': post.created_utc,
                                 'score': post.score,
                                 'author': post.author.name if post.author else 'deleted',
                                 'id': post.id,
                                 'title': post.title,
                                 'is_video': post.is_video,
                                 'shortlink': post.shortlink
                                 }
                    subreddit = post.subreddit.display_name if post.subreddit else 'deleted'
                    # create tuple with score and id(in case score is the same) to sort into heap
                    updated_post = (post.score, post.id, post_info)
                    update_posts_and_subreddits(updated_posts, updated_posts_week, updated_posts_month, 
                                                updated_posts_year, updated_post, day, item_path, subreddit)
                    total_count += 1
                    if total_count % 20 == 0:
                        time.sleep(1)

            except Exception as e:
                retry_count += 1
                total_count += 1
                if total_count % 20 == 0:
                    time.sleep(1)
                print(str(e), 'retry count: ', retry_count, 'total_count :', total_count)
                log_event(item_path, False, posts_m[total_count:total_count + 5], str(e))
                continue

        save_top_to_db(day, year_and_month, updated_posts)
    save_top_week_to_db(year_and_month, updated_posts_week)
    save_top_month_to_db(year_and_month, updated_posts_month)

    year, month = year_and_month.split('-')
    if month == '12':
        save_top_year_to_db(year, updated_posts_year)
        updated_posts_year.clear()


process_directory(directory)



