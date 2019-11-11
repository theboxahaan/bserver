# bserver

## Get QR Query
```console
foo:bar theboxahaan$ curl -d '{"vendorid":"1234", "amount":"100", "tokenid":"11222"}' -H "Content-Type: application/json" -X POST http://localhost:5000/api/get_qr > response
```

## Login Query

```console
foo:bar theboxahaan$ curl -d '{"username" : "ahaand@iitbhilai.ac.in", "password":"1c54facba35fa70dbccf9def1e2f113470328983b8f06b6b71cfdd305afc7935"}' -H "Content-Type: application/json" -X POST http://localhost:5000/api/login
```


## Check Balance Query

```console
foo:bar theboxahaan$ curl -d '{"auth_token":"cc3cf681404ee89b67e85982864e5ae15cae086ddb933eff2b77d9ed0813890b"}' -H "Content-Type: application/json" -X POST http://localhost:5000/api/check_balance
```

## P2P Query
```console
foo:bar theboxahaan$ curl -d '{"auth_token":"cc3cf681404ee89b67e85982864e5ae15cae086ddb933eff2b77d9ed0813890b", "payee":"harshvardhanp@iitbhilai.ac.in", "amount":"2"}' -H "Content-Type: application/json" -X POST http://localhost:5000/api/p2p
```

--------

## LDAP.db Schema
```
sqlite> .schema ldap
CREATE TABLE LDAP(
EMAIL TEXT NOT NULL PRIMARY KEY,
NAME TEXT NOT NULL,
PWD_HASH TEXT NOT NULL,
CURRENT_TOKEN TEXT NOT NULL,
IS_ACTIVE INT , balance int);
```

### Data
