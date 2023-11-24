from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer as JsonWebToken

# JWT creation. #FIXME add a random every boot
jwt = JsonWebToken("top secret!", expires_in=3600)

# Refresh token creation.#FIXME add a random every boot
refresh_jwt = JsonWebToken("telelelele", expires_in=7200)

# Auth object creation.
auth = HTTPTokenAuth("Bearer")
