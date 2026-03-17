from datetime import date, time

from adrf import serializers as aserializers
from rest_framework import serializers

from library_service.models.library_settings import LibrarySettings


WEEKDAY_KEYS = (
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
)


def _parse_schedule_time(value: str, field_name: str) -> time:
    if not isinstance(value, str):
        raise serializers.ValidationError({field_name: "Ожидается строка времени в формате ЧЧ:ММ."})

    try:
        hours, minutes = value.split(":")
        return time(hour=int(hours), minute=int(minutes))
    except (ValueError, TypeError) as exc:
        raise serializers.ValidationError({field_name: "Используйте формат ЧЧ:ММ."}) from exc


def _validate_schedule_window(value: object, field_name: str) -> dict:
    if not isinstance(value, dict):
        raise serializers.ValidationError({field_name: "Ожидается объект с настройками дня."})

    enabled = value.get("enabled")
    if not isinstance(enabled, bool):
        raise serializers.ValidationError({field_name: "Поле enabled обязательно и должно быть булевым."})

    if not enabled:
        return {"enabled": False}

    start = value.get("start")
    end = value.get("end")
    start_time = _parse_schedule_time(start, field_name)
    end_time = _parse_schedule_time(end, field_name)

    if start_time >= end_time:
        raise serializers.ValidationError({field_name: "Время начала должно быть раньше времени окончания."})

    return {
        "enabled": True,
        "start": start_time.strftime("%H:%M"),
        "end": end_time.strftime("%H:%M"),
    }


class LibrarySettingsSerializer(aserializers.ModelSerializer):
    def validate_staff_digest_week_schedule(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError("Ожидается объект с днями недели.")

        extra_keys = set(value) - set(WEEKDAY_KEYS)
        missing_keys = set(WEEKDAY_KEYS) - set(value)
        if extra_keys:
            raise serializers.ValidationError(f"Неизвестные дни недели: {', '.join(sorted(extra_keys))}.")
        if missing_keys:
            raise serializers.ValidationError(f"Не хватает дней недели: {', '.join(sorted(missing_keys))}.")

        return {
            day_name: _validate_schedule_window(value[day_name], day_name)
            for day_name in WEEKDAY_KEYS
        }

    def validate_staff_digest_schedule_overrides(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError("Ожидается объект с ключами-датами.")

        normalized_value = {}
        for date_key, window in value.items():
            try:
                date.fromisoformat(date_key)
            except ValueError as exc:
                raise serializers.ValidationError(
                    f"Ключ {date_key} должен быть датой в формате ГГГГ-ММ-ДД."
                ) from exc

            normalized_value[date_key] = _validate_schedule_window(window, date_key)

        return normalized_value

    class Meta:
        model = LibrarySettings
        fields = "__all__"
