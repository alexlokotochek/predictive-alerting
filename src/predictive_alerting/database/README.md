# 1. Setup mysql.

```docker run -p 3306:3306 --name mysql -e MYSQL_ROOT_PASSWORD=root -d mysql:5.7```

# 2. Initialize database and user.

2.1 ```docker exec -it mysql mysql -uroot -proot```

2.2 ```CREATE DATABASE predictive_alerting;```

2.3 ```CREATE USER 'banana'@'localhost' IDENTIFIED BY 'banana';```

2.4 ```GRANT ALL ON predictive_alerting.* TO 'banana'@'localhost';```

2.5 ```mysql_user=banana mysql_password=banana mysql_host=localhost mysql_db=predictive_alerting python3 init_db.py```

All tables from models should be created now, congrats!