"""Binary sensor platform for Zendo."""

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import API_VERSION, CONF_PUSH_NOTIFICATION_TOKEN, DOMAIN, SIGNAL_CONFIG_UPDATED


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Zendo binary sensors from a config entry."""
    async_add_entities([ZendoStatusBinarySensor(entry)])


class ZendoStatusBinarySensor(BinarySensorEntity):
    """Binary sensor indicating whether the Zendo API is configured and available."""

    _attr_has_entity_name = True
    _attr_name = "Status"
    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, entry: ConfigEntry) -> None:
        """Initialise the sensor."""
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_status"

    @property
    def is_on(self) -> bool:
        """Return True — the Zendo API is available whenever the integration is loaded."""
        return True

    @property
    def extra_state_attributes(self) -> dict[str, str | bool]:
        """Return API version and push notification configuration status."""
        token = self._entry.data.get(CONF_PUSH_NOTIFICATION_TOKEN)
        push_configured = isinstance(token, str) and len(token) > 0

        return {
            "api_version": API_VERSION,
            "push_notifications_configured": push_configured,
        }

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info to group entities under a single Zendo device."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._entry.entry_id)},
            name="Zendo",
            manufacturer="Zendo",
            entry_type=DeviceEntryType.SERVICE,
        )

    async def async_added_to_hass(self) -> None:
        """Register dispatcher listener to update state when config changes."""
        self.async_on_remove(
            async_dispatcher_connect(
                self.hass, SIGNAL_CONFIG_UPDATED, self.async_write_ha_state
            )
        )
