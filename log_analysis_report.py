#!/usr/local/bin/python3

import psycopg2

TOP_ARTICLES_QUERY = '''
select 
    a.title, 
    l.views 
from articles a
join (
    select 
        split_part(path, '/', 3) as slug, 
        count(1) as views 
    from log 
    where status = '200 OK' 
    group by path 
    order by views desc
) l on (a.slug = l.slug)
limit 3;
'''

TOP_AUTHORS_QUERY = '''
select 
    au.name as author_name, 
    sum(l.views) as views 
from articles ar
join authors au on ar.author = au.id
join (
    select 
        split_part(path, '/', 3) as slug, 
        count(1) as views 
    from log 
    where status = '200 OK' 
    group by path 
) l on (ar.slug = l.slug)
group by author_name
order by views desc
limit 3;
'''

REQUEST_ERROR_QUERY = '''
select 
    to_char(date, 'FMMonth FMDD, YYYY'), 
    round((error::decimal / NULLIF(ok, 0)) * 100, 2)  as "% errors"
from (
    select
        date_trunc('day', time) as date, 
        sum(case when status != '200 OK' then 1 else 0 end) as error, 
        sum(case when status = '200 OK' then 1 else 0 end) as ok 
    from log 
    group by date
) agg
where (error::decimal / NULLIF(ok, 0)) * 100 > 1;
'''


def query_db(sql_query_str):
    conn = psycopg2.connect(dbname='news')
    cursor = conn.cursor()
    cursor.execute(sql_query_str)
    result = cursor.fetchall()
    conn.close()
    return result


def present_top3_articles():
    top_3_articles = query_db(TOP_ARTICLES_QUERY)

    print('1. What are the most popular three articles of all time?')
    for title, views in top_3_articles:
        print('- {} -- {} views'.format(title, views))


def present_top3_authors():
    top_3_authors = query_db(TOP_AUTHORS_QUERY)

    print('2. Who are the most popular article authors of all time?')
    for author, views in top_3_authors:
        print('- {} -- {} views'.format(author, views))


def present_errors():
    errors = query_db(REQUEST_ERROR_QUERY)

    print('3. On which days did more than 1% of requests lead to errors?')
    for date, error_rate in errors:
        print('- {} -- {}% errors'.format(date, error_rate))


if __name__ == '__main__':
    present_top3_articles()
    present_top3_authors()
    present_errors()