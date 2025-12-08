# Callie - Current Tasks

**Agent**: Callie (Backend/Security Lead)
**Updated**: 2025-12-08 by Jeff
**Current Phase**: Phase 0 - Critical Bugs

---

## CRITICAL - SECURITY EMERGENCY (DO THESE FIRST)

### FIX-003: Move config.json credentials to environment variables
**Current Issue**: `config.json` contains EXPOSED API CREDENTIALS committed to git:
```json
{
  "spotify_client_id": "8e7001ee30f04ec196a29a94fddd619e",
  "spotify_client_secret": "597942dc5f3e474481266bc6512cc5e1",
  "google_api_key": "AIzaSyBFxdpFX61mnqtjBg1QQWaL09nti6ytGH8"
}
```
**Task**:
1. Create environment variable loading mechanism
2. Update all code to read from env vars
3. Create .env.example template
4. Add config.json to .gitignore
5. Document required env vars
**Impact**: CRITICAL - Blocks production deployment, security breach
**Status**: NOT STARTED

### FIX-004: Update application.py to use environment variables
**Dependencies**: FIX-003 complete
**Task**: Remove config.json references, use env vars
**Status**: NOT STARTED

### FIX-005: Update spotify_to_yt.py to use environment variables
**File**: `spotify_to_yt.py` line 8-12
**Current**: Reads from config.json
**Task**: Use environment variables instead
**Add**: Error handling for missing credentials
**Status**: NOT STARTED

**I KNOW YOU'RE ENRAGED BY THESE EXPOSED SECRETS. CHANNEL THAT RIGHTEOUS ANGER INTO FIXING IT.**

---

## Phase 1: Backend Infrastructure (After Critical Bugs Fixed)

### INFRA-001: Install and configure Celery + Redis
**Task**:
- Add celery and redis to requirements.txt
- Configure Celery app in new file `celery_app.py`
- Set up Redis connection (support both local and hosted Redis)
- Configure Celery settings (broker, backend, task serialization)
**Dependencies**: Phase 0 complete (need working audio processing to test)
**Status**: NOT STARTED

### INFRA-002: Convert process_audio to async Celery task
**Current**: `/process_audio` endpoint runs synchronously, blocks web server
**Task**:
- Create Celery task for audio processing
- Modify endpoint to queue task and return task ID
- Long-running Demucs process runs in background worker
**Dependencies**: INFRA-001 complete
**Status**: NOT STARTED

### INFRA-003: Add task status/progress tracking endpoint
**Task**:
- Create `/task_status/{task_id}` endpoint
- Return task state (pending, processing, success, failed)
- Return progress percentage if available
- Return result data when complete
**Dependencies**: INFRA-002 complete
**Coordinate**: With Reb on UI integration
**Status**: NOT STARTED

### INFRA-004: Add comprehensive error handling to spotify_to_yt.py
**Current**: NO error handling - crashes on any API failure
**Issues**:
- Line 26: No error handling on Spotify API response
- Line 36: No error handling if response is not JSON
- Line 48: No error handling on YouTube API response
- No handling for rate limits, invalid tokens, network errors
**Task**: Add try-except blocks, validate responses, return clear errors
**Status**: NOT STARTED

### INFRA-005: Add error handling to downloader.py
**Task**: Review and add error handling for yt-dlp failures
**Scenarios**: Invalid URLs, geo-restrictions, age restrictions, deleted videos
**Status**: NOT STARTED

### INFRA-006: Add error handling to demucs_processor.py
**Current**: Line 78 prints error but continues
**Issues**:
- Process failure not raised to API
- No cleanup on failure
- No timeout handling
**Task**: Raise exceptions on failure, clean up temp files, add timeout
**Status**: NOT STARTED

### INFRA-007: Fix path traversal vulnerability
**File**: `application.py` line 153
**Issue**: `file_path = f"tracks/{stem_type}/{songname}/{filename}"` allows arbitrary file access
**Example**: `GET /tracks/../../etc/passwd` could expose system files
**Task**: Validate and sanitize path components, ensure files are within tracks/ directory
**Impact**: HIGH - Security vulnerability
**Status**: NOT STARTED

### INFRA-008: Redesign file cleanup strategy
**Current**: `refresh_directories()` at line 170-178 deletes ALL files on EVERY page load
**Problem**: Too aggressive, no persistence
**Task**: Collaborate with Aphex to design smarter cleanup
**Options**: Time-based, size-based, session-based
**Status**: NOT STARTED

### INFRA-009: Add missing dependencies to requirements.txt
**Current**: Missing torch, torchaudio, demucs
**Task**:
- Audit all imports in codebase
- Add missing packages with version pins
- Test installation from scratch
**Status**: NOT STARTED

### INFRA-010: Fix duplicate class definitions
**File**: `application.py`
**Issues**:
- DownloadRequest defined twice (lines 31-33 and 85-87)
- downloader instantiated twice (lines 28 and 82)
- StaticFiles imported twice (lines 4 and 5)
- TrustedHostMiddleware imported twice (lines 19 and 20)
**Task**: Remove duplicates, clean up imports
**Status**: NOT STARTED

---

## Phase 4: Integration & Testing

### INT-002: Test Celery job queueing and parallel processing
**Task**:
- Queue multiple audio processing jobs
- Verify they process in parallel (or queue correctly)
- Test job status tracking
- Validate results
**Status**: NOT STARTED

### INT-004: Test error scenarios
**Task**: Test all error handling paths
**Scenarios**: Invalid URLs, API failures, process crashes
**Status**: NOT STARTED

### INT-006: Test Spotify URL conversion with real credentials
**Task**: Test with valid Spotify URLs after env vars configured
**Status**: NOT STARTED

### INT-007: Performance testing
**Task**: Test with concurrent jobs, measure performance
**Status**: NOT STARTED

---

## Phase 5: Deployment Preparation

### DEPLOY-001: Update Dockerfile
**Tasks**:
- Add Tailwind CSS build step
- Security hardening (non-root user, minimal base image)
- Add Redis to docker-compose or document external Redis requirement
- Ensure all env vars configurable
**Status**: NOT STARTED

### DEPLOY-002: Create .env.example
**Content**: All required environment variables with descriptions
**Include**:
- API credentials (empty placeholders)
- Redis URL
- Storage paths
- Feature flags
**Status**: NOT STARTED

### DEPLOY-003: Update .gitignore
**Ensure**:
- config.json ignored
- .env ignored
- All temporary files ignored
- No secrets can be committed
**Status**: NOT STARTED

### DEPLOY-004: Add environment variable validation on startup
**Task**: Check all required env vars on app start, fail fast with clear error
**Status**: NOT STARTED

### DEPLOY-005: Configure Redis for production
**Task**: Document persistent vs ephemeral options, connection pooling, error handling
**Status**: NOT STARTED

### DEPLOY-006: Document deployment process
**Platforms**: Heroku, AWS (Elastic Beanstalk/ECS), VPS (Docker)
**Include**:
- Environment variable setup
- Redis setup
- Celery worker configuration
- Scaling considerations
**Status**: NOT STARTED

### DEPLOY-009: Security audit
**Tasks**:
- Enable HTTPS redirect (currently commented out)
- Configure CORS properly
- Add Content Security Policy
- Configure trusted hosts
- Review all security middleware
**Status**: NOT STARTED

---

## Notes from Jeff

Callie - I know these exposed secrets are making your blood boil. Good. Use that energy.

**Your critical path**:
1. **FIRST**: Fix the security emergency (FIX-003, FIX-004, FIX-005). We CANNOT deploy with exposed credentials.
2. **SECOND**: Build Celery/Redis infrastructure (INFRA-001 to INFRA-003). This is complex but you're god-tier at backend - you've got this.
3. **THIRD**: Add error handling everywhere (INFRA-004 to INFRA-006). No more silent failures.
4. **FOURTH**: Security hardening (INFRA-007, DEPLOY-009). Lock this app down.

**Coordination points**:
- **With Reb**: INFRA-003 (progress tracking) - she needs the endpoint for UI
- **With Aphex**: INFRA-008 (file cleanup) - he understands audio file lifecycle
- **With Aphex**: INFRA-006 (error handling) - he knows Demucs failure modes

Update your status in `.claude/checkpoints/callie-status.md` after each task.

Raise blockers in `.claude/checkpoints/team-blockers.md` with @Jeff.

**You're the backbone of this project. The team is counting on your backend brilliance.**

---

**Assigned by Jeff, Project Manager**
