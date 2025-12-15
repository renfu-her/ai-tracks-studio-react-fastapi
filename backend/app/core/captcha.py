"""Simple in-memory image captcha utilities."""

from __future__ import annotations

import base64
import io
import random
import string
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict

from PIL import Image, ImageDraw, ImageFont


@dataclass
class CaptchaItem:
    """Captcha item with answer and expiration."""

    answer: str
    expires_at: datetime
    image_base64: str


_STORE: Dict[str, CaptchaItem] = {}
_TTL = timedelta(minutes=10)
_CAPTCHA_LEN = 6
_WIDTH, _HEIGHT = 150, 50


def _cleanup() -> None:
    """Remove expired captchas."""
    now = datetime.utcnow()
    expired_keys = [key for key, item in _STORE.items() if item.expires_at < now]
    for key in expired_keys:
        _STORE.pop(key, None)


def _random_text(length: int = _CAPTCHA_LEN) -> str:
    # Uppercase letters and digits without ambiguous characters
    chars = "ABCDEFGHJKMNPQRSTUVWXYZ23456789"  # exclude 0, O, I, L, 1
    return "".join(random.choices(chars, k=length))


def _generate_image(text: str) -> str:
    """Generate captcha image and return base64 data URL."""
    # Base image
    image = Image.new("RGB", (_WIDTH, _HEIGHT), (255, 255, 255))
    draw = ImageDraw.Draw(image)

    # Try to use a default PIL font
    try:
        font = ImageFont.load_default()
    except Exception:  # pragma: no cover
        font = None

    # Slightly randomize text position
    text_width, text_height = draw.textsize(text, font=font)
    x = (_WIDTH - text_width) / 2 + random.randint(-5, 5)
    y = (_HEIGHT - text_height) / 2 + random.randint(-3, 3)

    # Draw text with random color
    draw.text((x, y), text, fill=(random.randint(0, 120), random.randint(0, 120), random.randint(0, 120)), font=font)

    # Add noise lines
    for _ in range(6):
        start = (random.randint(0, _WIDTH), random.randint(0, _HEIGHT))
        end = (random.randint(0, _WIDTH), random.randint(0, _HEIGHT))
        draw.line([start, end], fill=(random.randint(100, 200), random.randint(100, 200), random.randint(100, 200)), width=1)

    # Save to base64
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    image_bytes = buffer.getvalue()
    base64_str = base64.b64encode(image_bytes).decode("utf-8")
    return f"data:image/png;base64,{base64_str}"


def generate_captcha() -> tuple[str, str]:
    """
    Generate an image captcha.

    Returns:
        captcha_id: Unique identifier
        image_base64: Captcha image in base64 data URL
    """
    _cleanup()
    text = _random_text()
    captcha_id = str(uuid.uuid4())
    image_base64 = _generate_image(text)
    _STORE[captcha_id] = CaptchaItem(
        answer=text,
        expires_at=datetime.utcnow() + _TTL,
        image_base64=image_base64,
    )
    return captcha_id, image_base64


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

    # Normalize answer (case-insensitive)
    user_ans = str(answer).strip().upper()
    if user_ans != item.answer:
        raise ValueError("Captcha answer is incorrect")

