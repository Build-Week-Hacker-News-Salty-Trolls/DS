## Project: Hacker News Saltines
## Product Vision: [PV Document](https://www.notion.so/mkirby/Product-Vision-Document-65e4fa49eb8c4b52beb0a4388f13d097)
---

### ML-Engineers: Harsh Desai, Nick Burkhalter

## ETL Pipeline

![Data Pipeline Flow](img/Data%20Pipeline%20Flow.png)

## Flask API Endpoints

BASE URL = `https://salty-salt.herokuapp.com`

1. Top 100 Salty Users
Returns top 100 
GET: `https://salty-salt.herokuapp.com/salty-users` 

Returns: 
![Top 100 Salty Users](img/salty_comments.png)


2. Top 100 Salty Comments

GET: `https://salty-salt.herokuapp.com/salty-comments` 

Returns: 
![Top 100 Salty Users](img/salty_users.png)

3. Most Saltiest Comments of a User

GET: `https://salty-salt.herokuapp.com/user-comments/wnight` 

Returns:
![Top 100 Salty Users](img/user_comments.png)