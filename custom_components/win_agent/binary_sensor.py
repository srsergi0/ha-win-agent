"""Binary sensor platform for Windows Direct Agent."""
from __future__ import annotations

from typing import Any
from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, SIGNAL_WIN_AGENT_UPDATE
from .coordinator import WinAgentCoordinator

BINARY_SENSOR_DESCRIPTIONS = [
    {
        "key": "session_locked",
        "name": "Session Locked",
        "icon": "mdi:lock",
        "device_class": BinarySensorDeviceClass.LOCK,
    },
    {
        "key": "fullscreen_active",
        "name": "Fullscreen Gaming Mode",
        "icon": "mdi:gamepad-variant",
        "device_class": BinarySensorDeviceClass.RUNNING,
    },
    {
        "key": "microphone_active",
        "name": "Microphone In Use",
        "icon": "mdi:microphone",
        "device_class": BinarySensorDeviceClass.SOUND,
    },
    {
        "key": "user_active",
        "name": "User Active (Presence)",
        "icon": "mdi:account",
        "device_class": BinarySensorDeviceClass.PRESENCE,
    },
    {
        "key": "power_plugged",
        "name": "Power Connected",
        "icon": "mdi:power-plug",
        "device_class": BinarySensorDeviceClass.PLUG,
    },
    {
        "key": "audio_mute",
        "name": "Audio Muted",
        "icon": "mdi:volume-mute",
    },
]

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Windows Direct Agent binary sensors."""
    coordinator: WinAgentCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities = [
        WinAgentBinarySensor(coordinator, desc)
        for desc in BINARY_SENSOR_DESCRIPTIONS
    ]
    async_add_entities(entities)

class WinAgentBinarySensor(CoordinatorEntity[WinAgentCoordinator], BinarySensorEntity):
    """Representation of a Windows Agent binary sensor."""

    def __init__(self, coordinator: WinAgentCoordinator, desc: dict[str, Any]) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self.desc = desc
        self._key = desc["key"]
        self._attr_unique_id = f"{coordinator.device_id}_{self._key}"
        self._attr_name = f"{coordinator.device_name} {desc['name']}"
        self._attr_icon = desc.get("icon")
        self._attr_device_class = desc.get("device_class")

    async def async_added_to_hass(self) -> None:
        """Register dispatcher update callback."""
        await super().async_added_to_hass()
        self.async_on_remove(
            async_dispatcher_connect(
                self.hass,
                SIGNAL_WIN_AGENT_UPDATE.format(self.coordinator.device_id),
                self._handle_update,
            )
        )

    def _handle_update(self) -> None:
        """Handle updated sensor data."""
        self.async_write_ha_state()

    @property
    def device_info(self) -> DeviceInfo:
        """Return information about the device."""
        return DeviceInfo(
            identifiers={(DOMAIN, self.coordinator.device_id)},
            name=self.coordinator.device_name,
            manufacturer="Custom WinAgent",
            model="Windows Direct Agent",
        )

    @property
    def is_on(self) -> bool | None:
        """Return true if the binary sensor is on."""
        val = self.coordinator.sensor_data.get(self._key)
        if isinstance(val, bool):
            return val
        if isinstance(val, str):
            return val.upper() in ("ON", "TRUE", "1")
        return bool(val) if val is not None else None
