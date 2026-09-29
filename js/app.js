/**
 * KRITI - Creative Prehistoric AI Companion UI (Natural Forest Edition)
 * Pure Vanilla JavaScript (No external frameworks)
 * Optimized for low-end / mid-range PCs & seamless Python backend integration.
 */

// ==========================================================================
// 1. DYNAMIC ASSET & PERSISTENCE SYSTEM (Avatar & Wallpaper)
// ==========================================================================

const DEFAULT_WALLPAPER = 'assets/prehistoric_forest.png';
const DEFAULT_AVATAR = 'assets/kriti_avatar.png';

let _currentBackground = DEFAULT_WALLPAPER;
let _currentAvatar = DEFAULT_AVATAR;

/**
 * Set and update the lost world background image.
 * Supports presets, local data URLs, image paths, and web URLs.
 * Automatically saves to localStorage if persist is true.
 */
function setBackgroundImage(url, persist = true) {
  if (!url) return;
  _currentBackground = url;
  const root = document.documentElement;
  
  if (url === 'misty_amber') {
    root.style.setProperty('--bg-image', 'linear-gradient(135deg, #1b120a 0%, #0d2318 50%, #06150e 100%)');
  } else if (url === 'deep_emerald') {
    root.style.setProperty('--bg-image', 'linear-gradient(135deg, #020a06 0%, #0c2b1c 50%, #133a27 100%)');
  } else if (url === 'orchid_cavern') {
    root.style.setProperty('--bg-image', 'linear-gradient(135deg, #180624 0%, #0b1a12 60%, #040e08 100%)');
  } else if (url.startsWith('data:') || url.startsWith('http') || url.includes('/')) {
    root.style.setProperty('--bg-image', `url("${url}")`);
  } else {
    root.style.setProperty('--bg-image', `url("${url}")`);
  }

  if (persist) {
    try {
      localStorage.setItem('kriti_wallpaper', url);
    } catch (e) {
      console.warn("Could not save wallpaper to localStorage (storage quota):", e);
    }
  }

  // Update active state in modal if open
  updateWallpaperModalActiveState(url);
}

// Allow changing the background directly via window.currentBackground = '...'
Object.defineProperty(window, 'currentBackground', {
  get: () => _currentBackground,
  set: (val) => setBackgroundImage(val, true)
});

/**
 * Set and update Kriti's avatar image.
 * Updates top bar crest, message bubbles, and persists to localStorage.
 */
function setKritiAvatar(avatarSrc, persist = true) {
  if (!avatarSrc) return;
  _currentAvatar = avatarSrc;

  // 1. Update top bar crest
  const headerAvatarImg = document.getElementById('header-avatar-img');
  if (headerAvatarImg) {
    headerAvatarImg.src = avatarSrc;
  }

  // 2. Update existing Kriti message avatars in the chat
  const msgAvatars = document.querySelectorAll('.message-entry.kriti .message-avatar img');
  msgAvatars.forEach(img => {
    img.src = avatarSrc;
  });

  // 3. Persist to localStorage
  if (persist) {
    try {
      localStorage.setItem('kriti_custom_avatar', avatarSrc);
    } catch (e) {
      console.warn("Could not save avatar to localStorage (storage quota):", e);
    }
  }
}

// Allow changing avatar directly via window.currentAvatar = '...'
Object.defineProperty(window, 'currentAvatar', {
  get: () => _currentAvatar,
  set: (val) => setKritiAvatar(val, true)
});

// ==========================================================================
// 2. PYTHON INTEGRATION API (Direct Global Window Functions)
// ==========================================================================

/**
 * Inserts a message sent by the human user.
 * @param {string} text - Message text to display
 */
window.addUserMessage = function(text) {
  if (!text || !text.trim()) return;
  appendMessage('user', text.trim());
};

/**
 * Inserts a response from Kriti, the AI Companion.
 * @param {string} text - Message text to display
 */
window.addKritiMessage = function(text) {
  if (!text || !text.trim()) return;
  
  // If typing indicator was visible, hide it
  setTypingIndicator(false);
  
  appendMessage('kriti', text.trim());
  
  // Return status to Online after response arrives
  if (getCurrentStatus() === 'Thinking') {
    window.setStatus('Online');
  }
};

/**
 * Updates the AI Companion status badge.
 * Standard states: 'Online' | 'Thinking' | 'Listening' | 'Speaking'
 * Also accepts custom status strings.
 * @param {string} text - New status text
 */
window.setStatus = function(text) {
  const statusBadge = document.getElementById('status-badge');
  const statusLabel = document.getElementById('status-text');
  const micBtn = document.getElementById('mic-btn');
  if (!statusBadge || !statusLabel) return;

  const cleanText = (text || 'Online').trim();
  statusLabel.textContent = cleanText;

  // Normalize state for styling hooks
  const lower = cleanText.toLowerCase();
  let mappedState = 'Online';
  if (lower.includes('think')) mappedState = 'Thinking';
  else if (lower.includes('listen')) mappedState = 'Listening';
  else if (lower.includes('speak')) mappedState = 'Speaking';
  else if (lower.includes('offline')) mappedState = 'Offline';

  statusBadge.setAttribute('data-status', mappedState);
  statusBadge.setAttribute('title', `System Status: ${cleanText}`);

  // Manage typing indicator visibility
  if (mappedState === 'Thinking') {
    setTypingIndicator(true);
    window.setAvatarState('thinking');
  } else if (mappedState === 'Speaking') {
    setTypingIndicator(false);
    window.setAvatarState('speaking');
  } else if (mappedState === 'Listening') {
    setTypingIndicator(false);
    window.setAvatarState('listening');
  } else {
    setTypingIndicator(false);
    window.setAvatarState('idle');
  }

  // Manage microphone pulse state
  if (micBtn) {
    if (mappedState === 'Listening') {
      micBtn.classList.add('listening');
    } else {
      micBtn.classList.remove('listening');
    }
  }

  // Dispatch custom event for external listeners
  window.dispatchEvent(new CustomEvent('kriti:status-change', { detail: { status: cleanText } }));
};

/**
 * Returns current status string
 */
function getCurrentStatus() {
  const label = document.getElementById('status-text');
  return label ? label.textContent.trim() : 'Online';
}

/**
 * Toggle or set typing indicator visibility
 */
function setTypingIndicator(show) {
  const indicator = document.getElementById('typing-indicator');
  const chatMessages = document.getElementById('chat-messages');
  if (!indicator || !chatMessages) return;

  if (show) {
    indicator.classList.add('visible');
    chatMessages.appendChild(indicator); // Keep at bottom
    scrollToBottom();
  } else {
    indicator.classList.remove('visible');
  }
}

// Outbound hook: When the user submits a message from the UI
window.onKritiSendMessage = null;

// ==========================================================================
// 3. FUTURE-READY ARCHITECTURAL HOOKS (Placeholders)
// ==========================================================================

/**
 * Future Hook: Change Animated Avatar State (idle, listening, speaking, thinking)
 */
window.setAvatarState = function(state) {
  const frame = document.getElementById('avatar-animated-frame');
  if (!frame) return;
  frame.className = `avatar-animated-frame state-${state || 'idle'}`;
};

/**
 * Future Hook: Display a Prehistoric Memory Notification Toast
 * @param {string} title
 * @param {string} message
 * @param {number} duration
 */
window.showMemoryNotification = function(title, message, duration = 4000) {
  const dock = document.getElementById('memory-notification-dock');
  if (!dock) return;

  const toast = document.createElement('div');
  toast.className = 'memory-toast';
  toast.innerHTML = `
    <span style="color: var(--amber-gold); font-size: 1.1rem;">🌿</span>
    <div>
      <strong style="color: var(--amber-soft); display: block; font-size: 0.8rem;">${title || 'Memory Recorded'}</strong>
      <span style="font-size: 0.78rem; color: var(--text-secondary);">${message || ''}</span>
    </div>
  `;

  dock.appendChild(toast);
  setTimeout(() => {
    toast.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(-10px)';
    setTimeout(() => toast.remove(), 400);
  }, duration);
};

/**
 * Future Hook: Toggle or adjust Voice Indicator waves
 */
window.setVoiceIndicator = function(active, level = 1) {
  const dock = document.getElementById('voice-indicator-dock');
  if (!dock) return;
  if (active) {
    dock.classList.add('active');
  } else {
    dock.classList.remove('active');
  }
};

// ==========================================================================
// 4. CHAT RENDERING & FORMATTING (Lightweight Markdown & Sanitization)
// ==========================================================================

function formatTime() {
  const now = new Date();
  let hours = now.getHours();
  const minutes = String(now.getMinutes()).padStart(2, '0');
  const ampm = hours >= 12 ? 'PM' : 'AM';
  hours = hours % 12 || 12;
  return `${hours}:${minutes} ${ampm}`;
}

/**
 * Escape raw HTML to prevent injection, then render safe markdown.
 */
function renderMarkdown(text) {
  let safe = text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");

  // Code blocks (```language ... ```)
  safe = safe.replace(/```([\s\S]*?)```/g, (match, code) => {
    return `<pre><code>${code.trim()}</code></pre>`;
  });

  // Inline code (`code`)
  safe = safe.replace(/`([^`]+)`/g, '<code>$1</code>');

  // Bold (**text**)
  safe = safe.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');

  // Italic (*text*)
  safe = safe.replace(/\*([^*]+)\*/g, '<em>$1</em>');

  // Paragraphs / newlines
  const paragraphs = safe.split(/\n\s*\n/);
  return paragraphs
    .map(p => `<p>${p.replace(/\n/g, '<br>')}</p>`)
    .join('');
}

function appendMessage(sender, text) {
  const chatContainer = document.getElementById('chat-messages');
  const typingIndicator = document.getElementById('typing-indicator');
  if (!chatContainer) return;

  const isUser = sender === 'user';
  const entry = document.createElement('div');
  entry.className = `message-entry ${isUser ? 'user' : 'kriti'}`;

  // Use dynamic avatar for Kriti or user explorer badge
  const avatarSrc = isUser ? 'assets/user_avatar.png' : _currentAvatar;
  const avatarClass = isUser ? 'user-avatar-img' : 'kriti-msg-avatar';
  const senderName = isUser ? 'Explorer' : 'Kriti';
  const timeStr = formatTime();

  entry.innerHTML = `
    <div class="message-avatar">
      <img src="${avatarSrc}" alt="${senderName}" class="${avatarClass}">
    </div>
    <div class="message-bubble">
      <div class="message-meta">
        <span class="message-sender">${senderName}</span>
        <span class="message-time">${timeStr}</span>
      </div>
      <div class="message-body">
        ${renderMarkdown(text)}
      </div>
    </div>
  `;

  // Insert before typing indicator if present
  if (typingIndicator && typingIndicator.parentNode === chatContainer) {
    chatContainer.insertBefore(entry, typingIndicator);
  } else {
    chatContainer.appendChild(entry);
  }

  scrollToBottom();
}

function scrollToBottom() {
  const chatContainer = document.getElementById('chat-messages');
  if (!chatContainer) return;
  chatContainer.scrollTo({
    top: chatContainer.scrollHeight,
    behavior: 'smooth'
  });
}

// ==========================================================================
// 5. STANDALONE INTERACTIVE FALLBACK (Warm Prehistoric AI Personality)
// ==========================================================================

const KRITI_PREHISTORIC_RESPONSES = [
  "From across the canopy of giant ferns, I hear your words! 🌿 In this ancient valley, creativity flows like primordial mountain streams. Let's sculpt this idea into something wondrous.",
  "Deep in the mossy hollows, time moves gently. What you've shared sparks the ancient runes of imagination. How would you like to expand this world?",
  "The prehistoric trees whisper memories of a billion sunrises. Your thought has that same rare spark—both wild and brilliant. Tell me more, traveler!",
  "I've fluttered past the misty caldera to bring you this: every great creation starts with a single step into the uncharted jungle. Shall we explore further?",
  "A marvelous query! Even in the Cretaceous twilight, such creative curiosities would illuminate the shadowed groves with soft, living bioluminescence."
];

function handleUserSubmission() {
  const input = document.getElementById('user-input');
  if (!input) return;
  const text = input.value.trim();
  if (!text) return;

  // Add user bubble
  window.addUserMessage(text);
  input.value = '';
  input.style.height = 'auto'; // Reset height

  // 1. If Python backend listener is registered
  if (typeof window.onKritiSendMessage === 'function') {
    window.onKritiSendMessage(text);
    return;
  }

  // 2. Check for PyWebView API binding
  if (window.pywebview && window.pywebview.api && typeof window.pywebview.api.on_user_message === 'function') {
    window.setStatus('Thinking');
    window.pywebview.api.on_user_message(text);
    return;
  }

  // 3. Dispatch standard DOM event for any Python / Web channel bridge
  window.dispatchEvent(new CustomEvent('kriti:user-send', { detail: { message: text } }));

  // 4. Standalone Fallback Simulation (if running in browser without Python)
  window.setStatus('Thinking');
  const delay = 800 + Math.random() * 1200;
  setTimeout(() => {
    const lower = text.toLowerCase();
    let reply = "";
    
    if (lower.includes('valley') || lower.includes('explore')) {
      reply = "Beyond the ridge of giant tree ferns lies the Hidden Emerald Basin. Steam rises from crystalline hot springs, and ancient dragonfly kin with wingspans like banners dance over the waters. It's a sanctuary of pure imagination.";
    } else if (lower.includes('story') || lower.includes('adventure')) {
      reply = "Imagine an explorer whose compass needle spins toward ancient amber stones rather than north. You discover a hidden canyon where prehistoric birds sing harmonies that open stone vaults carved into the living rock...";
    } else if (lower.includes('instinct') || lower.includes('unique')) {
      reply = "Unlike cold, rigid machines, my instincts are woven from the living fabric of prehistoric nature: patience like ancient granite, curiosity like a young raptor watching the dawn, and creativity that blooms like wild rainforest orchids.";
    } else if (lower.includes('poem') || lower.includes('ferns')) {
      reply = "*Silver mist rolls soft and deep,*\n*Where ancient giant cycads sleep.*\n*Through amber twilight, shadows gleam,*\n*A prehistoric lost-world dream.* 🌿✨";
    } else {
      const idx = Math.floor(Math.random() * KRITI_PREHISTORIC_RESPONSES.length);
      reply = KRITI_PREHISTORIC_RESPONSES[idx];
    }

    window.addKritiMessage(reply);
  }, delay);
}

// ==========================================================================
// 6. INITIALIZATION & EVENT LISTENERS
// ==========================================================================

function updateWallpaperModalActiveState(activeBg) {
  const bgCards = document.querySelectorAll('.bg-option-card');
  bgCards.forEach(card => {
    if (card.getAttribute('data-bg') === activeBg) {
      card.classList.add('active');
    } else {
      card.classList.remove('active');
    }
  });
}

document.addEventListener('DOMContentLoaded', () => {
  // 1. Restore Persisted Wallpaper (or use default)
  const savedBg = localStorage.getItem('kriti_wallpaper');
  if (savedBg) {
    setBackgroundImage(savedBg, false);
  } else {
    setBackgroundImage(_currentBackground, false);
  }

  // 2. Restore Persisted Avatar (or use default)
  const savedAvatar = localStorage.getItem('kriti_custom_avatar');
  if (savedAvatar) {
    setKritiAvatar(savedAvatar, false);
  } else {
    setKritiAvatar(_currentAvatar, false);
  }

  // 3. Initialize Atmospheric Spores & Fireflies Canvas
  let effectsEngine = null;
  if (window.KritiEffects) {
    effectsEngine = new window.KritiEffects('effects-canvas');
  }

  // 4. Set welcome time stamp
  const welcomeTime = document.getElementById('welcome-time');
  if (welcomeTime) welcomeTime.textContent = formatTime();

  // Elements
  const userInput = document.getElementById('user-input');
  const sendBtn = document.getElementById('send-btn');
  const micBtn = document.getElementById('mic-btn');
  const ecoBtn = document.getElementById('eco-mode-btn');
  const clearBtn = document.getElementById('clear-chat-btn');
  const headerAvatarCrest = document.getElementById('header-avatar-crest');
  const avatarPickerBtn = document.getElementById('avatar-picker-btn');
  const avatarFileInput = document.getElementById('avatar-file-input');
  const bgPickerBtn = document.getElementById('bg-picker-btn');
  const bgModal = document.getElementById('bg-modal');
  const modalCloseBtn = document.getElementById('modal-close-btn');
  const uploadLocalBgBtn = document.getElementById('upload-local-bg-btn');
  const bgFileInput = document.getElementById('bg-file-input');
  const applyCustomBgBtn = document.getElementById('apply-custom-bg');
  const customBgInput = document.getElementById('custom-bg-input');
  const resetBgBtn = document.getElementById('reset-bg-btn');

  // ========================================================================
  // Customizable Avatar Handlers (File input -> FileReader -> localStorage)
  // ========================================================================
  function triggerAvatarFileSelection() {
    if (avatarFileInput) avatarFileInput.click();
  }

  if (headerAvatarCrest) {
    headerAvatarCrest.addEventListener('click', triggerAvatarFileSelection);
  }
  if (avatarPickerBtn) {
    avatarPickerBtn.addEventListener('click', triggerAvatarFileSelection);
  }

  if (avatarFileInput) {
    avatarFileInput.addEventListener('change', function(e) {
      const file = e.target.files && e.target.files[0];
      if (!file) return;

      const reader = new FileReader();
      reader.onload = function(evt) {
        const dataUrl = evt.target.result;
        setKritiAvatar(dataUrl, true);
        window.showMemoryNotification('Avatar Updated', 'Kriti took on a new appearance 🌿');
      };
      reader.readAsDataURL(file);
      // Reset input so same file can be reselected if edited
      this.value = '';
    });
  }

  // ========================================================================
  // Customizable Wallpaper Handlers (File input -> FileReader -> localStorage)
  // ========================================================================
  if (uploadLocalBgBtn && bgFileInput) {
    uploadLocalBgBtn.addEventListener('click', () => bgFileInput.click());
  }

  if (bgFileInput) {
    bgFileInput.addEventListener('change', function(e) {
      const file = e.target.files && e.target.files[0];
      if (!file) return;

      const reader = new FileReader();
      reader.onload = function(evt) {
        const dataUrl = evt.target.result;
        setBackgroundImage(dataUrl, true);
        if (bgModal) bgModal.classList.remove('active');
        window.showMemoryNotification('Wallpaper Set', 'The lost world vista has changed 🌿');
      };
      reader.readAsDataURL(file);
      this.value = '';
    });
  }

  if (resetBgBtn) {
    resetBgBtn.addEventListener('click', () => {
      setBackgroundImage(DEFAULT_WALLPAPER, true);
      if (bgModal) bgModal.classList.remove('active');
      window.showMemoryNotification('Wallpaper Reset', 'Returned to the Jurassic Canopy.');
    });
  }

  // Auto-growing Textarea & Enter to Send
  if (userInput) {
    userInput.addEventListener('input', function() {
      this.style.height = 'auto';
      this.style.height = Math.min(this.scrollHeight, 140) + 'px';
    });

    userInput.addEventListener('keydown', function(e) {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleUserSubmission();
      }
    });
  }

  // Send Button Click
  if (sendBtn) {
    sendBtn.addEventListener('click', handleUserSubmission);
  }

  // Microphone Button (Toggles Listening state placeholder)
  if (micBtn) {
    micBtn.addEventListener('click', () => {
      const current = getCurrentStatus();
      if (current === 'Listening') {
        window.setStatus('Online');
      } else {
        window.setStatus('Listening');
      }
    });
  }

  // Eco Mode Toggle (Low-End PC performance booster)
  if (ecoBtn) {
    let ecoActive = false;
    ecoBtn.addEventListener('click', () => {
      ecoActive = !ecoActive;
      ecoBtn.classList.toggle('active', ecoActive);
      if (effectsEngine) {
        effectsEngine.setEcoMode(ecoActive);
      }
      ecoBtn.setAttribute('title', ecoActive ? 'Eco Mode Active (Low RAM/CPU)' : 'Eco Mode Disabled (Atmospheric FX On)');
    });
  }

  // Clear Chat Button
  if (clearBtn) {
    clearBtn.addEventListener('click', () => {
      const chatContainer = document.getElementById('chat-messages');
      if (!chatContainer) return;
      
      const entries = chatContainer.querySelectorAll('.message-entry:not(:first-child)');
      entries.forEach(el => el.remove());
      window.setStatus('Online');
    });
  }

  // Starter Prompts Chips
  const promptChips = document.querySelectorAll('.prompt-chip');
  promptChips.forEach(chip => {
    chip.addEventListener('click', function() {
      const prompt = this.getAttribute('data-prompt');
      if (userInput && prompt) {
        userInput.value = prompt;
        handleUserSubmission();
      }
    });
  });

  // Background Picker Modal
  if (bgPickerBtn && bgModal) {
    bgPickerBtn.addEventListener('click', () => bgModal.classList.add('active'));
    
    if (modalCloseBtn) {
      modalCloseBtn.addEventListener('click', () => bgModal.classList.remove('active'));
    }
    
    bgModal.addEventListener('click', (e) => {
      if (e.target === bgModal) bgModal.classList.remove('active');
    });

    const bgCards = document.querySelectorAll('.bg-option-card');
    bgCards.forEach(card => {
      card.addEventListener('click', function() {
        const bg = this.getAttribute('data-bg');
        setBackgroundImage(bg, true);
        bgModal.classList.remove('active');
      });
    });

    if (applyCustomBgBtn && customBgInput) {
      applyCustomBgBtn.addEventListener('click', () => {
        const val = customBgInput.value.trim();
        if (val) {
          setBackgroundImage(val, true);
          bgModal.classList.remove('active');
        }
      });
    }
  }

  console.log("🌿 Kriti AI Companion (Natural Forest Edition) initialized.");
});
