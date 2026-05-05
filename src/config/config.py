# src/config/config.py
# GROUP: config
# DESCRIPTION: Central system configuration (Telegram + Core + future AI)

from dataclasses import dataclass

from src.config.base import get_env


@dataclass
class TelegramConfig:
    token: str
    webhook_secret: str


@dataclass
class Config:
    telegram: TelegramConfig


def load_config() -> Config:
    return Config(
        telegram=TelegramConfig(
            token=get_env("TELEGRAM_TOKEN"),
            webhook_secret=get_env("WEBHOOK_SECRET"),
        )
    )