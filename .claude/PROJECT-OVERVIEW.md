# StreamStem - Project Overview

**Status**: ACTIVE - Phase 0 (Critical Bugs)
**Project Manager**: Jeff
**Started**: 2025-12-08
**Target Completion**: 2025-12-13 (5 days)

---

## Mission

Make StreamStem production-ready for online deployment with:
- All critical bugs fixed
- Secure credential management
- Celery/Redis background job processing
- Complete UI/UX redesign (accessible, responsive, delightful)
- Ready to deploy on Heroku/AWS/VPS

---

## Team

**Jeff** - Project Manager (Gandalf-level foresight)
- Plans, coordinates, resolves blockers
- Authority over priorities and assignments
- Monitors critical path

**Callie** - Backend/Security Lead (God-tier backend expert)
- Security fixes, Celery/Redis, error handling
- Enraged by security issues (good!)
- Paranoid about failure cases (excellent!)

**Reb** - UI/UX Lead (God-tier frontend/accessibility expert)
- Complete UI redesign, responsive, accessible
- Frustrated by poor UX (will fix it!)
- Obsessive about accessibility (perfect!)

**Aphex** - ML/Audio Specialist (God-tier Demucs expert)
- Fix type bugs, optimize parameters, audio quality
- Perfect pitch memory, frustrated by inefficiency
- Passionate about audio quality

---

## Critical Files

**Project Plan**: `.claude/plans/project-plan.md`
- Complete breakdown: phases, tasks, dependencies
- Risk analysis and mitigation
- Success criteria

**Task Assignments**:
- `.claude/tasks/aphex-tasks.md` - Aphex's current tasks
- `.claude/tasks/callie-tasks.md` - Callie's current tasks
- `.claude/tasks/reb-tasks.md` - Reb's current tasks

**Status Tracking**:
- `.claude/checkpoints/aphex-status.md` - Aphex's daily updates
- `.claude/checkpoints/callie-status.md` - Callie's daily updates
- `.claude/checkpoints/reb-status.md` - Reb's daily updates
- `.claude/checkpoints/jeff-status.md` - Jeff's coordination notes

**Communication**:
- `.claude/checkpoints/team-blockers.md` - Active blockers
- `.claude/checkpoints/team-discussion.md` - Team discussions

**Codebase Docs**:
- `CLAUDE.md` - Architecture, commands, configuration

---

## Current Phase: Phase 0 - Critical Bugs

**Status**: Tasks assigned, awaiting work start

**Critical bugs blocking everything**:
1. Type comparison bugs in demucs_processor.py (Aphex)
2. Exposed API credentials in config.json (Callie)
3. JavaScript typo in main.js (Reb)

**Why Phase 0 blocks everything**:
- Type bugs prevent stem separation from working
- Can't test any features without working stem separation
- Can't deploy with exposed credentials
- Must fix these before building new features

---

## Next Phases

**Phase 1**: Backend Infrastructure (Celery/Redis, error handling)
**Phase 2**: UI/UX Redesign (parallel with Phase 1)
**Phase 3**: ML/Audio Optimization (parallel with Phase 2)
**Phase 4**: Integration & Testing
**Phase 5**: Deployment Preparation

See `.claude/plans/project-plan.md` for full details.

---

## Success Metrics

**Functional**:
- All stem modes work (2/4/6 stems)
- Background processing with Celery
- Error handling prevents crashes
- Progress tracking shows real-time status

**Quality**:
- UI is accessible (WCAG 2.1 AA)
- UI is responsive (mobile/tablet/desktop)
- No secrets in codebase
- Security vulnerabilities fixed

**Deployment**:
- Docker builds successfully
- Environment variables configured
- Can deploy to any platform
- Documentation complete

---

## How Work Flows

1. **Jeff assigns tasks** via `.claude/tasks/{agent}-tasks.md`
2. **Agents update status** in `.claude/checkpoints/{agent}-status.md`
3. **Agents report blockers** in `.claude/checkpoints/team-blockers.md`
4. **Jeff monitors and coordinates** - removes blockers, assigns reviews
5. **Team discusses** in `.claude/checkpoints/team-discussion.md` when needed
6. **Jeff tracks progress** in `.claude/reports/`

---

## Key Principles

**Walk backwards from success**: See the finished product, work backwards to make it inevitable

**Think deeply 3x**: All agents self-check recursively before acting

**Trust expertise**: Agents are god-tier in their domains, defer to their judgment

**Never wrong**: Deep thinking means agents are never wrong, so they never waste time

**Coordinate, don't control**: Jeff orchestrates, doesn't micromanage

---

## Contact

This is an autonomous agent team. For questions or concerns:
- Agents: Update your status file or raise in team-blockers.md
- User: The team will keep you updated via progress reports

---

**The future is clear. The plan is solid. Success is inevitable.**

Created by Jeff with Gandalf-level foresight - 2025-12-08
