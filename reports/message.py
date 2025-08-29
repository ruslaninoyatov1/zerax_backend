MESSAGES = {
    "report_created": {
        "EN": "Report created successfully.",
        "RU": "Отчет успешно создан.",
        "UZ": "Hisobot muvaffaqiyatli yaratildi.",
    },
    "file_added": {
        "EN": "File added successfully.",
        "RU": "Файл успешно добавлен.",
        "UZ": "Fayl muvaffaqiyatli qo‘shildi.",
    },
    "export_success": {
        "EN": "Report exported successfully.",
        "RU": "Отчет успешно экспортирован.",
        "UZ": "Hisobot muvaffaqiyatli eksport qilindi.",
    },
    # --- errors ---
    "invalid_credentials": {
        "EN": "Invalid email or password.",
        "RU": "Неверный email или пароль.",
        "UZ": "Email yoki parol noto‘g‘ri.",
    },
    "permission_denied": {
        "EN": "You do not have permission to perform this action.",
        "RU": "У вас нет прав для выполнения этого действия.",
        "UZ": "Sizda bu amalni bajarish uchun ruxsat yo‘q.",
    },
    "not_found": {
        "EN": "Requested resource not found.",
        "RU": "Запрашиваемый ресурс не найден.",
        "UZ": "So‘ralgan resurs topilmadi.",
    },
    "validation_error": {
        "EN": "Invalid input data.",
        "RU": "Недопустимые входные данные.",
        "UZ": "Kiritilgan ma’lumot noto‘g‘ri.",
    },
}


def get_message(key, user=None, lang=None):
    """
    Get translated message by key.
    Priority: explicit lang param > user.language > default EN
    """
    language = lang or getattr(user, "language", "EN")
    return (
        MESSAGES.get(key, {}).get(language)
        or MESSAGES.get(key, {}).get("EN", "")
    )
