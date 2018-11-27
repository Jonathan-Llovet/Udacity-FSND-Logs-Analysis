#Logs Analysis

This is a Python application that prints a plain-text, readable report of analysis of sample server logs stored in a PostgreSQL database to give insights about a blog. 

This application is a project created as part of Udacity's Full-Stack Web Developer Nanodegree Program.

##Report Details
The report contains the following information about the blog:

1. The Most Popular Articles of All Time
    * This lists the three most frequently viewed blog posts of all time, with the most frequently viewed articles listed first.
  
2. The Most Popular Authors of All Time
    * This lists the authors whose works have been viewed most often, with the most frequently viewed author listed first. 
    * N.B. There is an author in the database whose name is "Anonymous Contributor". This is not an aggregation of article views from several contributors.
  
3. Days With Connection Issues
    * This lists all of the days in which more than 1% of requests to the server resulted in errors, i.e. those with the status "404 NOT FOUND".

##How Does it Work?
When run as a stand-alone script, this application creates a dictionary that contains the headers for each of the queries that are going to be run as keys, and the actual SQL queries to be made as values. This is done with the `name_queries` and `create_queries` functions. 

Then, the `report_logs` function is called, which runs the queries and prints the report. To do this, `report_logs` uses the `run_SELECT_query` for each of the queries that are passed to it from the dictionary `query_dict` that is returned from the `create_queries` function. 

The function `run_SELECT_query` establishes a connection to the `news` database, saves the result, and then closes the connection to the database before returning the query result. 

The query results each have two columns, which are converted to elements in a list. The `report_logs` function prints these out, generating the report.

##Installation and Dependencies
The application uses Python 3.5.2. Make sure that you have this or a later version installed.

You will need to install psycopg2 to connect to the PostgreSQL database. Run `pip install psycopg2` to install it. If you already have it installed, you will be notified by the output.

This application makes use of the "news" database that is set up in the Vagrant VM as part of Udacity's Full-Stack Web Developer Nanodegree Program. Make sure that the database has been fully installed per the instructions in the course notes.

Once it is installed, you will need to create the following Views in your database. These run queries that can be easily called by an alias in main queries,which helps ensure that the main queries are more readable. If these are not made in the database, the application **won't work**.

    CREATE VIEW daily_errors AS
    select TO_CHAR(date_trunc('day', time),'FMMonth, DD, YYYY') as day, 
    count(status) as num_errors
    from log
    where status = '404 NOT FOUND'
    group by day
    order by day;

    CREATE VIEW daily_requests AS
    SELECT TO_CHAR(date_trunc('day', time),'FMMonth, DD, YYYY') as day, 
    count(status) as requests
    from log
    group by day
    order by day;

##Usage
To generate a report, simply run `python3 log_analysis.py` in the directory containing the script. Otherwise, provide the path to the file. 

To save the report as a text file, use the `>` command as in the example below:
    python3 log_analysis.py > log_analysis_output.txt
This will save the output into a .txt file.

##License
This project is licensed under the terms of the MIT license.

