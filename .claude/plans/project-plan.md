# StreamStem Production Readiness - Project Plan

**Project Manager**: Jeff
**Created**: 2025-12-08
**Status**: ACTIVE
**Objective**: Make StreamStem production-ready for online deployment with fixed bugs, redesigned UI/UX, and background job processing

## Executive Summary

StreamStem has critical bugs blocking core functionality, security vulnerabilities preventing deployment, and significant UX issues. This plan walks backwards from successful deployment to establish a clear critical path with phases, dependencies, and assignments.

**Timeline Estimate**: 3-5 days of focused work
**Risk Level**: MEDIUM (Celery complexity, UI scope, deployment target flexibility)
**Success Criteria**: All bugs fixed, Celery/Redis working, UI redesigned, deployed and stable

---

## Critical Path Analysis

### BLOCKING EVERYTHING (Must Fix First)
1. **Type comparison bugs** in `demucs_processor.py` - Lines 47, 70 compare int to string
   - **Impact**: 6-stem mode NEVER works, 2-stem mode NEVER works
   - **Blocks**: All testing, all features
   - **Owner**: Aphex (primary) + Callie (review)

2. **Exposed API credentials** in `config.json`
   - **Impact**: Security breach, cannot deploy
   - **Blocks**: Production deployment
   - **Owner**: Callie (security critical)

### HIGH PRIORITY (Required for Production)
3. **Add Celery/Redis background processing** (user requirement)
   - **Impact**: Long-running tasks block web server
   - **Blocks**: Production scalability
   - **Owner**: Callie (backend infrastructure)

4. **Error handling missing** throughout codebase
   - **Impact**: Silent failures, poor UX
   - **Blocks**: Reliability
   - **Owner**: Callie (backend), Reb (frontend)

5. **Complete UI/UX redesign** (user requirement)
   - **Impact**: Poor accessibility, no responsive design
   - **Blocks**: User satisfaction
   - **Owner**: Reb (full ownership)

### MEDIUM PRIORITY (Required for Security/Stability)
6. **Path traversal vulnerability** (application.py:153)
7. **File cleanup strategy** (too aggressive, no persistence)
8. **Missing dependencies** in requirements.txt
9. **Dockerfile improvements** (Tailwind build, security)
10. **Progress tracking UI** (backend support + frontend display)

---

## Phase Breakdown

### PHASE 0: Critical Bugs (BLOCKING) - Day 1 Morning
**Objective**: Fix bugs that prevent core functionality from working at all

**Tasks**:
- [x] **FIX-001**: Type comparison bug in demucs_processor.py:47 (int vs "6") - **Aphex**
- [x] **FIX-002**: Type comparison bug in demucs_processor.py:70 (int vs "2") - **Aphex**
- [x] **FIX-003**: Move config.json credentials to environment variables - **Callie**
- [x] **FIX-004**: Update application.py to use environment variables - **Callie**
- [x] **FIX-005**: Update spotify_to_yt.py to use environment variables - **Callie**
- [x] **FIX-006**: Fix JavaScript typo main.js:312 ("mesdsdddddDDDdsage") - **Reb**

**Dependencies**: None (all parallel)
**Blockers Removed**: Enables testing of stem separation, prepares for deployment
**Success Criteria**: App can separate 2/4/6 stems correctly, no secrets in code

---

### PHASE 1: Backend Infrastructure - Day 1 Afternoon + Day 2
**Objective**: Add production-ready infrastructure and error handling

**Tasks**:
- [ ] **INFRA-001**: Install and configure Celery + Redis - **Callie**
- [ ] **INFRA-002**: Convert process_audio endpoint to async Celery task - **Callie**
- [ ] **INFRA-003**: Add task status/progress tracking endpoint - **Callie**
- [ ] **INFRA-004**: Add comprehensive error handling to spotify_to_yt.py - **Callie**
- [ ] **INFRA-005**: Add error handling to downloader.py - **Callie**
- [ ] **INFRA-006**: Add error handling to demucs_processor.py - **Callie**
- [ ] **INFRA-007**: Fix path traversal vulnerability (application.py:153) - **Callie**
- [ ] **INFRA-008**: Redesign file cleanup strategy (less aggressive) - **Callie** + **Aphex**
- [ ] **INFRA-009**: Add missing dependencies to requirements.txt - **Callie**
- [ ] **INFRA-010**: Fix duplicate class definitions in application.py - **Callie**

**Dependencies**: Phase 0 complete (need working stem separation to test Celery jobs)
**Blockers Removed**: Enables long-running tasks, production deployment, progress tracking
**Success Criteria**: Celery processes audio in background, progress tracking works, errors handled gracefully

---

### PHASE 2: UI/UX Redesign - Day 2 + Day 3 (PARALLEL with Phase 1)
**Objective**: Complete redesign with accessibility, responsiveness, modern UX

**Tasks**:
- [ ] **UI-001**: Design new layout (mobile-first, accessible) - **Reb**
- [ ] **UI-002**: Fix CSS bugs (invalid selectors, height units, duplicates) - **Reb**
- [ ] **UI-003**: Implement responsive design (mobile/tablet/desktop breakpoints) - **Reb**
- [ ] **UI-004**: Improve accessibility (focus indicators, ARIA labels, contrast) - **Reb**
- [ ] **UI-005**: Replace browser alerts with proper UI notifications - **Reb**
- [ ] **UI-006**: Add real-time progress tracking UI (connects to Celery status) - **Reb**
- [ ] **UI-007**: Improve form validation (inline, not just on submit) - **Reb**
- [ ] **UI-008**: Polish animations and transitions - **Reb**
- [ ] **UI-009**: Test with screen readers and keyboard navigation - **Reb**
- [ ] **UI-010**: Build production Tailwind CSS - **Reb**

**Dependencies**:
- Can start UI-001 to UI-005 immediately (static work)
- UI-006 requires INFRA-003 complete (progress tracking endpoint)
- UI-010 requires all CSS work complete

**Blockers Removed**: Enables delightful user experience, mobile usage, accessibility compliance
**Success Criteria**: Beautiful, accessible, responsive UI that works on all devices

---

### PHASE 3: ML/Audio Optimization - Day 3 (PARALLEL with Phase 2)
**Objective**: Optimize Demucs performance and audio quality

**Tasks**:
- [ ] **ML-001**: Review and optimize Demucs parameters (segment_size, overlap) - **Aphex**
- [ ] **ML-002**: Test audio quality across 2/4/6 stem modes - **Aphex**
- [ ] **ML-003**: Add progress reporting from Demucs subprocess - **Aphex** + **Callie**
- [ ] **ML-004**: Document optimal settings for different scenarios - **Aphex**
- [ ] **ML-005**: Add audio format validation and conversion - **Aphex**

**Dependencies**: Phase 0 complete (need type bugs fixed)
**Blockers Removed**: Ensures best possible audio quality and performance
**Success Criteria**: Optimal separation quality, clear progress feedback, all formats supported

---

### PHASE 4: Integration & Testing - Day 4
**Objective**: Integrate all components, test end-to-end, fix integration issues

**Tasks**:
- [ ] **INT-001**: Test complete workflow (URL → download → process → download stems) - **All**
- [ ] **INT-002**: Test Celery job queueing and parallel processing - **Callie**
- [ ] **INT-003**: Test progress tracking UI with real Celery tasks - **Reb** + **Callie**
- [ ] **INT-004**: Test error scenarios (invalid URLs, API failures, process crashes) - **All**
- [ ] **INT-005**: Test on multiple browsers and devices - **Reb**
- [ ] **INT-006**: Test Spotify URL conversion with real credentials - **Callie**
- [ ] **INT-007**: Performance testing (multiple concurrent jobs) - **Callie** + **Aphex**
- [ ] **INT-008**: Code review - all agents review each other's work - **All**

**Dependencies**: Phases 1, 2, 3 complete
**Blockers Removed**: Ensures everything works together
**Success Criteria**: Complete workflow works flawlessly, no bugs, excellent performance

---

### PHASE 5: Deployment Preparation - Day 4 + Day 5
**Objective**: Prepare for production deployment (deployment-target agnostic)

**Tasks**:
- [ ] **DEPLOY-001**: Update Dockerfile (Tailwind build, security hardening) - **Callie**
- [ ] **DEPLOY-002**: Create .env.example with all required variables - **Callie**
- [ ] **DEPLOY-003**: Update .gitignore (ensure secrets never committed) - **Callie**
- [ ] **DEPLOY-004**: Add environment variable validation on startup - **Callie**
- [ ] **DEPLOY-005**: Configure Redis for production (persistent vs ephemeral) - **Callie**
- [ ] **DEPLOY-006**: Document deployment process (Heroku/AWS/VPS options) - **Callie**
- [ ] **DEPLOY-007**: Test Docker build and run locally - **All**
- [ ] **DEPLOY-008**: Create deployment checklist - **Jeff**
- [ ] **DEPLOY-009**: Security audit (HTTPS, CORS, CSP, trusted hosts) - **Callie**
- [ ] **DEPLOY-010**: Final smoke test in production-like environment - **All**

**Dependencies**: Phase 4 complete
**Blockers Removed**: Ready to deploy anywhere
**Success Criteria**: App deploys successfully, runs securely in production

---

## Task Assignments by Agent

### Callie (Backend/Security Lead)
**Phase 0**: FIX-003, FIX-004, FIX-005 (move secrets to env vars)
**Phase 1**: All INFRA tasks (Celery, error handling, security)
**Phase 3**: ML-003 (progress reporting - backend side)
**Phase 4**: INT-002, INT-004, INT-006, INT-007 (backend testing)
**Phase 5**: All DEPLOY tasks (deployment prep)

**Priority**: Security issues FIRST (exposed credentials), then Celery infrastructure

### Reb (UI/UX Lead)
**Phase 0**: FIX-006 (JS typo)
**Phase 2**: All UI tasks (complete redesign)
**Phase 4**: INT-003, INT-004, INT-005 (frontend testing)

**Priority**: Start with static UI work (UI-001 to UI-005), coordinate with Callie on progress tracking

### Aphex (ML/Audio Lead)
**Phase 0**: FIX-001, FIX-002 (type bugs in demucs_processor)
**Phase 1**: INFRA-008 (file cleanup strategy - audio files)
**Phase 3**: All ML tasks (optimization)
**Phase 4**: INT-001, INT-004, INT-007 (testing stem separation)

**Priority**: Type bugs IMMEDIATELY (blocks everything), then optimization

### Jeff (Project Manager)
- Monitor daily status updates in `.claude/checkpoints/`
- Coordinate handoffs between phases
- Resolve blockers in `.claude/checkpoints/team-blockers.md`
- Create deployment checklist (DEPLOY-008)
- Facilitate code reviews
- Weekly progress reports in `.claude/reports/`

---

## Risk Assessment & Mitigation

### HIGH RISK
**Risk**: Celery/Redis complexity may cause delays
**Mitigation**: Callie has god-tier backend expertise, start early, use proven patterns
**Contingency**: If Celery blocks progress, ship with synchronous processing first, add Celery in v2

**Risk**: UI redesign scope creep
**Mitigation**: Reb defines clear scope in UI-001, Jeff monitors for scope expansion
**Contingency**: Prioritize core UX improvements, defer polish to v2

**Risk**: Deployment target uncertainty
**Mitigation**: Design deployment-agnostic (env vars, flexible storage), document multiple options
**Contingency**: User chooses target, we adapt quickly

### MEDIUM RISK
**Risk**: File cleanup strategy conflicts with user expectations
**Mitigation**: Aphex + Callie discuss in Phase 1, define retention policy
**Contingency**: Make configurable via environment variable

**Risk**: Progress tracking may not work smoothly with Celery
**Mitigation**: Callie builds robust status endpoint, Reb designs graceful degradation
**Contingency**: Show binary states (processing/complete) if granular progress fails

### LOW RISK
**Risk**: Audio quality regression from parameter changes
**Mitigation**: Aphex tests thoroughly, compares before/after
**Contingency**: Revert to current parameters if quality drops

---

## Communication Workflow

### Daily Standup (Async)
**Time**: Morning (whenever agent starts work)
**Location**: `.claude/checkpoints/{agent}-status.md`
**Format**:
- What I completed yesterday
- What I'm working on today
- Any blockers

**Jeff reads all status files and coordinates**

### Blockers
**Location**: `.claude/checkpoints/team-blockers.md`
**Format**: `@AgentName - Blocked by X, need Y`
**Response Time**: Jeff monitors continuously, responds within 1 hour

### Code Reviews
**Location**: `.claude/checkpoints/code-reviews/{agent}-{date}.md`
**Trigger**: When agent completes a task
**Process**: Jeff assigns reviewer based on domain (Callie reviews backend, Reb reviews UI, etc.)

### Team Discussions
**Location**: `.claude/checkpoints/team-discussion.md`
**Trigger**: 2+ agents disagree on approach
**Process**: Jeff facilitates, team reaches consensus

### Progress Reports
**Location**: `.claude/reports/week-{N}-summary.md`
**Frequency**: End of each work day
**Owner**: Jeff

---

## Success Criteria (Definition of Done)

### Functional Requirements
- [x] All critical bugs fixed (type comparisons, JS typo)
- [ ] Celery/Redis background processing working
- [ ] 2-stem, 4-stem, 6-stem modes all work correctly
- [ ] Spotify URL conversion working
- [ ] Error handling prevents crashes
- [ ] Progress tracking shows real-time status
- [ ] File download/streaming works

### Non-Functional Requirements
- [ ] UI is accessible (WCAG 2.1 AA minimum)
- [ ] UI is responsive (mobile, tablet, desktop)
- [ ] No secrets in codebase (all in env vars)
- [ ] Path traversal vulnerability fixed
- [ ] Comprehensive error messages
- [ ] Docker builds successfully
- [ ] Production-ready deployment docs

### Quality Gates
- [ ] All code reviewed by peer
- [ ] Integration tests pass
- [ ] Performance acceptable (2-3 min per 4min song)
- [ ] No console errors in browser
- [ ] Security audit passed

---

## Next Steps (Immediate Actions)

1. **Jeff**: Write initial task files for Callie, Reb, Aphex (`.claude/tasks/{agent}-tasks.md`)
2. **Aphex**: Fix type comparison bugs in demucs_processor.py (BLOCKS EVERYTHING)
3. **Callie**: Move credentials to environment variables (BLOCKS DEPLOYMENT)
4. **Reb**: Fix JS typo, begin UI design planning
5. **All**: Update status in `.claude/checkpoints/{agent}-status.md` after completing Phase 0 tasks

---

## Foresight Notes

I see the completed project clearly:
- Deployed on flexible infrastructure (Heroku/AWS/VPS)
- Beautiful, accessible UI that users love
- Stems separating perfectly in background
- No crashes, excellent error messages
- Security audit clean
- Users sharing the app with friends

**The path is clear. The team is ready. The future is inevitable.**

---

**Created by Jeff with Gandalf-level foresight**
**Last updated**: 2025-12-08
