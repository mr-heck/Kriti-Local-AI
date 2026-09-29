# Kriti Desktop AI Assistant - Python Integration Guide

This guide explains how to integrate the **Kriti Prehistoric Lost World UI** with your Python backend.

---

## 1. Exposed JavaScript Functions

The UI exposes three primary global functions on `window` specifically for Python calls:

### `window.addUserMessage(text)`
Adds a message bubble from the user aligned to the right.
```python
# From Python:
window.evaluate_js(f"addUserMessage({json.dumps(user_text)})")
```

### `window.addKritiMessage(text)`
Adds a response message bubble from Kriti aligned to the left with purple/amethyst accents, rich formatting, and automatically scrolls to the bottom.
```python
# From Python:
window.evaluate_js(f"addKritiMessage({json.dumps(ai_response)})")
```

### `window.setStatus(text)`
Updates the status indicator pill in the top bar.
Supported presets:
- `'Online'` - Emerald glowing pulse (ready state)
- `'Thinking'` - Amethyst/orchid pulsing light + shows animated spore typing indicator in chat
- `'Listening'` - Cyan acoustic pulse on badge + microphone button ring animation
- Any custom text - e.g. `'Downloading weights...'`, `'Processing audio...'`
```python
# From Python:
window.evaluate_js("setStatus('Thinking')")
```

### `window.currentBackground = '...'` or `setBackgroundImage(url)`
Dynamically switches the prehistoric background to any SVG, local image file, or online wallpaper URL:
```python
# From Python:
window.evaluate_js("currentBackground = 'https://example.com/jurassic-wallpaper.jpg'")
```

---

## 2. Capturing Outgoing User Messages in Python

When the user types a prompt in the input box and clicks Send (or presses Enter), the UI notifies Python through multiple mechanisms:

### Method A: PyWebView API (Recommended)
When using `pywebview`, define an API class and bind it to the window:
```python
import webview
import json

class API:
    def on_user_message(self, message):
        print("User typed:", message)
        # Call your LLM / backend logic here
        window.evaluate_js("setStatus('Thinking')")
        # When ready:
        window.evaluate_js(f"addKritiMessage('Hello traveler!')")

api = API()
window = webview.create_window('Kriti', 'index.html', js_api=api)
webview.start()
```

### Method B: Callback Assignment
You can assign an outbound callback directly in JavaScript:
```javascript
window.onKritiSendMessage = function(text) {
    // Forward to Python via WebSocket / QWebChannel / fetch()
};
```

### Method C: DOM Custom Event
The UI automatically fires a custom event `kriti:user-send`:
```javascript
window.addEventListener('kriti:user-send', (event) => {
    const message = event.detail.message;
    // Handle message
});
```

---

## 3. Supported Python Frameworks

| Framework | Best For | RAM Usage |
| :--- | :--- | :--- |
| **pywebview** | Native Windows desktop app using Microsoft Edge WebView2 | ~40-70 MB (Extremely low) |
| **PyQt6 / PySide6** | Complex multi-window desktop applications | ~100-150 MB |
| **Eel** | Quick scripting with local Chrome | ~80-120 MB |
| **FastAPI / Flask + WebSockets** | Client-Server / Browser based | Dependent on browser |

See `pywebview_demo.py` in this folder for a ready-to-run implementation!
