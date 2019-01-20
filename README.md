# Medium Artices Scrapper

#### Dependency

* Scrapy - [Installation](https://doc.scrapy.org/en/latest/intro/install.html) 
* Python 2.7
* MySQL

#### Database Connection

* The connection of MySQL database requires authorization of localhost
```
mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="test",
            database="mydatabase"
        )
```
##### NOTE - Make sure that localhost username and password are same as above. 
* In case they are not same then either 
  - change them according to the code above  
  - change the above code in the [file](https://github.com/khan0604/Medium-Scraping/blob/master/Primathon_Medium/spiders/Primathon_Medium_Spider.py) according to your system 
  
# RUN
* To run the medium scrapper use 
``` python main.py ```

# MAIN FILE
* [Primathon_Medium_Spider.py](https://github.com/khan0604/Medium-Scraping/blob/master/Primathon_Medium/spiders/Primathon_Medium_Spider.py) - The code for scrapping is coded in this file
