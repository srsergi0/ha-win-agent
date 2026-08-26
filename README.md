# 🖥️ Windows Direct Agent for Home Assistant

[![HACS Custom](https://img.shields.io/badge/HACS-Custom_Repository-orange.svg?style=for-the-badge)](https://hacs.xyz/)
[![Home Assistant](https://img.shields.io/badge/Home_Assistant-2024.1+-blue.svg?style=for-the-badge&logo=home-assistant)](https://www.home-assistant.io/)
[![Platform](https://img.shields.io/badge/Windows-10%20%7C%2011-0078D6.svg?style=for-the-badge&logo=windows)](https://microsoft.com)
[![ElectroBun](https://img.shields.io/badge/Desktop_App-ElectroBun-8b5cf6.svg?style=for-the-badge)](https://bun.sh)

Integración oficial y aplicación de escritorio nativa **ElectroBun** para conectar y controlar tu PC con Windows directamente desde **Home Assistant** con latencia ultrabaja, cero dependencias de brokers MQTT externos y soporte completo para 19+ sensores, botones de control, sliders de volumen y servicios interactivos.

---

## 🌟 Características Principales

- 🚀 **Conexión Directa LAN Punto a Punto**: Comunicación en tiempo real (WebSocket + REST) entre la aplicación de escritorio y Home Assistant sin necesidad de instalar o mantener brokers MQTT.
- 🎨 **Aplicación de Escritorio ElectroBun**:
  - Panel visual Glassmorphic Dark moderno.
  - Visor de tráfico y eventos en streaming en vivo con inspector de payloads JSON.
  - Configuración integrada de URL y Token de Home Assistant con prueba de conexión instantánea.
  - Centro de pruebas interactivas (captura de pantalla, notificaciones Toast, diálogo de confirmación, etc.).
- 📊 **19+ Sensores Inteligentes**:
  - 🖥️ **Ventana Activa**: Muestra la app o juego en primer plano (`msedge`, `Code`, `spotify`, etc.).
  - 🎵 **Multimedia en Reproducción**: Título, artista y fuente de audio actual.
  - 🔒 **Bloqueo de Sesión**: Detecta si la pantalla está bloqueada (`Win + L`).
  - 🎮 **Modo Juego / Pantalla Completa**: Detección de juegos y reproducción de vídeo inmersiva.
  - 🎙️ **Micrófono & 👁️ Cámara Web**: Indicadores de privacidad cuando el micrófono o cámara están en uso.
  - 👤 **Presencia & Inactividad del Usuario**: Tiempo exacto de inactividad de teclado/ratón.
  - ⚡ **Hardware**: CPU Load (%), RAM Usage (%), Primary Disk C: (%), GPU Load (%), Batería (%).
  - 🔊 **Volumen Maestro & Estado de Silencio**.
  - 📶 **Red Wi-Fi (SSID) / Ethernet**.
  - 📸 **Captura de Pantalla en Vivo**: Entidad de cámara de Home Assistant para capturar la pantalla a demanda.
- 🕹️ **Controles y Botones**:
  - 🔴 Apagar PC, 🔄 Reiniciar PC, 🌙 Suspender PC, 🔒 Bloquear PC, 🚪 Cerrar Sesión.
  - 🔊 Control deslizante de volumen (0-100%) y Switch de Silencio.
  - ⏯️ Controles de reproducción multimedia (Play/Pause, Siguiente, Anterior).
  - 💬 Notificaciones Windows nativas (Toast) y Diálogo de Confirmación Glassmorphic personalizado.

---

## 📦 Instalación mediante HACS

1. Abre **Home Assistant** y dirígete a **HACS** > **Integraciones**.
2. Haz clic en los **3 puntos (esquina superior derecha)** y selecciona **Repositorios personalizados**.
3. Pega la URL de este repositorio: `https://github.com/srsergi0/ha-win-agent` (o la URL de tu repo en GitHub).
4. En **Categoría**, selecciona `Integración` y haz clic en **Añadir**.
5. Busca **Windows Direct Agent**, haz clic en **Descargar** y luego **reinicia Home Assistant**.
6. En Home Assistant, ve a **Ajustes** > **Dispositivos y Servicios** > **Añadir Integración** y busca **Windows Direct Agent**.
7. Ingresa la IP de tu PC con Windows (ej: `192.168.1.50`) y el puerto (por defecto: `8182`).

---

## 💻 Configuración de la App de Escritorio ElectroBun

1. Inicia la aplicación en tu PC con Windows:
   ```powershell
   cd d:\Project\IoT-Hardware\win-mqtt-agent
   bun run dev
   ```
2. En la pestaña **Configuración HA**:
   - Ingresa la URL de tu Home Assistant (ej. `http://192.168.1.100:8123`).
   - Ingresa tu **Token de Acceso de Larga Duración** (obtenido en tu Perfil de Home Assistant > Tokens de acceso).
   - Haz clic en **Guardar y Conectar**.
3. ¡Listo! Observa en la pestaña **Tráfico en Vivo** cómo todos los sensores y métricas se sincronizan instantáneamente.

---

## 🎛️ Tarjeta Lovelace Recomendada para tu Dashboard

Puedes agregar esta tarjeta en tu panel de Home Assistant para visualizar el estado de tu PC:

```yaml
type: entities
title: 🖥️ Sergio PC
entities:
  - entity: sensor.sergio_pc_active_window
  - entity: sensor.sergio_pc_media_playing_info
  - entity: sensor.sergio_pc_cpu_load
  - entity: sensor.sergio_pc_memory_usage
  - entity: sensor.sergio_pc_gpu_load
  - entity: sensor.sergio_pc_primary_storage_usage
  - entity: number.sergio_pc_master_volume
  - entity: switch.sergio_pc_mute_master_audio
  - entity: binary_sensor.sergio_pc_session_locked
  - entity: binary_sensor.sergio_pc_fullscreen_gaming_mode
  - entity: binary_sensor.sergio_pc_microphone_in_use
  - entity: button.sergio_pc_lock_pc
  - entity: button.sergio_pc_sleep_pc
  - entity: button.sergio_pc_take_screenshot
```

---

## 📄 Licencia

Distribuido bajo la Licencia MIT. Consulta `LICENSE` para más detalles.
