Simple resources API
====================================

Run
-----------
1. Clone repository.
2. Run following command:
```bash
docker-compose up --build
```
3. For run tests:
```bash
docker-compose run api test.sh
```

Swagger
-----------
Swagger is available on endpoint http://localhost:8000/api/swagger. Also schema and redoc are available 
on following endpoints: http://localhost:8000/api/swagger.(json|yaml) http://localhost:8000/api/redoc.

Registration and authorization
-----------
Admin should be created using command:
```bash
docker-compose run api ./manage.py createsuperuser
```
JWT token is used in authorization header, e.g. ```Authorization: Bearer <Token>```.
User can be register via endpoint http://localhost:8000/api/v1/register by email and password.
```bash
curl -X POST http://localhost:8000/api/v1/register \
    -H 'Content-Type: application/json' \
    -d '{"email": "example@test.com", "password": "qweasdzxc123!"}'
{"id":8,"email":"example@test.com"}
```
Endpoint http://localhost:8000/api/v1/login is used to obtain JWT token.
```bash
curl -X POST http://localhost:8000/api/v1/login \
    -H 'Content-Type: application/json' \
    -d '{"email": "example@test.com", "password": "qweasdzxc123!"}'
{"refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTU3OTE3MjAzMiwianRpIjoiYWU0Njg5MDg5ZjVkNDg0ZWFmMTUwNDYxY2JiOWY4NDkiLCJ1c2VyX2lkIjo4fQ.Q5ycaYdi-4RAR-Y-bWOz0HUyJ9eiKXnO7MjjTRVfmhY", "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTc5MDg1OTMyLCJqdGkiOiIwNDg2ZTBjMzQ2N2Y0ODgzOTQzY2I1M2ZmMzhiMjNmMCIsInVzZXJfaWQiOjh9.nOX3h3mhdx6etNIllbE9qfJnxOPSb4Rbm0wXb_EVUVA"}
```
Admin can manage users info via endpoint http://localhost:8000/api/v1/users.
```bash
curl -X GET http://localhost:8000/api/v1/users \
    -H 'Content-Type: application/json' \
    -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTc5MDg1OTkzLCJqdGkiOiJmZGQ2YTA2NmQ0OTM0MDk4YWYyYTVjZGU1YmQ5M2RkNSIsInVzZXJfaWQiOjd9.oZv7wUhWhZrmB8JwP_T7vgTzfE9mH0eo6KPlGFxSpJg'
[{"id":1,"email":"test@test.test","first_name":"","last_name":"","is_staff":false},{"id":3,"email":"test-3@test.test","first_name":"","last_name":"","is_staff":false},{"id":6,"email":"admin2@admin.ru","first_name":"","last_name":"","is_staff":true},{"id":7,"email":"admin3@admin.admin","first_name":"","last_name":"","is_staff":true},{"id":8,"email":"example@test.com","first_name":"","last_name":"","is_staff":false}]
```
Common user can see own info via endpoint http://localhost:8000/api/v1/users/me.
```bash
curl -X GET http://localhost:8000/api/v1/users/me \
    -H 'Content-Type: application/json' \
    -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTc5MDg1OTMyLCJqdGkiOiIwNDg2ZTBjMzQ2N2Y0ODgzOTQzY2I1M2ZmMzhiMjNmMCIsInVzZXJfaWQiOjh9.nOX3h3mhdx6etNIllbE9qfJnxOPSb4Rbm0wXb_EVUVA'
{"id":8,"email":"example@test.com","first_name":"","last_name":""}
```

Main endpoints
-----------
1. ```/register``` - register new user.
2. ```/login``` - obtain JWT token.
3. ```/users``` - user management, allowed is only for admin.
4. ```/users/me``` - get current user data.
5. ```/quotas``` - user quotas management, allowed is only for admin.
6. ```/resources``` - resource management.
