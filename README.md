# Log Analysis Report

Running the following python script will run queries against the 
news database and generate a report that gives answers to the questions
under **Expected output**
```
python log_analysis_report.py
```

####Expected output
```
1. What are the most popular three articles of all time?
- Candidate is jerk, alleges rival -- 338647 views
- Bears love berries, alleges bear -- 253801 views
- Bad things gone, say good people -- 170098 views
2. Who are the most popular article authors of all time?
- Ursula La Multa -- 507594 views
- Rudolf von Treppenwitz -- 423457 views
- Anonymous Contributor -- 170098 views
3. On which days did more than 1% of requests lead to errors?
- July 17, 2016 -- 2.26% errors
```

###Prerequisits
Install
```
python
postgresql
```

Download the required database dump by clicking the following link
[newsdata.sql](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)

Unzip the file and run the following command to import
the data into your database

```
psql -d news -f newsdata.sql
```
