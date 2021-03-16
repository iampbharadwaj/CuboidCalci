# CuboidCalci

You can use the REST-based API using the following URL for Cuboid calculation:

#### URL:                                  
http://< web-server-ip >/               
- http://85.215.232.182/ 
 [ The IP address is the assigned IP for the web server, which can be used for testing. ]

#### Description:
REST API  endpoint

## HTTP Status Code:
Below are the possible HTTP Status Code that would be generated based on the request issued.

200 OK.  -    Synchronous request was successful using GET. 200 will also be returned for successful synchronous POST requests that do not result in item creation.

400 Bad Request -  Response to malformed requests or general client errors.

404 Not Found -   Resource does not exist.

### Testing the Endpoint

For checking the endpoint of the API, the request could be placed as shown in the following example.

Curl Example:

```
$curl -i -X GET http://85.215.232.182/

HTTP/1.1 200 OK
Date: Tue, 16 Mar 2021 13:44:09 GMT
Server: Apache/2.4.29 (Ubuntu)
Content-Length: 37
Vary: Accept-Encoding
Content-Type: text/html; charset=utf-8

Welcome to the Cuboid Calculator Page
```

### Calculation on Cuboid Edges:

In order to perform operation on the Cuboid edges to calculate the surface area, volume and sum of all the edges, below REST  
API can be queried with POST request.

#### URL:
- http://85.215.232.182/cuboid/calculate       

#### Description:
REST API for query to perform calculation on cuboid edges and write it to mysql database.

Curl Example:
```
$curl -d  { “cuboid_edges”: [33,44,55] } -i -X POST http://85.215.232.182/cuboid/calculate

HTTP/1.1 200 OK
Date: Tue, 16 Mar 2021 13:45:09 GMT
Server: Apache/2.4.29 (Ubuntu)
Content-Length: 37
Vary: Accept-Encoding
Content-Type: text/html; charset=utf-8

{
	“data”: {
		“sum_of_edges”: 528.0,
		“surface_area”: 11374.0,
		“volume”: 79860.0
	},
	“error”: null,
	“success”: true
}
```

### Result of Cuboid Calculator:

The REST API  to fetch the result of the calculation of Cuboid edges can be performed using following API, which gives the result history of entries from the database.

#### URL:
- http://85.215.232.182/cuboid/result

#### Description:
REST API for query the results of calculation performed on cuboid edges and get stored result from the database.
   
Curl Example:
``` 
$curl -i -X GET http://85.215.232.182/cuboid/result

HTTP/1.1 200 OK
Date: Tue, 16 Mar 2021 13:45:10 GMT
Server: Apache/2.4.29 (Ubuntu)
Content-Length: 1190
Content-Type: application/json

{"data":[{"height":12.0,"id":1,"length":12.0,"sum_of_edges":144.0,"surface_area":864.0,"timestamp":"2021-03-14 15:34:49","volume":1728.0,"width":12.0},{"height":12.0,"id":2,"length":12.0,"sum_of_edges":145.33,"surface_area":879.957,"timestamp":"2021-03-14 15:35:45","volume":1775.871,"width":12.332},{"height":120.0,"id":3,"length":120.0,"sum_of_edges":1452.0,"surface_area":87840.0,"timestamp":"2021-03-14 15:38:12","volume":1771200.0,"width":123.0},{"height":120.0,"id":4,"length":120.0,"sum_of_edges":964.0,"surface_area":29280.0,"timestamp":"2021-03-14 15:44:35","volume":14400.0,"width":1.0},{"height":110.0,"id":5,"length":110.0,"sum_of_edges":924.0,"surface_area":29040.0,"timestamp":"2021-03-15 11:23:17","volume":133100.0,"width":11.0},{"height":3.0,"id":6,"length":2.0,"sum_of_edges":36.0,"surface_area":52.0,"timestamp":"2021-03-15 13:57:18","volume":24.0,"width":4.0},{"height":4.0,"id":7,"length":3.0,"sum_of_edges":48.0,"surface_area":94.0,"timestamp":"2021-03-15 13:58:28","volume":60.0,"width":5.0},{"height":44.0,"id":8,"length":33.0,"sum_of_edges":528.0,"surface_area":11374.0,"timestamp":"2021-03-15 16:51:58","volume":79860.0,"width":55.0}],"error":null,"success":true}
```

### Listing the last 'n' created entries in the database 

The below mentioned REST API  is to fetch the given number of entries stored as result  based on previous entires stored in the database for the calculation performed on the Cuboid edges.

#### URL:
- http://85.215.232.182/cuboid/result/< number >

#### Description:
REST API to query the number of entries of the results  stored  in the database for the calculation performed on cuboid edges.

Curl Example:
```
$curl -i -X GET http://85.215.232.182/cuboid/result/3

HTTP/1.1 200 OK
Date: Tue, 16 Mar 2021 14:04:46 GMT
Server: Apache/2.4.29 (Ubuntu)
Content-Length: 454
Content-Type: application/json

{"data":[{"height":44.0,"id":8,"length":33.0,"sum_of_edges":528.0,"surface_area":11374.0,"timestamp":"2021-03-15 16:51:58","volume":79860.0,"width":55.0},{"height":4.0,"id":7,"length":3.0,"sum_of_edges":48.0,"surface_area":94.0,"timestamp":"2021-03-15 13:58:28","volume":60.0,"width":5.0},{"height":3.0,"id":6,"length":2.0,"sum_of_edges":36.0,"surface_area":52.0,"timestamp":"2021-03-15 13:57:18","volume":24.0,"width":4.0}],"error":null,"success":true}
```
