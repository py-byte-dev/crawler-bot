# Crawler Bot

**`crawler-bot`** is a telegram bot for parsing prices from websites via excel files.

This project was built as a test assignment, following the principles of **clean architecture and SOLID** for company TECHNESIS.

---

## Tech Stack

- Python 3.12
- Aiogram
- SQLite + SQLAlchemy
- bs4
- pandas
- Docker + Docker Compose

---

## Project Setup

1. **Create a configuration file based on the template:**
   ```bash
   cp .env.dist .env
   ```

2. **Edit the `.env` file and set the required environment variables:**
   ```env
   # Bot configuration
   BOT_TOKEN=your_bot_token
   
   #Database configuration
   DB_NAME=your_db_nane
   ```
3. **Create db on local host**
    ```
    touch your_db_name.db
    chmod 666 your_db_name.db
    ```

4. **Start the services using Docker Compose:**
   ```bash
   docker-compose up -d
   docker exec -it bot sh -c 'alembic upgrade head'
   ```

---


