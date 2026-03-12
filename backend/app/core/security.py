from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import jwt, JWTError

from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_access_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


def validate_password_strength(password: str) -> str | None:
    if len(password) < 8 or len(password) > 24:
        return "Password must be between 8 and 24 characters."

    if not re.search(r"[A-Z]", password):
        return "Password must contain at least 1 uppercase letter."

    if not re.search(r"[a-z]", password):
        return "Password must contain at least 1 lowercase letter."

    if not re.search(r"[0-9]", password):
        return "Password must contain at least 1 number."

    if not re.search(r"[!@#$%^&*()_\-+=\[{\]};:,.<>?/\\|`~'\"]", password):
        return "Password must contain at least 1 special character."

    return None
