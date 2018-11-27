#!/usr/bin/env python3

import psycopg2

def report_logs(queries, query_names):
    '''Generates blog traffic report'''
    header = "Blog Traffic Report"
    line_break = "*"*42+"\n"
    print(header+"\n")
    for name in query_names:
        print(name)
        print(line_break)
        result = run_SELECT_query(queries.get(name))
        for i in range(len(result)):
                print("{} - {}".format(result[i][0], result[i][1]))
        print("\n")

def run_SELECT_query(query, db="news"):
    """Connect to the database and run the query specified"""
    db = "dbname={}".format(db)
    conn = psycopg2.connect(db)
    cur = conn.cursor()
    cur.execute(query)
    query_result = cur.fetchall()
    cur.close()
    conn.close()
    return query_result
    
def name_queries():
    """Create a list of titles for queries that are going to be run"""
    query_names = ["The Most Popular Articles of All Time", "The Most Popular Authors of All Time", "Days With Connection Issues"]
    return query_names

def create_queries(query_names):
    """Create a dictionary of queries to be run"""
    queries = []
    # Create a query to select the 3 most popular articles of all time
    queries.append("""
        SELECT r.title, COUNT(l.path)::TEXT || ' views' AS popular_articles
        FROM articles AS r 
        INNER JOIN log AS l 
            ON r.slug = RIGHT(l.path,LENGTH(r.slug))
        GROUP BY r.title
        ORDER BY COUNT(l.path) DESC
        LIMIT 3;
        """)

    # Create a query to select the most popular authors of all time
    queries.append("""
        SELECT a.name, count(l.path) || ' views' AS calls
        FROM log AS l
        INNER JOIN 
            (SELECT a.name AS name, art.title AS title, art.slug AS slug
            FROM authors AS a
            INNER JOIN articles AS art
            ON art.author = a.id
            ) AS a
            ON a.slug = RIGHT(l.path,LENGTH(a.slug))
        GROUP BY a.name
        ORDER BY calls DESC
        LIMIT 5;
        """)

    # Create a query to select days where more than 1% of server requests resulted in errors
    queries.append("""
        SELECT de.day, ROUND((num_errors::NUMERIC / requests::NUMERIC * 100),1) AS perc_error
        FROM log
        INNER JOIN daily_errors as de
            ON TO_CHAR(DATE_TRUNC('day', log.time),'FMMonth, DD, YYYY') = de.day
        INNER JOIN daily_requests AS dr
            ON de.day = dr.day
        WHERE (num_errors::NUMERIC / requests::NUMERIC * 100) > 1
        GROUP BY de.day, perc_error
        ORDER BY de.day;
        """)
    
    query_results = dict(zip(query_names, queries))
    return query_results


if __name__ == "__main__":
    query_names = name_queries()
    queries = create_queries(query_names)
    report_logs(queries, query_names)