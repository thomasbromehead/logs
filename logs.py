import psycopg2
from datetime import date

db = psycopg2.connect("dbname=news")
cursor = db.cursor()

#FIRST EXERCISE - TOP 3 ARTICLES
print("1st Exercise")
cursor.execute("CREATE VIEW top_articles AS select path, count(path) as views from log group by path order by views desc offset 1 limit 3;")
cursor.execute("select * from top_articles")


cursor.execute("CREATE VIEW top_articles_with_views as select slug, views from articles join top_articles on path like CONCAT('%', slug) order by views desc")
cursor.execute("select * from top_articles_with_views")
top_articles = cursor.fetchall()

print('--------Most 3 successful articles of all times--------')
for article in top_articles:
  string = "ARTICLE: {} | VIEWS: {}".format(article[0], article[1])
  print(string)

print('\n')

#2ND EXERCISE - TOP AUTHORS
print("2nd Exercise")

cursor.execute("CREATE VIEW top_articles_8 AS select path, count(path) as views from log group by path order by views desc offset 1 limit 8;")
cursor.execute("CREATE VIEW top_articles_with_views_8 as select articles.author, views from articles join top_articles_8 on path like CONCAT('%', slug) order by views desc;")
cursor.execute("select name, sum(views) as total from top_articles_with_views_8 join authors on authors.id = top_articles_with_views_8.author group by name order by total desc;")
top_authors = cursor.fetchall()
print("------TOP AUTHORS------")
for author in top_authors:
  print("Author: {}, Total Views: {}".format(author[0], author[1]))


#3rd Exercise
print('\n')
print("3rd exercise")
# Get all 200s
cursor.execute("create view OKs as select status, extract(doy from time) as day from log where status like '200%'");
cursor.execute("select * from OKs")

#Count all 200s per day
cursor.execute("create view total_oks as select day, count(status) from OKs group by day;")
cursor.execute("select * from OKs")

# Get all errors
cursor.execute("create view errors as select status, extract(doy from time) as day from log where status not like '200%'");
cursor.execute("select * from errors")

# Count all 404s per day 
cursor.execute("create view total_errors as select day, count(status) from errors group by day;")
cursor.execute("select * from total_errors")

# Global view with 200s and 404s per day
cursor.execute("create view global_view as select total_oks.day, total_oks.count as status200, total_errors.count as status404 from total_oks join total_errors on total_oks.day = total_errors.day;")
cursor.execute("select * from global_view")

# Select Day with error percentage > 1%
cursor.execute(" create view error_days as select day, cast(status404 as decimal) / cast(status200 as decimal)*100 as error_percentage from global_view where cast(status404 as decimal) / cast(status200 as decimal) > 0.01;")
cursor.execute("select to_char(log.time, 'FMDay,DDth FMMonth YYYY') as Day, round(error_percentage,2) as Error_Percentage from log join error_days on extract(doy from time) = error_days.day limit 1;")
h = cursor.fetchall()
print('---------')
print("Days with more than 1% of 404s: {}, percentage: {} %".format((h[0][0]), h[0][1]))
