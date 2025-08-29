MESSAGES = {
    # --- Reports ---
    "report_created": {
        "EN": "Report created successfully.",
        "RU": "Отчет успешно создан.",
        "UZ": "Hisobot muvaffaqiyatli yaratildi.",
    },
    "export_success": {
        "EN": "Report exported successfully.",
        "RU": "Отчет успешно экспортирован.",
        "UZ": "Hisobot muvaffaqiyatli eksport qilindi.",
    },

    # --- Settings ---
    "settings_retrieved": {
        "EN": "Settings retrieved successfully.",
        "RU": "Настройки успешно получены.",
        "UZ": "Sozlamalar muvaffaqiyatli olindi.",
    },
    "settings_updated": {
        "EN": "Settings updated successfully.",
        "RU": "Настройки успешно обновлены.",
        "UZ": "Sozlamalar muvaffaqiyatli yangilandi.",
    },

    # --- Integrations ---
    "integration_created": {
        "EN": "Integration added successfully.",
        "RU": "Интеграция успешно добавлена.",
        "UZ": "Integratsiya muvaffaqiyatli qo‘shildi.",
    },
    "integration_updated": {
        "EN": "Integration updated successfully.",
        "RU": "Интеграция успешно обновлена.",
        "UZ": "Integratsiya muvaffaqiyatli yangilandi.",
    },
    "integration_deleted": {
        "EN": "Integration deleted successfully.",
        "RU": "Интеграция успешно удалена.",
        "UZ": "Integratsiya muvaffaqiyatli o‘chirildi.",
    },
}


def get_message(key, user):
    lang = getattr(user, "language", "EN")
    return MESSAGES.get(key, {}).get(lang, MESSAGES.get(key, {}).get("EN", ""))
