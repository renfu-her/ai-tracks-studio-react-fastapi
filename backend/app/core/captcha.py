"""Simple in-memory captcha utilities (math-based)."""

from __future__ import annotations

import random
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict


@dataclass
class CaptchaItem:
    """Captcha item with answer and expiration."""

    answer: int
    expires_at: datetime
    question: str


_STORE: Dict[str, CaptchaItem] = {}
_TTL = timedelta(minutes=10)


def _cleanup() -> None:
    """Remove expired captchas."""
    now = datetime.utcnow()
    expired_keys = [key for key, item in _STORE.items() if item.expires_at < now]
    for key in expired_keys:
        _STORE.pop(key, None)


def generate_captcha() -> tuple[str, str]:
    """
    Generate a simple math captcha.

    Returns:
        captcha_id: Unique identifier
        question: Question text to display
    """
    _cleanup()
    a, b = random.randint(1, 9), random.randint(1, 9)
    answer = a + b
    captcha_id = str(uuid.uuid4())
    question = f"{a} + {b} = ?"
    _STORE[captcha_id] = CaptchaItem(
        answer=answer,
        expires_at=datetime.utcnow() + _TTL,
        question=question,
    )
    return captcha_id, question


def validate_captcha(captcha_id: str, answer: str | int) -> None:
    """
    Validate a captcha answer.

    Raises:
        ValueError: If invalid, expired, or not found.
    """
    _cleanup()
    item = _STORE.pop(captcha_id, None)
    if not item:
        raise ValueError("Invalid or expired captcha")

    # Normalize answer
    try:
        user_ans = int(str(answer).strip())
    except Exception:
        raise ValueError("Invalid captcha answer")

    if user_ans != item.answer:
        raise ValueError("Captcha answer is incorrect")

