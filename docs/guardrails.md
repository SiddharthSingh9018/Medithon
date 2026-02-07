# Follow-Up: System Guardrails, Confidence, and Interpretation

This section clarifies how the system outputs should be interpreted, what they can and cannot claim, and how decision-makers should responsibly act on the signals produced.

## 1. What This System Can and Cannot Tell You

This system models public perception, not pharmacological truth.

### What the system can tell you

- How belief around a drug is forming, stabilizing, or collapsing
- Whether discussion is driven by fear, doubt, trust, or disappointment
- Which symptoms are most commonly associated with a drug in discourse
- Whether expectation and placebo alignment appear intact or broken
- When narratives shift faster than historical patterns suggest

### What the system cannot tell you

- Whether a drug actually causes side effects
- Whether a drug is clinically effective or unsafe
- Whether reported symptoms are medically valid
- Whether outcomes are causally linked to the drug
- Whether intervention is medically required

The system is explicitly not a diagnostic tool and not a replacement for pharmacovigilance, trials, or regulatory review. It is an early-warning perception monitor.

## 2. Confidence and Uncertainty Framing

All perception signals are treated as directional indicators, not absolute truths.

Each aggregated signal is interpreted alongside confidence context derived from:

- Support Volume: How many independent mentions contribute to the signal
- Persistence Over Time: Whether the signal appears consistently across multiple time windows or collapses quickly
- Source Diversity: Whether the signal is driven by many distinct users or a small, repeated subset

Signals with low volume, low persistence, or low source diversity are treated as weak or exploratory, not actionable alerts.

## 3. Baseline Definition (What Change Means)

In this system, a perception shift is never evaluated in isolation.

All changes are interpreted relative to explicit baselines:

- Historical Baseline (Drug-Level): Compared against the drug's own historical belief profile
- Category Baseline (Peer-Level): Compared against similar drugs in the same therapeutic category
- Platform Baseline (Channel-Level): Normalized against typical discourse behavior on each platform

Alerts are raised only when perception deviates meaningfully from one or more baselines, indicating a structural belief shift rather than transient noise.

## 4. Adversarial and Manipulation Awareness

The system assumes public discourse may include coordinated misinformation, astroturfed narratives, or targeted brand attacks.

Sudden perception shifts with low source diversity, high repetition, and rapid onset without historical precedent are flagged as potentially coordinated narratives rather than organic belief change.

The system does not attempt attribution. It only surfaces anomalous belief dynamics for human review.

## 5. Human-in-the-Loop Action Mapping

This system does not automate decisions. It supports human judgment.

Typical interpretation pathways include:

- Legitimacy or trust collapse: Communication and public education review
- Dosage confusion narratives: Labeling clarity or awareness campaigns
- Perceived side-effect panic: Pharmacovigilance cross-check
- Expectation or placebo failure signals: Market fit and messaging reassessment

The system role ends at signal surfacing, not intervention execution.

## 6. Ethical and Design Guardrails

To ensure responsible use, the system enforces:

- Aggregate-only analysis
- No user profiling or identity inference
- No medical or safety claims
- Clear disclosure of limitations in UI and API
- Strict separation of evidence, context, and interpretation layers

These guardrails are design decisions, not afterthoughts.

## Final Clarification (One Line)

This system does not ask whether a medicine works. It asks how people believe it works, and whether that belief is changing in ways that matter.
