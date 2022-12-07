## api endpoints

# POST
## register
`/api/register`

```json
requires
{
    "email":string,
    "password":string,
    "username":string,
    "firstname":string,
    "lastname":string
}
```
```json
response status 200
{
    "email": "user85@gmail.com",
    "message": "user registered successfully",
    "status": 200
}
```
```json
response status 400
{
    "message": "Unauthorized user",
    "status": 400
}
```

# POST
## login
`/api/ogin`
```json
requires
{
    "email":string,
    "password":string
}
```
```json
response status 200
{
    "message": "successful login",
    "email": "marc@gmail.com",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im1hcmNAZ21haWwuY29tIiwidXNlcmlkIjo2LCJleHAiOjE3MDE5NDA3NTl9.hry3Xzex7s6pPmkrBlfbcyGeTEBiPWz43CFr3Yebll4",
    "status": 200
}
```
```json
response status 400
{
    "message": "Unauthorized user",
    "status": 400
}
```

# POST
## add posts
`/api/add/post`
```json
requires
{
    "post":string,
    "channel_id":int
}
```
```json 
response status 200
{
    "message":"Message sent successfully",
    "status":200
}
```

# GET
## get all posts in specific channels
`/api/channel/posts`
```json
requires
{
    "channel_id":int
}
```
```json
response status 200
{
    "message": "all posts", 
    "data":[],
    "status":200
}
```
```json
response status 200
{
    "message":"there are no posts",
    "status":200
}
```

# POST
## follow user
`/api/follow/user`
```json
requires username as a parameter
{
    "username":string
}
```
```json
response status 200
{
    "message":"followed successfully",
    "status":200
}
```
```json
response status 400
{
    "message":"User not found",
    "status":400
}
```

# POST
## unfollow user
`/api/unfollow/user`
```json
requires username as a parameter
{
    "username":string
}
```
```json
response status 200
{
    "message":"Unfollowed successfully",
    "status":200
}
```
```json
response status 400
{
    "message":"User not found",
    "status":400
}
```

# GET
## all user's posts
`/api/all/user/posts`
```json
requires
{
    "user_id":int
}
```
```json
response status 200
{
    "message": "all posts", 
    "data":[],
    "status":200
}
```
```json
response status 200 when user has no posts
{
    "message":"no posts",
    "status":200
}
```
```json
response status 400
{
    "message":"please log in",
    "status":400
}
```

# POST
## join channel
`/api/join/channel`
```json
requires
{
    "user_id":int
}
```
```json
response status 200
{
    "message":"member added successfully",
    "status":200
}
```

# GET
## channel members
`/api/all/channel/members`
```json
requires
{
    "user_id":int
}
```
```json
response status 200
{
    "message":"members in the channel", 
    "data":[],
    "status":200
}
```

# GET
## User details
`/api/user/details`
```json
response status 200
{
    "message": "user details",
    "data": [
        "firstname",
        "lastname",
        "username",
        "email"
    ],
    "status":200
}
```
```json
response status 400
{
    "message":"user not authorized",
    "status":400
}
