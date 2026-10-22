from datetime import datetime, timedelta

def get_current_time(offset_hours):
    # Получаем текущее время в UTC
    utc_now = datetime.utcnow()
    # Вычисляем смещение
    offset = timedelta(hours=offset_hours)
    # Применяем смещение к текущему времени
    local_time = utc_now + offset
    # Форматируем время в ЧЧ:ММ
    formatted_time = local_time.strftime('%H:%M')
    return formatted_time