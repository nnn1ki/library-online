import { api } from "./axios";
import type { LibrarySettings } from "@api/types";

export async function getSettings(): Promise<LibrarySettings> {
  const { data } = await api.get("/api/settings/");
  return data;
}

export async function updateSettings(settings: LibrarySettings) {
  try {
    const payload = {
      max_books_per_order: settings.max_books_per_order,
      max_books_per_reader: settings.max_books_per_reader,
      max_borrow_days: settings.max_borrow_days,
      holidays: settings.holidays,
      new_order_wait: settings.new_order_wait,
      processing_order_wait: settings.processing_order_wait,
      staff_digest_enabled: settings.staff_digest_enabled,
      staff_notification_active_hours: settings.staff_notification_active_hours,
      staff_digest_stale_order_hours: settings.staff_digest_stale_order_hours,
      staff_digest_week_schedule: settings.staff_digest_week_schedule,
      staff_digest_schedule_overrides: settings.staff_digest_schedule_overrides,
      reader_status_notifications_enabled: settings.reader_status_notifications_enabled,
      reader_notification_statuses: settings.reader_notification_statuses,
    };

    if (settings.logo instanceof File) {
      const formData = new FormData();
      formData.append("max_books_per_order", String(payload.max_books_per_order));
      formData.append("max_books_per_reader", String(payload.max_books_per_reader));
      formData.append("max_borrow_days", String(payload.max_borrow_days));
      formData.append("new_order_wait", String(payload.new_order_wait));
      formData.append("processing_order_wait", String(payload.processing_order_wait));
      formData.append("staff_digest_enabled", String(payload.staff_digest_enabled));
      formData.append(
        "staff_notification_active_hours",
        String(payload.staff_notification_active_hours)
      );
      formData.append(
        "staff_digest_stale_order_hours",
        String(payload.staff_digest_stale_order_hours)
      );
      formData.append(
        "staff_digest_week_schedule",
        JSON.stringify(payload.staff_digest_week_schedule)
      );
      formData.append(
        "staff_digest_schedule_overrides",
        JSON.stringify(payload.staff_digest_schedule_overrides)
      );
      formData.append(
        "reader_status_notifications_enabled",
        String(payload.reader_status_notifications_enabled)
      );
      formData.append("holidays", JSON.stringify(payload.holidays));
      formData.append(
        "reader_notification_statuses",
        JSON.stringify(payload.reader_notification_statuses)
      );
      formData.append("logo", settings.logo);

      await api.put("/api/settings/update/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      return;
    }

    await api.put("/api/settings/update/", payload);
  } catch (error) {
    console.error("Ошибка при настроек", error);
    throw error;
  }
}
