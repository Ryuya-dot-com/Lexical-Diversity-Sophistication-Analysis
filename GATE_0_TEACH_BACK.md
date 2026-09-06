# Gate 0 construct teach-back protocol

- Protocol version: 1.2.5
- Status: optional check deferred until after Gate 1; local human-use
  authorization would still be required
- Purpose: construct-clarity gate, not app usability or validity evidence
- Participant packet: [version 1.1.0](GATE_0_TEACH_BACK_PARTICIPANT.md)

## What this optional check can establish

This check asks whether two independent intended readers can explain the frozen
project claim after reading its English plain-language summary. It can expose
ambiguous project wording. It cannot establish construct validity, usability,
population interpretability, participant knowledge, or a reading effect.

The English task tests the RMAL-facing explanation, not the Japanese Web-app
interface. A Japanese translation would be a new instrument version and its
responses must not be pooled silently with the English task. App-interface
interpretation belongs to Gate 2.

## Internal claim-to-implementation audit

Completed against `ROADMAP.md`, `README.md`, `index.html`,
`mwe_contract.json`, and the tested export contract on 2026-09-01.

| Claim in the participant packet | Repository truth | Preflight decision |
|---|---|---|
| List-to-text output is reference-conditioned, not learner knowledge | The app reports named TUBELEX, NGSL, or local BNC/COCA token/type profiles with separate boundaries | Consistent |
| Source-to-target recurrence is not participant knowledge | No source-to-target profile is implemented; it is optional in the roadmap | Retain as a conceptual distinction, not a current app capability |
| `P_word` and `P_mwe_sense` are tested person-to-text quantities | Neither is implemented by the app; external study code must join participant evidence to the text map | Consistent; future study quantity only |
| The app supports human MWE occurrence, idiomaticity, and contextual-sense review | Candidate decisions and `take in` OEWN sense review exist; automatic truth and general WSD do not | Consistent only for the bounded current scope |
| Word and MWE channels are not combined | The contract and UI keep denominators separate and implement no combined score | Consistent |
| 95%/98% are interpretive reference points, not guarantees | The app makes no comprehension or replacement-threshold calculation | Consistent |
| Named document sets can be resumed locally | Implemented and contract-tested; the stale `not_implemented` entry was removed before this audit | Consistent |

No contradiction requiring a participant-packet change remains. This is a
document/contract audit, not real-browser acceptance.

The separate `ANNOTATION_GUIDE.md` version 0.5 now maps every current contract
state, the synthetic M1–M5 fixture, occurrence/span/category training cases,
hard cases, idiomaticity, and contextual-sense decisions without relying on the
UI. `ANNOTATOR_TRAINING.md` separately freezes a synthetic-only staged training
and task-specific qualification protocol. Neither protocol has been authorized
or administered, so neither supplies qualification, agreement, or evidence that
the annotation guide can be applied independently. This Gate 0 packet tests only
understanding of the project claim.

## Governance route

The smallest defensible route is to treat Gate 0 as **formative internal design
feedback only**. Retain the gate decision and wording changes, but do not quote
the responses, analyze them as manuscript data, or present the two people as a
user sample. The later Gate 2 intended-user study—not this check—should supply
ethics-approved response-process and usability evidence.

This route is a project recommendation, not an ethics or legal determination.
BAAL's 2021 good-practice guide supplements rather than replaces local
institutional and funder rules. Current Japanese Personal Information
Protection Commission guidance applies duties to academic-research handling and
does not make an academic purpose a general exemption from appropriate
safeguards. JSPS guidance likewise treats identifiable human information in the
humanities and social sciences as requiring advance attention to consent,
purpose, disclosure, and safe management. The responsible researcher must
therefore obtain the applicable local determination before contact.

## Human-use prerequisites

Do not send the participant packet until every item below has a dated record.

- [x] Participant-facing text and decision key are separate files.
- [x] Task language and the construct it tests are explicit.
- [x] A transfer question checks a new MWE case rather than verbatim recall
  alone.
- [x] Current app capabilities and absent study quantities have been audited.
- [x] Discipline-level and current Japanese public guidance have been reviewed;
  neither substitutes for the responsible institution's decision.
- [ ] The responsible researcher has recorded the applicable institutional
  ethics/consent determination.
- [ ] The responsible researcher has fixed the response storage location,
  access, retention period, withdrawal point, and deletion procedure.
- [ ] The responsible researcher has confirmed non-coercive recruitment and
  the two eligibility decisions below.

The three open items require local authority and cannot be completed by the
software agent. Until then, the optional check is not ready for human
administration. It does not block desk-based material admission.

Record the decision here before changing the status above:

- Intended use: `formative internal feedback only` or `reportable research`
- Institution/unit and applicable policy:
- Determination type, reference, decision-maker, and date:
- Approved information/consent procedure:
- Approved storage service and data location:
- People with access:
- Retention trigger/date and deletion method:
- Withdrawal deadline and contact route:
- `GRAD-01` eligibility and absence of assessment dependency confirmed by/date:
- `RESEARCHER-01` eligibility confirmed by/date:
- Responsible researcher and authorization date:

If `reportable research` is selected, stop and obtain approval for the complete
protocol, instruments, recruitment, consent, data plan, and dissemination before
contact. Do not reuse the internal-feedback shortcut.

## Eligibility and administration

Use the same participant packet with:

- `GRAD-01`: one beginning applied-linguistics graduate student, able to read an
  English research summary, with no project role and no assessment dependency
  on the researcher; and
- `RESEARCHER-01`: one researcher who conducts L2 vocabulary research, can read
  an English research summary, and has no project role.

Participation must be voluntary. Give each respondent only the participant
packet; do not show the app, repository, protocol, decision key, or the other
response. Do not explain terms or answer questions during the task. Record only
the respondent code, eligibility decision, instrument version, date, response,
and optional completion time. Do not collect names or unnecessary demographics.

If treated as internal design feedback, do not later relabel the responses as
research data. If responses may be quoted, analyzed as reportable evidence, or
retained for publication, obtain the applicable determination and consent
before collection. Two responses are never population evidence.

Git ignore is not privacy protection. This repository is inside a Dropbox-synced
workspace, so do not store responses anywhere under it—including the ignored
`research_data/` directory—unless the institutional plan explicitly approves
that account, provider, location, access, and retention. The default is a
restricted institution-managed location outside both Git and this workspace.
Treat respondent codes, roles, and free-text answers as potentially identifiable
rather than anonymous; keep any contact-to-code link separately if one is
needed. Do not create or retain human-response files until the plan exists.

## Draft invitation — requires local approval

> I am requesting voluntary feedback on whether a short English description of
> a research idea is clear. This is not a test of you, and participation or
> refusal will have no effect on assessment, supervision, employment, or future
> opportunities. Please do not include your name or personal details. Your
> response will be handled according to the attached approved data notice. You
> may stop or request withdrawal until [approved deadline] by contacting
> [responsible researcher/contact]. Estimated time: [tested estimate].

Replace every bracketed field and attach the approved information/consent text
before use. Do not promise anonymity when the project team may infer identity
from recruitment, role, or writing.

## Frozen decision key — do not show respondents

Rate each domain `clear`, `incomplete`, or `critical misunderstanding`. Do not
calculate a total score and do not rescue an answer by inferring knowledge that
the respondent did not express.

| Domain | `clear` requires | `critical misunderstanding` includes |
|---|---|---|
| Construct and unit | Separates individual word tokens from contextual MWE occurrences and transfers the problem to the new example | Says every MWE must count as one/three unknown words, or treats component knowledge as contextual MWE knowledge |
| Three profiles | Distinguishes list membership, directional corpus recurrence, and tested participant knowledge | Treats list/corpus occurrence as participant learning, knowledge, or comprehension |
| Denominators and unresolved evidence | Identifies eligible word tokens for `P_word`, eligible confirmed MWE occurrences for `P_mwe_sense`, and retains unresolved evidence | Uses the same denominator for both or treats unresolved as known/absent without a rule |
| 95%/98% status | Calls them word-coverage reference points whose relationship with comprehension must be tested | Calls either value a universal comprehension guarantee or the project's new cutoff |
| App/study boundary | Assigns text mapping and human review/export to the app and participant knowledge/comprehension to separate study procedures | Says the app measures learner knowledge, comprehension, proficiency, or automatic MWE truth |
| Evidence ceiling | Rejects a combined score and replacement threshold without independent criterion evidence | Claims that the current prototype already validates a combined score, reading effect, or universal threshold |

If the optional check is run, it passes only when both respondents are `clear`
in all six domains without oral coaching. Any `incomplete` or `critical
misunderstanding` requires identifying the wording that allowed the failure,
revising once, and using new independent respondents. Revise the explanation,
not the decision key, unless the construct itself is explicitly changed and
versioned.

## Response-process memo template

Keep the completed memo separate so the participant packet remains frozen.

- Protocol, instrument version, and Git commit:
- Administration dates and mode:
- Ethics/consent determination:
- Storage, retention, withdrawal, and deletion record:
- Respondent eligibility: `GRAD-01`; `RESEARCHER-01`
- Domain ratings and response evidence:
- Critical or incomplete interpretations:
- Wording revision, if any:
- New-respondent rerun, if required:
- Gate decision: `pass` or `remain open`
- Decision date and responsible researcher:

Do not report an agreement coefficient, usability rate, or population estimate
from this two-person gate. Those require the later intended-user study.

## Governance references

- [BAAL Recommendations on Good Practice in Applied Linguistics
  (2021)](https://www.baal.org.uk/wp-content/uploads/2021/03/BAAL-Good-Practice-Guidelines-2021.pdf)
- [Japan Personal Information Protection Commission: general APPI
  guidelines](https://www.ppc.go.jp/personalinfo/legal/guidelines_tsusoku/)
- [JSPS, *For the Sound Development of Science*: human subjects and personal
  information](https://www.jsps.go.jp/file/storage/e-kousei/data/rinri_e.pdf)
