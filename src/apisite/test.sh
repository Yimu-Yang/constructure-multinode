curl -XPOST http://localhost:8000/user/register/ -d'{"name":"我比较", "companyId": 1, "password": "123123123"}'

curl -XPOST http://localhost:8000/user/login/ -d'{"id": 6, "password": "123123123"}'

curl -XPOST http://localhost:8000/user/register/ -d'{"name":"大神", "companyId": 1, "password": "123123123"}'

curl -XPOST http://localhost:8000/user/register/ -d'{"name":"对方", "companyId": 1, "password": "123123123"}'

curl -XPOST http://localhost:8000/user/register/ -d'{"name":"爱迪生", "companyId": 1, "password": "123123123"}'

curl -XPOST http://localhost:8000/user/register/ -d'{"name":"全额的", "companyId": 1, "password": "123123123"}'

curl -XPOST http://localhost:8000/user/register/ -d'{"name":"奥德赛", "companyId": 1, "password": "123123123"}'

curl -XPOST http://localhost:8000/user/requestVerify/ --header 'token: 2d0fc51c2eb03e2fe96e09a37cf594' -d'{"requestVerifyUser": [7,8,9,10,11]}'

curl -XPOST http://localhost:8000/user/login/ -d'{"id": 7, "password": "123123123"}'

curl -XGET http://localhost:8000/user/getVerifyStatus/ --header 'token: b8e59afaeb6a4cc9355b980a58405e'

curl -XPOST http://localhost:8000/user/verifyUser/ --header 'token: b8e59afaeb6a4cc9355b980a58405e' -d'{"userId": 6}'



curl -XGET http://localhost:8000/user/searchWorker/?companyId=1 --header 'token: b8e59afaeb6a4cc9355b980a58405e' 

curl -XPOST http://localhost:8000/user/login/ -d'{"id": 11, "password": "123123123"}'

curl -XGET http://localhost:8000/user/getVerifyStatus/ --header 'token: 80fb2bb787c8de11475b8ca8dd1b43'

curl -XPOST http://localhost:8000/user/verifyUser/ --header 'token: 80fb2bb787c8de11475b8ca8dd1b43' -d'{"userId": 6}' 