"""Constants for the Windows Direct Agent integration."""
from homeassistant.const import Platform

DOMAIN = "win_agent"
DEFAULT_PORT = 8182
DEFAULT_NAME = "Windows PC"
DEFAULT_SCAN_INTERVAL = 5

CONF_HOST = "host"
CONF_PORT = "port"
CONF_DEVICE_ID = "device_id"
CONF_DEVICE_NAME = "device_name"

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.BUTTON,
    Platform.SWITCH,
    Platform.NUMBER,
    Platform.CAMERA,
    Platform.TEXT,
]

EVENT_WIN_AGENT_COMMAND = "win_agent_command"
EVENT_WIN_AGENT_DIALOG_RESPONSE = "win_agent_dialog_response"
