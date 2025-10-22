from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

# Level calculation
LEVELS = {
    1: 0,
    2: 200,
    3: 500,
    4: 1000,
    5: 1700
}

def calculate_level(xp: int) -> int:
    level = 1
    for lvl, threshold in sorted(LEVELS.items(), key=lambda x: x[1]):
        if xp >= threshold:
            level = lvl
    return level
