import psycopg2
print(psycopg2)

db = psycopg2.connect("dbname=news")
cursor = db.cursor()
cursor.execute("Select path from log limit 10")
slugs = cursor.fetchall()
for slug in slugs:
  string_slug = (''.join(slug))
  
# print(slugs)
# for slug in slugs:
#   cursor.execute("Select A.title from Articles as A, Log as L WHERE A.slug LIKE (\"_%s\")", (slug,))

# print(results)

# select path, count(path) from log group by path order by count(path) desc;



