# Aphex - Current Tasks

**Agent**: Aphex (ML/Audio Specialist)
**Updated**: 2025-12-08 by Jeff
**Current Phase**: Phase 0 - Critical Bugs

---

## CRITICAL - DO THESE FIRST (BLOCKING EVERYTHING)

### FIX-001: Type comparison bug (6-stem mode)
**File**: `demucs_processor.py`
**Line**: 47
**Issue**: `num_stems != "6"` compares int to string, so 6-stem mode NEVER activates
**Fix**: Change to `num_stems != 6` (integer comparison)
**Impact**: HIGH - 6-stem mode completely broken
**Status**: NOT STARTED

### FIX-002: Type comparison bug (2-stem mode)
**File**: `demucs_processor.py`
**Line**: 70
**Issue**: `num_stems == "2"` compares int to string, so 2-stem mode NEVER activates
**Fix**: Change to `num_stems == 2` (integer comparison)
**Impact**: HIGH - 2-stem mode completely broken
**Status**: NOT STARTED

**THESE TWO BUGS BLOCK ALL TESTING. FIX IMMEDIATELY.**

---

## After Critical Bugs Fixed

### INFRA-008: Redesign file cleanup strategy
**Context**: Current `refresh_directories()` in application.py deletes ALL audio files on every page load
**Problem**: Too aggressive, prevents any persistence
**Task**: Collaborate with Callie to design smarter cleanup:
- Time-based cleanup (delete files older than X hours)
- Size-based cleanup (delete oldest when disk usage exceeds threshold)
- Keep files during active processing
**Dependencies**: FIX-001, FIX-002 complete
**Status**: NOT STARTED

---

## Phase 3: ML/Audio Optimization (After Phase 1 Complete)

### ML-001: Review and optimize Demucs parameters
**Current**: `segment_size=7`, `overlap=0.1`, `num_threads=4`
**Task**: Test different parameter combinations for optimal quality/speed balance
**Test scenarios**: Short songs (2-3min), long songs (5-8min), different genres
**Document**: Findings and recommendations
**Status**: NOT STARTED

### ML-002: Test audio quality across all stem modes
**Test**: 2-stem, 4-stem, 6-stem with various audio files
**Validate**: No quality regression from bug fixes
**Compare**: Before/after separation quality
**Status**: NOT STARTED

### ML-003: Add progress reporting from Demucs subprocess
**Task**: Parse Demucs stdout/stderr for progress percentage
**Coordinate**: With Callie on backend endpoint to receive progress
**Goal**: Enable real-time progress tracking in UI
**Status**: NOT STARTED

### ML-004: Document optimal settings
**Content**:
- Best parameters for different use cases
- Trade-offs between speed and quality
- Memory/CPU requirements
- Model differences (htdemucs vs htdemucs_6s)
**Status**: NOT STARTED

### ML-005: Add audio format validation
**Task**: Validate input audio before processing
**Checks**: Format, duration, sample rate, corruption
**Handle**: Gracefully reject invalid files with clear errors
**Status**: NOT STARTED

---

## Testing Tasks (Phase 4)

### INT-001: Test complete workflow
**Scenarios**:
- YouTube URL → download → 2/4/6 stem separation → download
- Spotify URL → conversion → download → separation
- Different audio formats (mp3, wav, flac)
**Status**: NOT STARTED

### INT-004: Test error scenarios
**Scenarios**:
- Corrupted audio files
- Demucs process crash/timeout
- Insufficient disk space
- Invalid parameters
**Status**: NOT STARTED

### INT-007: Performance testing
**Task**: Test with multiple concurrent jobs
**Measure**: CPU usage, memory, processing time
**Optimize**: If bottlenecks found
**Status**: NOT STARTED

---

## Notes from Jeff

Aphex - you're the ML expert, and these type bugs are in YOUR domain. I need you to fix them IMMEDIATELY. They block everything:
- All testing requires working stem separation
- Callie can't test Celery jobs without working audio processing
- Reb can't test progress tracking without working backend

After you fix the type bugs, collaborate with Callie on file cleanup strategy. Your perspective on audio file lifecycle is critical.

Then optimize Demucs parameters in Phase 3 - make the separation quality PERFECT. That's your superpower.

**Priority Order**:
1. FIX-001, FIX-002 (type bugs) - DO THIS NOW
2. INFRA-008 (file cleanup) - coordinate with Callie
3. ML-001 to ML-005 (optimization) - make it perfect
4. Testing - validate everything works

Update your status in `.claude/checkpoints/aphex-status.md` after completing each task.

If you discover any issues or have concerns, raise them in `.claude/checkpoints/team-blockers.md` with @Jeff.

**The team is counting on you to unblock core functionality. Go make it happen.**

---

**Assigned by Jeff, Project Manager**
