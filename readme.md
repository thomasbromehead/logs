# VIEWS USED

## __1st exercise__:

**Retrieve top 3 articles**
1. ```CREATE VIEW top_articles AS select path, count(path) as views from log group by path order by views desc offset 1 limit 3;```

**Get their slugs and total views with a join**

2. ```CREATE VIEW top_articles_with_views as select slug, views from articles join top_articles on path like CONCAT('%', slug) order by views desc```

## ___2nd exercise___ :

**Get top articles's path and total views**

1. ```CREATE VIEW top_articles_8 AS select path, count(path) as views from log group by path order by views desc offset 1 limit 8;```

**Get corresponding authors**

2. ```CREATE VIEW top_articles_with_views_8 as select articles.author, views from articles join top_articles_8 on path like CONCAT('%', slug) order by views desc;```

## __3rd exercise__ :
 **Get all 200s**
1. ```create view OKs as select status, extract(doy from time) as day from log where status like '200%'```

**Count all 200s per day**

2. ```create view total_oks as select day, count(status) from OKs group by day;```

**Get all errors**

3. ```create view errors as select status, extract(doy from time) as day from log where status not like '200%```

**Count all 404s per day**

4. ```create view total_errors as select day, count(status) from errors group by day;```

**Global view with 200s and 404s per day**

5. ```create view global_view as select total_oks.day, total_oks.count as status200, total_errors.count as status404 from total_oks join total_errors on total_oks.day = total_errors.day;```

**Select Day with error percentage > 1%**

6. ```create view error_days as select day, cast(status404 as decimal) / cast(status200 as decimal)*100 as error_percentage from global_view where cast(status404 as decimal) / cast(status200 as decimal) > 0.01;```

 