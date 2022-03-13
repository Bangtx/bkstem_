import json
from fastapi import Request, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from jose import jwt
from urllib.request import urlopen
from jwcrypto import jwk

from config.setting import (
    AUTH_CACHE_TTL,
    TOKEN_GENERATION_KEY,
    AWS_COGNITO_REGION,
    AWS_COGNITO_USERPOOL_ID,
    AWS_COGNITO_USER_GROUP,
)
from .cache import get as get_cache
from .cache import set as set_cache
from i18n import t
from models.member import Member
from utils.aws import get_user_from_cognito


class AuthError(Exception):
    def __init__(self, error, status_code=401):
        self.error = error
        self.status_code = status_code


class Auth:
    def __init__(self):
        pass

    def __call__(
        self,
        request: Request,
        authorization: HTTPAuthorizationCredentials = Security(
            HTTPBearer(auto_error=False)
        ),
    ):

        if not authorization:
            raise HTTPException(
                403, detail=t("fmbiz.auth.errors.not_authenticated")
            )

        token = authorization.credentials
        payload = self.verify_token(token)

        # check user's group
        if (
            "cognito:groups" in payload
            and AWS_COGNITO_USER_GROUP not in payload["cognito:groups"]
        ):
            raise HTTPException(
                403, detail=t("fmbiz.auth.errors.not_authenticated")
            )

        user_info = get_user_from_cognito(token)
        member = Member.find_by_email(user_info["email"])
        if len(member) == 0:
            raise HTTPException(
                403, detail=t("fmbiz.auth.errors.member_not_found")
            )

        return member[0]

    def get_jwks_keys(self, jwks_uri: str, kid):
        # Check jwks in cache
        cache = get_cache("jwks-" + kid)
        key = json.loads(cache) if cache else cache

        if not key:
            jsonurl = urlopen(jwks_uri)
            jwks = json.loads(jsonurl.read())

            for _key in jwks["keys"]:
                # Save jwks to cache
                set_cache(
                    "jwks-" + _key["kid"], json.dumps(_key), AUTH_CACHE_TTL
                )
                if _key["kid"] == kid:
                    key = _key

        return key

    def decode_token(self, token: str, rsa_key: dict):
        issuer = (
            f"https://cognito-idp.{AWS_COGNITO_REGION}.amazonaws.com"
            f"/{AWS_COGNITO_USERPOOL_ID}"
        )
        try:
            return jwt.decode(
                token,
                rsa_key,
                algorithms=["RS256"],
                issuer=issuer,
            )

        except jwt.ExpiredSignatureError:
            raise AuthError(
                {
                    "code": "token_expired",
                    "description": t("fmbiz.auth.errors.token_expired"),
                },
                401,
            )

        except jwt.JWTClaimsError:
            raise AuthError(
                {
                    "code": "invalid_claims",
                    "description": t("fmbiz.auth.errors.invalid_claims"),
                },
                401,
            )

        except Exception:
            raise AuthError(
                {
                    "code": "invalid_header",
                    "description": t("fmbiz.auth.errors.invalid_header"),
                },
                401,
            )

    def verify_token(self, token: str):
        try:
            jwks_uri = (
                f"https://cognito-idp.{AWS_COGNITO_REGION}.amazonaws."
                f"com/{AWS_COGNITO_USERPOOL_ID}/.well-known/jwks.json"
            )

            unverified_header = jwt.get_unverified_header(token)
            key = self.get_jwks_keys(jwks_uri, unverified_header["kid"])

            if not key:
                raise AuthError(
                    {
                        "code": "invalid_header",
                        "description": t("fmbiz.auth.errors.invalid_header"),
                    },
                    401,
                )
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"],
            }
            return self.decode_token(token, rsa_key)
        except jwt.JWTError:
            raise AuthError(
                {
                    "code": "invalid_header",
                    "description": t("fmbiz.auth.errors.invalid_header"),
                },
                401,
            )


def generate_key(kid: str) -> dict:
    """Generate a JWK key with common options"""
    return json.loads(
        jwk.JWK.generate(kid=kid, kty="RSA", use="sig", alg="RS256").export()
    )


def generate_token(key=None, **kwargs):
    """Generate JWT token from a JWK key"""
    if key is None:
        key = json.loads(TOKEN_GENERATION_KEY)
    payload = {
        "iss": kwargs.pop(
            "iss",
            f"https://cognito-idp.{AWS_COGNITO_REGION}."
            f"amazonaws.com/{AWS_COGNITO_USERPOOL_ID}",
        ),
    }

    # For claims in public claims, add them to the payload directly
    public_claims = ["sub", "exp", "nbf", "iat", "jti", "scope"]
    for claim in public_claims:
        if claim in kwargs:
            payload[claim] = kwargs.pop(claim)

    # For claims in private claims
    for claim in kwargs:
        payload[claim] = kwargs[claim]

    return jwt.encode(
        payload,
        key,
        algorithm=key.get("alg", "RS256"),
        headers={"kid": key["kid"]},
    )
