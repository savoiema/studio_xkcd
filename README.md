# Studio XKCD Api
Small api to query XKCD comics that also includes favorites feature.
### Getting started
The current version of the API lives at http://example.com/api

#### Endpoints
This service provides 2 endpoint

|Endpoint|What it does|
|--------|------------|
|`/api/`|Returns an array of XKCD comics|
|`/api/favorites`|Returns an array of favorites|

#### Api Calls
Every request should contain a `X-User-ID` in the header, the value should be a unique UUID for this user. Requests can be made to the `/api/` endpoint with out the `X-User-ID` but will not contain any favorites. the favorites endpoint requires this parameter and will throw an error if no `X-User-ID` is provided

```http request
GET /api HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Host: example.com
User-Agent: HTTPie/1.0.2
X-User-ID: 40F6E3C9-06B8-468E-A908-1C6F3EB6B0F1
```

#### `/api/` Endpoint
##### Implementation Notes
this api returns an array of XKCD comics

* The max number of items to request at a time is 20
* The default number of results to return is 20
* If a `X-User-ID` is provided. Favorites already in place will will have `"is_favorite": true`

##### Parameters
* `/api/<num>`: will get 20 comics from XKCD in descending chronological order starting with the id provided
* `/api/?count`: you can limit the number of items returned with the count parameter, with in the limits provided above

##### Examples
###### GET - `/api/` - `http -v --pretty=format example.com/api 'X-User-ID:40F6E3C9-06B8-468E-A908-1C6F3EB6B0F1'`
```http request
{
    "count": 20,
    "next": 2091,
    "results": [
        {
            "alt": "Thanks for bringing us along.",
            "day": "13",
            "img": "https://imgs.xkcd.com/comics/opportunity_rover.png",
            "imgRetina": "https://imgs.xkcd.com/comics/opportunity_rover_2x.png",
            "is_favorite": false,
            "link": "",
            "month": "2",
            "news": "",
            "num": 2111,
            "safe_title": "Opportunity Rover",
            "title": "Opportunity Rover",
            "transcript": "",
            "year": "2019"
        }
        ... results abbreviated ...
    ]
}
```

###### GET - `/api/123` - `http -v --pretty=format example.com/api/123 'X-User-ID:40F6E3C9-06B8-468E-A908-1C6F3EB6B0F1'`
```http request
GET /api/123 HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Host: example.com
User-Agent: HTTPie/1.0.2
X-User-ID: 40F6E3C9-06B8-468E-A908-1C6F3EB6B0F1



HTTP/1.1 200 error
Connection: keep-alive
Content-Length: 15563
Content-Type: application/json
Date: Thu, 14 Feb 2019 19:34:29 GMT
Etag: "05453918f623814272885043cfccf46f4b942cac"
Server: nginx/1.14.0 (Ubuntu)

{
    "count": 20,
    "next": 103,
    "results": [
        {
            "alt": "You spin me right round, baby, right round, in a manner depriving me of an inertial reference frame.  Baby.",
            "day": "3",
            "img": "https://imgs.xkcd.com/comics/centrifugal_force.png",
            "is_favorite": false,
            "link": "",
            "month": "7",
            "news": "",
            "num": 123,
            "safe_title": "Centrifugal Force",
            "title": "Centrifugal Force",
            "transcript": "[[ Bond is tied to a giant centrifuge ]]\nHat Guy: Do you like my centrifuge, Mister Bond? When I throw the lever, you will feel centrifugal force crush every bone in your body.\nMr. Bond: You mean centripetal force. There's no such thing as centrifugal force.\nHat Guy: A laughable claim, Mister Bond, perpetuated by overzealous teachers of science. Simply construct Newton's laws into a rotating system and you will see a centrifugal force term appear as plain as day.\nMr. Bond: Come now, do you really expect me to do coordinate substitution in my head while strapped to a centrifuge?\nHat Guy: No, Mr. Bond. I expect you to die.\n{{ alt: You spin me right round, baby, right round, in a manner depriving me of an inertial reference frame.  Baby. }}",
            "year": "2006"
        }
        ... results abbreviated ...
    ]
}
```

###### GET - `/api/?count=1` - `http -v --pretty=format 'example.com/api/?count=1' 'X-User-ID:40F6E3C9-06B8-468E-A908-1C6F3EB6B0F1'`
```http request
GET /api/?count=1 HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Host: example.com
User-Agent: HTTPie/1.0.2
X-User-ID: 40F6E3C9-06B8-468E-A908-1C6F3EB6B0F1



HTTP/1.1 200 error
Connection: keep-alive
Content-Length: 397
Content-Type: application/json
Date: Thu, 14 Feb 2019 19:36:28 GMT
Etag: "a874519912ada21a8b50b1472cc0d12a426124c5"
Server: nginx/1.14.0 (Ubuntu)

{
    "count": 1,
    "next": 2110,
    "results": [
        {
            "alt": "Thanks for bringing us along.",
            "day": "13",
            "img": "https://imgs.xkcd.com/comics/opportunity_rover.png",
            "imgRetina": "https://imgs.xkcd.com/comics/opportunity_rover_2x.png",
            "is_favorite": false,
            "link": "",
            "month": "2",
            "news": "",
            "num": 2111,
            "safe_title": "Opportunity Rover",
            "title": "Opportunity Rover",
            "transcript": "",
            "year": "2019"
        }
    ]
}
```


#### `/api/favorites` Endpoint
##### Implementation Notes
Gets, Creates, and deletes entries in the users favorites.

this endpoint requires the user to pass in the `X-User-ID` with a valid version 4 `UUID`.

* `GET`: returns an array of id's that are in the user's favorites
* `POST`: creates new favorite entries for this UUID
* `DELETE`: deletes an entry in the user favorites

##### Parameters
When querying the user's favorites you can request details. this will query XKCD and get the information for this favorite
* `/api/favorites/?details=true`: will return the users favorites with detailed information

##### Examples

###### GET - `/api/favorites` - `http -v --pretty=format 'example.com/api/favorites' 'X-User-ID:40F6E3C9-06B8-468E-A908-1C6F3EB6B0F1'`
```http request
GET /api/favorites HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Host: example.com
User-Agent: HTTPie/1.0.2
X-User-ID: 40F6E3C9-06B8-468E-A908-1C6F3EB6B0F1



HTTP/1.1 200 error
Connection: keep-alive
Content-Length: 31
Content-Type: application/json
Date: Sat, 23 Feb 2019 18:45:57 GMT
Etag: "e763f5aed375c83ab2ad60bd98e78754a21c18ec"
Server: nginx/1.14.0 (Ubuntu)

{
    "count": 1,
    "results": [
        1234
    ]
}
```
###### GET with details - `/api/favorites/?detailed=true` - `http -v --pretty=format 'example.com/api/favorites/?detailed=true' 'X-User-ID:40F6E3C9-06B8-468E-A908-1C6F3EB6B0F1'`
```http request
GET /api/favorites/?detailed=true HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Host: example.com
User-Agent: HTTPie/1.0.2
X-User-ID: 40F6E3C9-06B8-468E-A908-1C6F3EB6B0F1



HTTP/1.1 200 error
Connection: keep-alive
Content-Length: 1584
Content-Type: application/json
Date: Sat, 23 Feb 2019 19:18:32 GMT
Etag: "d80ba244d04d010a99dc3dc6aaa7861e06c21d7d"
Server: nginx/1.14.0 (Ubuntu)

{
    "count": 1,
    "results": [
        {
            "alt": "Actual quote from The Demo: '... an advantage of being online is that it keeps track of who you are and what you’re doing all the time ...'",
            "day": "5",
            "img": "https://imgs.xkcd.com/comics/douglas_engelbart_1925_2013.png",
            "imgRetina": "https://imgs.xkcd.com/comics/douglas_engelbart_1925_2013_2x.png",
            "link": "",
            "month": "7",
            "news": "",
            "num": 1234,
            "safe_title": "Douglas Engelbart (1925-2013)",
            "title": "Douglas Engelbart (1925-2013)",
            "transcript": "San Francisco, December 9th, 1968: \n[[We see a figure talking into a headset. It's a fair assumption that it's Douglas Engelbart.]]\nDouglas: ... We generated video signals with a cathode ray tube... We have a pointing device we call a \"mouse\"... I can \"copy\" text... ... and we have powerful join file editing... underneath the file here we can exchange \"direct messages\"...\n\n[[Douglas continues to narrate. Some music is playing.]]\nDouglas: ... Users can share files... ... files which can encode audio samples, using our \"masking codecs\"... The file you're hearing now is one of my own compositions...\nMusic: I heard there was a secret chord\n\n[[Douglas continues to narrate.]]\nDouglas: ... And you can superimpose text on the picture of the cat, like so... This cat is saying \"YOLO\", which stands for \"You Only Live Once\"... ...Just a little acronym we thought up...\n\n{{Title text: Actual quote from The Demo: '... an advantage of being online is that it keeps track of who you are and what youâre doing all the time ...'}}",
            "year": "2013"
        }
    ]
}
```
###### POST - `/api/favorites` - `http -v --pretty=format POST 'example.com/api/favorites' num=1234 'X-User-ID:40F6E3C9-06B8-468E-A908-1C6F3EB6B0F1'`
```http request
POST /api/favorites HTTP/1.1
Accept: application/json, */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 15
Content-Type: application/json
Host: example.com
User-Agent: HTTPie/1.0.2
X-User-ID: 40F6E3C9-06B8-468E-A908-1C6F3EB6B0F1

{
    "num": "1234"
}

HTTP/1.1 200 error
Connection: keep-alive
Content-Length: 91
Content-Type: application/json
Date: Sat, 23 Feb 2019 18:44:40 GMT
Server: nginx/1.14.0 (Ubuntu)

{
    "results": {
        "id": 16,
        "user_id": "40f6e3c9-06b8-468e-a908-1c6f3eb6b0f1",
        "xkcd_id": 1234
    }
}
```
###### DELETE - `/api/favorites` - `http -v --pretty=format DELETE 'example.com/api/favorites/1234' 'X-User-ID:40F6E3C9-06B8-468E-A908-1C6F3EB6B0F1'`
```http request
DELETE /api/favorites/1234 HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 0
Host: example.com
User-Agent: HTTPie/1.0.2
X-User-ID: 40F6E3C9-06B8-468E-A908-1C6F3EB6B0F1



HTTP/1.1 200 error
Connection: keep-alive
Content-Length: 78
Content-Type: application/json
Date: Sat, 23 Feb 2019 19:20:23 GMT
Server: nginx/1.14.0 (Ubuntu)

{
    "id": 16,
    "user_id": "40f6e3c9-06b8-468e-a908-1c6f3eb6b0f1",
    "xkcd_id": 1234
}
```


