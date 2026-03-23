"""The Zendo integration."""

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import HomeAssistantError
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.dispatcher import async_dispatcher_send

from .const import CONF_PUSH_NOTIFICATION_TOKEN, DOMAIN, SIGNAL_CONFIG_UPDATED

PLATFORMS: list[Platform] = [Platform.BINARY_SENSOR]

SERVICE_PUSH_NOTIFICATIONS_ENABLE = "push_notifications_enable"
SERVICE_PUSH_NOTIFICATIONS_ENABLE_SCHEMA = vol.Schema(
    {vol.Required("token"): cv.string}
)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Zendo from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {}

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    async def handle_push_notifications_enable(call: ServiceCall) -> None:
        """Handle the push_notifications_enable service call."""
        token = call.data["token"]

        entries = hass.config_entries.async_entries(DOMAIN)
        if not entries:
            raise HomeAssistantError("Zendo integration is not configured")

        target_entry = entries[0]
        hass.config_entries.async_update_entry(
            target_entry,
            data={**target_entry.data, CONF_PUSH_NOTIFICATION_TOKEN: token},
        )

        async_dispatcher_send(hass, SIGNAL_CONFIG_UPDATED)

    if not hass.services.has_service(DOMAIN, SERVICE_PUSH_NOTIFICATIONS_ENABLE):
        hass.services.async_register(
            DOMAIN,
            SERVICE_PUSH_NOTIFICATIONS_ENABLE,
            handle_push_notifications_enable,
            schema=SERVICE_PUSH_NOTIFICATIONS_ENABLE_SCHEMA,
        )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
        hass.services.async_remove(DOMAIN, SERVICE_PUSH_NOTIFICATIONS_ENABLE)

    return unload_ok
