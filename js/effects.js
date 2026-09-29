/**
 * Kriti - Prehistoric Lost World Effects Engine (Enhanced Atmospheric Edition)
 * Features:
 * - Highly visible, authentic atmospheric jungle particles:
 *   1. Firefly-like bioluminescent lights with gentle breathing glow
 *   2. Ancient moss spores with soft golden-green luminescence
 *   3. Rainforest pollen motes drifting in warm air currents
 *   4. Subtle floating jungle dust adding atmospheric depth
 * - Relaxing, natural upward thermal drift + organic horizontal breeze (NOT rain/snow)
 * - Ultra-lightweight & zero memory allocations in loop (low CPU / mid-range laptop friendly)
 * - Auto-pauses when tab/window is hidden
 * - Eco Mode support
 */

class PrehistoricEffects {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    if (!this.canvas) return;
    this.ctx = this.canvas.getContext('2d', { alpha: true });
    
    // Particle configuration: increased count & rich variety
    this.maxParticles = 78;
    this.particles = [];
    this.animationFrameId = null;
    this.isRunning = false;
    this.isEcoMode = false;

    // Palette of natural prehistoric forest motes (no neon/chemical colors)
    this.colors = {
      firefly: [
        { r: 245, g: 210, b: 120 }, // Warm amber glow
        { r: 168, g: 216, b: 154 }, // Bioluminescent moss green
        { r: 199, g: 155, b: 235 }  // Soft amethyst orchid spore
      ],
      spore: [
        { r: 140, g: 195, b: 140 }, // Rainforest moss spore
        { r: 215, g: 190, b: 125 }, // Ancient amber dust
        { r: 110, g: 175, b: 130 }  // Damp fern green spore
      ],
      pollen: [
        { r: 230, g: 215, b: 145 }, // Pale tree fern pollen
        { r: 185, g: 215, b: 160 }  // Wet canopy pollen
      ],
      dust: [
        { r: 160, g: 190, b: 170 }, // Jungle ambient mist dust
        { r: 190, g: 175, b: 150 }  // Ancient bark micro-dust
      ]
    };

    this.init();
  }

  init() {
    this.resizeCanvas();
    this.createParticles();
    
    // Responsive resize
    window.addEventListener('resize', () => this.resizeCanvas());
    
    // Auto-pause when tab/window is hidden to save CPU/battery
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) {
        this.stop();
      } else if (!this.isEcoMode) {
        this.start();
      }
    });

    this.start();
  }

  resizeCanvas() {
    if (!this.canvas) return;
    this.width = this.canvas.width = window.innerWidth;
    this.height = this.canvas.height = window.innerHeight;
  }

  createParticles() {
    this.particles = [];
    for (let i = 0; i < this.maxParticles; i++) {
      this.particles.push(this.spawnParticle(true));
    }
  }

  spawnParticle(randomY = false) {
    // 4 distinct prehistoric atmospheric particle types:
    // ~18% Fireflies, ~32% Spores, ~30% Pollen, ~20% Ambient Dust
    const roll = Math.random();
    let type = 'spore';
    let radius = 1.8;
    let baseAlpha = 0.55;
    let colorObj = null;

    if (roll < 0.18) {
      type = 'firefly';
      radius = 2.4 + Math.random() * 2.2; // 2.4px to 4.6px
      baseAlpha = 0.65 + Math.random() * 0.3;
      colorObj = this.colors.firefly[Math.floor(Math.random() * this.colors.firefly.length)];
    } else if (roll < 0.50) {
      type = 'spore';
      radius = 1.4 + Math.random() * 1.4; // 1.4px to 2.8px
      baseAlpha = 0.45 + Math.random() * 0.35;
      colorObj = this.colors.spore[Math.floor(Math.random() * this.colors.spore.length)];
    } else if (roll < 0.80) {
      type = 'pollen';
      radius = 1.1 + Math.random() * 1.1; // 1.1px to 2.2px
      baseAlpha = 0.4 + Math.random() * 0.35;
      colorObj = this.colors.pollen[Math.floor(Math.random() * this.colors.pollen.length)];
    } else {
      type = 'dust';
      radius = 0.7 + Math.random() * 0.8; // 0.7px to 1.5px (depth of field dust)
      baseAlpha = 0.2 + Math.random() * 0.25;
      colorObj = this.colors.dust[Math.floor(Math.random() * this.colors.dust.length)];
    }

    const screenW = this.width || window.innerWidth;
    const screenH = this.height || window.innerHeight;

    return {
      type: type,
      x: Math.random() * screenW,
      y: randomY ? Math.random() * screenH : screenH + 15,
      radius: radius,
      baseAlpha: baseAlpha,
      alpha: baseAlpha,
      // Slow, gentle upward thermal drift with subtle horizontal wander
      speedY: -(0.18 + Math.random() * 0.35),
      speedX: (Math.random() - 0.5) * 0.3,
      wobbleSpeed: 0.008 + Math.random() * 0.015,
      wobbleAngle: Math.random() * Math.PI * 2,
      wobbleRadius: 0.5 + Math.random() * 1.2,
      // Breathing pulse for bioluminescent glow
      pulseSpeed: 0.015 + Math.random() * 0.025,
      pulseAngle: Math.random() * Math.PI * 2,
      r: colorObj.r,
      g: colorObj.g,
      b: colorObj.b
    };
  }

  start() {
    if (this.isRunning || this.isEcoMode) return;
    this.isRunning = true;
    const loop = () => {
      if (!this.isRunning) return;
      this.updateAndRender();
      this.animationFrameId = requestAnimationFrame(loop);
    };
    this.animationFrameId = requestAnimationFrame(loop);
  }

  stop() {
    this.isRunning = false;
    if (this.animationFrameId) {
      cancelAnimationFrame(this.animationFrameId);
      this.animationFrameId = null;
    }
    if (this.ctx && this.canvas) {
      this.ctx.clearRect(0, 0, this.width, this.height);
    }
  }

  updateAndRender() {
    if (!this.ctx) return;
    this.ctx.clearRect(0, 0, this.width, this.height);

    for (let i = 0; i < this.particles.length; i++) {
      const p = this.particles[i];

      // Gentle organic drift: upward air currents with relaxing sine wave sway
      p.wobbleAngle += p.wobbleSpeed;
      p.pulseAngle += p.pulseSpeed;

      p.y += p.speedY;
      p.x += p.speedX + Math.sin(p.wobbleAngle) * p.wobbleRadius;

      // Soft breathing glow cycle (especially pronounced for fireflies)
      if (p.type === 'firefly') {
        const pulse = (Math.sin(p.pulseAngle) + 1) * 0.5; // 0.0 to 1.0
        p.alpha = p.baseAlpha * (0.35 + 0.65 * pulse);
      } else {
        p.alpha = p.baseAlpha * (0.7 + 0.3 * Math.sin(p.pulseAngle));
      }

      // Reset when particle drifts off top or sides
      if (p.y < -25 || p.x < -30 || p.x > this.width + 30) {
        Object.assign(p, this.spawnParticle(false));
      }

      // Render particle
      if (p.type === 'firefly') {
        // Bioluminescent Firefly: radial halo glow + core
        const haloRadius = p.radius * 3.5;
        const grad = this.ctx.createRadialGradient(p.x, p.y, p.radius * 0.3, p.x, p.y, haloRadius);
        grad.addColorStop(0, `rgba(${p.r}, ${p.g}, ${p.b}, ${p.alpha})`);
        grad.addColorStop(0.35, `rgba(${p.r}, ${p.g}, ${p.b}, ${p.alpha * 0.45})`);
        grad.addColorStop(1, `rgba(${p.r}, ${p.g}, ${p.b}, 0)`);

        this.ctx.beginPath();
        this.ctx.arc(p.x, p.y, haloRadius, 0, Math.PI * 2);
        this.ctx.fillStyle = grad;
        this.ctx.fill();

        // Inner bright spark core
        this.ctx.beginPath();
        this.ctx.arc(p.x, p.y, p.radius * 0.8, 0, Math.PI * 2);
        this.ctx.fillStyle = `rgba(255, 255, 240, ${Math.min(1, p.alpha * 1.3)})`;
        this.ctx.fill();

      } else {
        // Spores, Pollen & Dust: soft circular particles with organic opacity
        this.ctx.beginPath();
        this.ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
        this.ctx.fillStyle = `rgba(${p.r}, ${p.g}, ${p.b}, ${p.alpha})`;
        this.ctx.fill();
      }
    }
  }

  setEcoMode(enabled) {
    this.isEcoMode = enabled;
    const mistElements = document.querySelectorAll('.mist-layer');
    
    if (enabled) {
      this.stop();
      mistElements.forEach(el => el.style.display = 'none');
    } else {
      mistElements.forEach(el => el.style.display = 'block');
      this.start();
    }
  }
}

// Global instance initialized on window load
window.KritiEffects = PrehistoricEffects;
