# Ethics determination record

Record date: 2026-09-05  
Roadmap task: IR-115  
Internal control status: conditional before human-facing research  
Current no-human development/publication-preparation phase: proceed  
Future human-research determination: not yet applicable

## Determination

The Web app, public-source preparation, and present repository work do not
involve human participants. Static browser-local development, synthetic
fixtures, rights review, target-blind Wikipedia preparation, sampling design,
and synthetic platform checks may proceed without an ethics decision.

Human production of an annotation artifact is not automatically research on
the annotator. If adults are engaged as paid workers, contractors, or research
collaborators and the project studies only the delivered labels—not their
traits, behaviour, experience, or performance as people—the immediate controls
are a lawful work arrangement, fair payment, confidentiality, intellectual-
property terms, and secure data handling. An ethics application is not presumed
for that route.

IR-115 therefore is not a present P0 blocker. It becomes active before a study
collects or analyses person-level responses, timing, background, usability,
interviews, or other evidence about people, or if the applicable institution
classifies the proposed annotation arrangement as a human-participant survey or
experiment. Intended-user research remains the clearest later ethics trigger.

## Workstream decisions

| Workstream | Present state | Required next evidence |
|---|---|---|
| Browser-local application and automated tests | Proceed | Keep network-content collection and telemetry absent. |
| Wikipedia source identity, rights review, sampling design, and preprocessing | Proceed | Complete source and page-level rights gates; do not inspect targets before the sampling frame is frozen. |
| Project-team protocol examples and desk pilots | Proceed with claim limit | Do not count them as independent gold, user evidence, or a sealed test. |
| Independent production annotation | Later work-management gate | Before engagement, fix whether annotators are workers, contractors, collaborators, or participants; document payment, confidentiality, label-release rights, account security, and data retention. Seek an ethics determination only if the arrangement is human-participant research or remains genuinely unclear under the applicable unit's rules. |
| Intended-user or usability study | Hold | Before recruitment, use the applicable institutional route for task performance, timing, errors, comments, interviews, questionnaires, or recordings. |
| Existing participant-level data such as TECO | Dormant and separate | A downstream hypothesis, source/stimulus rights, consent or secondary-use terms, participant-data assessment, and institutional classification. It is not part of the first paper. |

## Proposed annotation work arrangement

This is the minimum current plan for later independent annotation. It does not
start recruitment, authorize expenditure, or classify a person as a research
participant.

| Element | Proposed plan or unresolved decision |
|---|---|
| Purpose | Create and evaluate an independently annotated English VPC/VID benchmark; annotator traits are not a research outcome. |
| People | Two or more adults complete first-pass annotation independently. The PI must choose and document a worker, contractor, collaborator, or participant route before engagement. Recruitment source and any relationship to the PI remain unresolved. |
| Material | Rights-cleared public English text for production and project-authored synthetic text for training and qualification. No participant-authored prose is a benchmark stimulus. |
| Analytic annotation records | Pseudonymous annotator ID; occurrence, span, category, idiomaticity, inventory, sense, uncertainty, and note decisions; qualification counts, critical errors, retry, and outcome; adjudication history; and aggregate agreement. No research timer is planned. |
| Administrative records | Name/contact detail, account identity, consent or work agreement, and payment record only where institutionally required. Keep these outside the analytic dataset and outside this repository. |
| Data not requested for research | Date of birth, sex/gender, nationality, ethnicity, health/disability, home address, voice/video, device identifier, IP address, and free-form biography. If the host records network/device metadata operationally, IT must identify it before use and keep it out of analysis. |
| Platform | A locally or institutionally managed INCEpTION instance is provisional. The public GitHub Pages app remains browser-local and receives no annotation or person-level data. |
| Platform records needing governance | Account directory, per-user source documents and labels, project log, application/server access logs, exports, backups, administrator access, and deletion/restoration copies. Exact automatic fields, server location, and backup chain are unknown until the host completes an inventory. |
| Publication default | Release adjudicated benchmark labels and aggregate agreement only. Do not release the identity key, account names, contact/payment/agreement records, raw server logs, or free-text administrative correspondence. Per-annotator labels require an explicit work/consent and disclosure-risk basis. |

The planned data flow is: rights-cleared or synthetic material enters the
managed instance; the host keeps account identity separately from analytic IDs;
each first-pass export and the project backup/log enter a restricted
store; the local converter produces pseudonymous analytic records; and only the
release-approved projection may enter Git, GitHub Pages, an API response, or a
public repository. Raw platform exports remain restricted because they may
contain source text and account metadata even when the analytic projection does
not.

## Basis for the conditional gate

The current Tohoku University Graduate School of International Cultural Studies
materials govern surveys and experiments involving humans. For an activity in
that scope, their preliminary checklist routes any Step 2 `yes` to possible
review, and the application procedure rejects retrospective review after the
survey or experiment. The checklist is not evidence that every service account,
payment record, or human-produced research artifact is itself a human study.

The classification question comes first: is the project studying people or
procuring expert annotation work? If it is a human-participant study, apply the
checklist before it begins. If it is an annotation work/collaboration route,
apply employment/procurement, fair-payment, privacy, security, authorship or
acknowledgement, and label-redistribution rules. Data management applies to
both; ethics review does not automatically apply to both.

## Conditional preliminary-checklist map

Use this map only if the proposed activity is classified as a survey or
experiment involving humans. It follows the current GSICS 14-question
preliminary checklist but does not replace the official form.

| Question | Current answer for the proposed route | Basis or action before submission |
|---|---|---|
| Step 1.1, teaching-method exercise | No | This is a publication-oriented research project, not a class exercise. |
| Step 1.2, university administration improvement | No | The project does not evaluate university operations. |
| 3, purpose concealed in advance | No | Explain benchmark creation, analysis, release, and withdrawal before work begins. |
| 4, no written consent | No, if classified as participant research | Use the approved written/electronic route; if classified as employment or collaboration, use the institutionally required agreement instead. |
| 5, cannot stop partway | No | Permit stopping without penalty and state the last technically possible record-removal point. |
| 6, possible disadvantage from information supplied | No anticipated; office to confirm | Collect no personal opinion or sensitive trait and publish no identifiable person-level result. |
| 7, possible mental or physical harm/distress | No anticipated; office to confirm | The task is ordinary text annotation, but burden, breaks, and maximum session length must be fixed before submission. |
| 8, asks personal information | No for the current analytic plan | No personal attribute is requested for research. Account/contact/payment administration is kept outside the analytic dataset; answer Yes if the later study itself asks for personal information. |
| 9, may collect identifying information | Depends on the later study and host | Minimize or disable identifiable operational logs and inventory unavoidable fields. Their existence is a security/privacy issue and does not by itself turn annotation work into a human study. |
| 10, power or family relationship | Pending recruitment route | Exclude relatives. If students, employees, supervisees, or project members are recruited, answer Yes and document anti-coercion controls. |
| 11, honorarium or financial inducement | Yes if the activity is a paid participant study | The current GSICS participant-cooperation standard is approximately JPY 1,000 per hour. Wages or contractor fees instead follow the applicable employment/procurement route and do not by themselves classify the work as a study. |
| 12, participants with disabilities | No as a selection criterion | Do not screen for disability; make the task accessible and seek an amendment if a protocol-specific issue arises. |
| 13, participants under 18 | No | Recruit adults only for this protocol. |
| 14, external ethics requirement/recommendation | No automatic Yes | The intended journal requires ethics and consent disclosures when applicable; it does not require ethics approval merely because a resource contains human-produced annotations. |

Do not submit an ethics application merely because the annotation platform has
accounts, logs, or payments. First freeze the work arrangement and intended
analysis. Submit the official checklist before recruitment only if the activity
is a human-participant survey/experiment or the responsible unit advises that
the boundary remains within its review remit.

## Data-management decisions before multi-user annotation

The project must record concrete values, using institutional or IT approval
where required, for:

- the server owner, physical/cloud region, responsible administrator, account
  authentication, transport and at-rest protection, patching, incident contact,
  and any vendor or subprocessor;
- the exact application, proxy, access, database, and backup log fields,
  especially username, IP address, user agent, timestamps, and deletion copies;
- the restricted store, access list, backup/restoration path, export route, and
  separation of identity/payment records from labels;
- the withdrawal deadline and which live, exported, backed-up, adjudicated,
  aggregated, or already released copies can still be deleted;
- the retention clock for raw annotations, qualification evidence, audit logs,
  consent, identity linkage, and payment records; and
- whether per-annotator labels may be publicly released, provided under
  controlled access, or withheld while adjudicated labels and aggregates are
  released.

The university-wide research-integrity page currently states a ten-year
retention period for materials supporting publications, while also directing
researchers to their unit's storage rules. Treat ten years as a question to the
responsible unit for raw annotation evidence, not as an automatic term for every
identity, account, agreement, or payment record. The final schedule must
minimize personal data while retaining the records required for research
integrity.

## Journal-facing consequence

The current *Language Resources and Evaluation* instructions ask authors to
make described resources public or clearly explain why they are unavailable,
include applicable ethics and consent declarations, maintain supporting
materials/code, and provide a Data Availability Statement. They also require
authors to hold the necessary rights for deposited data and allow justified
limits where privacy would be compromised. Thus journal reproducibility does
not justify publishing raw per-annotator records, identities, or server logs.
The intended release is rights-cleared source/annotation data, code, protocols,
an adjudicated label layer, and aggregate agreement; the Data Availability
Statement must name any restricted raw evidence and its access conditions.
Neither the journal's resource-sharing request nor its conditional ethics
language creates an independent requirement to obtain ethics approval for
ordinary commissioned annotation.

## Questions to resolve only before human work

Use these questions with the responsible administrative or ethics contact only
when the PI has chosen the annotation relationship or proposes a human study.

1. Under the chosen worker, contractor, collaborator, or participant route, is
   independent annotation of public English text within the unit's definition
   of a human-participant survey or experiment when only the resulting labels
   and aggregate agreement are analyzed?
2. Does the classification change if annotators are project members,
   contractors, paid research collaborators, students, or external volunteers?
3. May the minimum quality-control record contain pseudonymous annotator ID,
   labels, qualification result, structured decision notes, and adjudication
   history? Timing and language-background fields are not planned; would either
   require a separate justification or amendment if later proposed?
4. May per-annotator labels be released with the CC BY-SA benchmark, or only
   adjudicated labels and aggregate agreement statistics?
5. Does a separate usability study collecting completion, errors, assistance,
   time, interpretation, or free-text feedback require prior review?
6. Which storage, access-control, retention, destruction, agreement/consent,
   withdrawal, and compensation rules apply to the chosen relationship?
7. Does the proposed INCEpTION deployment and data flow above satisfy applicable
   security and data-management requirements? Which automatic log
   fields, server/backup locations, administrators, and deletion copies must be
   listed in the application?
8. Does the university's ten-year research-record rule apply to raw
   per-annotator exports, qualification records, project logs, and backups? What
   shorter or separate schedules apply to the identity key, account, consent,
   and payment records?
9. If a future study reuses de-identified TECO participant data locally, what
   secondary-use determination or notification is required?

If a formal determination is sought, request a dated response or identifier.
Archive any response outside the public repository if it contains names,
signatures, contact details, or internal administrative information; record
only the decision ID, scope, date, and non-sensitive conditions here.

## Fields to complete before the relevant human-work route

- Applicable institution and unit: pending
- Responsible PI and applicant role: pending
- Work relationship and classification: pending
- Determination or approval identifier, if applicable: not yet applicable
- Work agreement or approved protocol/version: pending
- Covered workstreams: pending
- Excluded workstreams: pending
- Conditions and expiry or amendment rule: pending
- Permitted engagement/recruitment start date: pending
- Managed storage location: pending
- Platform, host region, administrators, and log-field inventory: pending
- Account, identity-linkage, backup, export, and deletion route: pending
- Retention and destruction rule: pending
- Public-release permission for human-derived records: pending

These fields do not block present no-human work. Before the chosen human-work
route starts, complete the fields that apply to it and obtain ethics review only
if required. This record is a project control, not legal advice or an ethics
committee decision.

## Sources reviewed

- Tohoku University GSICS ethics documents, checked 2026-09-05: <https://www.intcul.tohoku.ac.jp/ja/research_screening>
- Preliminary checklist: <https://www.intcul.tohoku.ac.jp/word/reaserch/J-2_Preliminary_Checklist_for_Ethical_Review.docx>
- Review flowchart: <https://www.intcul.tohoku.ac.jp/pdf/reaserch/J-1_Flowchart_for_Ethical_Review.pdf>
- Human research ethics rules: <https://www.intcul.tohoku.ac.jp/pdf/reaserch/gsics_human_ethics_guidelines.pdf>
- Application procedure, version 2 dated 2025-09-18: <https://www.intcul.tohoku.ac.jp/pdf/reaserch/J-0_Procedures_for_Submitting_an_Application_for_Ethical_Review_03.pdf>
- Pre-submission checklist: <https://www.intcul.tohoku.ac.jp/pdf/reaserch/J-5_Pre-submission_Checklist_ja_v2.pdf>
- Research cooperation fee standard: <https://www.intcul.tohoku.ac.jp/pdf/reaserch/Standard_Rate_for_Research_Collaboration_Fees_ja.pdf>
- Tohoku University research-data management and publication policy commentary: <https://www.tohoku.ac.jp/japanese/newimg/newsimg/news20220104_05_guide.pdf>
- Tohoku University research-data retention and management rules: <https://www.bureau.tohoku.ac.jp/kenkyo/fb/rules.html>
- Personal Information Protection Commission guidance: <https://www.ppc.go.jp/personalinfo/legal/guidelines_anonymous/>
- Language Resources and Evaluation submission guidelines: <https://link.springer.com/journal/10579/submission-guidelines>
- Springer Nature sensitive/human-data sharing guidance: <https://support.springernature.com/en/support/solutions/articles/6000237612-sensitive-data-or-data-about-human-participants-sharing-expectations>
