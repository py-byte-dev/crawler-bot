from dataclasses import dataclass, field
from os import environ as env


@dataclass(slots=True)
class BotConfig:
    token: str = field(default_factory=lambda: env.get('BOT_TOKEN').strip())


@dataclass(slots=True)
class DBConfig:
    db_name: str = field(default_factory=lambda: env.get('DB_NAME').strip())

    def create_connection_string(self) -> str:
        return f'sqlite+aiosqlite:////app/{self.db_name}'


@dataclass(slots=True)
class Config:
    bot: BotConfig = field(default_factory=BotConfig)
    db: DBConfig = field(default_factory=DBConfig)
