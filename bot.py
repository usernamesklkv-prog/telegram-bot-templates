import os
from urllib.parse import urlencode

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

load_dotenv()

VALID_TEMPLATES = {"1", "2", "3", "4"}
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


def _proxy_url() -> str | None:
    explicit = os.getenv("TELEGRAM_PROXY_URL", "").strip()
    if explicit:
        return explicit
    if os.getenv("PYTHONANYWHERE_DOMAIN") or os.getenv("PYTHONANYWHERE_SITE"):
        return PYTHONANYWHERE_PROXY
    return None


def _build_application(token: str) -> Application:
    builder = Application.builder().token(token)
    proxy = _proxy_url()
    if proxy:
        builder = builder.proxy(proxy).get_updates_proxy(proxy)
    return builder.build()


def _help_text() -> str:
    return (
        "Одна команда = одна ссылка:\n\n"
        "/template <1-4> <end_date> <total_rewards> <participants> <my_rewards> "
        "[duration] [as_of_date]\n\n"
        "Примеры:\n"
        "/template 1 2026-05-23 50,000 1125 13\n"
        "/template 1 2026-05-23 50,000 1125 13 10\n"
        "/template 1 2026-05-23 50,000 1125 13 10 May_15,_2026\n\n"
        "Подсказки:\n"
        "- duration — длительность в днях (Event Duration), необязательно.\n"
        "- as_of_date — дата в тексте «as of …», вместо пробелов ставь _ "
        "(May_15,_2026), необязательно.\n"
        "- В Total Rewards можно писать запятые: 50,000."
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(_help_text())


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
    await update.message.reply_text("\n".join(lines))


async def template(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not 5 <= len(context.args) <= 7:
        await update.message.reply_text(
            "Ошибка: нужно от 5 до 7 аргументов.\n\n"
            f"{_help_text()}"
        )
        return

    args = [arg.strip() for arg in context.args]
    template_id, end, total, participants, my = args[:5]
    duration = args[5] if len(args) >= 6 else None
    asof = args[6].replace("_", " ") if len(args) >= 7 else None

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

    if duration is not None and not _is_number_like(duration):
        await update.message.reply_text(
            "Ошибка: Event Duration (duration) должен быть числом дней. Пример: 10"
        )
        return

    link = _build_link(template_id, end, total, participants, my, duration, asof)
    await update.message.reply_text(
        "Готово. Открой ссылку и сделай скриншот:\n\n"
        f"{link}"
    )


def main() -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is required in environment variables.")

    app = _build_application(token)
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("templates", templates))
    app.add_handler(CommandHandler("template", template))
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
