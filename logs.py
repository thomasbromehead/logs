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

# "select slug, count from articles join top_articles on path like CONCAT('%', slug)";


# cursor.execute(sql.SQL("select slug, views from top_articles, articles WHERE top_articles.path LIKE (\'/article/%s\') order by top_articles.views ").format(sql.Identifier('articles.slug')))
# top_articles = cursor.fetchall()
# print(top_articles)




# print(slugs)
# for slug in slugs:
#   cursor.execute("Select A.title from Articles as A, Log as L WHERE A.slug LIKE (\"_%s\")", (slug,))

# print(results)

# select path, count(path) from log group by path order by count(path) desc;



# CREATE VIEW top_articles AS select path, count(path) from log group by path order by count(path) desc offset 1 limit 8
