"""Camera platform for Windows Direct Agent."""
from __future__ import annotations

import base64
import logging
from homeassistant.components.camera import Camera
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import WinAgentCoordinator

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Windows Direct Agent camera."""
    coordinator: WinAgentCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([WinAgentScreenCamera(coordinator)])

class WinAgentScreenCamera(CoordinatorEntity[WinAgentCoordinator], Camera):
    """Representation of the desktop screen capture camera."""

    def __init__(self, coordinator: WinAgentCoordinator) -> None:
        """Initialize the camera."""
        CoordinatorEntity.__init__(self, coordinator)
        Camera.__init__(self)
        self._attr_unique_id = f"{coordinator.device_id}_screen_camera"
        self._attr_name = f"{coordinator.device_name} Screen Capture"
        self._attr_icon = "mdi:monitor-screenshot"
        self._last_image: bytes | None = None

    @property
    def device_info(self) -> DeviceInfo:
        """Return information about the device."""
        return DeviceInfo(
            identifiers={(DOMAIN, self.coordinator.device_id)},
            name=self.coordinator.device_name,
            manufacturer="Custom WinAgent",
            model="Windows Direct Agent",
        )

    async def async_camera_image(
        self, width: int | None = None, height: int | None = None
    ) -> bytes | None:
        """Return a fresh screen capture image."""
        try:
            res = await self.coordinator.async_send_action("take_screenshot")
            if res and isinstance(res, str):
                self._last_image = base64.b64decode(res)
        except Exception as err:
            _LOGGER.debug("Error capturing screen image: %s", err)

        return self._last_image
