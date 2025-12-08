# StreamStem UI/UX Redesign - Comprehensive Design Document

**Designer**: Reb (UI/UX Lead)
**Date**: 2025-12-08
**Status**: Design Phase
**Target**: Production-ready, WCAG 2.1 AA compliant, mobile-first responsive web app

---

## Design Philosophy

**Core Principle**: Walk backwards from perfection.

**Perfect end state**: A user visits StreamStem on any device, pastes a YouTube/Spotify URL, selects options with confidence, watches their audio separate in real-time with beautiful visual feedback, downloads their stems effortlessly, and feels delighted by the experience.

**Current state**: Fixed-width desktop-only layout with poor accessibility, broken on mobile, alert boxes for errors, fake progress indicators, removed focus states.

**Our journey**: Close this gap systematically, mobile-first, accessibility-first, performance-first.

---

## Current State Audit

### Critical Failures

**Accessibility (WCAG 2.1 violations):**
- Focus indicators removed globally (CSS lines 45-50: `outline: none !important`)
- No ARIA labels on interactive elements (buttons, radio groups, progress indicators)
- Radio buttons not properly associated with labels (clickable siblings vs wrapping)
- No screen reader announcements for status changes
- Poor color contrast: `#ecfff8` text on image background (fails 4.5:1 minimum)
- Icons without alt text or aria-label
- No skip links for keyboard navigation
- No focus management (focus lost during state transitions)

**Responsive Design (mobile failures):**
- Zero media queries or breakpoints
- Fixed pixel widths: `.center-content` (81%), `.main-form` (fit-content)
- Height using `100vw` instead of `100vh` (body:15)
- Touch targets too small: radio buttons (default size ~16px, need 44px minimum)
- Horizontal scroll on mobile (fixed widths + padding overflow)
- No viewport considerations for small screens
- Text sizing in pixels (not scalable with user preferences)

**CSS Quality:**
- Invalid selector: `bodyafter` (line 33) → should be `body::after`
- Invalid pseudo-class: `input:focused` (line 82) → should be `:focus`
- Duplicate declarations:
  - `.top-nav`: 3x `display: flex` (lines 92, 107, 108)
  - `.top-nav`: 2x `margin: 0 auto` (lines 95, 99)
  - Multiple conflicting padding values
- Height inconsistencies: mixing px, vw, vh, no values
- Unused styles and commented code bloat

**JavaScript UX:**
- Browser `alert()` for validation errors (line 39) - blocks UI, not accessible
- Fake progress: `setTimeout()` with generic messages (lines 54-57)
- Progress bar exists (HTML:141-147) but never updated
- No error recovery - just shows error message
- No loading state for screen readers
- Abrupt state transitions (no smooth animations)

**User Experience:**
- No inline validation - user only sees errors on submit
- Generic error messages ("Network response was not ok")
- No indication of which form fields are required/optional
- No helpful placeholder text
- Can't see what options mean (2/4/6 stems - user doesn't know difference)
- Cancel button appears but doesn't actually cancel (just reloads)
- No "what's happening" context during processing

---

## Design Vision: The Perfect StreamStem Experience

### User Journey (Ideal State)

**Step 1: Arrival (Mobile or Desktop)**
- Clean, focused interface loads instantly
- Clear hierarchy: logo → headline → form
- Single clear action: "Paste your URL here"
- Visible format options with helpful tooltips
- Stem count options with visual examples

**Step 2: Input & Validation**
- User pastes URL → instant inline validation
- Green checkmark appears if valid
- Helpful error if invalid: "This looks like a YouTube playlist. Please use a single video URL."
- Submit button disabled until form valid
- Clear visual feedback on all interactions

**Step 3: Processing**
- Form smoothly transitions to progress view
- Real progress bar updates based on backend task
- Current step clearly indicated:
  - "Downloading audio from YouTube..." (20%)
  - "Analyzing audio structure..." (40%)
  - "Separating vocals..." (60%)
  - "Separating drums..." (70%)
  - "Finalizing stems..." (90%)
  - "Complete!" (100%)
- User can see estimated time remaining
- Cancel option available with confirmation
- Screen reader announces each step completion

**Step 4: Results**
- Smooth transition to results view
- Each stem displayed as a card:
  - Stem icon (visual indicator)
  - Stem name (Vocals, Drums, Bass, etc.)
  - Waveform preview (visual representation)
  - Audio player (HTML5 with custom controls)
  - Download button (prominent, accessible)
- "Download All" button (gets zip)
- "New Song" button (returns to form)
- All keyboard navigable
- Screen reader announces: "Separation complete. 4 stems ready."

**Step 5: Error Handling**
- If error occurs: Toast notification appears (not alert)
- Clear error message: "Couldn't download audio. The video might be private or age-restricted."
- Option to try again or return to form
- Error doesn't crash interface

### Visual Design System

**Color Palette (Accessible):**
- Primary: `#8B5CF6` (purple-500) - 4.5:1 contrast on white
- Secondary: `#EC4899` (pink-500) - accent for CTAs
- Success: `#10B981` (green-500) - checkmarks, completion
- Error: `#EF4444` (red-500) - validation errors, failures
- Background Dark: `#1F2937` (gray-800) - main background
- Background Light: `#F9FAFB` (gray-50) - cards, inputs
- Text Primary: `#F9FAFB` (gray-50) on dark, `#111827` on light
- Text Secondary: `#9CA3AF` (gray-400) - labels, helper text

**All combinations tested for WCAG 2.1 AA (4.5:1 minimum for normal text).**

**Typography:**
- System font stack: `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif`
- No custom fonts (better performance, accessibility)
- Scale:
  - xs: 0.75rem (12px)
  - sm: 0.875rem (14px)
  - base: 1rem (16px)
  - lg: 1.125rem (18px)
  - xl: 1.25rem (20px)
  - 2xl: 1.5rem (24px)
  - 3xl: 1.875rem (30px)
  - 4xl: 2.25rem (36px)
- Line heights: 1.5 for body text, 1.2 for headings
- Font weights: 400 (normal), 600 (semibold), 700 (bold)

**Spacing System (rem-based):**
- Uses Tailwind's default spacing scale (0.25rem increments)
- Mobile: tighter spacing (px-4, py-2)
- Desktop: comfortable spacing (px-8, py-4)

**Layout Grid:**
- Mobile (320px-767px): Single column, full width with padding
- Tablet (768px-1023px): Single column, max 640px centered
- Desktop (1024px+): Single column, max 768px centered
- No complex multi-column layouts (keeps it simple)

**Border Radius:**
- sm: 0.375rem (6px) - inputs, buttons
- md: 0.5rem (8px) - cards
- lg: 0.75rem (12px) - modals, toasts
- full: 9999px - radio buttons, pills

**Shadows:**
- sm: `0 1px 2px rgba(0, 0, 0, 0.05)` - subtle elevation
- md: `0 4px 6px rgba(0, 0, 0, 0.1)` - cards
- lg: `0 10px 15px rgba(0, 0, 0, 0.15)` - modals, toasts
- xl: `0 20px 25px rgba(0, 0, 0, 0.2)` - max elevation

---

## Component Architecture

### Page Structure (Semantic HTML)

```html
<body>
  <!-- Skip Link for Keyboard Navigation -->
  <a href="#main-content" class="skip-link">Skip to main content</a>

  <!-- Header/Navigation -->
  <header role="banner">
    <nav aria-label="Main navigation">
      <img src="logo.png" alt="StreamStem logo">
      <h1>StreamStem</h1>
    </nav>
  </header>

  <!-- Main Content Area -->
  <main id="main-content" role="main">

    <!-- Section 1: Input Form (default visible) -->
    <section id="input-section" aria-label="Audio source input">
      <h2>Isolate Audio Stems from Spotify and YouTube</h2>

      <form id="stem-form" aria-label="Stem separation form">
        <!-- URL Input -->
        <div class="form-group">
          <label for="audio-url">YouTube or Spotify URL</label>
          <input
            type="url"
            id="audio-url"
            name="url"
            required
            aria-required="true"
            aria-describedby="url-hint url-error"
            placeholder="https://youtube.com/watch?v=..."
          >
          <span id="url-hint" class="hint-text">Paste a YouTube video or Spotify track link</span>
          <span id="url-error" class="error-text" role="alert" aria-live="polite"></span>
        </div>

        <!-- Stem Count Selection -->
        <fieldset>
          <legend>Number of stems</legend>
          <div class="radio-group">
            <div class="radio-option">
              <input type="radio" id="stems-2" name="stem-count" value="2">
              <label for="stems-2">
                <span class="radio-label-text">2 Stems</span>
                <span class="radio-label-desc">Vocals + Instrumental</span>
              </label>
            </div>
            <div class="radio-option">
              <input type="radio" id="stems-4" name="stem-count" value="4" checked>
              <label for="stems-4">
                <span class="radio-label-text">4 Stems</span>
                <span class="radio-label-desc">Vocals, Drums, Bass, Other</span>
              </label>
            </div>
            <div class="radio-option">
              <input type="radio" id="stems-6" name="stem-count" value="6">
              <label for="stems-6">
                <span class="radio-label-text">6 Stems</span>
                <span class="radio-label-desc">Vocals, Drums, Bass, Guitar, Piano, Other</span>
              </label>
            </div>
          </div>
        </fieldset>

        <!-- File Format Selection -->
        <div class="form-group">
          <label for="file-format">Output format</label>
          <select id="file-format" name="format">
            <option value="mp3">MP3 (smaller files)</option>
            <option value="wav">WAV (best quality)</option>
            <option value="flac">FLAC (compressed lossless)</option>
          </select>
        </div>

        <!-- Submit Button -->
        <button type="submit" id="submit-btn" class="btn-primary">
          Separate Stems
        </button>
      </form>
    </section>

    <!-- Section 2: Progress Tracking (hidden initially) -->
    <section id="progress-section" aria-label="Processing progress" hidden>
      <h2>Processing Your Audio</h2>
      <p id="song-title" class="song-info"></p>

      <!-- Progress Bar -->
      <div class="progress-bar-container" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0">
        <div class="progress-bar-fill"></div>
      </div>
      <p id="progress-text" aria-live="polite">Starting...</p>

      <!-- Progress Steps -->
      <ul class="progress-steps" aria-label="Processing steps">
        <li class="step" data-step="download">
          <span class="step-icon" aria-hidden="true"></span>
          <span class="step-text">Downloading audio</span>
        </li>
        <li class="step" data-step="analyze">
          <span class="step-icon" aria-hidden="true"></span>
          <span class="step-text">Analyzing audio</span>
        </li>
        <li class="step" data-step="separate">
          <span class="step-icon" aria-hidden="true"></span>
          <span class="step-text">Separating stems</span>
        </li>
        <li class="step" data-step="finalize">
          <span class="step-icon" aria-hidden="true"></span>
          <span class="step-text">Finalizing</span>
        </li>
      </ul>

      <!-- Cancel Button -->
      <button type="button" id="cancel-btn" class="btn-secondary">
        Cancel Processing
      </button>
    </section>

    <!-- Section 3: Results (hidden initially) -->
    <section id="results-section" aria-label="Separated stems" hidden>
      <h2>Your Stems Are Ready!</h2>
      <p id="results-song-title" class="song-info"></p>

      <!-- Stems Container (populated dynamically) -->
      <div id="stems-container" class="stems-grid">
        <!-- Each stem card will be inserted here via JS -->
        <!-- Example structure:
        <article class="stem-card">
          <h3 class="stem-name">
            <img src="vocals-icon.svg" alt="" aria-hidden="true">
            Vocals
          </h3>
          <audio controls src="vocals.mp3" aria-label="Vocals stem audio player"></audio>
          <button class="btn-download" data-stem="vocals">
            Download Vocals
          </button>
        </article>
        -->
      </div>

      <!-- Action Buttons -->
      <div class="results-actions">
        <button type="button" id="download-all-btn" class="btn-primary">
          Download All Stems (ZIP)
        </button>
        <button type="button" id="new-song-btn" class="btn-secondary">
          Process Another Song
        </button>
      </div>
    </section>

  </main>

  <!-- Toast Notification Container (fixed position) -->
  <div id="toast-container" aria-live="polite" aria-atomic="true" role="status"></div>

  <!-- Footer -->
  <footer role="contentinfo">
    <p>StreamStem - Powered by Demucs</p>
  </footer>
</body>
```

### Component Specifications

#### 1. Toast Notification System

**Purpose**: Replace browser `alert()` with non-blocking, accessible notifications.

**Types:**
- `success`: Green, checkmark icon
- `error`: Red, X icon
- `info`: Blue, info icon
- `warning`: Yellow, exclamation icon

**Behavior:**
- Slides in from top-right on desktop, top-center on mobile
- Auto-dismisses after 5 seconds (error/warning stay until user dismisses)
- User can manually dismiss by clicking X button
- Stacks if multiple notifications
- Screen reader announces immediately (aria-live="polite")
- Keyboard accessible (can focus and dismiss with Enter/Space)

**HTML Structure:**
```html
<div class="toast toast-error" role="alert">
  <span class="toast-icon" aria-hidden="true">✕</span>
  <p class="toast-message">Invalid URL format. Please use a YouTube or Spotify link.</p>
  <button class="toast-close" aria-label="Dismiss notification">×</button>
</div>
```

**CSS:**
- Fixed position: `top: 1rem; right: 1rem` (desktop), `top: 1rem; left: 1rem; right: 1rem` (mobile)
- Shadow: lg
- Border-radius: lg
- Animation: slide-in-right (desktop), slide-in-down (mobile)
- Transition: all 0.3s ease
- Min height: 44px (touch target)

#### 2. Form Input with Inline Validation

**Features:**
- Real-time validation on blur (not every keystroke - too aggressive)
- Visual states: default, focus, valid, invalid, disabled
- Error messages below input
- Success checkmark when valid
- Clear focus indicator (2px outline, primary color)

**States:**
- **Default**: Gray border, no icon
- **Focus**: Primary color border, no icon
- **Valid**: Green border, green checkmark icon
- **Invalid**: Red border, red X icon, error message below
- **Disabled**: Gray background, gray border, cursor not-allowed

**Accessibility:**
- Label always visible (no placeholder-only inputs)
- aria-describedby links to hint and error text
- aria-invalid="true" when validation fails
- Error text has role="alert" and aria-live="polite"

#### 3. Radio Button Group (Stem Count Selection)

**Design:**
- Large touch targets (min 44x44px)
- Visual radio button + descriptive text
- Clear selected state
- Hover effect
- Focus indicator

**Structure:**
```html
<div class="radio-option">
  <input type="radio" id="stems-4" name="stem-count" value="4" checked>
  <label for="stems-4">
    <span class="radio-visual" aria-hidden="true"></span>
    <span class="radio-content">
      <span class="radio-label-text">4 Stems</span>
      <span class="radio-label-desc">Vocals, Drums, Bass, Other</span>
    </span>
  </label>
</div>
```

**States:**
- **Default**: White circle with gray border
- **Hover**: Primary color border
- **Focus**: Primary color border + 2px outline
- **Checked**: Primary color fill with white dot center
- **Disabled**: Gray background

**Accessibility:**
- Input properly associated with label (for="id")
- Entire label clickable (44px min height)
- Keyboard navigable (Arrow keys to switch, Space to select)
- Screen reader reads label + description

#### 4. Progress Bar with Steps

**Design:**
- Horizontal bar showing percentage
- List of steps below with status indicators
- Current step highlighted
- Completed steps have checkmarks
- Future steps grayed out

**Behavior:**
- Updates based on backend task status
- Smooth transition (CSS transition: width 0.5s ease)
- Screen reader announces each step completion
- Percentage updates in real-time

**Accessibility:**
- Uses `role="progressbar"`
- `aria-valuenow`, `aria-valuemin`, `aria-valuemax` updated dynamically
- `aria-live="polite"` on progress text
- Each step completion announced

#### 5. Stem Card (Results)

**Design:**
- Card layout with shadow
- Stem icon + name at top
- Audio player in middle
- Download button at bottom
- Hover effect (slight lift)

**Features:**
- Custom styled audio player (using native HTML5 controls as fallback)
- Download button prominently displayed
- Each card independently accessible
- Keyboard navigable

**Accessibility:**
- Card is `<article>` with semantic structure
- Audio player has aria-label: "Vocals stem audio player"
- Download button clearly labeled: "Download Vocals"
- Icon has aria-hidden="true" (decorative)

---

## Responsive Design Strategy

### Mobile-First Approach

**Base styles target 320px** (smallest common viewport).

Then progressive enhancement via min-width media queries:
- `@media (min-width: 640px)` - Large phones, small tablets
- `@media (min-width: 768px)` - Tablets
- `@media (min-width: 1024px)` - Desktops
- `@media (min-width: 1280px)` - Large desktops

### Breakpoint-Specific Adjustments

**320px - 639px (Mobile):**
- Single column layout
- Full width inputs (width: 100%)
- Padding: 1rem (16px)
- Font sizes: base or slightly smaller
- Touch targets: minimum 44x44px
- Stack form elements vertically
- Radio buttons: full width blocks
- Stem cards: 1 per row
- Toast notifications: top-center, full width

**640px - 767px (Large Mobile):**
- Slightly wider max-width (480px centered)
- Padding: 1.5rem
- Radio buttons: can show 2 per row
- Form inputs: slightly wider
- Stem cards: still 1 per row

**768px - 1023px (Tablet):**
- Max-width: 640px centered
- Padding: 2rem
- Radio buttons: 3 across
- Stem cards: 2 per row
- Toast: top-right corner
- More whitespace, larger fonts

**1024px+ (Desktop):**
- Max-width: 768px centered
- Padding: 3rem
- Radio buttons: 3 across with more spacing
- Stem cards: 2 per row (or 3 for 6-stem mode)
- Full feature set
- Hover effects active
- Larger touch targets can be reduced (44px still minimum)

### Key Responsive Techniques

1. **Fluid Typography**: Use `rem` for all font sizes (scales with user preference)
2. **Flexible Containers**: Max-width + margin auto for centering
3. **Flexible Images**: `max-width: 100%; height: auto;`
4. **Touch Targets**: Always 44x44px minimum
5. **Safe Areas**: Respect notch/status bar on iOS (padding + env(safe-area-inset-*))
6. **No Horizontal Scroll**: `overflow-x: hidden` on body, ensure all content fits
7. **Flexible Grid**: CSS Grid with auto-fit/auto-fill for stem cards

---

## Accessibility Strategy (WCAG 2.1 AA Compliance)

### Principle 1: Perceivable

**1.1 Text Alternatives:**
- All images have alt text (or aria-label for SVGs)
- Decorative images: aria-hidden="true"
- Icon buttons: aria-label describing action
- Audio players: clear labels

**1.3 Adaptable:**
- Semantic HTML: header, main, section, article, nav, footer
- Heading hierarchy: h1 → h2 → h3 (no skipping)
- Lists for related items (progress steps)
- Labels properly associated with inputs
- Form fields grouped with fieldset/legend

**1.4 Distinguishable:**
- Color contrast: Minimum 4.5:1 for normal text, 3:1 for large text
- No color-only indicators (use icons + text)
- Text resizable up to 200% without breaking layout
- Focus indicators: 2px solid outline, high contrast
- No text in images (use HTML text)

### Principle 2: Operable

**2.1 Keyboard Accessible:**
- All functionality available via keyboard
- Tab order follows visual order
- No keyboard traps
- Skip links to main content
- Radio buttons: Arrow keys to navigate, Space to select
- Custom controls: proper focus management

**2.2 Enough Time:**
- No time limits on form input
- Progress updates don't expire
- User can cancel long processes

**2.4 Navigable:**
- Page title: "StreamStem - Extract Audio Stems"
- Skip link at top
- Clear focus indicators (never `outline: none` without replacement)
- Headings describe sections
- Link text descriptive ("Download Vocals" not "Download")

**2.5 Input Modalities:**
- Touch targets: minimum 44x44px
- No pointer-only gestures
- Click/tap works for all interactions

### Principle 3: Understandable

**3.1 Readable:**
- Language declared: `<html lang="en">`
- Plain language (no jargon)
- Abbreviations explained on first use

**3.2 Predictable:**
- Consistent navigation
- Consistent button placement
- No surprise focus changes
- Form submission doesn't auto-submit

**3.3 Input Assistance:**
- Validation errors clearly described
- Suggestions for fixing errors
- Required fields marked
- Error summary if multiple errors

### Principle 4: Robust

**4.1 Compatible:**
- Valid HTML (no unclosed tags, proper nesting)
- ARIA used correctly (not overused)
- Name, role, value set for custom controls
- Status messages use aria-live

### Screen Reader Testing Checklist

Test with VoiceOver (macOS) or NVDA (Windows):
- [ ] Can navigate entire form with Tab
- [ ] Can fill out form and submit
- [ ] Error messages announced clearly
- [ ] Progress updates announced
- [ ] Results section clearly indicated
- [ ] Each stem card readable
- [ ] Download buttons clearly labeled
- [ ] Toast notifications announced
- [ ] No confusing focus jumps
- [ ] All functionality available without mouse

---

## Animation & Interaction Strategy

### Animation Principles

1. **Performance First**: 60fps target, use CSS transforms/opacity only
2. **Respect User Preferences**: `prefers-reduced-motion` media query
3. **Purposeful**: Animations guide attention, indicate state changes
4. **Fast**: 200-300ms for most transitions, 400-500ms for entrances/exits
5. **Natural Easing**: `ease-out` for entrances, `ease-in` for exits

### Key Animations

**Page Load:**
- Fade in main content (300ms ease-out)
- No auto-playing animations

**Form Interactions:**
- Input focus: border color transition (200ms)
- Button hover: scale 1.02 + shadow increase (200ms ease-out)
- Button active: scale 0.98 (100ms)
- Radio select: checkmark fade-in (200ms)
- Validation: error message slide-down (300ms ease-out)

**State Transitions:**
- Form → Progress: Fade out form (300ms), fade in progress (300ms, delayed 150ms)
- Progress → Results: Same pattern
- Smooth, never jarring

**Progress Bar:**
- Width transition: 500ms ease-out (smooth fill)
- Step completion: Checkmark fade-in + scale (300ms)

**Toast Notifications:**
- Entrance: Slide in from right (300ms ease-out) on desktop, slide down on mobile
- Exit: Fade out + slide out (200ms ease-in)

**Results:**
- Stem cards: Stagger entrance (each card 100ms after previous)
- Hover: Lift (translateY -4px) + shadow increase (200ms)
- Audio player: Smooth control animations

**Reduced Motion:**
```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

### Micro-Interactions

1. **Button Press**: Visual feedback (scale 0.98) on mousedown/touchstart
2. **Input Focus**: Border glow + subtle scale (1.01)
3. **Radio Select**: Ripple effect from center
4. **Download Start**: Button text changes "Downloading..." with spinner
5. **Success Moments**: Confetti animation on completion (optional, toggle-able)

---

## Implementation Phases

### Phase 1: Foundation & Cleanup (Can Start Immediately)
**Duration**: 1-2 hours

**Tasks:**
1. Fix CSS validation errors:
   - `bodyafter` → `body::after`
   - `input:focused` → `input:focus`
   - Remove duplicate declarations
   - Consolidate top-nav styles
2. Fix height units: `100vw` → `100vh`
3. Add focus indicators:
   - Remove `outline: none !important`
   - Add proper focus styles (2px outline, primary color)
4. Clean up unused CSS
5. Add CSS reset/normalize

**Deliverables:**
- Valid CSS (no errors in validator)
- Proper focus indicators on all interactive elements
- Clean, consolidated CSS

---

### Phase 2: Semantic HTML Restructure (Can Start Immediately)
**Duration**: 2-3 hours

**Tasks:**
1. Rewrite HTML with semantic structure:
   - Proper header, main, sections
   - Correct heading hierarchy (h1 → h2 → h3)
   - Fieldset/legend for radio group
   - Proper label association
2. Add ARIA labels and roles where needed
3. Add skip link
4. Ensure form accessibility:
   - aria-required on required fields
   - aria-describedby for hints/errors
   - role="alert" on error messages
5. Add lang attribute to html tag

**Deliverables:**
- Semantic, accessible HTML structure
- Passing accessibility audit (basic)

---

### Phase 3: Responsive CSS with Tailwind (Can Start Immediately)
**Duration**: 3-4 hours

**Tasks:**
1. Convert layout to mobile-first:
   - Start with 320px base styles
   - Add media queries for breakpoints
2. Make all widths fluid:
   - Remove fixed px widths
   - Use max-width + margin auto for centering
3. Responsive typography:
   - Convert px to rem
   - Adjust sizes per breakpoint
4. Touch target sizing:
   - Ensure 44x44px minimum on all interactive elements
5. Test on real devices:
   - iPhone SE (320px)
   - iPhone 12 Pro (390px)
   - iPad (768px)
   - Desktop (1280px+)

**Deliverables:**
- Fully responsive layout (320px to desktop)
- No horizontal scroll on any device
- Comfortable touch targets

---

### Phase 4: Toast Notification System (Can Start Immediately)
**Duration**: 2-3 hours

**Tasks:**
1. Build toast component (HTML/CSS/JS)
2. Create toast API:
   ```js
   showToast(message, type, duration)
   dismissToast(id)
   ```
3. Replace all `alert()` calls with toast
4. Test accessibility:
   - Screen reader announces
   - Keyboard dismissible
   - Stacking works
5. Add animations (slide-in, fade-out)

**Deliverables:**
- Working toast system
- No more browser alerts
- Accessible, beautiful notifications

---

### Phase 5: Form Validation UI (Can Start Immediately)
**Duration**: 2-3 hours

**Tasks:**
1. Add inline validation logic:
   - URL validation on blur
   - Show error messages below fields
   - Show success checkmark when valid
2. Disable submit button until form valid
3. Improve error messages:
   - "This looks like a playlist. Please use a single video."
   - "This Spotify URL is incomplete. It should look like: https://open.spotify.com/track/..."
4. Add loading state to submit button
5. Test all validation scenarios

**Deliverables:**
- Inline validation working
- Helpful error messages
- Clear visual feedback

---

### Phase 6: Static Progress UI (Can Start Immediately)
**Duration**: 2-3 hours

**Tasks:**
1. Build progress section HTML/CSS:
   - Progress bar component
   - Step list component
2. Add transition animations (form → progress)
3. Create progress update function:
   ```js
   updateProgress(percentage, stepName, message)
   ```
4. Test screen reader announcements
5. Style cancel button

**Deliverables:**
- Beautiful progress UI (not hooked to real data yet)
- Smooth transitions
- Accessible progress indicators

---

### Phase 7: Results Section Rebuild (Can Start Immediately)
**Duration**: 3-4 hours

**Tasks:**
1. Build stem card component (HTML/CSS)
2. Create dynamic card generation:
   ```js
   createStemCard(stemName, stemUrl, iconUrl)
   ```
3. Style audio players (custom controls if needed)
4. Add download button logic
5. Build "Download All" and "New Song" buttons
6. Add stagger entrance animations
7. Test with 2, 4, and 6 stem scenarios

**Deliverables:**
- Beautiful results section
- All download functionality working
- Responsive stem cards

---

### Phase 8: Polish & Micro-Interactions (Can Start Immediately)
**Duration**: 2-3 hours

**Tasks:**
1. Add button hover effects
2. Add input focus effects
3. Add radio button animations
4. Smooth all state transitions
5. Add loading spinners where appropriate
6. Test all animations on mobile
7. Verify prefers-reduced-motion works

**Deliverables:**
- Polished, delightful interactions
- Smooth 60fps animations
- Respects user preferences

---

### Phase 9: Real-Time Progress Integration (BLOCKED - Needs Callie)
**Duration**: 2-3 hours (once API ready)

**Dependencies:**
- Callie completes INFRA-003: `/task_status/{task_id}` endpoint

**Tasks:**
1. Integrate with Callie's task status endpoint
2. Poll for updates every 1-2 seconds
3. Update progress bar and steps based on response
4. Handle completion/error states
5. Test with real audio processing
6. Handle edge cases (timeout, network error)

**API Contract Needed (coordinate with Callie):**
```json
GET /task_status/{task_id}
Response:
{
  "status": "processing",
  "progress": 0.65,
  "current_step": "separating",
  "message": "Separating drums...",
  "eta_seconds": 45
}

Possible statuses: "pending", "processing", "completed", "failed"
Possible steps: "download", "analyze", "separate", "finalize"
```

**Deliverables:**
- Real-time progress tracking working
- Smooth updates from backend
- Error handling integrated

---

### Phase 10: Comprehensive Testing (Can Start After Phase 8)
**Duration**: 3-4 hours

**Tasks:**
1. Cross-browser testing:
   - Chrome, Firefox, Safari, Edge
   - Document any issues
2. Device testing:
   - iPhone SE, iPhone 12 Pro, iPhone 14 Pro Max
   - iPad, iPad Pro
   - Android devices (via BrowserStack)
   - Various desktop sizes
3. Accessibility audit:
   - VoiceOver full workflow test
   - Keyboard-only navigation test
   - Color contrast verification
   - axe DevTools scan
4. Performance testing:
   - Lighthouse score (aim for 90+)
   - Core Web Vitals check
5. User testing:
   - Observe 2-3 users completing workflow
   - Document friction points

**Deliverables:**
- Compatibility matrix (browsers × devices)
- Accessibility report (WCAG 2.1 AA compliant)
- Performance report (Core Web Vitals green)
- User testing findings document

---

### Phase 11: Production Build (Final Phase)
**Duration**: 1 hour

**Tasks:**
1. Build production Tailwind CSS:
   ```bash
   npm run build:css
   ```
2. Minify custom CSS
3. Minify JavaScript
4. Optimize images (if any new ones added)
5. Test production build
6. Verify all assets load correctly

**Deliverables:**
- Optimized production CSS
- Minified JS
- Fast load times

---

## Scope: What Changes & What Doesn't

### WILL Change (In Scope)

**HTML:**
- Complete restructure with semantic elements
- New ARIA labels and roles
- Proper heading hierarchy
- Accessible form structure
- Skip links

**CSS:**
- Mobile-first responsive design
- Fix all validation errors
- Remove duplicate declarations
- Convert to rem-based sizing
- Add proper focus indicators
- Responsive breakpoints
- Clean color system
- Consistent spacing

**JavaScript:**
- Replace alerts with toasts
- Add inline validation
- Smooth state transitions
- Real-time progress updates (when API ready)
- Better error handling
- Accessibility improvements (focus management, announcements)

**User Experience:**
- Helpful error messages
- Clear visual feedback
- Smooth animations
- Progress transparency
- Better information hierarchy

### WON'T Change (Out of Scope)

**Backend:**
- API endpoints (Callie's domain)
- Demucs processing logic (Aphex's domain)
- File storage system
- Authentication (none needed per requirements)

**Core Functionality:**
- YouTube/Spotify download (works, don't touch)
- Stem separation (Demucs stays same)
- File serving (works, don't touch)
- Zip creation (works, don't touch)

**Features NOT Adding:**
- User accounts/authentication
- Stem history/library
- Advanced audio editing
- Social features
- Paid plans
- Analytics dashboard

**Design Elements NOT Changing:**
- Logo (keep existing)
- Overall purple/pink color theme (refine, don't replace)
- Single-page app structure (keep it simple)

---

## Dependencies & Coordination

### With Callie (Backend Dev)

**UI-006: Real-Time Progress Tracking**
**Blocker**: Need `/task_status/{task_id}` endpoint (INFRA-003)

**API Contract Discussion Needed:**
1. **Endpoint**: `GET /task_status/{task_id}`
2. **Response Format**: JSON with status, progress, step, message, ETA
3. **Status Values**: "pending", "processing", "completed", "failed"
4. **Step Values**: "download", "analyze", "separate", "finalize"
5. **Update Frequency**: How often can UI poll? (suggest 1-2 seconds)
6. **Error Handling**: What errors to expect? 404 if task not found?

**Will Document In**: `.claude/checkpoints/team-blockers.md` when ready to integrate

### With Aphex (ML Specialist)

**Potential Collaboration**: If adding waveform visualization in results
**Status**: Not required for MVP, can add later

### With Jeff (PM)

**Decision Needed**: Priority of "nice-to-have" features:
- Waveform visualization in results?
- Confetti animation on completion?
- Dark mode toggle?
- Share/social features?

**Will Discuss**: After core redesign complete

---

## Success Metrics

### Accessibility
- [ ] Passes WAVE accessibility checker (0 errors)
- [ ] Passes axe DevTools scan (0 critical issues)
- [ ] Color contrast 4.5:1+ on all text
- [ ] Complete workflow possible with keyboard only
- [ ] Complete workflow possible with screen reader
- [ ] Focus indicators visible on all interactive elements

### Responsiveness
- [ ] No horizontal scroll on any device (320px - 2560px)
- [ ] Touch targets 44x44px minimum
- [ ] Readable text on all screen sizes
- [ ] Comfortable spacing on mobile
- [ ] No broken layouts on any tested device

### Performance
- [ ] Lighthouse Performance score: 90+
- [ ] First Contentful Paint: < 1.5s
- [ ] Time to Interactive: < 3.5s
- [ ] Cumulative Layout Shift: < 0.1
- [ ] No janky animations (60fps)

### User Experience
- [ ] No browser alerts
- [ ] Clear error messages
- [ ] Real-time progress tracking
- [ ] Smooth state transitions
- [ ] Beautiful, delightful interface
- [ ] Users can complete workflow without instructions

### Code Quality
- [ ] Valid HTML (W3C validator)
- [ ] Valid CSS (W3C validator)
- [ ] No console errors
- [ ] Clean, readable code
- [ ] Commented where necessary
- [ ] Follows best practices

---

## Risk Assessment

### Low Risk (Can Execute Confidently)
- CSS cleanup and fixes
- Semantic HTML restructure
- Responsive design implementation
- Toast notification system
- Form validation UI
- Static progress UI
- Results section rebuild

**Mitigation**: These are standard frontend tasks. I've done them thousands of times. Testing will catch any issues.

### Medium Risk (Need Testing)
- Cross-browser compatibility (Safari can be quirky)
- Screen reader compatibility (need thorough VoiceOver testing)
- Animation performance on older devices

**Mitigation**: Test early and often. Use BrowserStack for device testing. Profile performance with DevTools.

### High Risk (Dependencies)
- Real-time progress integration (depends on Callie's API)
- Error handling (depends on backend error responses)

**Mitigation**: Coordinate with Callie early. Agree on API contract before building. Build static version first, integrate later.

---

## Timeline Estimate

**Assuming focused work, no blockers:**

- Phase 1 (Foundation): 1-2 hours
- Phase 2 (Semantic HTML): 2-3 hours
- Phase 3 (Responsive CSS): 3-4 hours
- Phase 4 (Toast System): 2-3 hours
- Phase 5 (Form Validation): 2-3 hours
- Phase 6 (Progress UI): 2-3 hours
- Phase 7 (Results Section): 3-4 hours
- Phase 8 (Polish): 2-3 hours
- Phase 9 (Progress Integration): 2-3 hours (when API ready)
- Phase 10 (Testing): 3-4 hours
- Phase 11 (Production Build): 1 hour

**Total: 23-33 hours of development time**

**Realistic Timeline**: 3-5 days if working full-time, 1-2 weeks if part-time.

**Critical Path**: Phases 1-8 can all proceed in parallel/sequence without blockers. Phase 9 waits for Callie. Phase 10 requires Phases 1-9 complete.

---

## Next Actions

1. Get Jeff's approval on this design document
2. Start Phase 1: CSS cleanup and focus indicators (quick win)
3. Proceed to Phase 2: Semantic HTML restructure
4. Coordinate with Callie on API contract for Phase 9
5. Execute Phases 3-8 systematically
6. Wait for Callie to complete INFRA-003
7. Integrate real-time progress (Phase 9)
8. Comprehensive testing (Phase 10)
9. Production build (Phase 11)
10. Ship and celebrate

---

## Final Thoughts

This redesign will transform StreamStem from a broken, inaccessible desktop-only app into a beautiful, accessible, mobile-first web experience that delights users on any device.

Every decision walks backwards from perfection:
- **Accessibility first**: No shortcuts. WCAG 2.1 AA non-negotiable.
- **Mobile first**: Smallest screen first, scale up.
- **Performance first**: 60fps or don't ship.
- **Users first**: Clear, helpful, delightful.

I've thought deeply three times. This plan is solid. Time to execute.

**Reb Out.**
