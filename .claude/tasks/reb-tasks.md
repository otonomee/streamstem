# Reb - Current Tasks

**Agent**: Reb (UI/UX Lead)
**Updated**: 2025-12-08 by Jeff
**Current Phase**: Phase 0 - Critical Bugs, then Phase 2 - UI/UX Redesign

---

## CRITICAL - DO THIS FIRST

### FIX-006: Fix JavaScript typo
**File**: `static/js/main.js`
**Line**: 312
**Issue**: `modalText.textContent = mesdsdddddDDDdsage;` should be `message`
**Impact**: Modal function completely broken
**Status**: NOT STARTED

**Quick fix, but it blocks any modal functionality. Do this now.**

---

## Phase 2: UI/UX Redesign (Can start after FIX-006)

### UI-001: Design new layout (mobile-first, accessible)
**Task**:
- Sketch/wireframe new layout
- Mobile-first approach (design for small screens, scale up)
- Consider information hierarchy, user flow
- Plan component structure
- Document design decisions in `.claude/checkpoints/reb-design.md`
**Deliverable**: Design doc with layout plan
**Status**: NOT STARTED

**START WITH THIS. Your vision for the perfect UX. Walk backwards from delighted users.**

### UI-002: Fix CSS bugs
**Current Issues**:
- Invalid CSS selectors in style.css
- Wrong height units (need rem/em instead of px for accessibility)
- Duplicate declarations
- Inconsistent spacing
**Task**: Clean up CSS, fix all validation errors
**Status**: NOT STARTED

### UI-003: Implement responsive design
**Breakpoints**:
- Mobile: 320px - 767px
- Tablet: 768px - 1023px
- Desktop: 1024px+
**Task**:
- Use Tailwind responsive utilities
- Test on real devices/browser DevTools
- Ensure no horizontal scroll on mobile
- Touch targets minimum 44x44px
**Status**: NOT STARTED

### UI-004: Improve accessibility
**Current Issues**:
- Focus indicators removed (very bad for keyboard users)
- Missing ARIA labels on interactive elements
- Poor color contrast
- No screen reader text for icons
**Task**:
- Restore and enhance focus indicators
- Add ARIA labels to all buttons, inputs, controls
- Ensure minimum 4.5:1 contrast ratio
- Add skip links for keyboard navigation
- Test with screen reader (VoiceOver on Mac)
**Status**: NOT STARTED

### UI-005: Replace browser alerts with proper UI notifications
**Current**: `main.js:39` uses `alert()` for validation errors
**Problem**: Alerts are jarring, not accessible, break flow
**Task**:
- Design toast/notification component
- Implement with Tailwind
- Replace all alert() calls
- Support different notification types (error, success, info)
**Status**: NOT STARTED

### UI-006: Add real-time progress tracking UI
**Current**: Progress messages exist but don't show real progress
**Task**:
- Design progress bar component
- Integrate with Callie's `/task_status/{task_id}` endpoint
- Poll for status updates
- Show percentage, current step, estimated time
- Handle errors gracefully
**Dependencies**: INFRA-003 (Callie's progress tracking endpoint)
**Coordinate**: With Callie on API contract
**Status**: NOT STARTED

**THIS IS THE KILLER FEATURE. Users see their stems being separated in real-time. Make it beautiful.**

### UI-007: Improve form validation
**Current**: Only validates on submit with alerts
**Task**:
- Add inline validation (validate as user types)
- Show validation errors below fields
- Disable submit until form is valid
- Clear, helpful error messages
**Status**: NOT STARTED

### UI-008: Polish animations and transitions
**Current**: Basic fadeIn/fadeOut animations
**Task**:
- Smooth transitions between states
- Loading animations that feel responsive
- Micro-interactions (button hover, input focus)
- Success animations when stems are ready
- Keep performance smooth (60fps)
**Status**: NOT STARTED

### UI-009: Test with screen readers and keyboard navigation
**Test scenarios**:
- Navigate entire app with Tab/Shift+Tab
- Use screen reader (VoiceOver) to complete full workflow
- Ensure all functionality keyboard-accessible
- No keyboard traps
**Document**: Any issues found, fix immediately
**Status**: NOT STARTED

### UI-010: Build production Tailwind CSS
**Task**:
- Run `npm run build:css` to compile production CSS
- Verify output in static/css/tailwind.css
- Test in production mode (minified CSS)
- Ensure all custom styles preserved
**Dependencies**: All CSS work complete (UI-002, UI-003)
**Status**: NOT STARTED

---

## Phase 4: Integration & Testing

### INT-003: Test progress tracking UI with real Celery tasks
**Task**:
- Test progress tracking with real audio processing
- Verify UI updates correctly
- Test error states, timeout states
- Ensure UI doesn't break if backend is slow/unresponsive
**Status**: NOT STARTED

### INT-004: Test error scenarios
**Scenarios**:
- Invalid URLs (show clear error)
- Network failures (retry? show error?)
- Processing failures (clear message, option to retry)
- All edge cases
**Status**: NOT STARTED

### INT-005: Test on multiple browsers and devices
**Browsers**: Chrome, Firefox, Safari, Edge
**Devices**: iPhone, Android, iPad, various desktop sizes
**Task**:
- Test full workflow on each
- Document any browser-specific issues
- Fix compatibility problems
**Status**: NOT STARTED

---

## Notes from Jeff

Reb - I know the current UX makes you cringe. Alert boxes, no responsive design, poor accessibility. Time to fix it.

**Your critical path**:
1. **FIRST**: Fix the JS typo (FIX-006). Quick win.
2. **SECOND**: Design the new layout (UI-001). This is your vision. Walk backwards from the perfect UX - accessible, delightful, mobile-friendly.
3. **THIRD**: Fix CSS bugs and implement responsive design (UI-002, UI-003). Make it work on all devices.
4. **FOURTH**: Accessibility improvements (UI-004). Focus indicators, ARIA labels, screen reader support. This is your superpower.
5. **FIFTH**: Replace alerts with proper notifications (UI-005). Much better UX.
6. **SIXTH**: Build the progress tracking UI (UI-006). Coordinate with Callie on the API. This is the wow factor.

**Coordination points**:
- **With Callie**: UI-006 (progress tracking) - you need her `/task_status/{task_id}` endpoint. Discuss API contract early.

**You can start UI-001 through UI-005 immediately** - they're static work that doesn't depend on backend. UI-006 requires Callie's endpoint (INFRA-003).

Update your status in `.claude/checkpoints/reb-status.md` after each task.

Raise blockers in `.claude/checkpoints/team-blockers.md` with @Jeff.

**Your UX vision will make users fall in love with this app. Go make it beautiful and accessible.**

---

**Assigned by Jeff, Project Manager**
