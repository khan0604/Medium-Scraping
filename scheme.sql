CREATE TABLE medium (
       id INT AUTO_INCREMENT PRIMARY KEY,
       title VARCHAR(255),
       subtitle VARCHAR(255),
       content TEXT,
       image_url VARCHAR(255),
       numberof_claps VARCHAR(255),
       author VARCHAR(255),
       author_bio VARCHAR(255),
       post_creation_date VARCHAR(255),
       blog_reading_time VARCHAR(255)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4)
