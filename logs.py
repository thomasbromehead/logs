import psycopg2
print(psycopg2)

db = psycopg2.connect("dbname=news")
cursor = db.cursor()

#FIRST EXERCISE - TOP 3 ARTICLES
print("1st Exercise")
cursor.execute('DROP VIEW top_articles')
cursor.execute("CREATE VIEW top_articles AS select path, count(path) as views from log group by path order by views desc offset 1 limit 3;")
cursor.execute("select * from top_articles")
results = cursor.fetchall()
print('results: ', results)

cursor.execute("CREATE VIEW top_articles_with_views as select slug, views from articles join top_articles on path like CONCAT('%', slug) order by views desc")
cursor.execute("select * from top_articles_with_views")
top_articles = cursor.fetchall()
print('top_articles: ', top_articles)

print('Most successful articles of all times')
for article in top_articles:
  string = "ARTICLE: {} | VIEWS: {}".format(article[0], article[1])
  print(string)

print('\n')

#2ND EXERCISE - TOP AUTHORS
print("2nd Exercise")

cursor.execute("DROP VIEW top_articles_8 CASCADE")
cursor.execute("CREATE VIEW top_articles_8 AS select path, count(path) as views from log group by path order by views desc offset 1 limit 8;")
cursor.execute("CREATE VIEW top_articles_with_views_8 as select articles.author, views from articles join top_articles_8 on path like CONCAT('%', slug) order by views desc;")
cursor.execute("select name, sum(views) as total from top_articles_with_views_8 join authors on authors.id = top_articles_with_views_8.author group by name order by total desc;")
top_authors = cursor.fetchall()
print("------TOP AUTHORS------")
for author in top_authors:
  print("Author: {}, Total Views: {}".format(author[0], author[1]))


#3rd Exercise
print("3rd exercise")
# Get all 200s
create view OKs as select status, extract(doy from time) as day from log where status like '200%';
#Count all 200s per day
create view total_oks as select day, count(status) from OKs group by day;
# Get all errors
create view total_errors as select status, extract(doy from time) as day from log where status not like '200%';
# Count all 404s per day 
create view total_errors as select day, count(status) from errors group by day;
# Global view with 200s and 404s per day
create view global_view as select total_oks.day, total_oks.count as status200, total_errors.count as status404 from total_oks join total_errors on total_oks.day = total_errors.day;
# Select Day with error percentage > 1%
select day, cast(status404 as decimal) / cast(status200 as decimal)*100 as error_percentage from global_view where cast(status404 as decimal) / cast(status200 as decimal) > 0.01;
