"""Switch platform for Windows Direct Agent."""
from __future__ import annotations

from typing import Any
from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import WinAgentCoordinator

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Windows Direct Agent switches."""
    coordinator: WinAgentCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([WinAgentMuteSwitch(coordinator)])

class WinAgentMuteSwitch(CoordinatorEntity[WinAgentCoordinator], SwitchEntity):
    """Representation of the Windows Audio Mute switch."""

    def __init__(self, coordinator: WinAgentCoordinator) -> None:
        """Initialize the switch."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.device_id}_mute_switch"
        self._attr_name = f"{coordinator.device_name} Mute Master Audio"
        self._attr_icon = "mdi:volume-mute"

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
        """Return true if audio is muted."""
        if not self.coordinator.data:
            return None
        val = self.coordinator.data.get("audio_mute")
        if isinstance(val, bool):
            return val
        if isinstance(val, str):
            return val.upper() in ("ON", "TRUE", "1")
        return bool(val)

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on mute."""
        await self.coordinator.async_send_action("mute_audio", {"state": True})
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off mute."""
        await self.coordinator.async_send_action("mute_audio", {"state": False})
        await self.coordinator.async_request_refresh()
