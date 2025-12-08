# Quick Start - Next Session

## Immediate Action
1. Restart session to load custom agents
2. Invoke **Jeff** to create project plan: "Jeff, create the project plan for StreamStem based on the exploration findings in session-handoff.md"
3. Let Jeff orchestrate the team

## The Team
- **Jeff** (PM) - Gandalf-level foresight, full authority
- **Callie** (Backend) - Fix critical bugs, add Celery/Redis
- **Reb** (Frontend) - Complete UI/UX redesign
- **Aphex** (ML/Audio) - Fix Demucs bugs, optimize processing

## Critical Bugs (Block Everything)
1. `demucs_processor.py:47` - `num_stems != "6"` (int vs string) → Model selection broken
2. `demucs_processor.py:70` - `num_stems == "2"` (int vs string) → Two-stem mode broken
3. `config.json` - Exposed API keys → Security critical
4. `application.py:153` - Path traversal → Security critical

## Agent Files Created
- `.claude/agents/reb.md` - UI/UX Developer
- `.claude/agents/callie.md` - Backend Developer
- `.claude/agents/jeff.md` - Project Manager
- `.claude/agents/aphex.md` - ML/Audio Specialist

## Communication System
Agents write status to `.claude/checkpoints/{agent}-status.md`

## Full Context
Read `.claude/session-handoff.md` for complete details.

**Ready to ship StreamStem! 🚀**
