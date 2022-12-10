## api endpoints

# POST
## register
### tested
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
### tested
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
### requires token
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
requires query parameter id
{
    "channel_id = request.args.get('id')"
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
### requires token
`/api/follow/user`
```json
requires username
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
### requires token
`/api/unfollow/user`
```json
requires username
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
### requires token
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
### requires token
#### tested
`/api/join/channel`
```json
requires
{
    "channel_name": string
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
### requires token
#### tested
`/api/all/channel/members`
```json
requires query parameter
{
    "channel_name = request.args.get('channel_name')"
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
### requires token
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
```

# POST
## file or image upload endpoint
### tested
`/fileupload`


# GET
## get all channels
### tested
`/api/all/channels`
```json
no requirements
response status 200
{
    "message": "all posts",
    "data":[],
    "status":200
}
```