# Foundational Discovery Methodology

Transforms a vague project idea into a rich, technology-agnostic context document (FOUNDATION.md) BEFORE any technical scaffolding happens. This document becomes the single source of truth that informs all subsequent phases.

**Not optional.** Every project runs this step. Complexity scales to the project profile.

---

## Flow

```
Deep exploration → Structured Q&A → Interactive refinement → Document generation → Profile validation
```

---

## 1. Deep Exploration

Read ALL available materials before asking a single question — project descriptions, reference projects, business context, prior art. Understand the full landscape so questions are informed, not naive.

**Adaptive to what exists:**
- Rich prior art (README, specs, docs, existing code) → thorough reading
- Blank slate → short/skip

**What to read (in order):**
1. README.md, ABOUT.md, or any project description
2. Existing specs or requirements documents
3. CLAUDE.md (if exists) — existing decisions and patterns
4. Source code structure (directory layout, key files)
5. Package manifests (package.json, pyproject.toml, Cargo.toml, etc.)
6. CI/CD configuration
7. Any referenced external documents or prior art

---

## 2. Structured Q&A

**Multiple-choice questions with descriptions.** Each option has a label + 1-2 sentence description of what it implies and its tradeoffs. This is dramatically more effective than open-ended questions because it reduces ambiguity, surfaces tradeoffs, and structures the decision space.

### Core rules

- **NEVER assume.** If there is ANY ambiguity, ask. This is the governing principle.
- **Each round builds on previous answers.** Don't ask about integrations before knowing if it's a product or a prototype.
- **No fixed number of rounds or questions.** As many as the project needs. The process converges naturally.
- Questions progress from high-level (vision, scope, constraints) → specific (features, behaviors, integrations).
- **Use AskUserQuestion with batched questions** (3-4 per call) for token efficiency.

### Profile-scaled depth

| Profile | Q&A Calls | Focus |
|---------|-----------|-------|
| Quick | 1 call (3-4 questions) | Vision + scope + key constraint. Fast convergence. |
| Standard | 2-3 calls | Vision → features → behaviors → constraints |
| Enterprise | 3-5 calls (soft limit: 8 rounds max) | Comprehensive: vision → features → integrations → security → edge cases → NFRs |

### Question categories (adapt to project type)

**Software/product projects:**
- Vision and problem statement
- Target users and use cases
- Core capabilities (features at high level)
- Constraints (technical, business, timeline)
- Integrations (external services, APIs, databases)
- Security and privacy requirements
- Non-functional requirements (performance, scalability)
- Priority and scope boundaries

**Research projects:**
- Research question and hypothesis
- Methodology and approach
- Data sources and collection
- Deliverables and success criteria
- Timeline and milestones

**Data projects:**
- Data sources and formats
- Processing pipeline requirements
- Output formats and consumers
- Quality and validation requirements
- Scale and performance needs

**Operations/automation projects:**
- Processes to automate
- Tools and systems involved
- Success metrics
- Error handling and recovery
- Monitoring and alerting needs

The methodology (structured multiple-choice building on answers) is universal; the content is domain-specific.

---

## 3. Interactive Refinement

After the Q&A rounds, present a brief synthesis of what was understood. The user discusses specifics — feature difficulty, tradeoffs, priority changes. This back-and-forth is expected. Stay in dialogue until confirmed.

For Quick profile: synthesis can be a 3-5 bullet summary. For Enterprise: detailed section-by-section review.

---

## 4. FOUNDATION.md Generation

Generate `docs/FOUNDATION.md`. Format: Markdown, dual-readable (humans + LLMs).

### Header instruction block

```markdown
<!-- INSTRUCTIONS FOR IMPLEMENTATION AGENTS
This document defines WHAT the system does and WHY. It is technology-agnostic.
Do NOT select specific technologies based on this document alone.
Technology selection happens in Phase 1: Technical Landscape.
Use this to understand the full scope before proposing any implementation.
-->
```

Adapt the instruction text to the project type (non-software projects may reference different phases or milestones).

### Document structure (adapts to project type)

**For software/product projects, a complete document typically includes:**

```
1.  Vision and Problem Statement (problem, vision, what this is NOT, context)
2.  Core Capabilities (summary of each major feature)
3.  System Behavior Specification (happy path, scheduling, state management, idempotency)
4+. Detailed Feature Sections (one per capability: requirements, data flow, error handling)
N.  Edge Cases and Error Handling (comprehensive)
N+1. Security and Privacy (threat model, defense layers, credentials, PII)
N+2. Non-Functional Requirements (performance, scalability, reliability, observability)
N+3. Priority Tiers — Tier 1 (MVP), Tier 2 (Differentiation), Tier 3 (Polish)
     Each with justification + effort estimate calibrated for AI-agent development
N+4. Glossary
Appendices (if needed): data contracts, config schema, reference matrices
```

**For non-software projects**, the sections change entirely but the principles remain: comprehensive, unambiguous, technology-agnostic, dual-readable, with clear priority tiers and scope boundaries.

### Profile-scaled depth

| Profile | FOUNDATION.md | Sections |
|---------|--------------|----------|
| Quick | Abbreviated, 1-2 pages | Vision + Core Capabilities + Priority Tiers |
| Standard | Full, 5-15 pages | All standard sections |
| Enterprise | Comprehensive, 10-30+ pages | All sections + appendices |

### Key properties

- **Technology-agnostic** (WHAT and WHY, never HOW)
- **Edge cases, security, and non-functional requirements are NOT optional** (except Quick profile where they are abbreviated)
- **Effort estimates calibrated for multi-agent AI development**
- **Priority tiers with justification**
- **Dual-readable** (humans and LLMs — clear structure, no ambiguity)

---

## 5. Profile Validation

After FOUNDATION.md generation, count complexity indicators to validate the selected profile:

**Complexity signals:**
- Feature count
- Integration count (external services, APIs)
- Security requirements (auth, encryption, compliance mentions)
- Team references (multi-team, cross-functional)
- Compliance mentions (GDPR, HIPAA, SOC2, PCI)
- Architecture complexity (microservices, event-driven, multi-region)

**Quick threshold:** <5 features, 0-1 integrations, no security model beyond basic auth
**Standard threshold:** 5-15 features, 1-5 integrations, standard security
**Enterprise threshold:** 15+ features OR 5+ integrations OR compliance requirements OR multi-team

**If project exceeds its profile threshold:**
- Suggest upgrade with specific reasons (e.g., "Found 8 features and 3 integrations — Standard profile recommended")
- User always has final say
- If user keeps Quick despite suggestion: proceed, but log warning in DECISIONS.md

**If project is simpler than its profile:**
- Suggest downgrade (e.g., "Simple CLI with 2 features — Quick profile would be faster")
- User always has final say

---

## 6. Exit Conditions

Discovery is complete when:
1. FOUNDATION.md exists in `docs/`
2. Project profile is validated (or user override documented)
3. User has confirmed the synthesis (no outstanding questions)
