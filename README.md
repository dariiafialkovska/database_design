# database_design
 

I have chosen exercise B. I have used PostgreSQL and Python to create schema and populate the database. 
## Queries
To perform queries you can run :
```bash
python compensation_data/queries/run_queries.py
```

## Running Code
Ideally If I had more time I would want to dockerize my code and setup of PostgreSQL. But here to setup the database you can run : 

```bash
python compensation_data/database.py
```

To process and load all the data into the database, execute:
```bash
python compensation_data/main.py
```


### SQL dump
You can find SQL dump in compensation_data folder

### Database schema diagram
!(table_schema.png)


## Query Results
You can find CSV files under compensation_data/queries folder

### City based compensation query results
!(image.png)

### Gender based compensation query results
!(image-1.png)

### Engineer job based compensation query results
!(image-2.png)