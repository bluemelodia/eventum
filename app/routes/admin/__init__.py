from admin import admin
from auth import auth
from events import events
from media import media
from posts import posts
from users import users
from whitelist import whitelist
from api import api

# note: silences pyflakes unused variables
assert (admin,
        auth,
        events,
        media,
        posts,
        users,
        whitelist,
        api)
