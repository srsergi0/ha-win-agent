"""Text platform for Windows Direct Agent."""
from __future__ import annotations

from typing import Any
from homeassistant.components.text import TextEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import WinAgentCoordinator

TEXT_DESCRIPTIONS = [
    {
        "key": "launch_url",
        "name": "Launch URL",
        "icon": "mdi:web",
    },
    {
        "key": "send_keys",
        "name": "Send Keystroke",
        "icon": "mdi:keyboard",
    },
    {
        "key": "send_notification",
        "name": "Send Windows Notification",
        "icon": "mdi:message-text",
    },
]

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Windows Direct Agent text entities."""
    coordinator: WinAgentCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities = [
        WinAgentText(coordinator, desc)
        for desc in TEXT_DESCRIPTIONS
    ]
    async_add_entities(entities)

class WinAgentText(CoordinatorEntity[WinAgentCoordinator], TextEntity):
    """Representation of a text command input entity."""

    def __init__(self, coordinator: WinAgentCoordinator, desc: dict[str, Any]) -> None:
        """Initialize the text entity."""
        super().__init__(coordinator)
        self.desc = desc
        self._command = desc["key"]
        self._attr_unique_id = f"{coordinator.device_id}_{self._command}"
        self._attr_name = f"{coordinator.device_name} {desc['name']}"
        self._attr_icon = desc.get("icon")
        self._state_value = ""

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
    def native_value(self) -> str:
        """Return the state of the text entity."""
        return self._state_value

    async def async_set_value(self, value: str) -> None:
        """Set the text value and dispatch action."""
        self._state_value = value
        self.async_write_ha_state()

        if self._command == "launch_url":
            await self.coordinator.async_send_action("launch_url", {"url": value})
        elif self._command == "send_keys":
            await self.coordinator.async_send_action("send_keys", {"keys": value})
        elif self._command == "send_notification":
            await self.coordinator.async_send_action("send_notification", {"title": "Home Assistant", "message": value})
