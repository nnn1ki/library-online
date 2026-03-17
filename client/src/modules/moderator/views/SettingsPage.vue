<script setup lang="ts">
import { computed, onBeforeMount, reactive, ref } from "vue";

import type { LibrarySettings } from "@core/api/types";
import { getSettings, updateSettings } from "@core/api/settings";
import GeneralSettingsBlock from "../components/settings/GeneralSettings/GeneralSettingsBlock.vue";
import StaffDigestSettingsBlock from "../components/settings/StaffDigestSettings/StaffDigestSettingsBlock.vue";
import ReaderNotificationSettingsBlock from "../components/settings/ReaderNotificationSettings/ReaderNotificationSettingsBlock.vue";
import HolidayCalendarBlock from "../components/settings/HolidayCalendar/HolidayCalendarBlock.vue";
import BrandingSettingsBlock from "../components/settings/BrandingSettings/BrandingSettingsBlock.vue";

const settings = ref<LibrarySettings>({
  max_books_per_order: 0,
  max_books_per_reader: 0,
  max_borrow_days: 0,
  holidays: [],
  logo: null,
  new_order_wait: 0,
  processing_order_wait: 0,
  staff_digest_enabled: true,
  staff_notification_active_hours: 2,
  staff_digest_stale_order_hours: 1,
  reader_status_notifications_enabled: true,
  reader_notification_statuses: ["processing", "ready", "cancelled"],
});
const settingsRevision = ref(0);

const blockSaving = reactive({
  branding: false,
  calendar: false,
  general: false,
  reader: false,
  staff: false,
});

const selectedHolidayCount = computed(() => settings.value.holidays.length);
const selectedReaderStatusesCount = computed(
  () => settings.value.reader_notification_statuses.length
);
const hasActiveSave = computed(() => Object.values(blockSaving).some(Boolean));

const generalSettings = computed(() => ({
  max_books_per_order: settings.value.max_books_per_order,
  max_books_per_reader: settings.value.max_books_per_reader,
  max_borrow_days: settings.value.max_borrow_days,
  new_order_wait: settings.value.new_order_wait,
  processing_order_wait: settings.value.processing_order_wait,
}));

const staffDigestSettings = computed(() => ({
  staff_digest_enabled: settings.value.staff_digest_enabled,
  staff_notification_active_hours: settings.value.staff_notification_active_hours,
  staff_digest_stale_order_hours: settings.value.staff_digest_stale_order_hours,
}));

const readerNotificationSettings = computed(() => ({
  reader_status_notifications_enabled: settings.value.reader_status_notifications_enabled,
  reader_notification_statuses: settings.value.reader_notification_statuses,
}));

const currentLogoLabel = computed(() => {
  if (typeof settings.value.logo === "string" && settings.value.logo)
    return "Текущий логотип загружен";
  return "Логотип не загружен";
});

onBeforeMount(async () => {
  await refreshSettings();
});

async function refreshSettings() {
  const loadedSettings = await getSettings();
  settings.value = {
    ...loadedSettings,
    holidays: loadedSettings.holidays ?? [],
    reader_notification_statuses: loadedSettings.reader_notification_statuses ?? [],
  };
  settingsRevision.value += 1;
}

async function saveSettingsPatch(
  section: keyof typeof blockSaving,
  patch: Partial<LibrarySettings>
) {
  blockSaving[section] = true;

  try {
    const payload: LibrarySettings = {
      ...settings.value,
      ...patch,
      holidays: [...(patch.holidays ?? settings.value.holidays)],
      reader_notification_statuses: [
        ...(patch.reader_notification_statuses ?? settings.value.reader_notification_statuses),
      ],
      logo: patch.logo ?? settings.value.logo,
    };

    await updateSettings(payload);
    await refreshSettings();
  } finally {
    blockSaving[section] = false;
  }
}
</script>

<template>
  <section class="settings-page">
    <header class="page-hero">
      <div class="hero-copy">
        <p class="eyebrow">Moderator / Settings</p>
        <h1>Настройки библиотеки и рассылок</h1>
        <p class="hero-text">
          Каждый блок редактируется и сохраняется отдельно. После обновления секция заново
          подтягивает актуальные настройки с сервера.
        </p>
      </div>

      <div class="hero-stats">
        <div class="stat-card">
          <span class="stat-label">Праздничных дат</span>
          <strong class="stat-value">{{ selectedHolidayCount }}</strong>
        </div>
        <div class="stat-card">
          <span class="stat-label">Reader-статусов включено</span>
          <strong class="stat-value">{{ selectedReaderStatusesCount }}</strong>
        </div>
        <div class="stat-card">
          <span class="stat-label">Статус страницы</span>
          <strong class="stat-value">{{ hasActiveSave ? "Идет обновление" : "Готово" }}</strong>
        </div>
      </div>
    </header>

    <div class="settings-layout">
      <div class="settings-column settings-column-main">
        <GeneralSettingsBlock
          :model-value="generalSettings"
          :saving="blockSaving.general"
          :sync-token="settingsRevision"
          @save="saveSettingsPatch('general', $event)"
        />

        <StaffDigestSettingsBlock
          :model-value="staffDigestSettings"
          :saving="blockSaving.staff"
          :sync-token="settingsRevision"
          @save="saveSettingsPatch('staff', $event)"
        />

        <ReaderNotificationSettingsBlock
          :model-value="readerNotificationSettings"
          :saving="blockSaving.reader"
          :sync-token="settingsRevision"
          @save="saveSettingsPatch('reader', $event)"
        />
      </div>

      <aside class="settings-column settings-column-side">
        <HolidayCalendarBlock
          :holidays="settings.holidays"
          @update:holidays="saveSettingsPatch('calendar', { holidays: $event })"
        />

        <BrandingSettingsBlock
          :current-logo-label="currentLogoLabel"
          :saving="blockSaving.branding"
          :sync-token="settingsRevision"
          @save="saveSettingsPatch('branding', { logo: $event })"
        />
      </aside>
    </div>
  </section>
</template>

<style scoped lang="scss">
.settings-page {
  display: grid;
  gap: 1.5rem;
  max-width: 1280px;
  margin: 1.25rem auto 2rem;
  padding: 0 1rem;
}

.page-hero {
  display: grid;
  grid-template-columns: minmax(0, 2.2fr) minmax(280px, 1fr);
  gap: 1rem;
  padding: 1.5rem;
  border-radius: 1.5rem;
  border: 1px solid var(--color-text-200);
  background:
    radial-gradient(circle at top right, var(--color-primary-100), transparent 34%),
    linear-gradient(135deg, var(--color-background-50), var(--color-secondary-50));
  box-shadow: 0 18px 40px rgba(17, 12, 29, 0.08);
}

.eyebrow {
  margin: 0 0 0.35rem;
  color: var(--color-text-600);
  font-size: var(--text-xs);
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.hero-copy h1 {
  margin: 0;
  font-size: clamp(var(--text-2xl), 3vw, var(--text-4xl));
  line-height: 1.05;
}

.hero-text {
  max-width: 58ch;
  margin: 0.85rem 0 0;
  color: var(--color-text-700);
  font-size: var(--text-sm);
  line-height: 1.6;
}

.hero-stats {
  display: grid;
  gap: 0.85rem;
}

.stat-card {
  display: grid;
  gap: 0.35rem;
  padding: 1rem 1.1rem;
  border: 1px solid var(--color-text-200);
  border-radius: 1rem;
  background: rgba(255, 255, 255, 0.42);
  backdrop-filter: blur(8px);
}

.stat-label {
  color: var(--color-text-600);
  font-size: var(--text-xs);
}

.stat-value {
  font-size: var(--text-xl);
  font-weight: 700;
}

.settings-layout {
  display: grid;
  grid-template-columns: minmax(0, 1.65fr) minmax(320px, 0.95fr);
  gap: 1.25rem;
}

.settings-column {
  display: grid;
  gap: 1.25rem;
}

.settings-column-side {
  align-content: start;
  gap: 3rem;
}

@media (max-width: 960px) {
  .page-hero,
  .settings-layout {
    grid-template-columns: 1fr;
  }

  .settings-column {
    max-width: 42rem;
    width: 100%;
    margin: 0 auto;
  }
}

@media (max-width: 640px) {
  .settings-page {
    gap: 1rem;
    margin: 0.85rem auto 1.5rem;
    padding: 0 0.75rem;
  }

  .page-hero {
    padding: 1.2rem;
  }
}
</style>
