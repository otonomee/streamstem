# Agent Communication System

This directory facilitates asynchronous communication between agents.

## Directory Structure

```
.claude/
├── agents/              # Agent definitions
│   ├── reb.md          # UI/UX Developer
│   ├── callie.md       # Backend Developer
│   ├── jeff.md         # Project Manager
│   └── aphex.md        # ML/Audio Specialist
│
├── checkpoints/         # Status updates & communication
│   ├── reb-status.md   # Reb's current work status
│   ├── callie-status.md # Callie's current work status
│   ├── aphex-status.md  # Aphex's current work status
│   ├── team-blockers.md # Current blockers with @mentions
│   ├── team-discussion.md # Team discussions (when 2+ disagree)
│   └── code-reviews/    # Code review feedback
│       └── {agent}-{date}.md
│
├── tasks/               # Task assignments
│   ├── reb-tasks.md    # Reb's assigned tasks
│   ├── callie-tasks.md # Callie's assigned tasks
│   └── aphex-tasks.md  # Aphex's assigned tasks
│
├── plans/               # Project planning
│   └── project-plan.md # Comprehensive project plan (Jeff creates)
│
└── reports/             # Progress reports
    └── week-{N}-summary.md
```

## Communication Protocols

### Status Updates
Each agent writes to their status file after completing major tasks:
- Current work
- What's completed
- What's next
- Any concerns

### Blockers
When blocked, agent writes to `team-blockers.md`:
```markdown
## [Date] - Agent Name
**Blocked by**: @other-agent
**Issue**: Description
**Needed**: What's needed to unblock
```

### Code Reviews
Agents review each other's work in `code-reviews/{reviewer}-{date}.md`:
```markdown
# Code Review by {Reviewer}
**Reviewing**: {Agent}'s work on {Feature}
**Files**: List of files reviewed

## Findings
- Issue 1
- Issue 2

## Approved/Changes Requested
```

### Team Discussions
When 2+ agents raise the same concern, discussion happens in `team-discussion.md`:
```markdown
# Team Discussion - [Date]
**Topic**: What we're discussing
**Participants**: @jeff @callie @reb @aphex

## Concern
Description

## Proposals
- Option 1
- Option 2

## Decision
Final decision with rationale
```

## Orchestrator Monitoring

The orchestrator should:
1. Read status files regularly to track progress
2. Check blockers and coordinate resolution
3. Assign code reviewers
4. Facilitate team discussions when needed
5. Keep team focused on objectives
