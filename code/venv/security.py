from user import User
# Below the user file is accessed and the User class is retrieved

users =[
    # The following replaces that which is commented out below
# ****************
User(1, 'Bob', 'asdf')
#    {
#        'id': 1,
#        'username': 'bob',
#        'password': 'asdf'
#    }
# ****************
]

# The following replaces the username mapping below
# username_mapping = {u.username: u for u in users}

# ****************
# The following mappings are created to easily retrieve user information, given the name or id
# This is faster than looping through values.
# username_mapping = { 'bob': {
#        'id': 1,
#        'username': 'bob',
#        'password': 'asdf'
#    }
#}
# ****************

# The following replaces the id mapping below
# userid_mapping = {u.id: u for u in users}

# ****************
#userid_mapping = {1: {
#        'id': 1,
#        'username': 'bob',
#        'password': 'asdf'
#    }
# ****************
#}

# The following function is to authenticate a user given the username and password
def authenticate(username, password):
    # if no user with the given username, None is returned
    user = User.find_by_username(username)
    if user and user.password == password:
        return user

def identity(payload):
    user_id = payload['identity']
    return User.find_by_id(user_id)
