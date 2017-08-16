# Logs Analysis Program Project
## Summary
The Log Analysis Program is a project from the Udacity Full-Stack Nanodegree program. The project comes with a SQL file to set up a PostgreSQL database with the tables needed to finish the project. The PostgreSQL database along with all of the associated project files are run on a Linux virtual machine. The goal of the project is to use the information in the database to write SQL queries to answer the given questions.

The questions to be answered are the following:
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

## Requirements
* Install [Virtual Box](https://www.virtualbox.org/)
* Install [Vagrant](https://www.vagrantup.com/)
* Download or Clone [fullstack-nanodegree-vm](https://github.com/udacity/fullstack-nanodegree-vm) repository
* Download the [news data](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) file

## Running the Program
1. From within the Vagrant folder you downloaded on to your machine use the command  `vagrant up` to set up the Virtual Machine.
2. Use `vagrant ssh` to log into your Virtual Machine.
3. Navigate into the Vagrant directory using `cd /vagrant`
4. Set up the News database in your Virtual Machine with `psql -d news -f newsdata.sql`
5. Create the views listed in the Views section below in order to run the queries to the database.
6. Use `python logdb.py` within the logs-analysis-project directory to run the program and generate the output to the text file.

## Output
````

What are the most popular three articles of all time?

 "Candidate is jerk, alleges rival" -- 338647 views 
 "Bears love berries, alleges bear" -- 253801 views 
 "Bad things gone, say good people" -- 170098 views 

Who are the most popular article authors of all time?

 Ursula La Multa -- 507594 views 
 Rudolf von Treppenwitz -- 423457 views 
 Anonymous Contributor -- 170098 views 
 Markoff Chaney -- 84557 views 

On which days did more than 1% of requests lead to errors?

 July 17, 2016 -- 2.26 % errors
 ````

 ## Views

Use `CREATE VIEW [view name] AS` then the query to create each view in the database.

 ### authors_articles
````sql
SELECT count(articles.title) AS countt, 
    articles.author, authors.name 
  FROM authors 
    JOIN articles ON authors.id = articles.author 
  GROUP BY articles.author, authors.name;
 ````
 
 ### Articles1
 ````sql
 SELECT CONCAT('/article/',slug) AS slug_revised, slug, author, title, id   FROM articles;
````

### request_404
````sql
 SELECT count(log.id) AS total, 
      date(log.time) AS day  
    FROM log 
  WHERE status != '200 OK' 
  GROUP BY date(log.time) 
  ORDER BY date(log.time);
````

### request_all
````sql
SELECT count(log.id) AS total, 
    date(log.time) AS day  
  FROM log 
  GROUP BY date(log.time) 
  ORDER BY date(log.time);
````
