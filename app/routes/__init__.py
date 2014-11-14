from app.routes.blog import blog
from app.routes.base import base
from app.routes.client import client

# note: silences pyflakes unused variables
assert (base,
        blog,
        client)
