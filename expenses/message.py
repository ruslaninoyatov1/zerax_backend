MESSAGES = {
    "expense_created": {
        "UZ": "Xarajat yaratildi",
        "RU": "Расход создан",
        "EN": "Expense created",
    },
    "expense_updated": {
        "UZ": "Xarajat yangilandi",
        "RU": "Расход обновлен",
        "EN": "Expense updated",
    },
    "expense_deleted": {
        "UZ": "Xarajat o'chirildi",
        "RU": "Расход удален",
        "EN": "Expense deleted",
    },
}

def get_message(key, user):
    lang = getattr(user, "language", "EN")
    return MESSAGES.get(key, {}).get(lang, MESSAGES.get(key, {}).get("EN"))
