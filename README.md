# auth
authorization/authentication API on FLASK

# RUN

1. write your **email** and **password** in .env file
2. run commands below to build image and run container

```
docker build -t myflaskapp .
docker run -p 5000:5000 myflaskapp
```
# Usage
Requests:

1. POST request for registration:
```
curl -i -X POST -H "Content-Type: application/json" -d "{\"name\":\"username\", \"email\" : \"email@gmail.com\", \"password\":\"123\"}" http://localhost:5000/auth/users/create
```
2. POST request for login:
```
curl -i -X POST -H "Content-Type: application/json" -d "{\"email\" : \"email@gmail.com\", \"password\":\"123\"}" http://localhost:5000/auth/users/token
```
3. Get request to verify email: 
```curl http://localhost:5000/auth/users/verify/<token>``` you will recieve link on your email after registration request
