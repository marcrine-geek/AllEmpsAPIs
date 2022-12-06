## api endpoints
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


- /api/login
- /api/add/general/posts
- /api/add/channel
- /all/channels
- /api/follow/user
- /api/unfollow/user
- /api/all/user/posts
- /api/join/channel
- /api/all/channel/members
