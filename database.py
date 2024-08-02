from sqllex import SQLite3x, TEXT, REAL, NOT_NULL, UNIQUE

db = SQLite3x(
    path='users',
    template={
        "users": {
            "userid": [TEXT, NOT_NULL, UNIQUE],
            "percent": [REAL, NOT_NULL],
            "tax": [REAL, NOT_NULL],
            "earned": [REAL, NOT_NULL]
        }
    }
)

users = db['users']
userid = users['userid']