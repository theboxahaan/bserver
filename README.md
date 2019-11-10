# bserver

## Get QR Query
```
curl -d '{"vendorid":"1234", "amount":"100", "tokenid":"11222"}' -H "Content-Type: application/json" -X POST http://localhost:5000/api/get_qr > response
```

## Login Query

```
curl -d '{"username" : "ahaand@iitbhilai.ac.in" , "password":"5bb03619cfece3e85fe9b5a500a2f4743ed3e09fd0440abbe07baf21e4f8c57d"}' -H "Content-Type: application/json" -X POST http://localhost:5000/api/login
```
