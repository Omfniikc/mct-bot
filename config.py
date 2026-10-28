import os

from dotenv import load_dotenv

load_dotenv()


def _get(name: str, default: str = "") -> str:
    """Читает переменную окружения, падает с понятной ошибкой, если её нет."""
    value = os.getenv(name)
    if value is None:
        raise RuntimeError(
            f"Переменная окружения {name} не задана. "
            f"Скопируй .env.example в .env и заполни значения."
        )
    return value


def _get_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in ("1", "true", "yes", "on")


# ─── Telegram ───
TG_TOKEN = _get("TG_TOKEN")
# Telegram user id администратора (для админ-команд и бэкапов БД)
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

# ─── Нейросеть (Tokify / OpenAI-совместимый API) ───
GPT_VISION_TOKEN = os.getenv("GPT_VISION_TOKEN", "")
GPT_TR_TOKEN = os.getenv("GPT_TR_TOKEN", "")
TOKIFY_API_KEY = os.getenv("TOKIFY_API_KEY", GPT_VISION_TOKEN or None) or _get("TOKIFY_API_KEY")
TOKIFY_BASE_URL = os.getenv("TOKIFY_BASE_URL", "https://tokify.sale/v1")

# ─── База данных ───
DB_PATH = os.getenv("DB_PATH", "./main.db")

# ─── ЮKassa ───
SHOP_ID = os.getenv("SHOP_ID", "")
PAY_TOKEN = os.getenv("PAY_TOKEN", "")

# ─── Webhook ───
WEBHOOK_HOST = os.getenv("WEBHOOK_HOST", "localhost")
WEBHOOK_PORT = int(os.getenv("WEBHOOK_PORT", "8444"))
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "/webhook/bot2")
WEBHOOK_URL = f"https://{WEBHOOK_HOST}{WEBHOOK_PATH}"

# Режим работы: true = long polling, false = webhook.
POLING = _get_bool("POLING", default=True)

# Прокси для запросов к Telegram. Пустая строка ("") = без прокси.
# Примеры: "http://127.0.0.1:12334", "socks5://127.0.0.1:12334"
PROXY_URL = os.getenv("PROXY_URL", "")
