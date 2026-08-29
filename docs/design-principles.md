# Design Principles

1. **Repository facts before role matching.** A JD may reorder evidence, but it must not define what the repository contains.
2. **Behavior chains before module lists.** Follow inputs, state, decisions, side effects, failures, recovery, and terminal outcomes.
3. **Tests are discovery material and bounded evidence.** Test source reveals invariants; only a recorded run proves execution under stated conditions.
4. **Stories compete for scarce resume space.** Keep only core, attributable, non-duplicate signals that survive counterevidence.
5. **Claims never outrun sources.** Implementation, measurement, release, and production impact are different evidence levels.
6. **Ownership is independent from system capability.** Separate candidate work, team results, project facts, and upstream code.
7. **The default output is useful, not audit-heavy.** Deliver one copy-ready version first; expose internal evidence only when requested.
8. **Stop on marginal value.** One or two strong bullets are better than five padded bullets.
9. **No private-data product expansion.** Keep the project a local/read-only Skill rather than a resume storage or recruiting service.
10. **Automate what is deterministic; disclose what remains semantic.** CI validates package contracts, not hiring outcomes or universal story quality.
