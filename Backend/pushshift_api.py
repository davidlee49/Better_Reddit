import requests


def pushshift_api(date_start, date_end, subreddit, title):

    api = [subreddit_req := f'subreddit={subreddit}', range_start := f'before={date_start}', range_end := f'after={date_end}', query_word := f'title={title}', size := 'size=80', test:='']

    api_cons = ''
    for i in api:
        if i:
            api_cons += i + "&"

    print(api_cons)

    response = requests.get(f"https://api.pushshift.io/reddit/submission/search/?{api_cons}")

    response = response.json()
    print(response)


    count = 0

    posts = {'posts': []}
    for post in response['data']:
        count += 1
        # print('https://www.reddit.com' + post['permalink'], post['score'], post['num_comments'], count)
        posts['posts'].append(('https://www.reddit.com' + post['permalink'], post['title'], post['thumbnail'], post['score'], post['num_comments'], count))

    return posts

