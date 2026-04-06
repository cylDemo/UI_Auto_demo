import random
import string
from datetime import datetime, timedelta


def generate_random_email(domain: str = "example.com") -> str:
    username_length = random.randint(8, 16)
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=username_length))
    return f"{username}@{domain}"


def generate_random_password(length: int = 12, include_special: bool = True) -> str:
    chars = string.ascii_letters + string.digits
    if include_special:
        chars += "!@#$%^&*"
    return ''.join(random.choices(chars, k=length))


def generate_random_name(prefix: str = "", length: int = 8) -> str:
    name = ''.join(random.choices(string.ascii_lowercase, k=length))
    return f"{prefix}{name}" if prefix else name


def get_future_date(days: int = 30) -> str:
    return (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")


def get_past_date(days: int = 30) -> str:
    return (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")


def get_current_timestamp() -> int:
    return int(datetime.now().timestamp())


def format_date(date: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    return date.strftime(format_str)
