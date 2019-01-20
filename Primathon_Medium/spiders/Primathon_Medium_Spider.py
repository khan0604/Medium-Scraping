# -*- coding: utf-8 -*-
import os
import scrapy
from w3lib.html import remove_tags
import mysql.connector


class PrimathonMediumSpiderSpider(scrapy.Spider):
    name = 'Primathon_Medium_Spider'


    def __init__(self):
        script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
        rel_path = "../../input.txt"
        abs_file_path = os.path.join(script_dir, rel_path)
        with open(abs_file_path) as f:
            self.start_urls = [url.strip() for url in f.readlines()]

    def connection(self):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="test",
            database="mydatabase"
        )
        return mydb

    def print_scrapped_data(self, response):
        print remove_tags(response.css('h1').extract_first())
        print remove_tags(response.css('.elevate-summary').extract_first())
        print remove_tags(response.css('.js-multirecommendCountButton').extract_first())
        print remove_tags(response.css('.ui-h2').extract_first())
        print remove_tags(response.css('p.ui-summary').extract_first())
        print remove_tags(response.css('span.u-noWrap:nth-child(1) > time:nth-child(1)').extract_first())


    def initialize_variables(self, response):
        title = remove_tags(response.css('h1').extract_first())
        subtitle= remove_tags(response.css('.elevate-summary').extract_first())
        claps = remove_tags(response.css('.js-multirecommendCountButton').extract_first())
        author = remove_tags(response.css('.ui-h2').extract_first())
        author_bio = remove_tags(response.css('p.ui-summary').extract_first())
        post_date = remove_tags(response.css('span.u-noWrap:nth-child(1) > time:nth-child(1)').extract_first())

        extract_content = response.css('div.section-inner:nth-child(2)').extract()
        content=""
        for para in extract_content:
            content += remove_tags(para)

        extract_time = response.css('span.u-noWrap:nth-child(1) > span:nth-child(3)').extract_first()
        read_time=""
        for i in range(len(extract_time)):
            if i>=33 and i<38:
                read_time +=extract_time[i]

        extract_imgurl= response.css('.elevateCover-image').extract_first()
        img_url=""
        if extract_imgurl:
          for i in range(len(extract_imgurl)):
            if i >= 62 and i < 132:
                img_url += extract_imgurl[i]
        return title, subtitle, content, img_url, claps, author, author_bio, post_date, read_time;

    def create_table(self, mydb):
        cursor = mydb.cursor()
        cursor.execute("SHOW TABLES")
        check = 0
        for x in cursor:
            check += 1

        if check > 0:
            print("Table Exists")
        else:
            cursor.execute("CREATE TABLE medium (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), subtitle VARCHAR(255), content TEXT, image_url VARCHAR(255),numberof_claps VARCHAR(255), author VARCHAR(255), author_bio VARCHAR(255), post_creation_date VARCHAR(255), blog_reading_time VARCHAR(255)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4")
            print("Table Created")

    def store_in_database(self, response, mydb):
        title, subtitle, content, img_url, claps, author, author_bio, post_date, read_time = self.initialize_variables(response)
        cursor = mydb.cursor()
        sql = "SELECT * FROM medium WHERE title = %s"
        val = (title,)
        cursor.execute(sql, val)
        result = cursor.fetchall()
        count = 0
        for x in result:
            count += 1
        if count > 0:
            sql = "UPDATE medium SET subtitle = %s, content= %s , image_url= %s , numberof_claps= %s , author = %s , author_bio = %s ,post_creation_date = %s , blog_reading_time = %s WHERE title = %s"
            val = (subtitle, content, img_url, claps, author, author_bio, post_date, read_time, title)
            cursor.execute(sql, val)
            mydb.commit()
        else:
            sql = "INSERT INTO medium (title, subtitle, content, image_url, numberof_claps, author, author_bio,post_creation_date, blog_reading_time) VALUES (%s, %s,%s, %s,%s, %s,%s, %s,%s)"
            val = (title, subtitle, content, img_url, claps, author, author_bio, post_date, read_time)
            cursor.execute(sql, val)
            mydb.commit()

    def print_from_database(self, mydb):
        cursor = mydb.cursor()
        cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = 'mydatabase' AND TABLE_NAME = 'medium'")
        result = cursor.fetchall()
        print result

        cursor.execute("SELECT * FROM medium")
        result = cursor.fetchall()
        for x in result:
            print (x)

    def parse(self, response):

        # function to connect with mysql database
        mydb = self.connection()

        # function to print scrapped data
        self.print_scrapped_data(response)

        # function to create table medium in database
        self.create_table(mydb)

        # function to store scrapped data in mysql database
        self.store_in_database(response, mydb)

        # function to print data stored in mysql database
        self.print_from_database(mydb)











