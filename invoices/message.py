# messages.py
MESSAGES = {
    "invoice_created": {
        "UZ": "Hisob-faktura yaratildi",
        "RU": "Счет создан",
        "EN": "Invoice created",
    },
    "invoice_updated": {
        "UZ": "Hisob-faktura yangilandi",
        "RU": "Счет обновлен",
        "EN": "Invoice updated",
    },
    "invoice_deleted": {
        "UZ": "Hisob-faktura o'chirildi",
        "RU": "Счет удален",
        "EN": "Invoice deleted",
    },
    "not_found": {
        "UZ": "Topilmadi",
        "RU": "Не найдено",
        "EN": "Not found",
    },
}

def get_message(key, user):
    lang = getattr(user, "language", "EN")
    return MESSAGES.get(key, {}).get(lang, MESSAGES.get(key, {}).get("EN"))
