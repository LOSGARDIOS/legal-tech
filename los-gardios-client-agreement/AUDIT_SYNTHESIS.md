# PASS 1 SYNTHESIS — Client Agreement ↔ Client Guide Architecture Audit

Consolidates the four Pass-1 specialist reports (Legal Architecture / Source Reconciliation / Business-Commercial / UX-Editorial) run against the Partner Agreement↔Handbook benchmark. **No files have been edited.** This document is findings + decision points only, per the Master Prompt's explicit "do not edit until audit is complete" instruction.

---

## A. Document Inventory

| Document | Version marker today | Role | Binding? | Signed? | Source authority |
|---|---|---|---|---|---|
| `AGREEMENT_SHORT_HE.md/.pdf` | **none** | Legal commitment (framework agreement + Appendices A–D) | Yes | Yes (digital signature, single envelope) | Top of hierarchy for everything except the two narrow carve-outs below |
| `CLIENT_GUIDE_HE.md/.pdf` (content duplicated as hardcoded strings in `build_html_guide.py` — see standing build bug) | **none** | Understanding / methodology / commercial-model explanation / Intake | Model A today (explanatory only, §15(a1)) — not independently signed | No | Subordinate; governs only where Agreement/Appendices are silent |
| `COMMERCIAL_PROPOSAL_TEMPLATE_HE.md` | — | Deal-specific commercial terms | Yes, for economic matters only (§15(a)(3)) | Yes (signed alongside Agreement) | Overrides Guide/Framework on economic terms only; cannot touch §§8–14/Appendix A§3 |
| Intake Form (inside Guide) | — | Client-supplied raw inputs | **No** | No | Not a document in the hierarchy — only the copied/approved Appendix B entry binds (Agent 1 recommends the Agreement say this affirmatively) |
| `AGREEMENT_v2_HE.md/.pdf` (46pp, historical) | — | Predecessor agreement | Superseded | Superseded | Used only as ground-truth for clause reconciliation |

**Standing build-pipeline defect (unrelated to legal architecture, still live):** `build_html_guide.py` does not parse `CLIENT_GUIDE_HE.md` — Guide content is separately hardcoded as Python string literals in the build script. Any Guide redesign must edit both, or the desync bug must be fixed first as part of this project (recommend fixing it first, since otherwise every subsequent Guide edit in this project has to be applied twice).

---

## B. Consolidated findings by theme

### 1. Incorporation model — Agent 1 recommends **Model C (hybrid), narrowly scoped**
- Keep Model A (explanatory-only) as the default for narrative/relationship content.
- Explicitly merge-and-bind a *short, enumerated* list of Guide passages that currently carry real operative content with no locked anchor elsewhere — after rewriting them into precise numbered clauses, visually flagged (e.g. boxed "מחייב" callout) so readers can tell Model B passages from Model A ones at a glance.
- Concrete first candidate for merging: **Track A/B/C definitions**, which today live *only* in the Guide (`CLIENT_GUIDE_HE.md:69-83`) with no anchor in the Agreement's own roadmap table or §1 — this is a "silent Model B" provision today (real legal consequence, no firewall protection).
- Explicitly flagged as a judgment call: pure Model A + just fixing the version/firewall gaps is a legitimate alternative to Model C.

### 2. Liquidated damages — intent/malice gate (Agent 1 + Agent 3 converge on this)
- Agent 3 (business): Guide (`CLIENT_GUIDE_HE.md:30`) promises deterrence is against "deliberate/malicious" harm only; the Agreement's actual §11 trigger has **no intent requirement** — live drafting defect, Guide over-promises relative to what the Agreement actually does.
- Agent 1 (legal): confirms independently via the proportionality test — negligent/good-faith uncured breach currently triggers the same floor/multiplier/cap schedule as intentional harm, which is the clause's main punitive-characterization exposure under Israeli LD doctrine (Contracts (Remedies) Law §15).
- Agent 1's recommendation: **keep** the existing floor/multiplier/cap architecture (more proportionate than the Partner model's flat ₪100,000 floor — deal-size-linked vs. one-size-fits-all), but **add an intent/malice gate** before it attaches at all; ordinary negligent uncured breach falls back to §11(b)'s actual-damage remedy instead.
- Flagged as a genuine business-judgment call: the org may prefer strict-liability triggering for stronger deterrent bite even against negligence — but that sits in direct tension with the stated "we never intend to sue, deterrence against deliberate harm only" rationale, so it should be a conscious choice, not inertia.

### 3. Version-freeze mechanism — Agent 1: **single highest-priority fix in the whole audit**
- `AGREEMENT_SHORT_HE.md:67`'s definition of "ההסכם" points to "מדריך הלקוח (בגרסתו שאושרה)" but no document anywhere records an actual version number, date, or file identifier — circular reference, unlike Partner Agreement's "גרסה 1.0 · עודכן לאחרונה: 10.09.2026" on both cover and operative clause.
- No field on the signature page ties a specific Guide version to what the client actually signed. Today there is no way to prove, in a dispute 18 months and 3 revisions later, which Guide version a given client saw.
- Recommended fix (mechanical, not a judgment call): version line on Guide cover (major.minor), Chapter.Section numbering in the Guide body (it currently has none — headings/prose pointers only, which break silently on rename), a real version field on the signature page, and bundling the exact signed Guide PDF into the same e-signature envelope as the Agreement (cheapest, since Appendices A–D already ride in one envelope).

### 4. Update firewall — mostly already sound, two gaps
- §15(b) already blocks implied changes to §§8–14/Appendix A§3 via Guide update/Proposal/supplementary understanding — functionally comparable to the Partner model's protection list. No removals recommended from the locked side.
- **Gap 1:** Track A/B/C definitions (see §1 above) aren't in the protected zone even though they function as binding terms today — lock a one-line definition of each in Appendix B or §1.
- **Gap 2:** numeric duplication drift — LD floors, SLA timers, Stop-Loss default, Buyout figures are restated in the Guide; a proper Agreement amendment doesn't auto-update those restatements. Not a legal-authority problem (Guide can never override), but an equitable-reliance risk. Fix is process (mandatory "Guide sync" step + version bump on any amendment to a locked numeric term), not drafting.

### 5. Hierarchy — already well-built, narrow tie-breaker gap
- Existing 6-rank hierarchy (Appendix D → Supplementary Understanding → signed Proposal (economic matters) → Appendices A-C → Guide → Framework Agreement) already implements the "specific overrides general, never silently overriding confidentiality/IP" rule.
- Gap: rank-3's "economic matters" carve-out may not clearly cover a Proposal term that addresses the same non-economic topic as a general Guide principle (e.g. Track B's substantive structure). Recommend broadening to "any individually-negotiated specific term," while explicitly preserving the §§8–14/Appendix A§3 shield.
- Recommend §15(a) state affirmatively that the Intake Form is outside the hierarchy entirely.

### 6. Source reconciliation (Agent 2, 103-row matrix vs. the 46pp historical agreement)
- 6 clauses flagged **Missing** (need keep/restore/intentionally-omit decision), 1 **Contradictory** cross-reference (Appendix C "מחזיק"/"בעל שליטה" vs. Appendix D §1 — may already be resolved by a prior-session edit, needs re-verification against current file state), 2 **Requires-decision** items.
- Full matrix retained in Agent 2's report; not reproduced here in full to avoid duplication — pull specific rows when resolving item D below.

### 7. Business/commercial architecture (Agent 3)
- LD intent-gate mismatch — covered in §2 above.
- Two Guide passages duplicate the same asset-protection-cost information (Ch.1 asset table at lines 21-28 vs. the newer ₪150,000/15,000 worked example at lines ~32-43) — recommend merging.
- A citation error: something described as belonging in Appendix B actually belongs in Appendix C (or vice versa — "vision belongs in App. B" flagged as wrong).
- Several promise-leak items where marketing language risks reading as a guarantee (results/revenue/AI/staffing/timelines) — need the 5-way sentence classification pass (Legal/Operating-methodology/Explanation/Example/Marketing).

### 8. UX/editorial architecture (Agent 4)
- Current Guide narrative doesn't follow the Master Prompt's mandated 14-step sequence: Genesis chapter is mislabeled/misplaced, protections/restrictions are front-loaded (psychologically wrong — should come after the value case), and **two required content areas are entirely absent**: growth modes and project infrastructure.
- Needs a full narrative reorder as part of the Guide redesign phase (this is largely already directed by the Master Prompt's explicit 14-step spec, not an open judgment call).

---

## D. FINAL STATUS (this session's closing pass)

**Agreement (`AGREEMENT_SHORT_HE.md`, 29 pages):** closed. Pass-1 audit → two locked decisions (Model C incorporation, LD intent/malice gate) → 8 historical clauses restored → H-08 liability-cap mechanism (per-engagement cap + anti-double-recovery, user-directed drafting) → adversarial client-counsel red-team + exhaustive cross-reference audit → consolidated fix pass → final full-document coherence read-through (this pass). No open contradictions found. Four items were raised for a floor/threshold/restriction and explicitly declined by the client (§10(d) general-knowledge carve-out, Appendix A §3(a) Buyout-circumvention scope, §12(d) IP-indemnity floor, §5(e) insolvency threshold) — left as-is by direction, not oversight.

**Guide (`CLIENT_GUIDE_HE.md`, 49 pages, v3.0):** closed as a content-architecture refinement (not a rebuild, per client correction) — design system preserved, 10-point reorder/refinement applied, two new chapters (Growth Modes, Project Infrastructure) built from repo-sourced material only, one duplication merged, cross-references fixed, consistency with final Agreement verified. Known open item: a subset of pages lost their original callout-box styling during the build-pipeline fix (now render as plain paragraphs) — functionally correct, not visually polished; flagged rather than silently accepted as final.

**Build pipeline:** fixed and independently verified (round-trip tested) — `CLIENT_GUIDE_HE.md` is now the actual source the Guide renders from.

**Not covered by this session, by design:** no Israeli-qualified-lawyer sign-off (this was never a substitute for one); a handful of template blanks (signatory names/titles, official notice email, e-signature platform) remain for the client to fill per `PARAMETERS_TO_CONFIRM.md`'s administrative items; whether this Agreement, used as a uniform template across all clients, triggers חוק החוזים האחידים review was flagged in that same file and was never resolved — worth one final check with counsel, not something this session can decide.

---

## E. FINAL COMPRESSION & SCOPE AUDIT (post-closure round)

Triggered by a separate client request, after D above: does the Agreement still carry Guide-style material, and can it compress toward ~10 pages? Run as two phases — an analysis-only pass, reviewed by the client before any edit landed.

**Compression finding:** after 8+ rounds of audit/restoration/compression this session, the document is close to its legal floor. Every section was classified against an A–F test (legal-necessary / explain-how-org-operates / duplicated Guide detail / client-fill-in / example-rationale / deal-specific). Result: ~300–500 words of genuinely safe compression found, not the ~19 pages needed to reach 10. The 10-page target was accepted as an optimization hypothesis, not enforced — per explicit client instruction not to weaken protections or force a page count. Realistic floor: ~27–29 pages, because what remains is overwhelmingly locked mechanisms (long *because* precisely drafted: §11(a), §12(a)/(a1), §15(a)/(a1), §2(a)) or provisions recently restored to close a named CRITICAL/HIGH finding (§4(b), Appendix B §2(c)/§3, Appendix C §1(a), Appendix A §1(c)) — moving any of these to the Guide would silently reopen a closed finding.

**Out-of-scope change found and reconciled — §8(a) "קשר מוגן" vs. H-03.** Git-archaeology (not assumption) confirmed: `MASTER_AUDIT_MATRIX.md`'s H-03 (HIGH, Enforceability) flagged this definition's open-ended counterparty-side catch-all ("...גורם עסקי אחר," no geographic/materiality limit) as early as `21d4cc7`, warning of a real risk the *entire clause* could be voided under Israeli proportionality doctrine for restraint-of-trade overbreadth — and recommended narrowing it. H-03 was never addressed by name across ~15 subsequent commits. This session's `ee63abc` consolidation pass then added a symmetric catch-all to the previously-closed org-side prong (for an unrelated, independently valid reason — a client-counsel red-team finding about mutuality) *without* cross-checking it against H-03, making the standing overbreadth concern broader rather than narrower. Reconciled in `433aed9`: removed the org-side catch-all (the named-role list already covers the real population — no protection lost), and made the clause's existing-but-implicit "the org actually exposed/brokered/was materially involved" nexus explicit on both prongs, giving a court an objective, examinable boundary instead of an open-ended one. H-03's other two sub-recommendations — a Buyout-style release mechanism, and a carve-out for when the org itself is the breaching party — are new commercial mechanisms, not narrowing, and were deliberately left as open items rather than decided inside a compression pass.

**Three other out-of-scope-flagged items — reviewed, kept as-is:** §12(a1)'s later-added attribution priority-order/burden-of-proof/closed-engagement refinements (consistent with the H-08 mechanism's own design, not a scope change); §1's "average monthly consideration" rescoping to the breached engagement only (client-favorable, internally consistent with the LD table's proportionality recital); the opening-page governing-state default (resolves to information already on the same page, doesn't silently pick a forum).

**Applied (client-approved, `433aed9`):** §8(a) reconciliation above; §7(a) trimmed (Genesis-description sentence removed — already duplicated in Guide ch.1/ch.4; the good-faith duty, asset-protection duty, and pre-signature Genesis-rights trigger all preserved); Supplementary Understanding appendix now cross-references §15(b) instead of restating it (closes an edit-one-not-both drift risk `MASTER_AUDIT_MATRIX.md` M-09 had flagged); roadmap table's redundant "what activates it" column dropped. Net effect: 29 pages, unchanged — these were targeted, not page-count-driven.

**Guide-consistency check (this round):** confirmed `CLIENT_GUIDE_HE.md` only cross-references §7(a) and §8(a) by pointer, never restates their text — so none of the above required a Guide-side update. Verified directly (grep + read), not assumed.

**Remaining genuine open items, not part of this or any compression pass, flagged for awareness:** `MASTER_AUDIT_MATRIX.md` M-08 (CRITICAL, unresolved) — Appendix D's DPA applicability runs purely on a manual checkbox with no objective statutory-trigger fallback; H-09 (HIGH, unresolved) — §14's arbitration forum for non-Israel clients stays all-Israeli (institution/seat/procedural law) regardless of the client's own jurisdiction, a possible surprising-term risk for a low-bargaining-power foreign client. Both predate this session's compression work and are counsel questions, not drafting ones.

---

## C. Decision points — RESOLVED

**Decision 1 — Incorporation model: Model C, scoped (CONFIRMED by user).**
Guide stays Model A (explanatory-only) as the default. A short, numbered list of Guide passages that today function as "silent Model B" (real operative content, no locked anchor) will be rewritten into precise legal clauses and visually flagged as binding (e.g. boxed "מחייב" callout). First confirmed candidate: Track A/B/C definitions (§B.1 above / Agent 1 Gap #1).

**Decision 2 — Liquidated damages: add an intent/malice gate (CONFIRMED by user).**
§11's floor/multiplier/cap architecture is kept (proportionate, deal-size-linked — superior to the Partner model's flat floor) but will require intent/malice for LD liability to attach at all. Ordinary negligent uncured breach falls back to §11(b)'s actual-damage/disgorgement remedy instead of the schedule. This closes the Guide↔Agreement mismatch (Agent 3's top finding) and the punitive-characterization exposure (Agent 1's proportionality test) in one fix.

These two decisions unblock everything else. Remaining items below are routine execution per the Master Prompt (§46: "do not ask permission for routine tool/subagent/rendering/diagram use") and proceed without separate sign-off:
- Version-freeze mechanism (Item 3): Guide cover version line, Chapter.Section numbering, signature-page version field, envelope-bundling.
- Firewall gap closure (Item 4): lock Track A/B/C definitions (ties into Decision 1), add "Guide sync" process note for numeric drift.
- Hierarchy tie-breaker broadening + explicit Intake-Form-outside-hierarchy statement (Item 5).
- Source reconciliation items (Item 6): 6 Missing clauses, 1 Contradictory cross-ref, 2 Requires-decision — will re-verify each against current file state and apply KEEP/MOVE/REMOVE with recorded reason; flagged back to the user only if a specific clause turns out to be a genuine substantive judgment call rather than a mechanical fix.
- Guide Ch.1 duplicate-table merge, citation-error fix, promise-leak softening (Item 7).
- Guide 14-step narrative reorder, Genesis relocation, protections moved later, growth-modes + project-infrastructure sections added (Item 8).
- Fixing the `build_html_guide.py`/`.md` desync bug first, before further Guide content edits, so edits aren't applied twice.
