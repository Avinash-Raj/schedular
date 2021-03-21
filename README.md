# Event Schedular Backend
Backend of a schedular app used to allocate/scedule a meeting with an employee by checking his/her available time.

### How to run?

Single compose command will do the work for you. 

```sh
docker-compose up
```

Browse `http://localhost:8000/swagger` to see the list of available api endpoints.

### Default User

Created a default test user with admin role in-order to test the avialble endpoints.
Just use the below credentials on login endpoint to generate authtoken. 

```
"email": "admin@stickboy.com",
"password": "admin"
```


Here is the postman collections url to test the endpoints manually.

https://www.postman.com/collections/43347c4c5c4158cd70b0