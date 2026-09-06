# Research and data governance

Status: current no-human work may proceed; conditional human-work controls,
2026-09-05

This policy separates work that uses no human research data from work that
recruits people or reuses participant-level records. It does not treat every
human-produced artifact as human-participant research. The applicable route
must be resolved before a human-facing study begins.

## Current operating boundary

Static development, public-source preparation, sampling design, and synthetic
platform checks may proceed. They are not subject to the later human-work gate.

The following work may continue without waiting for a human-study decision:

- static, browser-local software development with project-authored fixtures;
- source and rights research using public metadata;
- target-blind acquisition, verification, and preprocessing of lawfully reusable
  public text; and
- project-team desk work used only to design the protocol, provided it is not
  reported as independent human evidence or a validated gold benchmark.

The following human-facing research is on hold until the applicable review or
approval route covers the exact plan:

- studying annotators' timing, background, experience, comments, behaviour, or
  person-level performance rather than only acquiring their annotation work;
- intended-user, usability, interview, questionnaire, think-aloud, teaching, or
  classroom evaluation;
- collecting names, contact details, demographics, language background,
  performance, free-text feedback, IP addresses, or device identifiers for a
  study; and
- participant-level secondary analysis, including any future TECO outcome
  join, unless its consent, access terms, and institutional classification have
  been reviewed separately.

No held activity may be described as exempt or outside review merely because it
is low risk, conducted online, uses adults, or studies language rather than
health.

Independent production annotation is a separate boundary. If annotators are
engaged as workers, contractors, or research collaborators and only the
delivered labels are analyzed, do not presume that they are research
participants. Before engagement, document the relationship, fair payment,
confidentiality, label/publication rights, authorship or acknowledgement where
applicable, account security, access, retention, and deletion. Use the human-
research route only if the project studies people, the arrangement includes
participant responses, or the responsible unit places it in that scope.

## Data classes and locations

| Class | Examples | Storage and release rule |
|---|---|---|
| Public project material | Code, synthetic fixtures, protocols, rights metadata | May enter Git and GitHub Pages after the normal license and release checks. |
| Public benchmark material | Admitted Wikipedia text, attribution, standoff labels | May be released only after the source, page-level rights, annotation, and CC BY-SA gates pass. |
| Restricted or uncleared person-linked records | Identifiable or linkable per-annotator labels, timestamps, errors, task logs, demographics, comments, agreement/consent state | Store only in a managed restricted location. Never put them in Git, GitHub Pages, an API response, or this Dropbox workspace unless that exact release and location are authorized. |
| Direct identifiers and administration | Names, email addresses, work agreements or consent forms, payment and bank records | Keep apart from analytic records with access limited to the responsible PI or administrator. Never publish. |
| Linkage and security data | Participant-to-study-ID key, withdrawal ledger, incident record | Keep separately from research data, encrypt where institutionally supported, and limit access to the named data custodian. |

The public app does not send textarea content, MWE patterns, labels, or exported
workspaces to a project server. GitHub Pages or another host may process ordinary
request metadata under its own terms, but the app must not add analytics,
telemetry, content logging, remote models, or third-party form collection
without a new privacy/data-governance review and, if used for research about
people, the applicable ethics review.

## Minimum human-study controls

Before recruitment, the study-specific record must name the responsible PI,
institutional unit, determination or approval identifier, approved protocol
version, recruitment population, inclusion and exclusion rules, consent route,
withdrawal deadline, burden, compensation, collected fields, storage location,
access list, retention period, destruction method, release fields, and incident
contact. Unknown values do not receive defaults.

Collect the minimum fields needed for the prespecified question. Use random
study IDs in analytic files. Keep identity, consent, and payment records outside
the analytic dataset. Free text is potentially identifying and must be reviewed
before quotation or release. Pseudonymization is not the same as irreversible
anonymization.

Withdrawal remains possible on the terms stated in the approved information
sheet. The sheet must state the last point at which linked records can be
removed; the project must not promise deletion after irreversible aggregation
or lawful public release if it cannot perform it.

## Annotation and release boundary

Project-team pilot decisions may improve the guide but cannot become the
independent test set. Production annotators must label independently before
adjudication and must not see model suggestions or sealed-test outcomes.
Whether their per-annotator labels may be published is decided by the applicable
work agreement or consent and release plan, not by the source-text license.

The public benchmark release must remove direct identifiers and unapproved
person-level metadata. Aggregate agreement statistics may be released after the
work/consent basis and disclosure-risk checks pass. Copyright permission, work-
product rights, open-source licensing, informed consent where applicable, and
ethics approval where applicable are separate gates; passing one does not pass
the others.

## Incidents and changes

Stop the affected processing after unauthorized disclosure, lost credentials,
unexpected collection, consent mismatch, re-identification risk, or use outside
the approved purpose. Preserve the minimum incident record, notify the PI and
the applicable institutional contact, and follow their reporting instructions.

A change to population, incentives, collected fields, task burden, logging,
platform, storage, sharing, or analysis purpose requires review before use. A
later approval cannot retroactively authorize already completed recruitment or
data collection.

## Current authority check

If a planned activity is a survey or experiment involving humans administered
by Tohoku University's Graduate School of International Cultural Studies, its
current official materials require the departmental preliminary checklist and
state that a required ethical review must be completed in advance. Within that
scope, any Step 2 `yes` routes the activity to possible review. The existence of
a service account, operational log, or payment for work does not by itself
establish that the activity is a human-participant study. The current research-
cooperation standard is approximately JPY 1,000 per hour when that participant
route applies. The PI must confirm the applicable unit and work relationship.

The current pre-submission checklist also requires exact access holders,
storage locations and methods, external-platform personal-information handling,
and a non-vague retention period. The university-wide research-integrity page
states ten years for materials supporting a publication but delegates concrete
storage rules to the unit. The project therefore classifies raw per-annotator
exports, platform logs, and backups separately from identity, work-agreement or
consent, account, and payment records and seeks unit guidance where retention
obligations are unclear; it does not apply one automatic period to every class.

Official sources:

- <https://www.intcul.tohoku.ac.jp/ja/research_screening>
- <https://www.intcul.tohoku.ac.jp/word/reaserch/J-2_Preliminary_Checklist_for_Ethical_Review.docx>
- <https://www.intcul.tohoku.ac.jp/pdf/reaserch/J-1_Flowchart_for_Ethical_Review.pdf>
- <https://www.intcul.tohoku.ac.jp/pdf/reaserch/gsics_human_ethics_guidelines.pdf>
- <https://www.intcul.tohoku.ac.jp/pdf/reaserch/J-0_Procedures_for_Submitting_an_Application_for_Ethical_Review_03.pdf>
- <https://www.intcul.tohoku.ac.jp/pdf/reaserch/J-5_Pre-submission_Checklist_ja_v2.pdf>
- <https://www.intcul.tohoku.ac.jp/pdf/reaserch/Standard_Rate_for_Research_Collaboration_Fees_ja.pdf>
- <https://www.tohoku.ac.jp/japanese/newimg/newsimg/news20220104_05_guide.pdf>
- <https://www.bureau.tohoku.ac.jp/kenkyo/fb/rules.html>
- <https://www.ppc.go.jp/personalinfo/legal/guidelines_anonymous/>
