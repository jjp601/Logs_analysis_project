#!/usr/bin/env python3

#  File for Logs Analysis Project

import psycopg2

DBNAME = 'news'

#  List of Questions
question = [
    'What are the most popular three articles of all time?',
    'Who are the most popular article authors of all time?',
    'On which days did more than 1% of requests lead to errors?']


def run_query(query):
    """ Runs the given query and returns the answer """
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(query)
    answer = c.fetchall()
    db.close()
    return answer


def popular_articles():
    """ Returns the three most popular articles based on views """
    top_articles = run_query('''
                            SELECT count(log.ip) as views, Articles1.title
                            FROM Articles1
                            JOIN log ON log.path = articles1.slug_revised
                            GROUP BY articles1.title
                            ORDER BY views DESC LIMIT 3
                            ''')
    f = open("log_report.txt", "w+")
    f.write("\n" + question[0] + "\n\n")

    for views, title in top_articles:
        f.write(" \"{}\" -- {} views \n".format(title, views))
    f.close()


def popular_authors():
    """ Returns the most popular authors based on article view """
    top_authors = run_query('''
                           SELECT authors_articles.name, count(log.ip) as views
                           FROM authors_articles
                           JOIN Articles1
                           ON authors_articles.author = Articles1.author
                           JOIN log ON Articles1.slug_revised = log.path
                           GROUP BY authors_articles.name
                           ORDER BY views DESC
                           ''')
    f = open("log_report.txt", "a+")
    f.write("\n" + question[1] + "\n\n")

    for name, views in top_authors:
        f.write(" {} -- {} views \n".format(name, views))
    f.close()


def high_error_days():
    """ Returns the days with bad requests greater than 1% """
    error_days = run_query('''
                          SELECT to_char(request_all.day, 'FMMonth dd, YYYY') AS day, 
                          round(request_404.total * 100.00 / request_all.total, 2)
                          AS percentage
                          FROM request_all 
                          JOIN request_404 ON request_404.day = request_all.day 
                          WHERE (request_404.total * 100 / request_all.total) > 1''')  # noqa
    f = open("log_report.txt", "a+")
    f.write("\n" + question[2] + "\n\n")

    for day, percentage in error_days:
        f.write(" {} -- {} % errors".format(day, percentage))
    f.close()

if __name__ == '__main__':
    popular_articles()
    popular_authors()
    high_error_days()
