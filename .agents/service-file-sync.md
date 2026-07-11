# Service File Sync

Three files describe services and must stay in sync:

- `custom_components/zendo/services.yaml` - service schema (selectors,
  required flags, defaults, min/max). Source of truth for structure.
- `custom_components/zendo/strings.json` - translatable strings source.
  Contains `name` and `description` for services, fields, config flow steps,
  etc. Source of truth for user-facing text.
- `custom_components/zendo/translations/en.json` - compiled English
  translation. Must always be an exact copy of `strings.json`.

When adding or editing a service, update all three files together. The `name`
and `description` values in `services.yaml` must match `strings.json` (and
therefore `en.json`). After changing `strings.json`, copy its full contents
to `translations/en.json`.
