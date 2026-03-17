<script setup lang="ts">
import { computed, onBeforeMount, reactive, ref } from "vue";

import type {
  LibrarySettings,
  StaffDigestScheduleOverrides,
  StaffDigestWeekSchedule,
} from "@core/api/types";
import { getSettings, updateSettings } from "@core/api/settings";
import { defaultStaffDigestWeekSchedule } from "@core/api/types";
import GeneralSettingsBlock from "../components/settings/GeneralSettings/GeneralSettingsBlock.vue";
import StaffDigestSettingsBlock from "../components/settings/StaffDigestSettings/StaffDigestSettingsBlock.vue";
import StaffRecipientsSettingsBlock from "../components/settings/StaffRecipientsSettings/StaffRecipientsSettingsBlock.vue";
import WorkScheduleSettingsBlock from "../components/settings/WorkScheduleSettings/WorkScheduleSettingsBlock.vue";
import ReaderNotificationSettingsBlock from "../components/settings/ReaderNotificationSettings/ReaderNotificationSettingsBlock.vue";
import BrandingSettingsBlock from "../components/settings/BrandingSettings/BrandingSettingsBlock.vue";

function cloneWeekSchedule(schedule: StaffDigestWeekSchedule): StaffDigestWeekSchedule {
  return Object.fromEntries(
    Object.entries(schedule).map(([dayKey, value]) => [dayKey, { ...value }])
  ) as StaffDigestWeekSchedule;
}

function cloneOverrides(overrides: StaffDigestScheduleOverrides): StaffDigestScheduleOverrides {
  return Object.fromEntries(
    Object.entries(overrides).map(([dateKey, value]) => [dateKey, { ...value }])
  );
}

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
  staff_digest_week_schedule: cloneWeekSchedule(defaultStaffDigestWeekSchedule),
  staff_digest_schedule_overrides: {},
  reader_status_notifications_enabled: true,
  reader_notification_statuses: ["processing", "ready", "cancelled"],
});
const settingsRevision = ref(0);

const blockSaving = reactive({
  branding: false,
  general: false,
  reader: false,
  schedule: false,
  staff: false,
});

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

const staffScheduleSettings = computed(() => ({
  holidays: settings.value.holidays,
  staff_digest_week_schedule: settings.value.staff_digest_week_schedule,
  staff_digest_schedule_overrides: settings.value.staff_digest_schedule_overrides,
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
    staff_digest_week_schedule: cloneWeekSchedule(
      loadedSettings.staff_digest_week_schedule ?? defaultStaffDigestWeekSchedule
    ),
    staff_digest_schedule_overrides: cloneOverrides(
      loadedSettings.staff_digest_schedule_overrides ?? {}
    ),
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
      staff_digest_week_schedule: cloneWeekSchedule(
        patch.staff_digest_week_schedule ?? settings.value.staff_digest_week_schedule
      ),
      staff_digest_schedule_overrides: cloneOverrides(
        patch.staff_digest_schedule_overrides ?? settings.value.staff_digest_schedule_overrides
      ),
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
          Здесь администратор управляет правилами работы библиотеки, уведомлениями для сотрудников и
          читателей, рабочим календарем и логотипом сервиса.
        </p>
        <div class="hero-guide">
          <p>
            1. Редактируйте блоки по отдельности: каждое изменение сразу сохраняется на сервере.
          </p>
          <p>2. В рабочем календаре задаются обычные часы, праздники и исключения по датам.</p>
          <p>
            3. Для сотрудников можно настроить автоматическую сводку и вручную выбрать получателей.
          </p>
          <p>4. Для читателей можно выбрать, по каким статусам заказа отправлять письма.</p>
        </div>
      </div>
    </header>

    <div class="settings-layout">
      <div class="settings-span-full">
        <WorkScheduleSettingsBlock
          :model-value="staffScheduleSettings"
          :saving="blockSaving.schedule"
          :sync-token="settingsRevision"
          @save="saveSettingsPatch('schedule', $event)"
        />
      </div>
      <div class="settings-column settings-column-main">
        <GeneralSettingsBlock
          :model-value="generalSettings"
          :saving="blockSaving.general"
          :sync-token="settingsRevision"
          @save="saveSettingsPatch('general', $event)"
        />

        <StaffRecipientsSettingsBlock />
      </div>

      <aside class="settings-column settings-column-side">
        <BrandingSettingsBlock
          :current-logo-label="currentLogoLabel"
          :saving="blockSaving.branding"
          :sync-token="settingsRevision"
          @save="saveSettingsPatch('branding', { logo: $event })"
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
  grid-template-columns: minmax(0, 1fr);
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
  max-width: none;
  margin: 0.85rem 0 0;
  color: var(--color-text-700);
  font-size: var(--text-sm);
  line-height: 1.6;
}

.hero-guide {
  display: grid;
  gap: 0.35rem;
  margin-top: 0.75rem;
}

.hero-guide p {
  margin: 0;
  color: var(--color-text-600);
  font-size: var(--text-sm);
  line-height: 1.6;
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
  gap: 1.5rem;
}

.settings-span-full {
  grid-column: 1 / -1;
}

@media (max-width: 960px) {
  .settings-layout {
    grid-template-columns: 1fr;
  }

  .settings-column {
    max-width: 42rem;
    width: 100%;
    margin: 0 auto;
  }
}

@media (max-width: 840px) {
  .settings-page {
    gap: 1rem;
    margin: 0.85rem auto 1.5rem;
    padding: 0 1rem;
  }

  .page-hero {
    width: 100%;
    max-width: 34rem;
    margin: 0 auto;
    padding: 1.2rem;
  }

  .settings-span-full,
  .settings-column {
    width: 100%;
    max-width: 34rem;
    margin: 0 auto;
  }
}
</style>
