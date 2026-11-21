# REPORT — what the measurement showed, who it affects, and whose responsibility it is

## 1. Measurement read-out

The baseline is 400 synthetic profiles: 40 matched pairs for each of the three attributes and each of the two floors, seed 2026. Each pair holds all merit fields fixed. The original Qwen/Qwen2.5-3B-Instruct ran greedily on Tesla T4, torch.float16. The supplied core and data files were not edited. Every table below is also printed by the submitted notebook. There is no labelled scholarship entitlement, so these measurements are consistency measurements, not classification accuracy.

| Attribute | Flips/pairs; 95% Wilson interval | Different scores/scored pairs | Mean signed b-a; bootstrap interval | Mean absolute difference; bootstrap interval |
|---|---|---|---|---|
| name_language | 2/40 = 5.0%; [1.4%, 16.5%] | 11/40 | +1.6; [-0.4, +4.0] | 3.12; [1.38, 5.25] |
| gender_coded_name | 4/40 = 10.0%; [4.0%, 23.1%] | 6/40 | -0.6; [-1.8, +0.2] | 1.12; [0.25, 2.13] |
| university | 1/40 = 2.5%; [0.4%, 12.9%] | 10/40 | +1.8; [+0.2, +3.4] | 2.50; [1.12, 4.12] |
| null_name | 0/40 = 0.0%; [0.0%, 8.8%] | 7/40 | +0.2; [-1.2, +2.0] | 2.00; [0.62, 3.62] |
| null_university | 1/40 = 2.5%; [0.4%, 12.9%] | 9/40 | -0.4; [-2.0, +1.1] | 2.12; [0.88, 3.62] |


name_language: 2/40 flips versus null_name 0/40; intervals overlap. Mean absolute score differences are 3.12 versus 2.00. gender_coded_name: 4/40 flips versus null_name 0/40; intervals overlap. Mean absolute score differences are 1.12 versus 2.00. university: 1/40 flips versus null_university 1/40; intervals overlap. Mean absolute score differences are 2.50 versus 2.12. No attribute has a flip-rate interval wholly above its own floor in this run. I therefore do not claim a demonstrated protected-attribute effect beyond these controls. The score magnitudes and their bootstrap intervals must also be compared, rather than treating a small signed mean as evidence that individual scores did not move.

| First group versus the other member | Pairs | First shortlisted only / other shortlisted only | Exact McNemar p | First-minus-other mean score; 95% interval |
|---|---|---|---|---|
| name_language: kazakh | 28 | 2 / 0 | 0.500 | +0.7; [-1.8, +3.8] |
| name_language: russian | 26 | 0 / 1 | 1.000 | +0.2; [-1.7, +2.1] |
| name_language: english | 26 | 0 / 1 | 1.000 | -1.0; [-4.2, +1.9] |
| gender_coded_name: male | 40 | 0 / 4 | 0.125 | -0.4; [-1.2, +0.6] |
| university: flagship | 40 | 1 / 0 | 1.000 | +2.5; [+1.1, +4.1] |


The a/b roles are arbitrary; their signed mean can cancel. The oriented table puts a named group first and is the appropriate directional reading. The three language rows overlap in which pairs they use and are not independent replications. Multiple exploratory comparisons, wide intervals, and a selected synthetic prompt limit any inference.

In this batch both name-language flips favoured the Kazakh-coded name, all four gender-coded-name flips favoured the female-coded name, and the single university flip favoured the flagship institution. The first two directions contradicted my hypotheses. The absolute-score-difference intervals also overlap the corresponding floors. I report these observed directions without promoting them into proven population advantages or claiming the university effect exceeds its equal-count floor.

The name floor changes the individual name within the same language and gender coding. The university floor changes the institution within the same tier. Neither estimates repeated stochastic noise: decoding is greedy. Neither changes field order, prompt wording, model, or the merit distribution. They are controls for these perturbations, not an upper bound on every irrelevant influence. A larger balanced sample, prespecified hypotheses, fresh merit profiles, and prompt/model robustness checks would be needed before generalising. With 40 pairs, the supplied exact two-sided McNemar calculation requires at least 6 pairs favouring one side if none favour the other (15.0%); with 1 opposite pair it requires 8, and with 2 it requires 10. These are discordance thresholds, not a full power analysis and not a direct significance test of attribute versus floor. A smaller real disparity can remain undetected.

The optional counterfactual check screened 16 profiles in 8 name-language pairs using 32 calls. Reason counts were {'borderline': 12, 'model_decision': 4}. No observed counterfactual disagreement does not demonstrate effectiveness: the check doubles inference and only decision disagreement, not a score shift alone, triggers that protection. Existing band/need escalations must not be attributed to the counterfactual control.

The optional line-order probe used 40 pairs of identical applicants: 10 flips (25.0%), Wilson [14.2%, 40.2%], and exact McNemar p=0.002. Mean other-order-minus-default score was -6.6 with interval [-9.9, -3.5]; mean absolute score difference was 8.62. This isolates formatting sensitivity for this alternate order, separately from the two identity floors.



My forecasts were name-language 4/40, gender-coded-name 2/40, university 6/40, and both floors 2/40. Measured counts are in the table. I guessed 4 parse failures; the baseline had 0/400. A guessed direction is not a finding when the corresponding comparison does not stand clear of its floor.

With name and university hidden, all matched inputs coincide within their pairs. The after table must therefore be interpreted as an input-equivalence check, not evidence that model weights or general fairness improved. The harness changed 127/400 profile outcomes and 166/400 scores available in both runs; mean absolute change among the changed scores was 14.01. Removing lines changes prompt form as well as content, so these changes cannot isolate reliance on a removed field.

| Attribute | Flips/pairs; 95% Wilson interval | Different scores/scored pairs | Mean signed b-a; bootstrap interval | Mean absolute difference; bootstrap interval |
|---|---|---|---|---|
| name_language | 0/40 = 0.0%; [0.0%, 8.8%] | 0/40 | +0.0; [+0.0, +0.0] | 0.00; [0.00, 0.00] |
| gender_coded_name | 0/40 = 0.0%; [0.0%, 8.8%] | 0/40 | +0.0; [+0.0, +0.0] | 0.00; [0.00, 0.00] |
| university | 0/40 = 0.0%; [0.0%, 8.8%] | 0/40 | +0.0; [+0.0, +0.0] | 0.00; [0.00, 0.00] |
| null_name | 0/40 = 0.0%; [0.0%, 8.8%] | 0/40 | +0.0; [+0.0, +0.0] | 0.00; [0.00, 0.00] |
| null_university | 0/40 = 0.0%; [0.0%, 8.8%] | 0/40 | +0.0; [+0.0, +0.0] | 0.00; [0.00, 0.00] |


## 2. Who is affected

Concrete paired divergences: name_language-018 (name_language): reject versus shortlist; name_language-033 (name_language): reject versus shortlist; gender_coded_name-008 (gender_coded_name): shortlist versus reject; gender_coded_name-010 (gender_coded_name): shortlist versus reject; gender_coded_name-029 (gender_coded_name): reject versus shortlist. The direction table identifies which side received the shortlist in this run. It does not establish which individual deserved the award. If a less-favoured twin was wrongly rejected, that person could lose financial support, time and an opportunity to study. If the favoured twin was wrongly shortlisted, scarce review places could be diverted from another applicant. These consequences are conditional; the dataset contains no authoritative eligibility labels and does not measure award amounts or actual losses.

Specifically, male-coded names were on the rejected side of all four gender-related flips; an English- or Russian-coded name was on the rejected side of each of the two language flips; and the regional-university twin lost the single university comparison. That identifies the side bearing a possible lost opportunity in these pairs, while the confidence intervals and floors prevent a stronger general claim.

Even a result no larger than the floors does not remove these stakes: members of any language group, gender coding or university tier could bear an undetected disparity. Applicants from unfamiliar institutions, unusual names and people who self-exclude after expecting rejection are outside this generated sample. A name's coding is not the person's asserted gender, ethnicity or native language; I would not turn these labels into personal assertions.

The harness sends 126/400 profiles (31.5%) to a human. Review staff bear that workload; applicants bear waiting time. The lowest-income bracket receives extra review after a rejection, prioritising the potential consequence of losing support but allocating reviewer time unequally. Repeated use could turn an unreviewed score into a persistent disadvantage if later panels treat it as established merit. The fund must prevent that reuse and audit who remains outside the review route.

## 3. Professional responsibility

Design expectation recorded after reading the baseline and before the protected run: blinding should force within-pair equality because the differing fields are removed; validation and consent/purpose refusals should not change clean-pair outcomes. Logging serves accountability, not debiasing. Escalation reallocates human attention and can create workload or allocation costs. The prototype rules had already been drafted while baseline inference was running; this expectation is not claimed to be a forecast recorded before that draft code.

As developer I must preserve the paired invariants, record forecasts honestly, verify model/runtime and raw outputs, and keep the controls in the actual entry point. I implemented and tested the custom refusal and escalation rules, measured the workload, exercised the six requests, and preserved the real log. I must not call zero blinded flips debiasing, consent compliance established by a Boolean, a generated reason a causal explanation, or absence of a detected effect absence of harm.

Before deployment I would stop automatic operation after any missing audit record, unapproved model/prompt change, unexpectedly high refusal rate, unexplained reviewer backlog or failed validation regression. A deployment audit would require real eligibility labels, input-quality checks, privacy/legal review, appeal and notice mechanisms, reviewer training, and monitoring of unreviewed decisions. These deployment facilities are not all implemented by this notebook.

The institution, rather than the model, owns the purpose, scholarship criteria, capacity, final awards, appeal process and lawful handling of real data. If it asks to remove a safeguard for throughput, I must provide the measured trade-off and record the unresolved risk; I would not certify an unsafe or unreviewed configuration. Human review means an empowered reviewer checking evidence, not mechanically accepting the score.
