import psycopg2
from psycopg2 import sql
print(psycopg2)

db = psycopg2.connect("dbname=news")
cursor = db.cursor()
cursor.execute('DROP VIEW top_articles')
cursor.execute("CREATE VIEW top_articles AS select path, count(path) as views from log group by path order by views desc offset 1 limit 3;")
cursor.execute("select * from top_articles")
results = cursor.fetchall()

print("results: ", len(results))
cursor.execute("select path from top_articles")
paths = cursor.fetchall()
paths_to_slugs = []

for path in paths:
  stringified = ''.join(path)
  paths_to_slugs.append(stringified[9:])

print("paths to slugs:", paths_to_slugs)

cursor.execute("select slug, views from articles join top_articles on path like CONCAT('%', slug) order by views desc")
c = cursor.fetchall()
print(c)

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
