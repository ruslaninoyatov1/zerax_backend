MESSAGES = {
    "account_created": {
        "UZ": "Hisob yaratildi",
        "RU": "Счет создан",
        "EN": "Account created",
    },
    "account_updated": {
        "UZ": "Hisob yangilandi",
        "RU": "Счет обновлен",
        "EN": "Account updated",
    },
    "account_deleted": {
        "UZ": "Hisob o'chirildi",
        "RU": "Счет удален",
        "EN": "Account deleted",
    },
    "journal_created": {
        "UZ": "Jurnal yozuvi yaratildi",
        "RU": "Журнальная запись создана",
        "EN": "Journal entry created",
    },
    "journal_updated": {
        "UZ": "Jurnal yozuvi yangilandi",
        "RU": "Журнальная запись обновлена",
        "EN": "Journal entry updated",
    },
    "journal_deleted": {
        "UZ": "Jurnal yozuvi o'chirildi",
        "RU": "Журнальная запись удалена",
        "EN": "Journal entry deleted",
    },
}


def get_message(key, user):
    lang = getattr(user, "language", "EN")
    return MESSAGES.get(key, {}).get(lang, MESSAGES.get(key, {}).get("EN"))
