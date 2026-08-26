"""Button platform for Windows Direct Agent."""
from __future__ import annotations

from typing import Any
from homeassistant.components.button import (
    ButtonDeviceClass,
    ButtonEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import WinAgentCoordinator

BUTTON_DESCRIPTIONS = [
    {
        "key": "shutdown",
        "name": "Shutdown PC",
        "icon": "mdi:power",
        "device_class": ButtonDeviceClass.RESTART,
    },
    {
        "key": "restart",
        "name": "Restart PC",
        "icon": "mdi:restart",
        "device_class": ButtonDeviceClass.RESTART,
    },
    {
        "key": "sleep",
        "name": "Sleep PC",
        "icon": "mdi:sleep",
    },
    {
        "key": "lock",
        "name": "Lock PC",
        "icon": "mdi:lock",
    },
    {
        "key": "logoff",
        "name": "Log Off",
        "icon": "mdi:logout",
    },
]

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Windows Direct Agent buttons."""
    coordinator: WinAgentCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities = [
        WinAgentButton(coordinator, desc)
        for desc in BUTTON_DESCRIPTIONS
    ]
    async_add_entities(entities)

class WinAgentButton(CoordinatorEntity[WinAgentCoordinator], ButtonEntity):
    """Representation of a Windows Agent action button."""

    def __init__(self, coordinator: WinAgentCoordinator, desc: dict[str, Any]) -> None:
        """Initialize the button."""
        super().__init__(coordinator)
        self.desc = desc
        self._command = desc["key"]
        self._attr_unique_id = f"{coordinator.device_id}_{self._command}"
        self._attr_name = f"{coordinator.device_name} {desc['name']}"
        self._attr_icon = desc.get("icon")
        self._attr_device_class = desc.get("device_class")

    @property
    def device_info(self) -> DeviceInfo:
        """Return information about the device."""
        return DeviceInfo(
            identifiers={(DOMAIN, self.coordinator.device_id)},
            name=self.coordinator.device_name,
            manufacturer="Custom WinAgent",
            model="Windows Direct Agent",
        )

    async def async_press(self) -> None:
        """Handle the button press by broadcasting command."""
        self.coordinator.async_send_command(self._command)
