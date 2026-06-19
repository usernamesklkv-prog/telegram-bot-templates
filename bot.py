import asyncio
import logging
import os
import time
from urllib.parse import urlencode

from dotenv import load_dotenv
from telegram import Update
from telegram.error import NetworkError, RetryAfter, TimedOut
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.request import HTTPXRequest

load_dotenv()
logging.basicConfig(
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.INFO,
)
VALID_TEMPLATES = {"1", "2", "3", "4"}
DEFAULT_BOT_TOKEN = "8708862445:AAFt1lMGw8s3f75VXkIOCrAsQzLkwZeAZ5w"
DEFAULT_BASE_URL = "https://usernamesklkv-prog.github.io/telegram-bot-templates"
PYTHONANYWHERE_PROXY = "http://proxy.server:3128"
TEMPLATE_DESCRIPTIONS = {
    "1": "Billions Network (BILL)",
    "2": "LayerZero (ZRO)",
    "3": "Kite AI (KITE)",
    "4": "Aave (AAVE)",
}


def _is_number_like(value: str) -> bool:
    normalized = value.replace(",", "").replace(" ", "")
    if not normalized:
        return False
    if normalized.count(".") > 1:
        return False
    if normalized.startswith("-"):
        normalized = normalized[1:]
    return normalized.replace(".", "", 1).isdigit()


def _build_link(
    template_id: str,
    end: str,
    total: str,
    participants: str,
    my: str,
    duration: str | None = None,
    asof: str | None = None,
) -> str:
    params = {
        "end": end,
        "total": total,
        "participants": participants,
        "my": my,
    }
    if duration:
        params["duration"] = duration
    if asof:
        params["asof"] = asof
    query = urlencode(params)
    base_url = os.getenv("TEMPLATE_BASE_URL", DEFAULT_BASE_URL).strip().rstrip("/")
    return f"{base_url}/templates/{template_id}.html?{query}"


def _is_pythonanywhere() -> bool:
    home = os.getenv("HOME", "").lower()
    return (
        "pythonanywhere" in home
        or bool(os.getenv("PYTHONANYWHERE_DOMAIN"))
        or bool(os.getenv("PYTHONANYWHERE_SITE"))
    )


def _proxy_url() -> str | None:
    explicit = os.getenv("TELEGRAM_PROXY_URL", "").strip()
    if explicit.lower() in {"none", "false", "0", "direct"}:
        return None
    if explicit:
        return explicit
    for key in ("HTTP_PROXY", "http_proxy", "HTTPS_PROXY", "https_proxy"):
        value = os.getenv(key, "").strip()
        if value:
            return value
    if _is_pythonanywhere():
        return PYTHONANYWHERE_PROXY
    return None


def _make_request(proxy: str | None) -> HTTPXRequest:
    kwargs: dict = {
        "connect_timeout": 30.0,
        "read_timeout": 30.0,
        "write_timeout": 30.0,
        "pool_timeout": 30.0,
        "httpx_kwargs": {"trust_env": False},
    }
    if proxy:
        kwargs["proxy"] = proxy
    return HTTPXRequest(**kwargs)


def _build_application(token: str) -> Application:
    proxy = _proxy_url()
    if proxy:
        logging.info("Using proxy: %s", proxy)
    request = _make_request(proxy)
    updates_request = _make_request(proxy)
    return (
        Application.builder()
        .token(token)
        .request(request)
        .get_updates_request(updates_request)
        .build()
    )

async def _reply_with_retry(update: Update, text: str, max_attempts: int = 5) -> None:
    if not update.message:
        return

    delay = 2.0
    for attempt in range(1, max_attempts + 1):
        try:
            await update.message.reply_text(text)
            return
        except RetryAfter as exc:
            await asyncio.sleep(float(exc.retry_after) + 1.0)
        except (NetworkError, TimedOut) as exc:
            if attempt >= max_attempts:
                logging.error("Failed to send message after %s attempts: %s", max_attempts, exc)
                return
            logging.warning(
                "Send failed (attempt %s/%s): %s. Retrying in %.0fs...",
                attempt,
                max_attempts,
                exc,
                delay,
            )
            await asyncio.sleep(delay)
            delay = min(delay * 2, 15.0)


async def _on_error(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.exception("Unhandled bot error", exc_info=context.error)


def _help_text() -> str:
    return (
        "Одна команда = одна ссылка\n\n"
        "Формат команды\n"
        "/template <шаблон> <end_date> <total_rewards> <participants> <my_rewards> "
        "[duration] [as_of_date]\n"
        "Значения вводятся через пробел, строго в этом порядке\n\n"
        "1. шаблон (просто ставим цифру в соответствии с проектом)\n"
        "Нумерация шаблона:\n"
        "1 — Billions Network (BILL)\n"
        "2 — LayerZero (ZRO)\n"
        "3 — Kite AI (KITE)\n"
        "4 — Aave (AAVE)\n\n"
        "2. end_date\n"
        "Дата окончания проекта Boost (например 2026-07-20)\n\n"
        "3. total_rewards\n"
        "Кол-во токенов в проект (например Aave — 50,000)\n\n"
        "4. participants\n"
        "Кол-во участников (например 1125)\n\n"
        "5. my_rewards\n"
        "Кол-во монет у друга с США (например 12)\n\n"
        "6. duration\n"
        "Сколько дней длится проект (например 14)\n\n"
        "7. as_of_date\n"
        "Дата старта, пробелы в дате заменяй на _ (нижнее подчёркивание) "
        "(например June_16,_2026)\n\n"
        "Примеры:\n"
        "/template 1 2026-05-23 50,000 1125 13 10 May_15,_2026"
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _reply_with_retry(update, _help_text())


async def templates(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lines = ["Доступные шаблоны:"]
    for template_id, title in TEMPLATE_DESCRIPTIONS.items():
        lines.append(f"{template_id} - {title}")
    lines.append("")
    lines.append("Использование:")
    lines.append(
        "/template <1-4> <end_date> <total_rewards> <participants> <my_rewards> "
        "[duration] [as_of_date]"
    )
    await _reply_with_retry(update, "\n".join(lines))


async def template(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not 5 <= len(context.args) <= 7:
        await _reply_with_retry(
            update,
            "Ошибка: нужно от 5 до 7 аргументов.\n\n"
            f"{_help_text()}",
        )
        return

    args = [arg.strip() for arg in context.args]
    template_id, end, total, participants, my = args[:5]
    duration = args[5] if len(args) >= 6 else None
    asof = args[6].replace("_", " ") if len(args) >= 7 else None

    if template_id not in VALID_TEMPLATES:
        await _reply_with_retry(update, "Ошибка: номер шаблона должен быть от 1 до 4.")
        return

    if len(end) < 6:
        await _reply_with_retry(update, "Ошибка: End Date слишком короткий. Пример: 2026-05-23")
        return

    for label, value in (
        ("Total Rewards", total),
        ("Total Participants", participants),
        ("My Rewards", my),
    ):
        if not _is_number_like(value):
            await _reply_with_retry(
                update,
                f"Ошибка: {label} должен быть числом (допустимы запятые и точка).",
            )
            return

    if duration is not None and not _is_number_like(duration):
        await _reply_with_retry(
            update,
            "Ошибка: Event Duration (duration) должен быть числом дней. Пример: 10",
        )
        return

    link = _build_link(template_id, end, total, participants, my, duration, asof)
    await _reply_with_retry(
        update,
        "Готово. Открой ссылку и сделай скриншот:\n\n"
        f"{link}",
    )


def _bot_token() -> str:
    token = os.getenv("TELEGRAM_BOT_TOKEN", DEFAULT_BOT_TOKEN).strip()
    if not token or token in {"your_telegram_bot_token", "PASTE_YOUR_TELEGRAM_BOT_TOKEN_HERE"}:
        token = DEFAULT_BOT_TOKEN
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is required.")
    return token


def main() -> None:
    token = _bot_token()
    while True:
        try:
            app = _build_application(token)
            app.add_error_handler(_on_error)
            app.add_handler(CommandHandler("start", start))
            app.add_handler(CommandHandler("templates", templates))
            app.add_handler(CommandHandler("template", template))
            logging.info("Bot started. Waiting for commands...")
            app.run_polling(drop_pending_updates=True)
            break
        except NetworkError as exc:
            logging.warning("Network error: %s. Retrying in 15 seconds...", exc)
            time.sleep(15)

if __name__ == "__main__":
    main()
