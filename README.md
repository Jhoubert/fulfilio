# Fulfill test

#### Description

There is my solution of the challenge.

#### Stack

This project was written in Python, usign flask as framework and PostgreSql as Database, All stack mentioned below.

+ Python
    + Flask
    + Blueprints
    + Celery
    + SqlAlchemy
    + APISpec
    + Marshmallow
+ PostgreSQL
+ Docker / Docker-compose
+ JWT
+ Swagger documentation yml and schemas bassed.
+ RabbitMQ


#### Docs
I've implemented a swagger documentation in order to be easy to use or test, all the swagger data is provided by schemas used for create or return data, so is really trustable source of guidance.

The endpoint of swagger documentation for this project is `api/v1/docs` when the project is running you can open in your browser [http://localhost/api/v1/docs/]

-------
### Running
   
For running the app you only needs to have docker with docker-compose already installed.
There is no extra script or SQL required to run for deploy database nor any component. 
all is easy configurable from docker-compose, all the available configurations detailed bellow.


    DEFAULT_APP_USER = Set the default user to login on the app, leave empty if you do not want a default user.
    DEFAULT_APP_PASSWORD = Set the default user password to login.

_NOTE:You also can set your own database information using the environment variables in the postgresql section and backend section as well. just ensure the data is same because if is not it may fails._


When you have all your configuration done you now can run the project using docker-compose

`docker-compose up`


NOTE: In the file `fulfilio.postman_collection.json` you can find a postman collection to test uploading file and checking the progress with another one endpoint.


[http://localhost/api/v1/docs/]: http://localhost/api/v1/docs/