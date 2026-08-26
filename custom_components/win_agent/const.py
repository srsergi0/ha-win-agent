"""Constants for the Windows Direct Agent integration."""
from homeassistant.const import Platform

DOMAIN = "win_agent"
DEFAULT_NAME = "Windows PC"
DEFAULT_DEVICE_ID = "sergio_pc_agent"

CONF_DEVICE_ID = "device_id"
CONF_DEVICE_NAME = "device_name"

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.BUTTON,
    Platform.NUMBER,
    Platform.CAMERA,
    Platform.TEXT,
]

EVENT_WIN_AGENT_COMMAND = "win_agent_command"
EVENT_WIN_AGENT_TELEMETRY = "win_agent_telemetry"
EVENT_WIN_AGENT_STATE_UPDATE = "win_agent_state_update"
EVENT_WIN_AGENT_DIALOG_RESPONSE = "win_agent_dialog_response"
SIGNAL_WIN_AGENT_UPDATE = "win_agent_update_{}"
