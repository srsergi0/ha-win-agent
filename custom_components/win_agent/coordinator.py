"""DataUpdateCoordinator for Windows Direct Agent."""
from __future__ import annotations

import asyncio
from datetime import timedelta
import logging
from typing import Any

import aiohttp
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)

class WinAgentCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Class to manage fetching data from the Windows PC agent."""

    def __init__(self, hass: HomeAssistant, host: str, port: int, device_id: str, device_name: str) -> None:
        """Initialize the coordinator."""
        self.host = host
        self.port = port
        self.device_id = device_id
        self.device_name = device_name
        self.base_url = f"http://{host}:{port}"
        self._session: aiohttp.ClientSession | None = None

        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_{device_id}",
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from the PC agent API."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/api/sensors", timeout=aiohttp.ClientTimeout(total=4)) as resp:
                    if resp.status != 200:
                        raise UpdateFailed(f"Error fetching sensor data: HTTP {resp.status}")
                    data = await resp.json()
                    return data.get("sensors", {})
        except asyncio.TimeoutError as err:
            raise UpdateFailed(f"Timeout connecting to Windows Agent at {self.base_url}") from err
        except Exception as err:
            raise UpdateFailed(f"Connection error to Windows Agent: {err}") from err

    async def async_send_action(self, command: str, data: dict[str, Any] | None = None) -> Any:
        """Send a command directly to the Windows Agent."""
        payload = {
            "command": command,
            "data": data or {},
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/action",
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=10),
                ) as resp:
                    if resp.status == 200:
                        res_json = await resp.json()
                        return res_json.get("result")
                    else:
                        _LOGGER.error("Failed to execute %s on %s: HTTP %s", command, self.base_url, resp.status)
                        return None
        except Exception as err:
            _LOGGER.error("Error sending action %s to %s: %s", command, self.base_url, err)
            return None
