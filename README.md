# 🌿 Kriti - Prehistoric Lost World AI Companion UI (Natural Forest Edition)

**Kriti** is a creative desktop AI assistant interface themed as an ancient, friendly, intelligent companion living in a lost Jurassic forest valley.

Built with **HTML5, CSS3, and Vanilla JavaScript**—zero external frameworks, ultra-low RAM consumption, and optimized for smooth performance on mid-range and low-end laptops.

---

## 🌟 What's New in this Version

1. **Customizable Avatar**:
   - Avatar image is no longer hardcoded.
   - Click the circular amber avatar crest or the dedicated **Avatar** button in the top bar to choose any local `PNG`, `JPG`, or `WEBP` file.
   - Images automatically crop and scale smoothly within the circular glowing prehistoric frame.
   - Saves to browser `localStorage` and persists across sessions.

2. **Customizable Wallpaper**:
   - Open the **Wallpaper** modal and upload any local image file (`PNG`, `JPG`, `WEBP`) as the background.
   - Retains the soft dark readability overlay for crisp text contrast.
   - Persists in `localStorage` across reboots or reloads. Includes a "Reset to Default" button.

3. **Natural Forest Glow Palette**:
   - Eliminated artificial, radioactive, and cyberpunk neon greens.
   - Implemented authentic prehistoric rainforest colors: damp moss green (`#3b6545`), ancient fern green (`#47885b`, `#5a9e6f`), deep jungle canopy (`#0e291b`), and wet tropical emerald (`#3f8f5d`).
   - Atmosphere feels like an "ancient living jungle" with soft diffuse organic illumination.

4. **Atmospheric Spores, Pollen & Fireflies**:
   - Highly visible, relaxing particles (~78 motes) featuring 4 distinct types:
     - **Bioluminescent Fireflies**: Larger motes with radial glow halos and sinusoidal breathing intensity.
     - **Moss Spores**: Golden-moss glowing motes.
     - **Rainforest Pollen**: Sunlit drifting clusters.
     - **Jungle Dust**: Faint background depth-of-field particles.
   - Gentle upward thermal rise + horizontal waft (avoids snow/rain appearance).
   - Zero object allocation in animation loop; pauses on window blur for 0% idle CPU.

5. **Future-Ready Architecture (Placeholders Prepared)**:
   - **Typing animation**: `.streaming-cursor` and `.token-stream-container` ready for streaming LLM tokens.
   - **Voice indicator**: `#voice-indicator-dock` with acoustic waveform bars.
   - **Speaking indicator**: `data-status="Speaking"` support with glowing speaking ring.
   - **Memory notifications**: `#memory-notification-dock` with prehistoric amber leaf toast alerts (`window.showMemoryNotification(title, message)`).
   - **Animated Kriti avatar**: `#avatar-animated-frame` with state classes (`.state-idle`, `.state-listening`, `.state-speaking`, `.state-thinking`).

---

## 📂 Project Structure

```text
kriti-desktop-assistant/
├── index.html                                        # Single-page interface with customizable avatar & wallpaper
├── css/
│   └── style.css                                     # Natural forest theme, glassmorphism & future hooks
├── js/
│   ├── app.js                                        # Main logic, localStorage persistence, Python API
│   └── effects.js                                    # Enhanced particles (fireflies, spores, pollen, dust)
├── assets/
│   ├── prehistoric_forest.png                        # Default lost world vector wallpaper
│   ├── kriti_avatar.png                            # Default friendly creature avatar
│   └── user_avatar.png                             # Explorer amber leaf badge
├── python_bridge_examples/
│   ├── pywebview_demo.py                           # Ready-to-run desktop wrapper
│   └── bridge_documentation.md                     # Python integration guide
└── README.md                                         # Project documentation
```

---

## 🚀 How to Run

### In Any Web Browser
Simply open [`index.html`](file:///C:/Users/ABHISHEK/.gemini/antigravity/scratch/kriti-desktop-assistant/index.html).
- Upload custom avatars and wallpapers; they will persist even when refreshing!
- Click prompt chips or type messages to test responses.

### With Python Native Desktop Window (PyWebView)
```bash
pip install pywebview
python python_bridge_examples/pywebview_demo.py
```
