"""Number platform for Windows Direct Agent."""
from __future__ import annotations

from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE
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
    """Set up the Windows Direct Agent number entities."""
    coordinator: WinAgentCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([WinAgentVolumeNumber(coordinator)])

class WinAgentVolumeNumber(CoordinatorEntity[WinAgentCoordinator], NumberEntity):
    """Representation of the Master Volume slider."""

    _attr_native_min_value = 0
    _attr_native_max_value = 100
    _attr_native_step = 1
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_mode = NumberMode.SLIDER

    def __init__(self, coordinator: WinAgentCoordinator) -> None:
        """Initialize the volume number entity."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.device_id}_master_volume_slider"
        self._attr_name = f"{coordinator.device_name} Master Volume"
        self._attr_icon = "mdi:volume-high"

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
    def native_value(self) -> float | None:
        """Return the current volume value."""
        val = self.coordinator.sensor_data.get("audio_volume")
        try:
            return float(val) if val is not None else None
        except (ValueError, TypeError):
            return None

    async def async_set_native_value(self, value: float) -> None:
        """Set the volume value."""
        int_val = int(value)
        self.coordinator.update_state_locally("audio_volume", int_val)
        self.coordinator.async_send_command("set_volume", {"volume": int_val})
