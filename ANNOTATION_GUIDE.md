# MWE Annotation Guide

Version: `0.5.0-contextual-sense`
Status: standalone occurrence, span, category, idiomaticity, and contextual-sense modules complete; not approved for production annotation

This guide describes the order and recorded states for annotating English multiword-expression occurrences in this project. It is independent of the web interface: an annotator must be able to apply the rules from the text and record the same fields in a table or another tool.

The normative machine-readable sources are:

- `resources/target_population_contract.json` for candidate-independent discovery and eligibility;
- `mwe_contract.json` for occurrence, span, category, idiomaticity, inventory, and sense states;
- `resources/hybrid_sense_inventory_contract_2026_09_03.json` for bounded
  sense-routing provenance;
- `resources/inventory_governance.md` for inventory admission and lifecycle
  status.

If this guide conflicts with a contract, stop and report the conflict. Do not invent a label.

## Annotation order

Apply the stages in this order:

1. search the complete text without starting from a dictionary list;
2. decide whether each candidate is an occurrence;
3. mark lexical members and any intervening gap;
4. assign an MWE category;
5. judge contextual idiomaticity;
6. look up the form in a named, versioned inventory;
7. assign a contextual sense only when the bounded route permits it;
8. record uncertainty and provenance explicitly.

Later stages must not retroactively decide earlier ones. In particular, a dictionary match does not prove occurrence status, and a missing dictionary match does not prove that a candidate is literal or out of scope.

## Candidate-independent search

Definition: inspect the full text for eligible constructions without using an admitted inventory as a whitelist. Search aids may suggest candidates, but the annotator must review every token sequence that meets the population contract.

Decision tree:

1. Does the construction contain the required verbal and particle/prepositional or fixed-expression material?
2. Is the construction within the population described by `target_population_contract.json`?
3. If yes or unresolved, create a candidate record before consulting an inventory.
4. If clearly outside the population, do not create an MWE occurrence record; retain an exclusion note if the item was surfaced by a search aid.

| Kind | Example | Action |
|---|---|---|
| Positive | *take the forms in* | Create a candidate; an intervening noun phrase does not exclude it. |
| Negative | ordinary single-word *take* with no eligible partner | Do not create an MWE candidate. |
| Borderline | *take the visitor in* before the context establishes particle versus spatial reading | Create a candidate and leave the occurrence unresolved. |

Candidate discovery is exhaustive over the declared corpus denominator. Reporting only inventory-selected or prefiltered candidates is forbidden.

## Occurrence status

Definition: `status` records whether the candidate is an occurrence of an in-scope MWE, independently of its inventory or sense result.

Decision tree:

1. Verify that the candidate contains a verbal head and at least one other
   lexicalized component in the same syntactic construction. Ordinary tense,
   aspect, agreement, or non-finite inflection does not change the canonical
   form.
2. Verify that the proposed members jointly instantiate an in-scope
   construction in this context. A known citation form or adjacent spelling is
   not sufficient.
3. If the evidence establishes an in-scope occurrence and one category, use
   `confirmed`.
4. If the sequence is literal/compositional, spatial rather than particle-like,
   accidental, headed by a nonverb, elliptical down to fewer than two expressed
   lexicalized members, or otherwise outside scope, use `rejected`.
5. If particle/preposition status, lexicalized membership, or category remains
   genuinely unresolved, use `candidate`. Do not turn missing evidence into a
   rejection.

For a transitive particle candidate, movement before or after the direct object
is positive particle evidence; for an intransitive candidate, occurrence
without a governed noun phrase is positive evidence. These diagnostics do not
override the contextual VPC tests below. Incidental adjacency across unrelated
phrases or sentence boundaries is never an occurrence.

| Kind / state | Example | Meaning |
|---|---|---|
| Positive — `confirmed` | *take the forms in* meaning collect them | An in-scope occurrence is established. |
| Negative — `rejected` | *take the visitor in the room* with *in the room* modifying location | The surfaced sequence is not the target MWE occurrence. |
| Borderline — `candidate` | a clipped context compatible with both readings | The occurrence decision remains open. |

A rejected or unresolved candidate carries no positive inventory or sense conclusion.

## Member and gap spans

Definition: `member_spans` mark only the lexical members of the MWE. `gap_spans` mark intervening material between discontinuous members. Character spans are zero-based, half-open intervals and must point to the exact submitted text.

Decision tree:

1. Mark the inflected verbal head and every other lexicalized component, in
   source-token order. Use the surface token, not an invented lemma token.
2. Treat replaceable arguments, possessors, determiners, modifiers, and other
   open slots as nonmembers. A pronoun or full noun-phrase object between a verb
   and particle is normally a gap.
3. Set `gap_token_ids` to every token ID strictly between the first and last
   member that is not itself a member. The gap list is mechanical once members
   are fixed; do not select only the linguistically interesting interveners.
4. A continuous occurrence has no gap token. Particle movement changes member
   positions and gaps, not the canonical form or category.
5. Record overlapping candidates separately. Record an embedded construction
   only when it also qualifies as an MWE outside the larger expression; a shared
   token may belong to both records, while density counts its union once.
6. Reject a record with fewer than two unique member tokens, unordered or
   duplicated members, a member also listed as a gap, or an incomplete gap.

| Kind | Example | Spans |
|---|---|---|
| Positive | *take the forms in* | members: *take*, *in*; gap: *the forms* |
| Negative | the same example with *the forms* included as a member | Incorrect unless that phrase is proven lexically fixed. |
| Borderline | *spill those beans* | members: *spill*, *beans*; gap: *those* |

Overlapping candidates are assessed independently; one accepted occurrence does not automatically reject another span.

## Hard-case bank

The public [hard-case bank](annotations/hard_case_bank.json) contains only
project-authored synthetic text for training and QA. It prespecifies pronoun
insertion, long gaps, overlap, nesting, coordination, spelling error,
punctuation, quoted speech, and metalinguistic mention, with at least two cases
per stratum. Each case records admissible decision routes and a rationale, not
benchmark gold. Quoted use remains eligible; explicit mention is rejected.
Spelling is never silently repaired, and nested or token-sharing candidates are
reviewed independently. Every case records redistribution permission and
reproduces no third-party text.

## Category

Definition: `category` records the construction class, not its sense or inventory status.

Decision tree:

1. Identify the functional verbal head and its proposed lexicalized dependents.
   If the construction belongs only to an excluded category such as LVC, IRV,
   MVC, or IAV, reject it for this project rather than relabeling it.
2. If the relevant dependent is a particle, apply the VPC tests in order:

   1. Remove the particle. If the remaining sentence cannot refer to the same
      event or state, use `VPC.full`.
   2. Otherwise ask whether the particle expresses direction or position in the
      current reading. If yes, reject the VPC candidate.
   3. Otherwise ask whether the construction has a literal counterpart in which
      the particle is spatial. If yes, use `VPC.semi`; if no, reject the VPC
      candidate under the frozen PARSEME 1.2 boundary.
3. For a verb with another proposed lexicalized dependent, apply the VID tests
   only after the structural route. Use `VID` when at least one component is a
   cranberry word, or a normally available lexical, morphological,
   morphosyntactic, or syntactic substitution makes the construction
   unacceptable or causes an unexpected expression-level meaning shift.
4. If none of the applicable VPC or VID tests passes, use `rejected`. If a test
   cannot be applied reliably from the available context, keep `status:
   candidate`; do not force the familiar category.

This order follows the project's frozen mapping to [PARSEME 1.2 structural,
VID, and VPC tests](https://parsemefr.lis-lab.fr/parseme-st-guidelines/1.2/fulldoc.php).
The project labels map to `V.VPC.full`, `V.VPC.semi`, and `V.VID` in STREUSLE;
PARSEME 2.0 renames the VPC labels to `IVPC.full` and `IVPC.semi`. Do not mix
those spellings in project records.

| Kind / state | Example | Rationale |
|---|---|---|
| Positive — `VPC.full` | *take the forms in* meaning collect | Verb-particle construction in the training fixture. |
| Positive — `VPC.semi` | a partially transparent verb-particle item accepted under the project rule | Apply the ordered reduction, current-spatial, and literal-counterpart tests above. |
| Positive — `VID` | *spill the beans* meaning reveal a secret | Expression-level idiomatic interpretation. |
| Negative | a free verb plus spatial prepositional phrase | Reject as an in-scope occurrence when the syntax and context establish that analysis. |
| Borderline | a prepositional reading competing with a particle reading | Leave the occurrence unresolved until the syntactic evidence is sufficient. |

These labels do not assert a lexical sense. If an authorized pilot later shows
that annotators cannot apply a boundary consistently, stop, clarify the rule or
narrow the scope, and version the guide before continuing.

## Tokenization exceptions

Definition: tokenization determines which source-aligned token IDs are
available; it does not decide whether those tokens are lexicalized MWE members.

Decision tree:

1. Use only the token IDs and character/UTF-8 offsets produced by the frozen
   preprocessing contract. Never retokenize inside the annotation file.
2. Internal straight or curly apostrophes remain inside one normalized token.
   ASCII hyphens split token records, while punctuation is otherwise not a
   token under the current tokenizer.
3. Orthographic splitting does not create lexicalized components: a single
   hyphenated lexical item remains outside the MWE population unless it also
   contains two independently lexicalized members under the construct rule.
4. Punctuation with no token ID is neither a member nor a `gap_token_id`; its
   source characters remain recoverable from the surrounding offsets.
5. If the frozen tokens cannot express the intended members without merging or
   splitting a token, record `tokenization_mismatch`, leave the candidate
   unresolved or excluded, and escalate the preprocessing issue. Do not edit
   tokens locally.

| Kind | Example | Correct handling |
|---|---|---|
| Positive | *couldn't take it in* | *couldn't* is one token; members are *take* and *in*; *it* is the gap. |
| Negative | treating the split parts of *stage-managed* as an MWE solely because the tokenizer emits two tokens | Exclude; orthographic token count is not lexicalized membership. |
| Borderline | a lexicalized component is fused with an external word | Record `tokenization_mismatch` and escalate; do not repair the token ad hoc. |

## Exact-span disagreement coding

Definition: when two records disagree, code the first decision stage that
caused the mismatch. Do not report every downstream symptom as a separate
error.

Decision tree:

1. Different occurrence set: use an occurrence-level code.
2. Same occurrence but different member or gap IDs: use a span-level code.
3. Same occurrence and exact spans but different category: use a category-level
   code.
4. If the cause is not recoverable, use `unclassified` and retain both raw
   records for adjudication.

The controlled codes and project-authored examples are frozen in
`annotations/training_cases.json`:

| Level | Codes |
|---|---|
| Occurrence | `literal_or_spatial_promoted`, `accidental_sequence_promoted` |
| Span | `inflected_member_missed`, `particle_movement_missed`, `open_slot_marked_member`, `required_member_omitted`, `gap_not_complete`, `tokenization_mismatch`, `embedded_occurrence_omitted` |
| Category | `particle_preposition_boundary`, `vpc_full_semi_boundary`, `vpc_vid_boundary` |
| Fallback | `unclassified` |

| Kind | Example | First-cause code |
|---|---|---|
| Positive | one record includes the object as a member and the other treats it as a gap | `open_slot_marked_member` |
| Negative | also counting the resulting gap mismatch as a second independent error | Code only the first recoverable cause. |
| Borderline | raw records disagree but the responsible stage cannot be reconstructed | `unclassified`; adjudication must retain both records. |

## Idiomaticity

Definition: `idiomaticity_status` records whether the marked expression has a
conventionalized, nonfreely-compositional interpretation in the submitted
context. It is separate from structural category, occurrence status, candidate
origin, inventory membership, and fine-grained sense assignment.

Decision tree:

1. Use the complete submitted context and the fixed member span. Do not inspect
   an inventory definition, candidate sense, model prediction, or another
   annotator's label before this decision.
2. If occurrence or category is still unresolved (`status: candidate`), use
   `not_assessed`; the executable contract forbids an idiomaticity conclusion
   on an unresolved candidate.
3. Ask whether the contextual interpretation follows from the ordinary
   meanings of the members and the construction. If it does, use `literal`.
   In this contract, `literal` operationally means *compositional/non-idiomatic*
   and is not restricted to concrete physical language.
4. A metaphorical or otherwise figurative interpretation that is still
   compositionally built from the members also receives `literal`. Begin the
   decision note with `figurative_but_compositional:` so this known subtype can
   be reported separately rather than mistaken for concrete literal language.
5. Use `idiomatic` only when the context supports a conventionalized
   expression-level interpretation that is not freely derived from the normal
   contextual contribution of the members. Nonliteral subject matter alone is
   insufficient.
6. Use `ambiguous` only after assessment when both a compositional and an
   idiomatic interpretation remain materially supported by the full available
   context. Do not use it merely for low confidence, unfamiliarity, several
   fine-grained idiomatic senses, or an unresolved category.
7. Use `not_assessed` when the decision has not been performed, is not
   permitted, or must wait for an earlier stage.

| Kind / state | Example | Meaning |
|---|---|---|
| Positive — `idiomatic` | *spill the beans* meaning reveal the secret | Conventional idiomatic reading. |
| Negative — `literal` | beans physically spilling from a container | Compositional reading. |
| Negative — `literal` subtype | *the proposal moved forward* where the directional metaphor is compositionally understood | Record `figurative_but_compositional:` at the start of the note. |
| Borderline — `ambiguous` | a complete context that materially supports both physical and conventional readings | Context does not resolve idiomaticity after assessment. |
| Administrative — `not_assessed` | a newly discovered candidate awaiting review | No idiomaticity conclusion yet. |

Category and idiomaticity are stored separately on the same occurrence record.
For example, both M5 candidates retain the candidate category `VID`; one is a
confirmed occurrence with `idiomaticity.status: idiomatic`, while the physical
counterpart is rejected with `idiomaticity.status: literal`. Category does not
answer the contextual-usage question. Conversely, an idiomaticity decision
does not choose a dictionary sense: one idiomatic interpretation may still
have several plausible inventory senses.

Candidate origin also remains separate. An `open-text-first-pass` candidate is
found while reading the declared document population without a target list. A
`candidate-list-assisted` candidate is surfaced later by a list, rule, or model.
Apply the same idiomaticity decision tree to both, but preserve their origins in
document or dataset provenance and report them as separate discovery strata.
The current browser workflow generates only `candidate-list-assisted` records
from the user-supplied pattern TSV; it cannot establish open-text recall. The
current occurrence schema has no per-record origin field, so do not invent one
inside `mwe_contract.json`; an open-text benchmark must retain origin in its
higher-level annotation provenance until that schema is deliberately versioned.

### Loss-aware MAGPIE comparison projection

MAGPIE starts from a fixed dictionary idiom list and automatic pre-extraction,
then asks whether a highlighted potentially idiomatic expression is idiomatic,
literal, or outside that binary distinction. Its secondary route distinguishes
false extraction, unclear context, and non-standard usage. A comparison with
this project is therefore a candidate-list-conditioned projection, not an
open-text occurrence or recall comparison.

| Project record | MAGPIE-type comparison value | Rule |
|---|---|---|
| `idiomatic`, terminal occurrence/category decision | `idiomatic` (`i`) | Include only when the frozen candidate frame and exact span are comparable. |
| `literal`, rejected solely as the compositional counterpart of the same listed expression | `literal` (`l`) | Concrete literal and `figurative_but_compositional:` cases stay distinguishable in project strata. |
| `ambiguous` | unresolved / no binary value | Exclude from binary scoring and report the count and denominator. |
| `not_assessed` | missing / no value | Exclude from scoring and report as incomplete annotation. |
| rejected accidental, wrong-span, spatial/prepositional, or otherwise false extraction | false extraction (`f`) | Do not relabel it `literal`. |
| interpretable but outside the binary distinction | no automatic mapping to MAGPIE `other` (`o`) | Retain the project decision and adjudicate any crosswalk explicitly. |

This projection follows the distinction in [Haagsma, Bos, and Nissim
(2020)](https://aclanthology.org/2020.lrec-1.35/), but it does not claim label
identity: the candidate inventories, context windows, instructions, annotators,
and aggregation procedures differ. Never pool `open-text-first-pass` records
with the list-conditioned binary score. If independent annotators cannot apply
the binary boundary reliably, report the multi-state distribution and
unresolved rate instead of forcing a binary primary outcome.

## Form and sense inventory

Definition: inventory lookup records whether a normalized form or a sense candidate is present in the exact named and versioned resource consulted. It does not establish project gold.

Decision tree for `form_lookup_status`:

1. Use `matched` only when the normalized form matches the stated inventory rule.
2. Use `out_of_inventory` only after the complete frozen inventory has been searched.
3. Use `not_attempted` when lookup was not performed.

Decision tree for `sense_lookup_status`:

1. Use `matched` when one or more bounded sense candidates were retrieved from the declared route.
2. Use `out_of_inventory` only when the complete permitted sense inventory and route were searched with no candidate.
3. Use `not_attempted` when sense lookup was not performed.
4. Use `inventory_ineligible` when the confirmed type is outside the declared
   scope of the inventory or projection.

| Kind / state | Example | Meaning |
|---|---|---|
| Positive — `matched` | the normalized form is found in the declared inventory version | Resource match only; not an occurrence or sense judgment. |
| Negative — `out_of_inventory` | the full frozen inventory was searched and contains no admissible item | A bounded resource result with preserved denominator. |
| Borderline — `not_attempted` | normalization or authority is unresolved, so no lookup is run | No inventory claim; do not force a match or miss. |
| Administrative — `inventory_ineligible` | a confirmed VID is outside a projection declared only for one VPC form | No semantic absence claim; retain it in the confirmed-occurrence denominator. |

A miss in a single convenient dictionary is not `out_of_inventory`. Preserve resource name, version, stable identifier or URL, normalized query, and lookup result. The current hybrid candidate inventory contains no admitted project sense records and is not a production sense source.

## Contextual sense

Definition: `sense_assignment_status` records the outcome of matching the occurrence in context to the candidates supplied by the permitted sense route.

Decision tree:

1. If exactly one sense is supported, use `assigned` and record exactly one stable sense identifier.
2. If two or more distinct project senses jointly apply, use `multiple_assigned`
   and record every applicable identifier.
3. If two or more named alternatives are plausible but the context cannot
   resolve among them, use `ambiguous` and record every retained identifier.
4. If the available context or evidence is insufficient to make the declared
   judgment, use `abstained` and record none.
5. If assignment has not been done, use `unassigned`.
6. If the complete bounded inventory was reviewed, the occurrence has a
   coherent meaning, and no admitted sense is adequate, use
   `out_of_inventory` and record none.
7. If the occurrence is outside the declared inventory scope, use
   `inventory_ineligible` and record none.

| Kind / state | Example | Required selection |
|---|---|---|
| Positive — `assigned` | training contexts distinguish OEWN `%2:31:00::` from `%2:32:00::` | Exactly one identifier. |
| Positive — `multiple_assigned` | one synthetic utterance deliberately realizes two distinct admitted readings at once | Two or more jointly applicable identifiers. |
| Borderline — `ambiguous` | two named candidate senses remain plausible because the synthetic context does not disambiguate them | Two or more alternative identifiers. |
| Borderline — `abstained` | the synthetic excerpt is truncated before the evidence needed for a sense judgment | Zero identifiers. |
| Administrative — `unassigned` | contextual assignment has not begun | Zero identifiers. |
| Negative — `out_of_inventory` | every admitted sense was shown, but none expresses the coherent contextual meaning | Zero identifiers. |
| Administrative — `inventory_ineligible` | the confirmed form is outside the inventory's declared type/POS projection | Zero identifiers. |

An external link or retrieved candidate remains source evidence, not project
gold. The frozen project inventory is the only assignment space; source glosses,
examples, and external identifiers explain its candidates but cannot silently
add, merge, or reorder project senses. If two source entries differ only in
granularity, first apply the recorded `equivalent`, `broader`, `narrower`, or
`overlapping` mapping. Do not select both merely because both glosses resemble
the context. Use `multiple_assigned` only for distinct admitted project senses
that genuinely hold together. Use `ambiguous` for named alternatives that the
context leaves unresolved, `abstained` when the evidence cannot support the
task at all, and `out_of_inventory` only after complete review establishes that
no admitted sense is adequate. Type-level `unresolved` or `no_bounded_route`
never licenses an occurrence-level semantic OOI decision.

Export each confirmed occurrence with the complete nested `sense` record:

| Assignment outcome | `lookup_status` | selected IDs | decision provenance |
|---|---|---:|---|
| `assigned` | `matched` | exactly 1 | required |
| `multiple_assigned` | `matched` | 2 or more | required |
| `ambiguous` | `matched` | 2 or more | required |
| `abstained` | `matched` | 0 | required |
| `unassigned` | `matched` or `not_attempted` | 0 | absent |
| `out_of_inventory` | `matched` or `out_of_inventory` | 0 | required |
| `inventory_ineligible` | `inventory_ineligible` | 0 | required |

Evaluation keeps these outcomes separate. Gold `assigned`,
`multiple_assigned`, and `ambiguous` records with nonempty ID sets form the
sense-set denominator. Report exact unordered-set accuracy, micro label-pair
F1, macro per-occurrence set F1, and exact assignment-state accuracy. Thus an
identical two-ID prediction does not erase the difference between joint
applicability and unresolved alternatives. Report abstention, OOI, and
inventory-ineligible rates separately rather than scoring them as empty senses.
This separation follows multi-label WSD evidence that more than one sense can
apply to one instance ([Conia and Navigli, 2021](https://aclanthology.org/2021.eacl-main.286/))
and selective-prediction evidence that uncertain cases need an explicit
abstention route ([Xin et al., 2021](https://aclanthology.org/2021.acl-long.84/)).
Those studies motivate the state design; they do not validate this project's
inventory, examples, or annotators.

## Uncertainty states

Definition: uncertainty must be represented by an existing contract state at the stage where it occurs; never hide it in free text or force a positive label.

Decision tree:

1. Unresolved occurrence: `status: candidate`.
2. Unresolved idiomaticity after assessment: `idiomaticity_status: ambiguous`.
3. Idiomaticity not yet assessed: `idiomaticity_status: not_assessed`.
4. Lookup not run: the relevant lookup status is `not_attempted`.
5. Several senses genuinely apply together: `sense_assignment_status: multiple_assigned`.
6. Named alternatives remain unresolved: `sense_assignment_status: ambiguous`.
7. Evidence is insufficient for the task: `sense_assignment_status: abstained`.
8. Assignment not run: `sense_assignment_status: unassigned`.
9. Complete bounded inventory has no adequate sense: `sense_assignment_status: out_of_inventory`.
10. The occurrence is outside the declared inventory scope: both sense states are `inventory_ineligible`.

Free-text notes may explain an uncertainty state but must not replace it.

| Kind | Example | Correct handling |
|---|---|---|
| Positive | two distinct admitted senses intentionally hold together | Record `multiple_assigned` and both identifiers. |
| Negative | choosing the familiar first sense only to complete the row | Do not force `assigned`; use the supported uncertainty state. |
| Borderline | two named senses are plausible but the context cannot choose between them | Record `ambiguous` and both identifiers. |
| Borderline | the excerpt omits evidence needed to perform the task | Record `abstained`, not `ambiguous` or `out_of_inventory`. |

## Contract-state coverage

| Field | Permitted states covered by this guide |
|---|---|
| `status` | `candidate`, `confirmed`, `rejected` |
| `category` | `VPC.full`, `VPC.semi`, `VID` |
| `idiomaticity_status` | `idiomatic`, `literal`, `ambiguous`, `not_assessed` |
| `form_lookup_status` | `matched`, `out_of_inventory`, `not_attempted` |
| `sense_lookup_status` | `matched`, `out_of_inventory`, `not_attempted`, `inventory_ineligible` |
| `sense_assignment_status` | `assigned`, `multiple_assigned`, `ambiguous`, `abstained`, `unassigned`, `out_of_inventory`, `inventory_ineligible` |

## Synthetic training fixture key

The executable fixture `tests/fixtures/mwe_cases.json` is the minimal guide-only check. Expected reasoning:

- `M1-word-versus-confirmed-form`: confirm continuous *take in*; mark the two members; form lookup is `matched`; sense lookup is `not_attempted` and assignment is `unassigned`.
- `M2-discontinuous-members-and-gaps`: confirm discontinuous *take … in*; mark the intervening noun phrase as a gap, not a member.
- `M3-one-form-two-contextual-senses`: treat the two *take in* contexts independently and assign the context-supported stable sense identifier to each.
- `M4-confirm-versus-reject-context`: confirm the pronoun-gap particle occurrence and reject the spatial prepositional candidate.
- `M5-idiomatic-versus-literal-vid`: confirm idiomatic `VID` *spill the beans* and reject the literal physical-spilling candidate.

The key tests state handling, not annotator agreement or qualification.

## Final record checklist

Before a record is complete, verify that:

- discovery did not use an inventory whitelist;
- the submitted text and offsets reproduce the marked members and gaps;
- occurrence, category, and idiomaticity were decided separately;
- every inventory statement names the resource and version;
- every selected sense has a stable source identifier and preserved provenance;
- uncertainty uses an explicit contract state;
- excluded and unresolved cases remain in the denominator;
- no source candidate is presented as project gold without an admissible human adjudication record.

## Current stop

Do not administer this guide to annotators yet. The applicable institutional
human-use determination must be recorded, and an unexposed qualification form,
authorized training/pilot, agreement, and adjudication evidence must be
completed before production use. The current cases and training protocol are
synthetic document/software evidence, not annotator qualification or
reliability evidence.
