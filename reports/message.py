MESSAGES = {
    # ---- REPORTS ----
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
    "invalid_export_type": {
        "EN": "Invalid export type.",
        "RU": "Недопустимый тип экспорта.",
        "UZ": "Eksport turi noto‘g‘ri.",
    },
    "export_failed": {
        "EN": "Report export failed.",
        "RU": "Не удалось экспортировать отчет.",
        "UZ": "Hisobot eksport qilishda xatolik yuz berdi.",
    },

    # ---- EXPENSES ----
    "expense_created": {
        "EN": "Expense created successfully.",
        "RU": "Расход успешно создан.",
        "UZ": "Xarajat muvaffaqiyatli yaratildi.",
    },
    "expense_updated": {
        "EN": "Expense updated successfully.",
        "RU": "Расход успешно обновлен.",
        "UZ": "Xarajat muvaffaqiyatli yangilandi.",
    },
    "expense_deleted": {
        "EN": "Expense deleted successfully.",
        "RU": "Расход успешно удален.",
        "UZ": "Xarajat muvaffaqiyatli o‘chirildi.",
    },

    # ---- INVOICES ----
    "invoice_created": {
        "EN": "Invoice created successfully.",
        "RU": "Счет успешно создан.",
        "UZ": "Hisob-faktura muvaffaqiyatli yaratildi.",
    },
    "invoice_updated": {
        "EN": "Invoice updated successfully.",
        "RU": "Счет успешно обновлен.",
        "UZ": "Hisob-faktura muvaffaqiyatli yangilandi.",
    },
    "invoice_deleted": {
        "EN": "Invoice deleted successfully.",
        "RU": "Счет успешно удален.",
        "UZ": "Hisob-faktura muvaffaqiyatli o‘chirildi.",
    },

    # ---- ACCOUNTING ----
    "account_created": {
        "EN": "Account created successfully.",
        "RU": "Счет успешно создан.",
        "UZ": "Hisob muvaffaqiyatli yaratildi.",
    },
    "journal_created": {
        "EN": "Journal entry created successfully.",
        "RU": "Бухгалтерская запись успешно создана.",
        "UZ": "Buxgalteriya yozuvi muvaffaqiyatli yaratildi.",
    },
    "balance_sheet": {
        "EN": "Balance sheet generated successfully.",
        "RU": "Балансовый отчет успешно создан.",
        "UZ": "Balans hisobot muvaffaqiyatli yaratildi.",
    },

    # ---- SYSTEM / ERRORS ----
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
    Priority: explicit lang param > user.language > default EN.
    """
    language = lang or getattr(user, "language", "EN")
    return (
        MESSAGES.get(key, {}).get(language)
        or MESSAGES.get(key, {}).get("EN", "")
        or f"Message not found for key '{key}'"
    )
