import os
from urllib.parse import urlencode

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

load_dotenv()

VALID_TEMPLATES = {"1", "2", "3", "4"}
DEFAULT_BASE_URL = "https://usernamesklkv-prog.github.io/telegram-bot-templates"
TEMPLATE_DESCRIPTIONS = {
    "1": "Billions Network (BILL)",
    "2": "LayerZero (ZRO)",
    "3": "Kite AI (KITE)",
    "4": "Aave (AAVE)",
}


def _base_url() -> str:
    base = os.getenv("TEMPLATE_BASE_URL", DEFAULT_BASE_URL).strip().rstrip("/")
    if not base:
        raise RuntimeError("TEMPLATE_BASE_URL is required in environment variables.")
    return base


def _is_number_like(value: str) -> bool:
    normalized = value.replace(",", "").replace(" ", "")
    if not normalized:
        return False
    if normalized.count(".") > 1:
        return False
    if normalized.startswith("-"):
        normalized = normalized[1:]
    return normalized.replace(".", "", 1).isdigit()


def _build_link(template_id: str, end: str, total: str, participants: str, my: str) -> str:
    query = urlencode(
        {
            "end": end,
            "total": total,
            "participants": participants,
            "my": my,
        }
    )
    return f"{_base_url()}/templates/{template_id}.html?{query}"


def _help_text() -> str:
    return (
        "Одна команда = одна ссылка:\n\n"
        "/template <1-4> <end_date> <total_rewards> <participants> <my_rewards>\n\n"
        "Пример:\n"
        "/template 1 2026-05-23 50000 1125 13\n\n"
        "Подсказка: если в значениях есть пробелы, используй _ вместо пробела."
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(_help_text())


async def templates(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lines = ["Доступные шаблоны:"]
    for template_id, title in TEMPLATE_DESCRIPTIONS.items():
        lines.append(f"{template_id} - {title}")
    lines.append("")
    lines.append("Использование:")
    lines.append("/template <1-4> <end_date> <total_rewards> <participants> <my_rewards>")
    await update.message.reply_text("\n".join(lines))


async def template(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) != 5:
        await update.message.reply_text(
            "Ошибка: нужно ровно 5 аргументов.\n\n"
            f"{_help_text()}"
        )
        return

    template_id, end, total, participants, my = [arg.strip() for arg in context.args]

    if template_id not in VALID_TEMPLATES:
        await update.message.reply_text("Ошибка: номер шаблона должен быть от 1 до 4.")
        return

    if len(end) < 6:
        await update.message.reply_text("Ошибка: End Date слишком короткий. Пример: 2026-05-23")
        return

    for label, value in (
        ("Total Rewards", total),
        ("Total Participants", participants),
        ("My Rewards", my),
    ):
        if not _is_number_like(value):
            await update.message.reply_text(
                f"Ошибка: {label} должен быть числом (допустимы запятые и точка)."
            )
            return

    link = _build_link(template_id, end, total, participants, my)
    await update.message.reply_text(
        "Готово. Открой ссылку и сделай скриншот:\n\n"
        f"{link}"
    )


def main() -> None:
    token = os.getenv("8708862445:AAFt1lMGw8s3f75VXkIOCrAsQzLkwZeAZ5w", "").strip()
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is required in environment variables.")

    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("templates", templates))
    app.add_handler(CommandHandler("template", template))
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
