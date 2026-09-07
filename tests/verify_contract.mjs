import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {runInNewContext} from 'node:vm';
import {
  analyze, analyzeDeclaredSegments, analyzeWordCoverage, findMweCandidates, lookupMweForm,
  lookupMweSenses, makeExportRecord, makeMweDocumentSetRecord, makeMweReviewRecord,
  makeMweWorkspaceRecord, mweOccurrencesCsv,
  parseBatchJson, parseJsonInput, parseMwePatternTsv, prepareMweFormReferenceProfile,
  prepareMweSenseReferenceProfile, prepareWordReferenceProfile, restoreMweDocumentSetRecord,
  restoreMweWorkspaceRecord, roundedRatio, sha256, summarizeMweDocument,
  summarizeMweFormCoverage, tokenize, tokenizeForAsciiWordProfile, tokenRecords, wordCoverageCsv
} from '../metrics.mjs';

const fixtureUrl = new URL('./fixtures/metric_cases.json', import.meta.url);
const sampleUrl = new URL('../samples.json', import.meta.url);
const contractUrl = new URL('../metric_contract.json', import.meta.url);
const mweContractUrl = new URL('../mwe_contract.json', import.meta.url);
const mweFixtureUrl = new URL('./fixtures/mwe_cases.json', import.meta.url);
const oewnSubsetUrl = new URL('../resources/oewn_take_in_2025.json', import.meta.url);
const oewnNoticeUrl = new URL('../resources/OEWN_WORDNET_NOTICE.txt', import.meta.url);
const wordProfileUrl = new URL('../resources/tubelex_en_regex_ascii_2025.json', import.meta.url);
const ngslProfileUrl = new URL('../resources/ngsl_1_2_ascii_forms.json', import.meta.url);
const mweFormProfileUrl = new URL('../resources/oewn_2025_multiword_verbs.json', import.meta.url);
const fixture = JSON.parse(readFileSync(fixtureUrl, 'utf8'));
const sampleDocument = JSON.parse(readFileSync(sampleUrl, 'utf8'));
const contract = JSON.parse(readFileSync(contractUrl, 'utf8'));
const mweContract = JSON.parse(readFileSync(mweContractUrl, 'utf8'));
const mweFixture = JSON.parse(readFileSync(mweFixtureUrl, 'utf8'));
const oewnSubsetText = readFileSync(oewnSubsetUrl, 'utf8');
const oewnSubset = JSON.parse(oewnSubsetText);
const oewnNotice = readFileSync(oewnNoticeUrl, 'utf8');
const wordProfile = prepareWordReferenceProfile(JSON.parse(readFileSync(wordProfileUrl, 'utf8')));
const ngslProfileText = readFileSync(ngslProfileUrl, 'utf8');
const ngslProfile = prepareWordReferenceProfile(JSON.parse(ngslProfileText));
const mweFormProfile = prepareMweFormReferenceProfile(
  JSON.parse(readFileSync(mweFormProfileUrl, 'utf8'))
);
const mweSenseProfile = prepareMweSenseReferenceProfile(oewnSubset);

assert.equal(contract.contract_version, '0.1.0-probe');
assert.equal(fixture.contract_version, contract.contract_version);
for (const testCase of fixture.cases) {
  assert.deepEqual(analyze(testCase.text), testCase.expected, testCase.id);
}
assert.equal(roundedRatio(1, 128), 0.007813);
assert.deepEqual(tokenizeForAsciiWordProfile("Don't re-use café."), ['don', 't', 're', 'use']);
const wordCoverage = analyzeWordCoverage(
  'They took it in, then spilled the beans and played qqqqqq.', wordProfile
);
assert.deepEqual(wordCoverage.token_coverage, {numerator: 10, denominator: 11, value: 0.909091});
assert.deepEqual(wordCoverage.type_coverage, {numerator: 10, denominator: 11, value: 0.909091});
assert.equal(wordCoverage.items[0].word, 'qqqqqq');
assert.equal(wordCoverage.items[0].status, 'unmatched');
assert.match(wordCoverageCsv(wordCoverage), /"qqqqqq","1","unmatched"/);
const ngsl1000 = analyzeWordCoverage(
  'The favorite difficulty thick found xylophone.', ngslProfile, 1000
);
assert.deepEqual(ngsl1000.token_coverage, {numerator: 3, denominator: 6, value: 0.5});
assert.equal(ngsl1000.items.find(item => item.word === 'difficulty').status, 'beyond_cutoff');
assert.equal(ngsl1000.items.find(item => item.word === 'xylophone').status, 'unmatched');
assert.deepEqual(ngsl1000.items.find(item => item.word === 'found').head_mappings, [
  {lemma: 'find', rank: 81}, {lemma: 'found', rank: 2807}
]);
assert.equal(ngsl1000.items.find(item => item.word === 'found').ambiguous_head_mapping, true);
assert.deepEqual(
  analyzeWordCoverage('The favorite difficulty thick found xylophone.', ngslProfile, 2000)
    .token_coverage,
  {numerator: 5, denominator: 6, value: 0.833333}
);
assert.throws(() => analyzeWordCoverage('the', ngslProfile), /rank cutoff/);
assert.deepEqual(lookupMweForm('Take   In', mweFormProfile), {
  inventory_id: 'oewn-2025-ascii-multiword-verb-forms',
  inventory_version: '2025.projection-1', status: 'matched',
  entry_id: 'take in#v', sense_count: 17
});

const patternTsv = [
  'VPC.full\ttake in\ttake/takes/took/taken/taking in\t4',
  'VID\tspill the beans\tspill/spills/spilled/spilling bean/beans\t2'
].join('\n');
const patterns = parseMwePatternTsv(
  patternTsv, ['VPC.full', 'VPC.semi', 'VID']
);
assert.equal(patterns.length, 2);
assert.deepEqual(tokenRecords('They took it in.').map(token => token.surface), [
  'They', 'took', 'it', 'in'
]);
const candidateDocument = findMweCandidates(
  'They took it in, then spilled the beans.', patterns
);
candidateDocument.text = 'They took it in, then spilled the beans.';
assert.deepEqual(
  candidateDocument.occurrences.map(item => [item.canonical_form, item.member_token_ids, item.gap_token_ids]),
  [
    ['take in', ['t2', 't4'], ['t3']],
    ['spill the beans', ['t6', 't8'], ['t7']]
  ]
);
assert.throws(
  () => parseMwePatternTsv('VPC.full take in', ['VPC.full']),
  /four tab-separated/
);
assert.throws(
  () => findMweCandidates('take it in take it in', patterns, 1),
  /candidate count exceeds/
);
assert.throws(
  () => findMweCandidates('x'.repeat(100_001), patterns),
  /exceeds 100,000/
);
const reviewedDocument = structuredClone(candidateDocument);
reviewedDocument.occurrences = reviewedDocument.occurrences.map(item => ({
  ...item,
  status: 'confirmed',
  decision: {source: 'test-review', note: 'synthetic fixture decision'},
  form_lookup: lookupMweForm(item.canonical_form, mweFormProfile),
  sense: lookupMweSenses(item.canonical_form, mweSenseProfile).state
}));
reviewedDocument.occurrences[0].idiomaticity = {
  status: 'idiomatic',
  decision: {source: 'test-review', note: 'contextual idiomaticity decision'}
};
reviewedDocument.occurrences[0].sense.assignment_status = 'assigned';
reviewedDocument.occurrences[0].sense.selected_sense_ids = [
  reviewedDocument.occurrences[0].sense.candidate_sense_ids[0]
];
reviewedDocument.occurrences[0].sense.decision = {
  source: 'test-review', note: 'contextual sense decision'
};
assert.deepEqual(summarizeMweFormCoverage(reviewedDocument, mweContract), {
  occurrence_coverage: {numerator: 2, denominator: 2, value: 1},
  type_coverage: {numerator: 2, denominator: 2, value: 1},
  unmatched_forms: []
});
const mweReviewRecord = await makeMweReviewRecord({
  document: reviewedDocument,
  contract: mweContract,
  patternSource: patternTsv,
  tokenizer: contract.tokenizer,
  authorizationAttested: true,
  wordProfile,
  wordRankCutoff: null,
  mweFormProfile,
  mweSenseProfile,
  generatedAt: '2026-09-01T00:00:00.000Z'
});
assert.equal(mweReviewRecord.schema_version, '0.4.0-mwe-review');
assert.equal(mweReviewRecord.text.raw_text_included, false);
assert.equal(mweReviewRecord.input_authorization.attested, true);
assert.equal(mweReviewRecord.active_runtime_resources.length, 3);
assert.equal(mweReviewRecord.summary.word_coverage.token_coverage.denominator, 8);
assert.equal(mweReviewRecord.summary.review.sense_inventory_coverage.numerator, 1);
assert.equal(mweReviewRecord.summary.review.sense_assignment_coverage.numerator, 1);
assert.equal(mweReviewRecord.summary.review.idiomaticity_annotation_coverage.numerator, 1);
assert.equal(mweReviewRecord.occurrences[0].sense.lookup_status, 'matched');
assert.equal(mweReviewRecord.occurrences[0].sense.candidate_sense_ids.length, 17);
assert.equal(mweReviewRecord.occurrences[0].sense.assignment_status, 'assigned');
assert.equal(mweReviewRecord.occurrences[0].idiomaticity.status, 'idiomatic');
assert.ok(!JSON.stringify(mweReviewRecord).includes(reviewedDocument.text));
assert.match(mweReviewRecord.text.sha256_utf8, /^[0-9a-f]{64}$/);
assert.match(mweOccurrencesCsv(reviewedDocument, mweContract), /"take in"/);
assert.match(mweOccurrencesCsv(reviewedDocument, mweContract), /"matched","take in#v","17"/);
assert.match(mweOccurrencesCsv(reviewedDocument, mweContract), /"idiomatic","contextual idiomaticity decision"/);
assert.match(mweOccurrencesCsv(reviewedDocument, mweContract), /"assigned","take_in%2:42:00::","contextual sense decision"/);
assert.match(mweOccurrencesCsv(reviewedDocument, mweContract), /"take_in%2:42:00::/);
const mweWorkspaceRecord = await makeMweWorkspaceRecord({
  document: reviewedDocument, contract: mweContract, patternSource: patternTsv,
  authorizationAttested: true, savedAt: '2026-09-01T00:00:00.000Z',
  wordProfileKey: 'tubelex', wordProfile, wordRankCutoff: null,
  mweFormProfile, mweSenseProfile
});
assert.equal(mweWorkspaceRecord.schema_version, mweContract.workspace_file.schema_version);
assert.equal(mweWorkspaceRecord.raw_content_included, true);
assert.equal(mweWorkspaceRecord.document.text, reviewedDocument.text);
assert.match(mweWorkspaceRecord.document.sha256_utf8, /^[0-9a-f]{64}$/);
assert.equal(Object.hasOwn(mweWorkspaceRecord.document, 'tokens'), false);
const oversizedOccurrenceDocument = structuredClone(reviewedDocument);
oversizedOccurrenceDocument.occurrences = Array.from(
  {length: mweContract.candidate_generation.limits.candidates_per_text + 1},
  () => structuredClone(reviewedDocument.occurrences[0])
);
assert.throws(
  () => summarizeMweDocument(oversizedOccurrenceDocument, mweContract),
  /occurrence count exceeds/
);
assert.deepEqual(await restoreMweWorkspaceRecord({
  record: mweWorkspaceRecord, contract: mweContract, authorizationAttested: true,
  wordProfileKey: 'tubelex', wordProfile, wordRankCutoff: null,
  mweFormProfile, mweSenseProfile
}), {document: reviewedDocument, patternSource: patternTsv});
const tamperedWorkspace = structuredClone(mweWorkspaceRecord);
tamperedWorkspace.document.occurrences[0].member_token_ids[0] = 't99999';
await assert.rejects(() => restoreMweWorkspaceRecord({
  record: tamperedWorkspace, contract: mweContract, authorizationAttested: true,
  wordProfileKey: 'tubelex', wordProfile, wordRankCutoff: null,
  mweFormProfile, mweSenseProfile
}), /Unknown token ID/);
const tamperedWorkspaceText = structuredClone(mweWorkspaceRecord);
tamperedWorkspaceText.document.text = tamperedWorkspaceText.document.text.replace('They', 'We');
await assert.rejects(() => restoreMweWorkspaceRecord({
  record: tamperedWorkspaceText, contract: mweContract, authorizationAttested: true,
  wordProfileKey: 'tubelex', wordProfile, wordRankCutoff: null,
  mweFormProfile, mweSenseProfile
}), /text SHA-256/);
const mismatchedWorkspaceResource = structuredClone(mweWorkspaceRecord);
mismatchedWorkspaceResource.active_runtime_resources[0].profile_version = 'wrong';
await assert.rejects(() => restoreMweWorkspaceRecord({
  record: mismatchedWorkspaceResource, contract: mweContract, authorizationAttested: true,
  wordProfileKey: 'tubelex', wordProfile, wordRankCutoff: null,
  mweFormProfile, mweSenseProfile
}), /runtime resources/);
const documentSetRecord = makeMweDocumentSetRecord({
  contract: mweContract, setId: 'pilot-set', setLabel: 'Pilot passages',
  documents: [
    {id: 'passage-1', label: 'Passage one', workspace: mweWorkspaceRecord},
    {id: 'passage-2', label: 'Passage two', workspace: mweWorkspaceRecord}
  ],
  savedAt: '2026-09-01T00:30:00.000Z', authorizationAttested: true
});
assert.equal(documentSetRecord.schema_version, mweContract.document_set_file.schema_version);
assert.equal(documentSetRecord.documents.length, 2);
assert.deepEqual((await restoreMweDocumentSetRecord({
  record: documentSetRecord, contract: mweContract, authorizationAttested: true,
  wordProfiles: new Map([['tubelex', {profile: wordProfile, maximumRank: null}]]),
  mweFormProfile, mweSenseProfile
})).documents.map(item => item.id), ['passage-1', 'passage-2']);
assert.throws(() => makeMweDocumentSetRecord({
  contract: mweContract, setId: 'pilot-set', setLabel: 'Pilot passages',
  documents: [
    {id: 'duplicate', label: 'One', workspace: mweWorkspaceRecord},
    {id: 'duplicate', label: 'Two', workspace: mweWorkspaceRecord}
  ],
  savedAt: '2026-09-01T00:30:00.000Z', authorizationAttested: true
}), /Duplicate MWE document ID/);
const tamperedDocumentSet = structuredClone(documentSetRecord);
tamperedDocumentSet.documents[1].workspace.document.text = 'Changed text.';
await assert.rejects(() => restoreMweDocumentSetRecord({
  record: tamperedDocumentSet, contract: mweContract, authorizationAttested: true,
  wordProfiles: new Map([['tubelex', {profile: wordProfile, maximumRank: null}]]),
  mweFormProfile, mweSenseProfile
}), /text SHA-256/);
// Sense states survive JSON save/resume without turning uncertainty into assignment.
{
  const options = {
    contract: mweContract, authorizationAttested: true, patternSource: patternTsv,
    savedAt: '2026-09-01T00:00:00.000Z', wordProfileKey: 'tubelex', wordProfile,
    wordRankCutoff: null, mweFormProfile, mweSenseProfile,
    wordProfiles: new Map([['tubelex', {profile: wordProfile, maximumRank: null}]])
  };
  const documents = [];
  for (const [status, count] of [
    ['assigned', 1], ['multiple_assigned', 2], ['ambiguous', 2],
    ['abstained', 0], ['unassigned', 0], ['out_of_inventory', 0]
  ]) {
    const document = structuredClone(reviewedDocument);
    const occurrence = document.occurrences[0];
    occurrence.idiomaticity = {status: 'not_assessed', decision: null};
    Object.assign(occurrence.sense, {
      assignment_status: status,
      selected_sense_ids: occurrence.sense.candidate_sense_ids.slice(0, count),
      decision: status === 'unassigned' ? null : occurrence.sense.decision
    });
    const workspace = JSON.parse(JSON.stringify(await makeMweWorkspaceRecord({
      ...options, document
    })));
    const restored = await restoreMweWorkspaceRecord({...options, record: workspace});
    assert.deepEqual(restored, {document, patternSource: patternTsv});
    const summary = summarizeMweDocument(restored.document, mweContract);
    assert.equal(summary.sense_assignment_status_counts[status], 1);
    assert.equal(summary.sense_assignment_status_counts.inventory_ineligible, 1);
    assert.deepEqual(summary.sense_assignment_coverage, {
      numerator: ['assigned', 'multiple_assigned'].includes(status) ? 1 : 0,
      denominator: 1, value: ['assigned', 'multiple_assigned'].includes(status) ? 1 : 0
    });
    documents.push({id: status, label: status, workspace});
  }
  const set = JSON.parse(JSON.stringify(makeMweDocumentSetRecord({
    ...options, setId: 'sense-states', setLabel: 'Synthetic sense states', documents
  })));
  assert.deepEqual((await restoreMweDocumentSetRecord({...options, record: set})).documents,
    documents);

  // Imported provenance must be nonblank text, never coerced into a displayed note.
  for (const slot of ['decision', 'idiomaticity', 'sense']) {
    for (const field of ['source', 'note']) {
      for (const value of [undefined, null, false, 17, {}, [], '', ' \t ']) {
        const record = structuredClone(mweWorkspaceRecord);
        const occurrence = record.document.occurrences[0];
        const parent = slot === 'decision' ? occurrence : occurrence[slot];
        parent.decision[field] = value;
        await assert.rejects(() => restoreMweWorkspaceRecord({
          ...options, record: JSON.parse(JSON.stringify(record))
        }), /decision provenance/);
      }
    }
  }
  for (const slot of ['decision', 'idiomaticity', 'sense']) {
    for (const value of [undefined, false, 0, '', {}, {source: 'test-review'}]) {
      const record = structuredClone(mweWorkspaceRecord);
      if (slot === 'decision') {
        record.document.occurrences[0] = structuredClone(candidateDocument.occurrences[0]);
      }
      const occurrence = record.document.occurrences[0];
      const parent = slot === 'decision' ? occurrence : occurrence[slot];
      if (slot === 'idiomaticity') parent.status = 'not_assessed';
      if (slot === 'sense') {
        parent.assignment_status = 'unassigned';
        parent.selected_sense_ids = [];
      }
      parent.decision = value;
      await assert.rejects(() => restoreMweWorkspaceRecord({
        ...options, record: JSON.parse(JSON.stringify(record))
      }), /decision|idiomaticity state|terminal result/);
    }
  }
  const invalidSet = structuredClone(set);
  invalidSet.documents.at(-1).workspace.document.occurrences[0].sense.decision.note = {};
  await assert.rejects(() => restoreMweDocumentSetRecord({...options, record: invalidSet}),
    /Sense decision provenance/);
  const invalidDocument = structuredClone(reviewedDocument);
  invalidDocument.occurrences[0].sense.decision.note = {};
  await assert.rejects(() => makeMweWorkspaceRecord({...options, document: invalidDocument}),
    /Sense decision provenance/);
  assert.throws(() => mweOccurrencesCsv(invalidDocument, mweContract), /Sense decision provenance/);
}
const ngslReviewRecord = await makeMweReviewRecord({
  document: reviewedDocument, contract: mweContract, patternSource: patternTsv,
  tokenizer: contract.tokenizer, authorizationAttested: true,
  wordProfile: ngslProfile, wordRankCutoff: 1000, mweFormProfile, mweSenseProfile,
  generatedAt: '2026-09-01T00:00:00.000Z'
});
// Async records must describe the validated input at call time, not later edits.
{
  const options = {
    contract: mweContract, patternSource: patternTsv, authorizationAttested: true,
    savedAt: '2026-09-01T00:00:00.000Z', generatedAt: '2026-09-01T00:00:00.000Z',
    tokenizer: contract.tokenizer, wordProfileKey: 'tubelex', wordProfile,
    wordRankCutoff: null, mweFormProfile, mweSenseProfile,
    wordProfiles: new Map([['tubelex', {profile: wordProfile, maximumRank: null}]])
  };
  for (const [build, expected] of [
    [makeMweWorkspaceRecord, mweWorkspaceRecord], [makeMweReviewRecord, mweReviewRecord]
  ]) {
    const document = structuredClone(reviewedDocument);
    const pending = build({...options, document});
    document.occurrences[0].decision.note = 'Changed while hashing.';
    const saved = await pending;
    assert.deepEqual(saved, expected, `${build.name} must snapshot before awaiting`);
    document.occurrences[0].sense.selected_sense_ids.length = 0;
    assert.deepEqual(saved, expected, 'Returned decisions must not alias the caller');
  }
  for (const [restore, original] of [
    [restoreMweWorkspaceRecord, mweWorkspaceRecord], [restoreMweDocumentSetRecord, documentSetRecord]
  ]) {
    const expected = await restore({...options, record: original});
    const record = structuredClone(original);
    const pending = restore({...options, record});
    const workspace = record.document ? record : record.documents[0].workspace;
    workspace.document.text = workspace.document.text.replace('They', 'We');
    workspace.document.occurrences[0].decision.note = 'Changed while validating.';
    assert.deepEqual(await pending, expected, `${restore.name} must restore the validated snapshot`);
  }
}
assert.equal(ngslReviewRecord.summary.word_coverage.selected_rank_cutoff, 1000);
assert.equal(
  ngslReviewRecord.active_runtime_resources[0].profile_id,
  'ngsl-1.2-ascii-research-forms'
);
const localWordProfile = prepareWordReferenceProfile({
  identity: {
    profile_id: 'bnc-coca-level6-v1.0.0-first-2k-local',
    profile_version: '1.0.0.local-projection-1',
    profile_status: 'local_only', title: 'Synthetic local-profile contract fixture'
  },
  construct: {
    coverage_channel: 'word', reference_function: 'ranked_inventory',
    excluded_inferences: ['learner knowledge']
  },
  source: {
    delivery_mode: 'researcher_supplied_local_file', artifact_sha256: 'a'.repeat(64),
    release_or_edition: 'synthetic fixture'
  },
  rights: {
    browser_delivery_permitted: false, local_user_import_permitted: true,
    license_identifier: 'project-authored-test-fixture'
  },
  corpus_design: {token_count: null},
  table: {projected_row_count: 3, source_headword_count: 3, ambiguous_surface_form_count: 0},
  measurement: {band_boundaries: [1, 2]},
  rows: [
    ['abilities', [['able', 1]]], ['taken', [['take', 1]]],
    ['unaccented', [['accent', 2]]]
  ]
});
assert.deepEqual(analyzeWordCoverage(
  'Abilities were taken unaccented.', localWordProfile, 1
).items.filter(item => ['abilities', 'taken', 'unaccented'].includes(item.word))
  .map(item => [item.word, item.status]), [
  ['unaccented', 'beyond_cutoff'], ['abilities', 'matched'], ['taken', 'matched']
]);
await assert.rejects(makeMweReviewRecord({
  document: reviewedDocument, contract: mweContract, patternSource: patternTsv,
  tokenizer: contract.tokenizer, authorizationAttested: true,
  wordProfile: localWordProfile, wordRankCutoff: 1, mweFormProfile, mweSenseProfile,
  generatedAt: '2026-09-01T00:00:00.000Z'
}), /runtime hash/);
localWordProfile.runtimeProfileSha256 = 'b'.repeat(64);
const localReviewRecord = await makeMweReviewRecord({
  document: reviewedDocument, contract: mweContract, patternSource: patternTsv,
  tokenizer: contract.tokenizer, authorizationAttested: true,
  wordProfile: localWordProfile, wordRankCutoff: 1, mweFormProfile, mweSenseProfile,
  generatedAt: '2026-09-01T00:00:00.000Z'
});
assert.equal(localReviewRecord.active_runtime_resources[0].profile_status, 'local_only');
assert.equal(localReviewRecord.active_runtime_resources[0].runtime_profile_sha256, 'b'.repeat(64));
const mismatchedLookupDocument = structuredClone(reviewedDocument);
mismatchedLookupDocument.occurrences[0].form_lookup.entry_id = 'wrong#v';
await assert.rejects(
  makeMweReviewRecord({
    document: mismatchedLookupDocument, contract: mweContract, patternSource: patternTsv,
    tokenizer: contract.tokenizer, authorizationAttested: true, wordProfile, mweFormProfile,
    wordRankCutoff: null, mweSenseProfile,
    generatedAt: '2026-09-01T00:00:00.000Z'
  }),
  /does not match the active profile/
);
const mismatchedSenseDocument = structuredClone(reviewedDocument);
mismatchedSenseDocument.occurrences[0].sense.candidate_sense_ids.pop();
await assert.rejects(
  makeMweReviewRecord({
    document: mismatchedSenseDocument, contract: mweContract, patternSource: patternTsv,
    tokenizer: contract.tokenizer, authorizationAttested: true, wordProfile, mweFormProfile,
    wordRankCutoff: null, mweSenseProfile, generatedAt: '2026-09-01T00:00:00.000Z'
  }),
  /sense lookup does not match/
);
await assert.rejects(
  makeMweReviewRecord({
    document: reviewedDocument, contract: mweContract, patternSource: patternTsv,
    tokenizer: contract.tokenizer, authorizationAttested: false,
    wordProfile, wordRankCutoff: null, mweFormProfile, mweSenseProfile,
    generatedAt: '2026-09-01T00:00:00.000Z'
  }),
  /authorization attestation/
);

assert.equal(mweFixture.contract_version, mweContract.contract_version);
assert(!mweContract.scope.not_implemented.includes('document-set-mwe-review'));
assert.deepEqual(
  mweContract.external_resource_dependencies.map(item => item.id),
  [
    'tubelex-en-regex-ascii-word-frequency',
    'ngsl-1.2-ascii-research-forms',
    'oewn-2025-ascii-multiword-verb-forms',
    'oewn'
  ]
);
const senseDependency = mweContract.external_resource_dependencies.find(item => item.subset_id);
assert.equal(senseDependency.subset_id, oewnSubset.subset_id);
assert.equal(
  senseDependency.path_sha256,
  await sha256(oewnSubsetText)
);
assert.equal(
  mweContract.external_resource_dependencies.find(item => item.id.startsWith('ngsl')).path_sha256,
  await sha256(ngslProfileText)
);
assert.deepEqual(mweContract.reference_profiles.word.local_import, {
  profile_id: 'bnc-coca-level6-v1.0.0-first-2k-local',
  source_artifact_sha256: 'ac81c7a60e5c76cd2bbf0c59b0501808f0d4fa026b2936919dd54329a9bb6a69',
  generated_profile_size_bytes: 366120,
  generated_profile_sha256: 'ebd06548187988eb1a61ab967cc39c01461023043ee7aef427606e5bf508f138',
  delivery_rule: 'researcher generates and imports the exact profile locally; neither source nor generated profile is bundled, transmitted, or retained by the app',
  special_list_rule: 'basewrd31 proper nouns, basewrd32 marginal words, basewrd33 transparent compounds, and basewrd34 acronyms are excluded'
});
const oewnTakeInSenseIds = [
  'take_in%2:42:00::', 'take_in%2:32:00::', 'take_in%2:43:00::',
  'take_in%2:41:00::', 'take_in%2:40:09::', 'take_in%2:39:06::',
  'take_in%2:35:01::', 'take_in%2:35:00::', 'take_in%2:31:00::',
  'take_in%2:40:00::', 'take_in%2:39:00::', 'take_in%2:35:02::',
  'take_in%2:35:04::', 'take_in%2:34:01::', 'take_in%2:34:00::',
  'take_in%2:30:03::', 'take_in%2:30:00::'
];
assert.equal(oewnSubset.resource.artifact_size_bytes, 9986555);
assert.equal(
  oewnSubset.resource.artifact_sha256,
  '7d749f6e2c39e6970e4997839dcf6e42fd281f3c2fae0171d2192bae8cfa4b51'
);
assert.equal(oewnSubset.projection.entry_id, 'take in#v');
assert.equal(oewnSubset.projection.sense_count, 17);
assert.equal(mweSenseProfile.profile.identity.profile_id, 'oewn-2025-take-in-v');
assert.equal(
  lookupMweSenses('Take   In', mweSenseProfile).state.candidate_sense_ids.length,
  17
);
assert.deepEqual(lookupMweSenses('spill the beans', mweSenseProfile).state, {
  inventory_id: null, inventory_version: null, lookup_status: 'inventory_ineligible',
  candidate_sense_ids: [], assignment_status: 'inventory_ineligible',
  selected_sense_ids: [], decision: {
    source: 'runtime-sense-profile-scope',
    note: 'The current bounded sense projection does not cover spill the beans.'
  }
});
assert.equal(oewnSubset.license.local_notice, 'resources/OEWN_WORDNET_NOTICE.txt');
assert.match(oewnNotice, /WordNet 3\.1 Copyright 2011 by Princeton University/);
assert.deepEqual(oewnSubset.projection.senses.map(sense => sense.sense_id), oewnTakeInSenseIds);
assert.equal(
  oewnSubset.projection.senses.find(sense => sense.sense_id === 'take_in%2:31:00::')
    .definitions[0],
  'take up mentally'
);
assert.equal(
  oewnSubset.projection.senses.find(sense => sense.sense_id === 'take_in%2:32:00::')
    .definitions[0],
  'fool or hoax'
);
const duplicateSenseSubset = structuredClone(oewnSubset);
duplicateSenseSubset.projection.senses[1].sense_id =
  duplicateSenseSubset.projection.senses[0].sense_id;
assert.throws(
  () => prepareMweSenseReferenceProfile(duplicateSenseSubset),
  /sense reference row/
);
assert.deepEqual(
  mweContract.occurrence_record.categories, mweContract.scope.category_scheme.projection
);
assert.deepEqual(
  mweContract.occurrence_record.sense_assignment_statuses,
  [
    'assigned', 'multiple_assigned', 'ambiguous', 'abstained', 'unassigned',
    'out_of_inventory', 'inventory_ineligible'
  ]
);
for (const testCase of mweFixture.cases) {
  assert.deepEqual(summarizeMweDocument(testCase, mweContract), testCase.expected, testCase.id);
}
assert.deepEqual(
  mweFixture.cases.map(testCase => testCase.id.slice(0, 2)),
  ['M1', 'M2', 'M3', 'M4', 'M5']
);
for (const occurrence of mweFixture.cases[2].occurrences) {
  assert.deepEqual(occurrence.sense.candidate_sense_ids, oewnTakeInSenseIds);
  assert.ok(occurrence.sense.decision.source);
}
const pronounContrast = mweFixture.cases[3];
const pronounTokens = new Map(pronounContrast.tokens.map(token => [token.id, token.normalized]));
assert.deepEqual(pronounContrast.occurrences.map(occurrence => occurrence.status), ['confirmed', 'rejected']);
for (const occurrence of pronounContrast.occurrences) {
  assert.deepEqual(occurrence.member_token_ids.map(id => pronounTokens.get(id)), ['took', 'in']);
  assert.deepEqual(occurrence.gap_token_ids.map(id => pronounTokens.get(id)), ['it']);
}
const idiomContrast = mweFixture.cases[4];
assert.deepEqual(idiomContrast.occurrences.map(item => item.category), ['VID', 'VID']);
assert.deepEqual(idiomContrast.occurrences.map(item => item.status), ['confirmed', 'rejected']);
assert.deepEqual(
  idiomContrast.occurrences.map(item => item.idiomaticity.status),
  ['idiomatic', 'literal']
);
assert.equal(idiomContrast.occurrences[0].form_lookup.inventory_id, null);
assert.equal(idiomContrast.occurrences[0].sense.inventory_id, null);
const invalidGapCase = structuredClone(mweFixture.cases[1]);
invalidGapCase.occurrences[0].gap_token_ids = [];
assert.throws(
  () => summarizeMweDocument(invalidGapCase, mweContract),
  /gap tokens do not match/
);
const invalidAbstentionCase = structuredClone(mweFixture.cases[0]);
invalidAbstentionCase.occurrences[0].sense.assignment_status = 'abstained';
assert.throws(
  () => summarizeMweDocument(invalidAbstentionCase, mweContract),
  /lacks matched candidates/
);
for (const [status, selected] of [
  ['multiple_assigned', ['fixture:sense:one', 'fixture:sense:two']],
  ['ambiguous', ['fixture:sense:one', 'fixture:sense:two']],
  ['abstained', []]
]) {
  const stateCase = structuredClone(mweFixture.cases[0]);
  Object.assign(stateCase.occurrences[0].sense, {
    inventory_id: 'fixture-inventory',
    inventory_version: '1',
    lookup_status: 'matched',
    candidate_sense_ids: ['fixture:sense:one', 'fixture:sense:two'],
    assignment_status: status,
    selected_sense_ids: selected,
    decision: {source: 'project-authored-state-test', note: `Exercise ${status} state.`}
  });
  const result = summarizeMweDocument(stateCase, mweContract);
  assert.equal(result.sense_assignment_status_counts[status], 1);
  assert.deepEqual(
    result.sense_assignment_coverage,
    {numerator: status === 'multiple_assigned' ? 1 : 0, denominator: 1,
      value: status === 'multiple_assigned' ? 1 : 0}
  );
}
const outOfInventoryCase = structuredClone(mweFixture.cases[0]);
Object.assign(outOfInventoryCase.occurrences[0].sense, {
  inventory_id: 'fixture-inventory', inventory_version: '1',
  lookup_status: 'out_of_inventory', assignment_status: 'out_of_inventory',
  decision: {source: 'project-authored-state-test', note: 'Complete inventory has no candidate.'}
});
assert.equal(
  summarizeMweDocument(outOfInventoryCase, mweContract)
    .sense_assignment_status_counts.out_of_inventory,
  1
);
const matchedOutOfInventoryCase = structuredClone(mweFixture.cases[0]);
Object.assign(matchedOutOfInventoryCase.occurrences[0].sense, {
  inventory_id: 'fixture-inventory', inventory_version: '1', lookup_status: 'matched',
  candidate_sense_ids: ['fixture:sense:one'], assignment_status: 'out_of_inventory',
  selected_sense_ids: [],
  decision: {source: 'project-authored-state-test', note: 'Shown candidate is inadequate.'}
});
assert.equal(
  summarizeMweDocument(matchedOutOfInventoryCase, mweContract)
    .sense_assignment_status_counts.out_of_inventory,
  1
);
const ineligibleCase = structuredClone(mweFixture.cases[0]);
ineligibleCase.occurrences[0].sense = lookupMweSenses(
  'spill the beans', mweSenseProfile
).state;
assert.equal(
  summarizeMweDocument(ineligibleCase, mweContract)
    .sense_assignment_status_counts.inventory_ineligible,
  1
);
const missingSenseDecisionCase = structuredClone(mweFixture.cases[2]);
missingSenseDecisionCase.occurrences[0].sense.decision = null;
assert.throws(
  () => summarizeMweDocument(missingSenseDecisionCase, mweContract),
  /Sense decision provenance is inconsistent/
);
const missingIdiomaticityDecisionCase = structuredClone(mweFixture.cases[4]);
missingIdiomaticityDecisionCase.occurrences[0].idiomaticity.decision = null;
assert.throws(
  () => summarizeMweDocument(missingIdiomaticityDecisionCase, mweContract),
  /Idiomaticity decision provenance is inconsistent/
);
const inventedInventoryCase = structuredClone(mweFixture.cases[4]);
Object.assign(inventedInventoryCase.occurrences[0].form_lookup, {
  inventory_id: 'not-actually-used', inventory_version: '1'
});
assert.throws(
  () => summarizeMweDocument(inventedInventoryCase, mweContract),
  /Form inventory identity is inconsistent/
);
const unresolvedCase = structuredClone(mweFixture.cases[3]);
Object.assign(unresolvedCase.occurrences[1], {status: 'candidate', decision: null});
const unresolvedResult = summarizeMweDocument(unresolvedCase, mweContract);
assert.equal(unresolvedResult.unresolved_occurrence_count, 1);
assert.deepEqual(
  unresolvedResult.occurrence_annotation_coverage,
  {numerator: 1, denominator: 2, value: 0.5}
);

assert.equal(sampleDocument.samples_version, '0.4.0-probe');
assert.equal(sampleDocument.comparison_sets.length, 3);
const sets = Object.fromEntries(sampleDocument.comparison_sets.map(set => [set.id, set]));
const samples = sampleDocument.comparison_sets.flatMap(set => set.samples);
// The public examples enter the real candidate/save/restore flow without gold labels.
assert.equal(sampleDocument.mwe_examples.length, 5);
const examplePatterns = 'VPC.full\ttake in\ttake/takes/took/taken/taking in\t4\nVID\tspill the beans\tspill/spills/spilled/spilling bean/beans\t2';
for (const example of sampleDocument.mwe_examples) {
  assert.equal(await sha256(example.text), example.provenance.text_sha256);
  assert.ok(!('occurrences' in example) && !('senses' in example));
  assert.ok(example.label_en && example.prompt_en);
  if (example.provenance.kind === 'project_authored') {
    assert.equal(example.text, mweFixture.cases.find(item => item.id === example.id).text);
    assert.equal(example.provenance.license, 'MIT OR CC-BY-4.0');
  } else {
    assert.equal(example.provenance.kind, 'tatoeba_cc0');
    assert.equal(example.provenance.license, 'CC0-1.0');
    assert.equal(example.provenance.source_url, `https://tatoeba.org/en/sentences/show/${example.id.slice(8)}`);
    assert.match(example.provenance.source_artifact_sha256, /^[a-f0-9]{64}$/);
  }
  const document = {text: example.text, ...findMweCandidates(example.text,
    parseMwePatternTsv(examplePatterns, mweContract.occurrence_record.categories))};
  assert.ok(document.occurrences.length);
  assert.ok(document.occurrences.every(item => item.status === 'candidate' && item.decision === null));
  const saved = await makeMweWorkspaceRecord({document, contract: mweContract,
    patternSource: examplePatterns, authorizationAttested: true, savedAt: '2026-09-07T00:00:00.000Z',
    wordProfileKey: 'tubelex', wordProfile, wordRankCutoff: null, mweFormProfile, mweSenseProfile});
  const restored = await restoreMweWorkspaceRecord({record: saved, contract: mweContract,
    authorizationAttested: true, wordProfileKey: 'tubelex', wordProfile, wordRankCutoff: null,
    mweFormProfile, mweSenseProfile});
  assert.deepEqual(restored.document, document);
}

{
  const source = readFileSync(new URL('../app.mjs', import.meta.url), 'utf8');
  const fields = new Map();
  const control = id => {
    if (!fields.has(id)) fields.set(id, {value: '', defaultValue: '', checked: false, focus() {}});
    return fields.get(id);
  };
  let accept = false, prompts = 0, refreshed = 0;
  const context = {document: {getElementById: control}, mweExamples: sampleDocument.mwe_examples,
    mweDocument: null, mweRevision: 0, mweStatus: {textContent: ''},
    window: {confirm() { prompts++; return accept; }},
    updateMwePendingEdits() { refreshed++; }};
  runInNewContext(source.slice(source.indexOf('function loadMweExample()'),
    source.indexOf("document.getElementById('mwe-example').addEventListener")), context);
  control('mwe-example').value = sampleDocument.mwe_examples[0].id;
  control('mwe-patterns').defaultValue = examplePatterns;
  control('mwe-patterns').value = 'Unfinished pattern draft';
  control('mwe-text').value = 'Unfinished text';
  control('mwe-authorization').checked = true;
  control('word-reference').value = 'ngsl-1000';
  context.loadMweExample();
  assert.equal(control('mwe-text').value, 'Unfinished text');
  assert.equal(control('mwe-patterns').value, 'Unfinished pattern draft');
  assert.equal(context.mweRevision, 0);
  accept = true;
  context.loadMweExample();
  assert.equal(control('mwe-text').value, sampleDocument.mwe_examples[0].text);
  assert.equal(control('mwe-patterns').value, examplePatterns);
  assert.equal(control('mwe-authorization').checked, false);
  assert.equal(control('word-reference').value, 'ngsl-1000');
  assert.equal(context.mweRevision, 1);
  assert.equal(refreshed, 1);
  context.mweDocument = {text: 'A review to preserve'};
  context.loadMweExample();
  assert.equal(prompts, 2, 'An active review cannot be replaced even after a confirmed draft replacement');
  assert.equal(context.mweDocument.text, 'A review to preserve');
  assert.equal(context.mweRevision, 1);
}
for (const sample of samples) {
  assert.deepEqual(analyze(sample.text), sample.result, sample.id);
}

const [repeated, varied] = sets['matched-repetition'].samples;
const [repeatedTokens, variedTokens] = [repeated, varied].map(sample => tokenize(sample.text));
assert.equal(
  repeatedTokens.filter((token, index) => token !== variedTokens[index]).length,
  38,
  'matched-pair changed token positions'
);
assert.equal(
  Math.round((varied.result.type_token_ratio - repeated.result.type_token_ratio) * 100),
  varied.result.types - repeated.result.types,
  'TTR difference is the type-count difference divided by 100'
);

const [oneSentence, sevenSentences] = sets['segmentation-invariance'].samples;
assert.deepEqual(tokenize(oneSentence.text), tokenize(sevenSentences.text));
assert.deepEqual(oneSentence.result, sevenSentences.result);
assert.equal((oneSentence.text.match(/[.!?]+/g) || []).length, 1);
assert.equal((sevenSentences.text.match(/[.!?]+/g) || []).length, 7);

const [short, full] = sets['nested-length'].samples;
assert.deepEqual(tokenize(full.text).slice(0, short.result.tokens), tokenize(short.text));
assert.notEqual(short.result.type_token_ratio, full.result.type_token_ratio);

assert.equal(
  await sha256('abc'),
  'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad'
);
assert.deepEqual(parseBatchJson('[{"id":"one"}]', 100), [{id: 'one'}]);
assert.deepEqual(parseJsonInput('{"local":true}', 100, 'Local profile'), {local: true});
assert.throws(() => parseBatchJson('[]', 1), /Batch JSON exceeds/);
assert.throws(() => parseBatchJson('{', 100), /not valid JSON/);
assert.throws(() => parseBatchJson('\uD800', 100), /unpaired Unicode surrogate/);
await assert.rejects(() => sha256('\uD800'), /unpaired Unicode surrogate/);
const exportRecord = await makeExportRecord({
  contract,
  relationship: 'paired',
  designNote: 'Same 100-token template with 38 matched lexical substitutions.',
  contentScopeAttested: true,
  generatedAt: '2026-09-01T00:00:00.000Z',
  inputs: [
    {
      id: 'a', label: 'Repeated', provenance: 'project-authored synthetic',
      text: repeated.text
    },
    {
      id: 'b', label: 'Varied', provenance: 'project-authored synthetic',
      text: varied.text
    }
  ]
});
assert.equal(exportRecord.inputs.length, 2);
assert.equal(
  exportRecord.relationship_meaning, contract.workspace.relationship_meanings.paired
);
assert.equal(exportRecord.content_scope_attested, true);
assert.equal(exportRecord.attestation_scope, contract.workspace.required_attestation);
assert.equal(exportRecord.generated_at, '2026-09-01T00:00:00.000Z');
assert.match(contract.workspace.record_timestamp, /not a trusted timestamp/);
assert.equal(exportRecord.method.project_license, 'MIT OR CC-BY-4.0');
assert.equal(exportRecord.method.claims, 'descriptive-only');
assert.deepEqual(exportRecord.method.excluded_inferences, contract.scope.excluded_inferences);
assert.deepEqual(exportRecord.method.limitations, contract.limitations);
assert.deepEqual(exportRecord.method.external_resource_dependencies, []);
assert.deepEqual(exportRecord.method.method_references, contract.method_references);
assert.deepEqual(exportRecord.method.metric_reference_ids, contract.metric_reference_ids);
assert.equal(exportRecord.method.reference_scope, contract.reference_scope);
for (const [metric, referenceIds] of Object.entries(contract.metric_reference_ids)) {
  assert.ok(Object.hasOwn(contract.metrics, metric));
  for (const referenceId of referenceIds) {
    const reference = contract.method_references[referenceId];
    assert.ok(reference, `Missing method reference: ${referenceId}`);
    assert.equal(reference.url, `https://doi.org/${reference.doi}`);
  }
}
assert.equal(contract.metric_reference_ids.type_token_ratio.length, 2);
assert.deepEqual(exportRecord.inputs.map(input => input.result), [repeated.result, varied.result]);
assert.equal(exportRecord.difference_second_minus_first.tokens, 0);
assert.equal(exportRecord.difference_second_minus_first.types, 24);
assert.equal(exportRecord.difference_second_minus_first.type_token_ratio, 0.24);
assert.ok(
  exportRecord.warning_codes.includes('types-and-ttr-algebraically-dependent-at-fixed-length')
);
for (const input of exportRecord.inputs) {
  assert.equal(input.raw_text_included, false);
  assert.ok(!Object.hasOwn(input, 'text'));
  assert.match(input.sha256_utf8, /^[0-9a-f]{64}$/);
}
for (const warningCode of exportRecord.warning_codes) {
  assert.ok(contract.workspace.warning_codes.includes(warningCode));
  assert.ok(contract.workspace.warning_meanings_ja[warningCode]);
  assert.equal(
    exportRecord.warning_meanings_ja[warningCode],
    contract.workspace.warning_meanings_ja[warningCode]
  );
}
assert.deepEqual(Object.keys(exportRecord.warning_meanings_ja), exportRecord.warning_codes);
assert.deepEqual(
  Object.keys(contract.workspace.warning_meanings_ja),
  contract.workspace.warning_codes
);
assert.ok(!JSON.stringify(exportRecord).includes(repeated.text));
const singleRecord = await makeExportRecord({
  contract,
  relationship: 'single',
  designNote: 'One project-authored tokenizer boundary example.',
  contentScopeAttested: true,
  generatedAt: '2026-09-01T00:00:00.000Z',
  inputs: [{id: 'a', label: 'No ASCII tokens', provenance: 'synthetic', text: '日本語'}]
});
assert.equal(singleRecord.difference_second_minus_first, null);
assert.ok(singleRecord.warning_codes.includes('no-recognized-tokens'));
const independentRecord = await makeExportRecord({
  contract,
  relationship: 'independent',
  designNote: 'Two separately interpreted text spans for a warning-path check.',
  contentScopeAttested: true,
  generatedAt: '2026-09-01T00:00:00.000Z',
  inputs: [
    {id: 'a', label: 'Short', provenance: 'synthetic', text: short.text},
    {id: 'b', label: 'Full', provenance: 'synthetic', text: full.text}
  ]
});
assert.ok(independentRecord.warning_codes.includes('cross-length-difference-confounded'));
assert.ok(independentRecord.warning_codes.includes('independent-texts-not-causal'));
const declaredText = 'One word.\nOne one.\n\nThree four five.';
const declaredAnalysis = analyzeDeclaredSegments(
  declaredText, contract.input.max_declared_segments_per_text
);
assert.equal(declaredAnalysis.segment_count, 3);
assert.deepEqual(
  declaredAnalysis.segments.map(segment => segment.result.tokens), [2, 2, 3]
);
assert.deepEqual(
  declaredAnalysis.distribution.type_token_ratio,
  {minimum: 0.5, median: 1, maximum: 1}
);
const declaredRecord = await makeExportRecord({
  contract,
  relationship: 'declared-segments',
  designNote: 'Each non-empty line is a researcher-declared unit in one document.',
  contentScopeAttested: true,
  generatedAt: '2026-09-01T00:00:00.000Z',
  inputs: [{id: 'a', label: 'Three units', provenance: 'synthetic', text: declaredText}]
});
assert.equal(declaredRecord.inputs.length, 1);
assert.equal(declaredRecord.difference_second_minus_first, null);
assert.equal(declaredRecord.declared_segment_analysis.segment_count, 3);
assert.ok(declaredRecord.warning_codes.includes('segments-not-independent-observations'));
assert.ok(!JSON.stringify(declaredRecord).includes(declaredText));
const batchInputs = [
  {id: ' d1 ', label: 'Document 1', provenance: 'synthetic', text: 'amber cobalt'},
  {id: 'd2', label: 'Document 2', provenance: 'synthetic', text: 'dune ember ember'},
  {id: 'd3', label: 'Document 3', provenance: 'synthetic', text: 'frost glade haze iris'}
];
const batchRecord = await makeExportRecord({
  contract,
  relationship: 'batch',
  designNote: 'Three project-authored documents; dependence is not assumed.',
  contentScopeAttested: true,
  generatedAt: '2026-09-01T00:00:00.000Z',
  inputs: batchInputs
});
assert.deepEqual(batchRecord.inputs.map(input => input.id), ['d1', 'd2', 'd3']);
assert.deepEqual(
  batchRecord.inputs.map(input => input.result), batchInputs.map(input => analyze(input.text))
);
assert.equal(batchRecord.difference_second_minus_first, null);
assert.equal(batchRecord.declared_segment_analysis, null);
assert.equal(batchRecord.batch_analysis.document_count, 3);
assert.deepEqual(
  batchRecord.batch_analysis.distribution.tokens,
  {minimum: 2, median: 3, maximum: 4}
);
assert.ok(batchRecord.warning_codes.includes('batch-documents-not-independent'));
assert.ok(batchRecord.warning_codes.includes('batch-summary-unweighted'));
for (const input of batchInputs) assert.ok(!JSON.stringify(batchRecord).includes(input.text));
await assert.rejects(
  async () => makeExportRecord({
    contract,
    relationship: 'declared-segments',
    designNote: 'Too many declared lines.',
    contentScopeAttested: true,
    generatedAt: '2026-09-01T00:00:00.000Z',
    inputs: [{
      id: 'a', label: 'Too many', provenance: 'synthetic',
      text: Array(1001).fill('word').join('\n')
    }]
  }),
  /Declared-segment count exceeds/
);
await assert.rejects(
  async () => makeExportRecord({
    contract,
    relationship: 'batch',
    designNote: 'Duplicate identifier check.',
    contentScopeAttested: true,
    generatedAt: '2026-09-01T00:00:00.000Z',
    inputs: [batchInputs[0], {...batchInputs[1], id: 'd1'}]
  }),
  /Duplicate input ID: d1/
);
await assert.rejects(
  async () => makeExportRecord({
    contract,
    relationship: 'paired',
    designNote: 'Duplicate paired identifier check.',
    contentScopeAttested: true,
    generatedAt: '2026-09-01T00:00:00.000Z',
    inputs: [batchInputs[0], {...batchInputs[1], id: 'd1'}]
  }),
  /Duplicate input ID: d1/
);
await assert.rejects(
  async () => makeExportRecord({
    contract,
    relationship: 'batch',
    designNote: 'Zero-token document check.',
    contentScopeAttested: true,
    generatedAt: '2026-09-01T00:00:00.000Z',
    inputs: [batchInputs[0], {id: 'zero', label: 'Zero', provenance: 'synthetic', text: '日本語'}]
  }),
  /Batch document has no recognized tokens: zero/
);
await assert.rejects(
  async () => makeExportRecord({
    contract: {
      ...contract,
      input: {...contract.input, max_combined_utf16_code_units_per_batch: 5}
    },
    relationship: 'batch',
    designNote: 'Combined-size check.',
    contentScopeAttested: true,
    generatedAt: '2026-09-01T00:00:00.000Z',
    inputs: [
      {id: 'one', label: 'One', provenance: 'synthetic', text: 'one'},
      {id: 'two', label: 'Two', provenance: 'synthetic', text: 'two'}
    ]
  }),
  /Combined batch text exceeds/
);
await assert.rejects(
  async () => makeExportRecord({
    contract,
    relationship: 'batch',
    designNote: 'Count check.',
    contentScopeAttested: true,
    generatedAt: '2026-09-01T00:00:00.000Z',
    inputs: [batchInputs[0]]
  }),
  /Batch document count exceeds/
);
await assert.rejects(
  async () => makeExportRecord({
    contract,
    relationship: 'single',
    designNote: 'Attestation boundary check.',
    contentScopeAttested: false,
    generatedAt: '2026-09-01T00:00:00.000Z',
    inputs: [{id: 'a', label: 'One', provenance: 'synthetic', text: 'word'}]
  }),
  /Content-scope attestation is required/
);
await assert.rejects(
  async () => makeExportRecord({
    contract,
    relationship: 'single',
    designNote: 'Unicode identity check.',
    contentScopeAttested: true,
    generatedAt: '2026-09-01T00:00:00.000Z',
    inputs: [{
      id: 'unicode', label: 'Unicode', provenance: 'synthetic', text: `word${'\uD800'}`
    }]
  }),
  /unpaired Unicode surrogate/
);
await assert.rejects(
  async () => makeExportRecord({
    contract,
    relationship: 'single',
    designNote: 'Timestamp format check.',
    contentScopeAttested: true,
    generatedAt: '2026-09-01T00:00:00Z',
    inputs: [{id: 'time', label: 'Time', provenance: 'synthetic', text: 'word'}]
  }),
  /exact UTC ISO string/
);
await assert.rejects(
  async () => makeExportRecord({
    contract, relationship: 'group', designNote: 'test', contentScopeAttested: true,
    inputs: [], generatedAt: 'x'
  }),
  /Unsupported comparison relationship/
);

// Page-exit protection shares one warning across raw drafts, reviews and sets.
{
  const source = readFileSync(new URL('../app.mjs', import.meta.url), 'utf8');
  const start = source.indexOf('function warnOnPageExit(');
  assert.ok(start >= 0, 'Page exit must protect in-memory work');
  const events = new Map(), queued = [], timers = [];
  const form = () => ({
    fields: [{value: '', defaultValue: ''}], handlers: new Map(),
    querySelectorAll(selector) {
      assert.equal(selector, 'input[type="text"], textarea:not([readonly])');
      return this.fields;
    },
    addEventListener(type, callback) { this.handlers.set(type, callback); }
  });
  const forms = [form(), form(), form()];
  const context = {
    mweForm: forms[0], mweDocumentSetForm: forms[1], workspaceForm: forms[2],
    mweDocument: null, currentExport: null, mweDocumentSet: new Map(),
    queueMicrotask: callback => queued.push(callback),
    setTimeout: callback => timers.push(callback),
    window: {
      addEventListener: (type, callback) => events.set(type, callback),
      removeEventListener: (type, callback) => {
        if (events.get(type) === callback) events.delete(type);
      }
    }
  };
  runInNewContext(source.slice(start, source.indexOf('function downloadText(')) +
    source.slice(source.indexOf('// Refresh after form handlers and native reset defaults.'),
      source.lastIndexOf('initialize();')), context);
  const microtasks = () => { while (queued.length) queued.shift()(); };
  const refresh = () => { microtasks(); while (timers.length) { timers.shift()(); microtasks(); } };
  const warns = () => events.has('beforeunload');
  context.updatePageExitWarning();
  assert.equal(warns(), false, 'An empty page must not install a warning');
  forms[0].fields.push({value: 'Default pattern', defaultValue: 'Default pattern'});
  for (const f of forms) {
    for (const type of ['input', 'change', 'submit']) {
      f.fields[0].value = 'Synthetic draft';
      f.handlers.get(type)(); refresh();
      assert.equal(warns(), true);
      const event = {preventDefault() { this.prevented = true; }};
      events.get('beforeunload')(event);
      assert.equal(event.prevented, true);
      assert.equal(event.returnValue, true);
      assert.equal(f.fields[0].value, 'Synthetic draft', 'Asking to leave cannot clear work');
      f.handlers.get('reset')();
      microtasks(); // A listener checkpoint can precede the native reset defaults.
      f.fields[0].value = ''; // Native reset happens after the event handlers.
      refresh();
      assert.equal(warns(), false, 'Remove the listener after work is cleared');
    }
  }
  for (const key of ['mweDocument', 'currentExport']) {
    context[key] = {synthetic: true};
    context.updatePageExitWarning();
    assert.equal(warns(), true, 'Programmatically restored work must also be protected');
    context[key] = null;
    context.updatePageExitWarning();
    assert.equal(warns(), false);
  }
  context.mweDocumentSet.set('synthetic', {});
  context.updatePageExitWarning();
  assert.equal(warns(), true, 'A set is at risk even without an open review');
  context.mweDocumentSet.clear();
  context.updatePageExitWarning();
  assert.equal(warns(), false);
  assert.match(source, /function updateMwePendingEdits\(\) \{\s+updatePageExitWarning\(\);/,
    'Async review/set rendering must refresh the warning too');
}

// Exercise the actual app's synchronous submit/reset guards without a DOM library.
// This is an event-handler regression check, not a browser rendering test.
{
  const appSource = readFileSync(new URL('../app.mjs', import.meta.url), 'utf8');
  const controls = new Map();
  const control = id => {
    if (!controls.has(id)) controls.set(id, {value: '', disabled: false, children: [],
      replaceChildren(...children) { this.children = children; }});
    return controls.get(id);
  };
  const handlers = new Map();
  let renderCount = 0;
  let allowReset = false;
  let resetPrompts = 0;
  const context = {
    document: {getElementById: control},
    mweForm: {addEventListener: (event, handler) => handlers.set(event, handler)},
    mweStatus: {textContent: ''}, mweResults: {hidden: true},
    mweDocument: null, mweContract, mweDocumentDirty: false,
    clearingOnPageExit: false, mweRevision: 0,
    window: {confirm() { resetPrompts += 1; return allowReset; }},
    updateMwePendingEdits() {},
    pendingMweEdits: () => [],
    wordProfiles: new Map([['tubelex', {profile: wordProfile, maximumRank: null}]]),
    parseMwePatternTsv, findMweCandidates, analyzeWordCoverage,
    renderMweReview() { renderCount += 1; context.lockMweSourceInputs(true); }
  };
  runInNewContext(
    appSource.slice(appSource.indexOf('function lockMweSourceInputs('),
      appSource.indexOf('function reviewedOccurrence(')) +
    appSource.slice(appSource.indexOf('function invalidateMweReview('),
      appSource.indexOf('function describeMweExample(')) +
    appSource.slice(appSource.indexOf("mweForm.addEventListener('submit'"),
      appSource.indexOf("for (const id of ['mwe-text', 'mwe-patterns', 'mwe-authorization']")),
    context
  );
  control('mwe-text').value = 'She took it in.';
  control('mwe-patterns').value = 'VPC.full\ttake in\ttake/takes/took/taken/taking in\t4';
  control('word-reference').value = 'tubelex';
  control('mwe-authorization').checked = true;
  let prevented = 0;
  const submit = () => handlers.get('submit')({preventDefault() { prevented += 1; }});
  submit();
  assert.equal(renderCount, 1);
  assert.equal(context.mweDocument.occurrences.length, 1);
  assert.equal(control('mwe-analyze-button').disabled, true);
  context.mweDocument.occurrences[0].decision = {note: 'Preserve this synthetic judgment.'};
  for (const existing of [context.mweDocument, structuredClone(context.mweDocument)]) {
    context.mweDocument = existing; // Existing and restored review states.
    const before = JSON.stringify(existing);
    control('word-reference').value = 'unavailable'; // Must not reach the error-reset path.
    submit();
    assert.equal(context.mweDocument, existing);
    assert.equal(JSON.stringify(context.mweDocument), before);
    assert.match(context.mweStatus.textContent, /再抽出しませんでした/);
  }
  assert.equal(renderCount, 1);
  assert.equal(prevented, 3);
  const reviewOutputs = ['mwe-occurrences', 'mwe-token-picker', 'mwe-summary'];
  const discardedControl = {validationMessage: 'Synthetic invalid review field'};
  for (const id of reviewOutputs) control(id).replaceChildren(discardedControl);
  control('word-coverage-items').value = 'Synthetic previous coverage';
  const beforeCancelledReset = JSON.stringify(context.mweDocument);
  const revisionBeforeReset = context.mweRevision;
  let resetCancelled = false;
  handlers.get('reset')({preventDefault() { resetCancelled = true; }});
  assert.equal(resetCancelled, true);
  assert.equal(context.mweRevision, revisionBeforeReset, 'Cancelled reset must not cancel pending work');
  assert.equal(JSON.stringify(context.mweDocument), beforeCancelledReset);
  assert.equal(control('mwe-analyze-button').disabled, true);
  for (const id of reviewOutputs) assert.equal(control(id).children[0], discardedControl);
  assert.equal(control('word-coverage-items').value, 'Synthetic previous coverage');
  allowReset = true;
  handlers.get('reset')();
  assert.equal(context.mweDocument, null);
  assert.ok(context.mweRevision > revisionBeforeReset);
  assert.equal(context.mweResults.hidden, true);
  assert.equal(control('mwe-analyze-button').disabled, false);
  for (const id of reviewOutputs) assert.equal(control(id).children.length, 0,
    'Confirmed reset must detach the previous review, including invalid controls');
  assert.equal(control('word-coverage-items').value, '');
  // Source invalidation and extraction failure must use the same cleanup path.
  for (const reason of ['source-change', 'extraction-error']) {
    for (const id of reviewOutputs) control(id).replaceChildren(discardedControl);
    control('word-coverage-items').value = 'Stale coverage';
    if (reason === 'source-change') {
      context.mweDocument = {};
      context.invalidateMweReview();
    } else {
      control('word-reference').value = 'unavailable';
      submit();
    }
    assert.equal(context.mweDocument, null);
    for (const id of reviewOutputs) assert.equal(control(id).children.length, 0, reason);
    assert.equal(control('word-coverage-items').value, '');
  }
  control('word-reference').value = 'tubelex';
  submit();
  assert.equal(renderCount, 2);
  assert.equal(control('mwe-analyze-button').disabled, true);

  // Review commits may update their own card, never rebuild sibling controls.
  // Any full render here fails because this harness has no DOM creation API.
  let cardReplacements = 0;
  let senseReplacements = 0;
  let focused = false;
  const card = {
    contains: element => element.card === card,
    replaceWith() { cardReplacements += 1; },
    querySelector() { return {replaceWith() { senseReplacements += 1; }}; }
  };
  const note = {
    value: '  Synthetic review note.  ', setCustomValidity() {}, reportValidity() {},
    closest() { return card; }
  };
  Object.assign(context, {
    structuredClone, lookupMweForm, lookupMweSenses, mweFormProfile, mweSenseProfile,
    summarizeMweDocument, summarizeMweFormCoverage,
    fillDefinitionList() {}, ratioText: item => JSON.stringify(item),
    occurrenceCard: item => item, senseReview: item => item
  });
  runInNewContext(
    appSource.slice(appSource.indexOf('function reviewedOccurrence('),
      appSource.indexOf('function idiomaticityReview(')) +
    appSource.slice(appSource.indexOf('function renderMweReview('),
      appSource.indexOf('function invalidateMweReview(')),
    context
  );
  const occurrenceId = context.mweDocument.occurrences[0].id;
  control(`decision-${occurrenceId}-confirmed`).focus = () => { focused = true; };
  context.setMweDecision(occurrenceId, 'confirmed', note);
  assert.equal(cardReplacements, 1);
  assert.equal(focused, true);
  note.value = '  Synthetic idiomaticity note.  ';
  context.setIdiomaticity(occurrenceId, {value: 'idiomatic'}, note);
  assert.equal(senseReplacements, 0);
  assert.equal(note.value, 'Synthetic idiomaticity note.');
  note.value = 'Synthetic abstention note.';
  context.setSenseDecision(
    occurrenceId, {value: 'abstained', setCustomValidity() {}},
    {querySelectorAll: () => []}, note
  );
  assert.equal(context.mweDocument.occurrences[0].sense.assignment_status, 'abstained');

  // A corrected field must not keep an old error when another field now fails.
  const validationControl = value => ({
    value, validationMessage: '',
    setCustomValidity(message) { this.validationMessage = message; },
    reportValidity() { return !this.validationMessage; }
  });
  const senseBeforeValidation = structuredClone(context.mweDocument.occurrences[0].sense);
  const senseIds = senseBeforeValidation.candidate_sense_ids;
  for (const [value, count] of [['assigned', 1], ['multiple_assigned', 2],
    ['ambiguous', 2], ['abstained', 0], ['out_of_inventory', 0]]) {
    const state = validationControl(value);
    const reason = validationControl('');
    const selected = {querySelectorAll: () => senseIds.slice(0, count === 0 ? 1 : count - 1)
      .map(value => ({value}))};
    const before = JSON.stringify({document: context.mweDocument, revision: context.mweRevision});
    context.setSenseDecision(occurrenceId, state, selected, reason);
    assert.notEqual(state.validationMessage, '');
    selected.querySelectorAll = () => senseIds.slice(0, count).map(value => ({value}));
    context.setSenseDecision(occurrenceId, state, selected, reason);
    assert.equal(state.validationMessage, '', 'The corrected sense count must not retain its old error');
    assert.notEqual(reason.validationMessage, '');
    reason.value = 'Synthetic validation recovery.';
    selected.querySelectorAll = () => senseIds.slice(0, count === 0 ? 1 : count - 1).map(value => ({value}));
    context.setSenseDecision(occurrenceId, state, selected, reason);
    assert.notEqual(state.validationMessage, '');
    assert.equal(reason.validationMessage, '', 'A corrected reason must not retain its old error');
    assert.equal(JSON.stringify({document: context.mweDocument, revision: context.mweRevision}), before,
      'Invalid attempts must not change any recorded decision or revision');
    selected.querySelectorAll = () => senseIds.slice(0, count).map(value => ({value}));
    context.setSenseDecision(occurrenceId, state, selected, reason);
    assert.equal(state.validationMessage, '');
    assert.equal(reason.validationMessage, '');
    assert.equal(context.mweDocument.occurrences[0].sense.assignment_status, value);
  }
  context.mweDocument.occurrences[0].sense = senseBeforeValidation;
  const beforeClearingIdiomaticity = JSON.stringify(context.mweDocument);
  allowReset = false;
  context.setIdiomaticity(occurrenceId, {value: 'not_assessed'}, note);
  assert.equal(JSON.stringify(context.mweDocument), beforeClearingIdiomaticity,
    'Canceling a destructive idiomaticity change must preserve recorded decisions');
  allowReset = true;
  note.value = 'Updated occurrence note.';
  context.setMweDecision(occurrenceId, 'confirmed', note);
  note.value = 'Updated idiomaticity note.';
  context.setIdiomaticity(occurrenceId, {value: 'literal'}, note);
  assert.equal(cardReplacements, 1, 'Same-status edits must preserve existing controls');
  assert.equal(senseReplacements, 0, 'Idiomaticity edits must never rebuild independent sense controls');
  note.value = 'Discard when returning to unassigned.';
  context.setSenseDecision(
    occurrenceId, {value: 'unassigned', setCustomValidity() {}},
    {querySelectorAll: () => []}, note
  );
  assert.equal(note.value, '');
  assert.equal(context.mweDocument.occurrences[0].sense.decision, null);

  // Destructive changes must be cancellable before touching the model or controls.
  const baseline = structuredClone(context.mweDocument);
  baseline.occurrences[0].sense.assignment_status = 'assigned';
  baseline.occurrences[0].sense.selected_sense_ids = [baseline.occurrences[0].sense.candidate_sense_ids[0]];
  baseline.occurrences[0].sense.decision = {source: 'synthetic-review', note: 'Recorded sense rationale.'};
  const snapshot = () => JSON.stringify({document: context.mweDocument,
    revision: context.mweRevision, dirty: context.mweDocumentDirty,
    note: note.value, cardReplacements, senseReplacements});
  for (const status of ['candidate', 'rejected']) control(`decision-${occurrenceId}-${status}`).focus = () => {};
  for (const change of [
    () => context.setMweDecision(occurrenceId, 'candidate', note),
    () => context.setMweDecision(occurrenceId, 'rejected', note),
    () => context.setIdiomaticity(occurrenceId, {value: 'not_assessed'}, note),
    () => context.setSenseDecision(occurrenceId, {value: 'unassigned', setCustomValidity() {}},
      {querySelectorAll: () => []}, note)
  ]) {
    context.mweDocument = structuredClone(baseline);
    context.mweDocumentDirty = false;
    note.value = 'Pending rationale.';
    allowReset = false;
    const before = snapshot();
    const prompts = resetPrompts;
    change();
    assert.equal(resetPrompts, prompts + 1);
    assert.equal(snapshot(), before, 'Cancel must preserve the recorded model, draft, revision and render state');
  }
  allowReset = true;
  context.mweDocument = structuredClone(baseline);
  context.setIdiomaticity(occurrenceId, {value: 'not_assessed'}, note);
  assert.equal(context.mweDocument.occurrences[0].idiomaticity.status, 'not_assessed');
  assert.deepEqual(context.mweDocument.occurrences[0].sense, baseline.occurrences[0].sense);
  assert.equal(senseReplacements, 0, 'Clearing idiomaticity must not hide or rebuild sense controls');
  const independentRecord = await makeMweWorkspaceRecord({
    document: context.mweDocument, contract: mweContract, patternSource: control('mwe-patterns').value,
    authorizationAttested: true, savedAt: '2026-09-01T00:00:00.000Z', wordProfileKey: 'tubelex',
    wordProfile, wordRankCutoff: null, mweFormProfile, mweSenseProfile
  });
  assert.deepEqual((await restoreMweWorkspaceRecord({
    record: independentRecord, contract: mweContract, authorizationAttested: true,
    wordProfileKey: 'tubelex', wordProfile, wordRankCutoff: null, mweFormProfile, mweSenseProfile
  })).document, structuredClone(context.mweDocument), 'An independent saved sense must survive resume');
  context.mweDocument = structuredClone(baseline);
  context.setSenseDecision(occurrenceId, {value: 'unassigned', setCustomValidity() {}},
    {querySelectorAll: () => []}, note);
  assert.equal(context.mweDocument.occurrences[0].sense.decision, null);
  assert.deepEqual(context.mweDocument.occurrences[0].idiomaticity, baseline.occurrences[0].idiomaticity);
  context.mweDocument = structuredClone(baseline);
  note.value = 'Revised occurrence rationale.';
  context.setMweDecision(occurrenceId, 'rejected', note);
  assert.equal(context.mweDocument.occurrences[0].sense, null);
  assert.deepEqual(context.mweDocument.occurrences[0].idiomaticity, baseline.occurrences[0].idiomaticity);
  // A sibling draft must not prompt; a draft in the rebuilt card must prompt.
  const localDraft = {card};
  context.pendingMweEdits = () => [{control: localDraft}];
  allowReset = false;
  const beforeLocalDraft = snapshot();
  context.setMweDecision(occurrenceId, 'confirmed', note);
  assert.equal(snapshot(), beforeLocalDraft);
  const promptsWithLocalDraft = resetPrompts;
  context.pendingMweEdits = () => [{control: {card: {}}}];
  context.setMweDecision(occurrenceId, 'confirmed', note);
  assert.equal(resetPrompts, promptsWithLocalDraft, 'Do not prompt for unaffected sibling drafts');
  assert.equal(context.mweDocument.occurrences[0].status, 'confirmed');
  context.pendingMweEdits = () => [];
  allowReset = true;
  context.setMweDecision(occurrenceId, 'candidate', note);
  assert.equal(context.mweDocument.occurrences[0].decision, null);
  assert.equal(context.mweDocument.occurrences[0].sense, null);
  assert.equal(context.mweDocument.occurrences[0].idiomaticity.status, 'not_assessed');
  note.value = 'Draft on an unresolved candidate.';
  allowReset = false;
  const beforeUnresolvedDraft = snapshot();
  context.setMweDecision(occurrenceId, 'candidate', note);
  assert.equal(snapshot(), beforeUnresolvedDraft);

  // Exercise the real delete callback, including cancellation and sibling retention.
  let deleteCandidate;
  let removed = false;
  let focusedAfterDelete = false;
  context.mweDocument = structuredClone(reviewedDocument);
  context.currentWordCoverage = analyzeWordCoverage(reviewedDocument.text, wordProfile, null);
  Object.assign(context, {
    occurrence: context.mweDocument.occurrences[0],
    remove: {addEventListener: (_, handler) => { deleteCandidate = handler; }},
    article: {remove() { removed = true; },
      nextElementSibling: {querySelector: () => ({focus() { focusedAfterDelete = true; }})}}
  });
  runInNewContext(appSource.slice(appSource.indexOf("  remove.addEventListener('click'"),
    appSource.indexOf('  actions.append(remove)')), context);
  const beforeDelete = snapshot();
  deleteCandidate();
  assert.equal(snapshot(), beforeDelete);
  assert.equal(removed, false);
  assert.equal(focusedAfterDelete, false);
  allowReset = true;
  deleteCandidate();
  assert.equal(removed, true);
  assert.equal(focusedAfterDelete, true);
  assert.deepEqual(structuredClone(context.mweDocument.occurrences), [reviewedDocument.occurrences[1]]);

  const workspaceHandlers = new Map();
  const pageEvents = new Map();
  const basicInput = {value: 'Unsaved basic text.', defaultValue: ''};
  Object.assign(context, {
    currentExport: {synthetic: true}, analysisRevision: 0,
    exportButton: {disabled: false}, workspaceResults: {hidden: false}, workspaceStatus: {},
    workspaceForm: {
      querySelectorAll: () => [basicInput],
      addEventListener: (event, handler) => workspaceHandlers.set(event, handler),
      reset: () => workspaceHandlers.get('reset')()
    },
    setTimeout() {}, updateWorkspaceMode() {}
  });
  context.window.addEventListener = (event, handler) => pageEvents.set(event, handler);
  context.mweForm.reset = () => handlers.get('reset')();
  runInNewContext(appSource.slice(appSource.indexOf("workspaceForm.addEventListener('reset'"),
    appSource.indexOf("relationship.addEventListener('change'")), context);
  allowReset = false;
  workspaceHandlers.get('reset')({preventDefault() {}});
  assert.equal(context.currentExport.synthetic, true);
  assert.equal(context.analysisRevision, 0);
  assert.equal(basicInput.value, 'Unsaved basic text.');
  const promptsBeforeExit = resetPrompts;
  pageEvents.get('pagehide')();
  assert.equal(resetPrompts, promptsBeforeExit, 'Page-exit cleanup must not prompt');
  assert.equal(context.currentExport, null);
  assert.equal(context.mweDocument, null);
  assert.equal(context.clearingOnPageExit, false);
}

// Draft detection compares live controls to recorded values, not to completion status.
{
  const appSource = readFileSync(new URL('../app.mjs', import.meta.url), 'utf8');
  const fields = new Map();
  const tokens = [{type: 'checkbox', value: 't1', checked: false}];
  const senses = [
    {type: 'checkbox', value: 's1', checked: true},
    {type: 'checkbox', value: 's2', checked: false}
  ];
  const details = {open: false, querySelectorAll: () => senses};
  let focused;
  const field = (id, value) => {
    const control = {id, value, type: 'text', closest: () => details,
      focus() { focused = id; }, scrollIntoView() {}};
    fields.set(id, control);
    return control;
  };
  const occurrence = {
    id: 'mwe-1', canonical_form: 'take in', status: 'candidate', decision: null,
    idiomaticity: {status: 'not_assessed', decision: null}, sense: null
  };
  const context = {
    mweDocument: {occurrences: [occurrence]}, mweStatus: {},
    document: {getElementById: id => fields.get(id), querySelectorAll: () => tokens},
    updateMwePendingEdits() { return context.pendingMweEdits(); }
  };
  runInNewContext(
    appSource.slice(appSource.indexOf('function pendingMweEdits('),
      appSource.indexOf('function updateMwePendingEdits(')) +
    appSource.slice(appSource.indexOf('function ensureMweEditsRecorded('),
      appSource.indexOf('function lockMweSourceInputs(')), context
  );
  const note = field('decision-mwe-1', '');
  const manual = field('manual-canonical-form', '');
  assert.equal(context.ensureMweEditsRecorded(), true, 'Unresolved is a valid saved state');
  note.value = 'An unrecorded draft.';
  const before = JSON.stringify(occurrence);
  assert.equal(context.ensureMweEditsRecorded(), false);
  assert.equal(focused, 'decision-mwe-1');
  assert.equal(JSON.stringify(occurrence), before, 'Detection must not record a decision');
  note.value = '   ';
  assert.equal(context.ensureMweEditsRecorded(), true);
  occurrence.status = 'confirmed';
  occurrence.decision = {note: ' Recorded note. '};
  note.value = 'Recorded note.';
  occurrence.idiomaticity = {status: 'idiomatic', decision: {note: 'Idiom note.'}};
  const idiom = field('idiomaticity-mwe-1', 'idiomatic');
  field('idiomaticity-note-mwe-1', 'Idiom note.');
  occurrence.sense = {assignment_status: 'assigned', selected_sense_ids: ['s1'], decision: {note: 'Sense note.'}};
  const senseStatus = field('sense-status-mwe-1', 'assigned');
  const senseNote = field('sense-note-mwe-1', 'Sense note.');
  assert.equal(context.pendingMweEdits().length, 0);
  // Native textareas use LF; that display normalization is not an edit to an imported record.
  const notePairs = [[note, occurrence.decision], [fields.get('idiomaticity-note-mwe-1'), occurrence.idiomaticity.decision],
    [senseNote, occurrence.sense.decision]];
  const originalNotes = notePairs.map(([, decision]) => decision.note);
  for (const ending of ['\n', '\r\n', '\r']) {
    for (const [input, decision] of notePairs) {
      decision.note = `First line.${ending}Second line.`;
      input.value = 'First line.\nSecond line.';
    }
    const before = JSON.stringify(occurrence);
    assert.equal(context.pendingMweEdits().length, 0, 'Line-ending normalization must not block untouched exports');
    assert.equal(JSON.stringify(occurrence), before, 'Comparing notes must preserve the original bytes');
    senseNote.value = 'First line.Second line.';
    assert.equal(context.pendingMweEdits().length, 1, 'Removing a line break is a real edit');
  }
  notePairs.forEach(([input, decision], index) => { input.value = decision.note = originalNotes[index]; });
  idiom.value = 'literal';
  senses[1].checked = true;
  senseNote.value = 'Changed note.';
  assert.equal(context.pendingMweEdits().length, 2, 'Group related sense fields together');
  idiom.value = 'idiomatic';
  assert.equal(context.ensureMweEditsRecorded(), false);
  assert.equal(details.open, true, 'Open the containing sense panel before returning');
  assert.equal(focused, 'sense-note-mwe-1');
  senseNote.value = 'Sense note.';
  assert.equal(context.pendingMweEdits()[0].control, senses[1], 'Detect checkbox-only edits');
  senses[0].checked = senses[1].checked = false;
  occurrence.sense = {assignment_status: 'abstained', selected_sense_ids: [], decision: {note: 'Abstention.'}};
  senseStatus.value = 'abstained';
  senseNote.value = 'Abstention.';
  assert.equal(context.ensureMweEditsRecorded(), true, 'Recorded abstention must not block export');
  tokens[0].checked = true;
  assert.equal(context.pendingMweEdits()[0].label, '手動候補の追加');
  tokens[0].checked = false;
  manual.value = 'An unfinished manual candidate';
  assert.equal(context.ensureMweEditsRecorded(), false);
  manual.value = '';
  assert.equal(context.ensureMweEditsRecorded(), true, 'Reverting edits removes the warning');

  const handlers = new Map();
  let downloads = 0;
  const guardContext = {
    document: {getElementById: id => ({addEventListener: (_, fn) => handlers.set(id, fn)})},
    mweDocument: {}, mweRevision: 0, ensureMweEditsRecorded: () => false,
    downloadText() { downloads += 1; }
  };
  for (const [start, end] of [
    ["document.getElementById('export-mwe-csv').addEventListener", 'function renderMweDocumentSet('],
    ["document.getElementById('save-mwe-document').addEventListener", "document.getElementById('mwe-document-set-documents').addEventListener"],
    ["document.getElementById('export-mwe-document-set').addEventListener", "document.getElementById('clear-mwe-document-set').addEventListener"]
  ]) runInNewContext(appSource.slice(appSource.indexOf(start), appSource.indexOf(end)), guardContext);
  for (const id of ['export-mwe-csv', 'export-mwe-json', 'export-mwe-workspace',
    'save-mwe-document', 'export-mwe-document-set']) await handlers.get(id)();
  assert.equal(downloads, 0, 'Every judgment-bearing save path must stop on a pending edit');
}

// Manual additions must respect the same candidate limit as extraction and exports.
{
  const source = readFileSync(new URL('../app.mjs', import.meta.url), 'utf8');
  const limit = mweContract.candidate_generation.limits.candidates_per_text;
  const text = 'She took it in. '.repeat(limit);
  const document = {text, ...findMweCandidates(text,
    parseMwePatternTsv(examplePatterns, mweContract.occurrence_record.categories))};
  document.occurrences[0].status = 'rejected';
  document.occurrences[0].decision = {source: 'synthetic-review', note: 'Keep this existing decision.'};
  const first = structuredClone(document.occurrences[0]);
  const selected = [{value: 't1', checked: true}, {value: 't2', checked: true}];
  const canonical = {value: 'synthetic manual expression'};
  let add, renders = 0;
  const appended = [];
  const controls = {'manual-canonical-form': canonical, 'manual-mwe-category': {value: 'VID'},
    'add-manual-mwe': {addEventListener(_, handler) { add = handler; }},
    'mwe-occurrences': {append(item) { appended.push(item); }}};
  const context = {mweDocument: document, mweContract, mweRevision: 0, nextMweId: limit + 1,
    mweStatus: {}, document: {getElementById: id => controls[id], querySelectorAll: () => selected},
    occurrenceCard: item => item,
    renderMweReviewSummary() { summarizeMweDocument(document, mweContract); renders++; }};
  runInNewContext(source.slice(source.indexOf("document.getElementById('add-manual-mwe').addEventListener"),
    source.indexOf("document.getElementById('export-mwe-csv').addEventListener")), context);
  const before = JSON.stringify({document, selected, canonical});
  assert.doesNotThrow(() => add(), 'Reject an over-limit addition before creating an invalid document');
  assert.equal(JSON.stringify({document, selected, canonical}), before, 'Keep records and the manual draft intact');
  assert.equal(context.mweRevision, 0);
  assert.equal(context.nextMweId, limit + 1);
  assert.equal(appended.length, 0);
  assert.equal(renders, 0);
  assert.match(context.mweStatus.textContent, new RegExp(String(limit)));
  document.occurrences.pop(); // A reviewer frees a slot; retry the preserved draft.
  add();
  assert.equal(document.occurrences.length, limit);
  assert.deepEqual(document.occurrences[0], first);
  assert.equal(document.occurrences.at(-1).id, `mwe-${limit + 1}`);
  assert.equal(document.occurrences.at(-1).status, 'candidate');
  assert.equal(document.occurrences.at(-1).decision, null);
  assert.equal(canonical.value, '');
  assert.ok(selected.every(input => !input.checked));
  assert.equal(renders, 1);
  assert.equal(appended.length, 1);
}

// Delay real event-handler dependencies deterministically; no timing sleeps or DOM library.
{
  const source = readFileSync(new URL('../app.mjs', import.meta.url), 'utf8');
  const controls = new Map();
  const handlers = new Map();
  const control = id => {
    if (!controls.has(id)) controls.set(id, {
      value: '', defaultValue: '', textContent: '', checked: true, disabled: false, dataset: {},
      replaceChildren(...options) { this.options = options; },
      addEventListener: (type, fn, capture) => handlers.set(`${id}:${type}:${!!capture}`, fn)
    });
    return controls.get(id);
  };
  const fire = (id, type, capture = false) => handlers.get(`${id}:${type}:${capture}`)({
    target: control(id), preventDefault() {}
  });
  const downloads = [];
  const context = {
    document: {getElementById: control, querySelectorAll: () => [], createElement: () => ({})},
    mweForm: control('mwe-form'), mweDocumentSetForm: control('mwe-document-set-form'),
    mweStatus: control('mwe-status'), mweResults: {hidden: true},
    mweRevision: 0, mweDocument: null, mweDocumentSet: new Map(), mweDocumentDirty: true,
    currentSetDocumentId: null,
    currentWordProfile: wordProfile, currentWordRankCutoff: null, mweFormProfile, mweSenseProfile,
    mwePatternSource: patternTsv, contract, mweContract, clearingOnPageExit: false,
    wordProfiles: new Map([['tubelex', {profile: wordProfile, maximumRank: null}]]),
    localBncCocaProfile: {size: 1, sha256: 'synthetic', id: 'synthetic'},
    window: {confirm: () => true}, parseJsonInput, parseMwePatternTsv, findMweCandidates,
    analyzeWordCoverage, makeMweDocumentSetRecord,
    ensureMweEditsRecorded: () => true, pendingMweEdits: () => [],
    updatePageExitWarning() {}, // Tested with live state and form events above.
    renderMweReview() { context.mweDocumentDirty = true; context.updateMwePendingEdits(); },
    downloadText(name) { downloads.push(name); }
  };
  for (const [start, end] of [
    ['function updateMwePendingEdits(', 'function ensureMweEditsRecorded('],
    ['function lockMweSourceInputs(', 'function reviewedOccurrence('],
    ['function invalidateMweReview(', "document.getElementById('add-manual-mwe').addEventListener"],
    ["document.getElementById('export-mwe-json').addEventListener", 'function renderMweDocumentSet('],
    ['function renderMweDocumentSet(', 'function documentSetDocuments('],
    ['function documentSetDocuments(', 'function fillList(']
  ]) runInNewContext(source.slice(source.indexOf(start), source.indexOf(end)), context);

  control('word-reference').value = 'tubelex';
  control('mwe-document-set-id').value = ' synthetic-set ';
  control('mwe-document-set-label').value = ' Synthetic set ';
  control('mwe-document-id').value = ' synthetic-document ';
  control('mwe-document-label').value = ' Synthetic document ';
  context.mweDocument = structuredClone(reviewedDocument);
  // A draft edit in either form must cancel each in-flight judgment save.
  for (const id of ['export-mwe-json', 'export-mwe-workspace', 'save-mwe-document']) {
    for (const form of ['mwe-form', 'mwe-document-set-form']) {
      const gate = Promise.withResolvers();
      context.makeMweReviewRecord = context.makeMweWorkspaceRecord = () => gate.promise;
      const pending = fire(id, 'click');
      fire(form, 'input', true);
      gate.resolve(mweWorkspaceRecord);
      await pending;
      assert.equal(downloads.length, 0, `${id} must not save after an edit`);
      assert.equal(context.mweDocumentSet.size, 0);
      assert.equal(context.mweDocumentDirty, true);
    }
  }
  // Independent downloads must not cancel each other; errors are handled, not unhandled.
  context.makeMweReviewRecord = async () => mweReviewRecord;
  context.makeMweWorkspaceRecord = async () => mweWorkspaceRecord;
  await Promise.all(['export-mwe-json', 'export-mwe-workspace'].map(id => fire(id, 'click')));
  assert.equal(downloads.length, 2);
  context.makeMweReviewRecord = async () => { throw new Error('Synthetic save failure.'); };
  await fire('export-mwe-json', 'click');
  assert.equal(context.mweStatus.textContent, 'Synthetic save failure.');
  await fire('save-mwe-document', 'click');
  assert.equal(context.mweDocumentSet.size, 1);
  assert.equal(context.mweDocumentDirty, false);
  assert.equal(control('mwe-document-set-id').value, 'synthetic-set');
  assert.equal(control('mwe-document-set-label').value, 'Synthetic set');
  assert.equal(control('mwe-document-id').value, 'synthetic-document');
  assert.equal(control('mwe-document-label').value, 'Synthetic document');
  const saveGate = Promise.withResolvers();
  context.makeMweWorkspaceRecord = () => saveGate.promise;
  const staleSave = fire('save-mwe-document', 'click');
  fire('clear-mwe-document-set', 'click');
  const clearedStatus = control('mwe-document-set-status').textContent;
  saveGate.resolve(mweWorkspaceRecord);
  await staleSave;
  assert.equal(context.mweDocumentSet.size, 0, 'A late save must not resurrect a cleared set');
  assert.equal(context.mweDocumentDirty, true);
  assert.equal(control('mwe-document-set-status').textContent, clearedStatus);

  // Two file selections may finish out of order, including a stale read error.
  for (const failOlder of [false, true]) {
    fire('mwe-form', 'reset');
    const gate = Promise.withResolvers();
    control('mwe-workspace-file').files = [{size: 1, text: () => gate.promise}];
    control('mwe-workspace-file').value = 'same-file.json';
    const older = fire('mwe-workspace-file', 'change');
    assert.equal(control('mwe-workspace-file').value, '', 'The same file must remain selectable after cancellation');
    context.restoreMweWorkspaceRecord = async ({record}) => ({
      document: {...record.document, tokens: reviewedDocument.tokens}, patternSource: record.pattern_tsv
    });
    control('mwe-workspace-file').files = [{size: 1, text: async () => JSON.stringify(mweWorkspaceRecord)}];
    await fire('mwe-workspace-file', 'change');
    const current = context.mweDocument;
    const status = control('mwe-workspace-status').textContent;
    control('mwe-workspace-file').value = 'newer-selection';
    if (failOlder) gate.reject(new Error('Stale read failure.'));
    else gate.resolve(JSON.stringify(mweWorkspaceRecord));
    await older;
    assert.equal(context.mweDocument, current, 'Newer import must win');
    assert.equal(control('mwe-workspace-status').textContent, status);
    assert.equal(control('mwe-workspace-file').value, 'newer-selection', 'Stale cleanup must not clear a newer selection');
  }
  // Cancel during validation, after file.text has already completed.
  for (const id of ['mwe-workspace-file', 'mwe-document-set-file', 'bnc-coca-profile', 'load-mwe-document']) {
    fire('mwe-form', 'reset');
    const gate = Promise.withResolvers();
    const started = Promise.withResolvers();
    const delayed = () => { started.resolve(); return gate.promise; };
    context.restoreMweWorkspaceRecord = context.restoreMweDocumentSetRecord = context.sha256 = delayed;
    control(id).files = [{size: 1, text: async () => JSON.stringify(
      id === 'mwe-document-set-file' ? documentSetRecord : mweWorkspaceRecord
    )}];
    control(id).value = 'same-file.json';
    if (id === 'load-mwe-document') {
      context.mweDocumentSet.set('synthetic', {id: 'synthetic', label: 'Synthetic', workspace: mweWorkspaceRecord});
      control('mwe-document-set-documents').value = 'synthetic';
    }
    const pending = fire(id, id === 'load-mwe-document' ? 'click' : 'change');
    await started.promise;
    if (id !== 'load-mwe-document') assert.equal(control(id).value, '', 'Release file selection before awaiting');
    fire('mwe-form', 'reset');
    const before = JSON.stringify([...context.mweDocumentSet]);
    const status = control('bnc-coca-profile-status').textContent;
    gate.resolve(id === 'bnc-coca-profile' ? 'synthetic' : {
      document: reviewedDocument, patternSource: patternTsv,
      setId: 'stale', setLabel: 'Stale', documents: documentSetRecord.documents
    });
    await pending;
    assert.equal(context.mweDocument, null, `${id} must not restore after reset`);
    assert.equal(JSON.stringify([...context.mweDocumentSet]), before);
    assert.equal(control('bnc-coca-profile-status').textContent, status);
    assert.equal(context.wordProfiles.has('bnc-coca-1000'), false);
  }
  // Loading an existing document must fix its identity just as adding it does.
  context.mweDocumentSet.set('other', {id: 'other', label: 'Other document', workspace: mweWorkspaceRecord});
  control('mwe-document-set-id').value = 'synthetic-set';
  control('mwe-document-set-label').value = 'Synthetic set';
  context.restoreMweWorkspaceRecord = restoreMweWorkspaceRecord;
  context.makeMweWorkspaceRecord = makeMweWorkspaceRecord;
  await fire('load-mwe-document', 'click');
  assert.equal(context.currentSetDocumentId, 'synthetic');
  assert.equal(control('mwe-document-id').value, 'synthetic');
  assert.equal(control('mwe-document-id').disabled, true, 'Restored document identity must stay fixed');
  assert.match(control('mwe-current-document-status').textContent, /現在の文書：synthetic。.*反映済み/);
  control('mwe-document-set-documents').value = 'other';
  fire('mwe-document-set-documents', 'change');
  assert.equal(context.currentSetDocumentId, 'synthetic', 'Picking a document must not switch the active review');
  await fire('load-mwe-document', 'click');
  assert.equal(context.currentSetDocumentId, 'synthetic');
  assert.match(control('mwe-document-set-status').textContent, /現在のレビューを閉じてから/);
  const beforeIdentityChange = JSON.stringify([...context.mweDocumentSet]);
  for (const id of ['other', 'new-id']) {
    control('mwe-document-id').value = id; // A disabled control is not the only guard.
    await fire('save-mwe-document', 'click');
    assert.match(control('mwe-document-set-status').textContent, /IDは変更できません/);
    assert.equal(JSON.stringify([...context.mweDocumentSet]), beforeIdentityChange);
  }
  control('mwe-document-id').value = 'synthetic';
  control('mwe-document-label').value = ' Updated document name. ';
  fire('mwe-document-label', 'input');
  assert.equal(context.mweDocumentDirty, true);
  assert.match(control('mwe-current-document-status').textContent, /現在の文書：synthetic。.*追加／更新してください/);
  const downloadsBeforeRename = downloads.length;
  fire('export-mwe-document-set', 'click');
  assert.equal(downloads.length, downloadsBeforeRename, 'A changed name must not be omitted from a set download');
  await fire('save-mwe-document', 'click');
  assert.equal(context.mweDocumentSet.get('synthetic').label, 'Updated document name.');
  assert.equal(context.mweDocumentSet.get('other').label, 'Other document');
  assert.equal(control('mwe-document-label').value, 'Updated document name.');
  assert.equal(context.mweDocumentDirty, false);
  assert.match(control('mwe-current-document-status').textContent, /反映済み/);
  fire('export-mwe-document-set', 'click');
  assert.equal(downloads.length, downloadsBeforeRename + 1);
  fire('mwe-form', 'reset');
  assert.equal(control('mwe-document-id').disabled, false);
  assert.equal(control('mwe-current-document-status').textContent, '現在開いているレビューはありません。');
  assert.equal(context.mweDocumentSet.size, 2);
  control('mwe-text').value = 'Another synthetic text.';
  fire('mwe-form', 'submit');
  assert.equal(control('mwe-current-document-status').textContent, '現在のレビューは文書セットに未追加です。');

  // A rejected local-file replacement must not erase a previously verified profile.
  fire('mwe-form', 'reset');
  const retainedProfile = {profile: {identity: {profile_id: 'synthetic'}}};
  const retainedSelection = {profile: retainedProfile, maximumRank: 1};
  context.wordProfiles.set('bnc-coca-1000', retainedSelection);
  context.wordProfiles.set('bnc-coca-2000', {profile: retainedProfile, maximumRank: 2});
  control('bnc-coca-profile').files = [{size: 2, text() { throw new Error('Must not read a wrong-size file.'); }}];
  await fire('bnc-coca-profile', 'change');
  assert.equal(context.wordProfiles.get('bnc-coca-1000'), retainedSelection,
    'An invalid replacement must preserve the verified local profile');
  const localOptions = [{disabled: false}, {disabled: false}];
  context.document.querySelectorAll = selector => selector.includes('data-local-profile') ? localOptions : [];
  context.localBncCocaProfile.size = 100;
  const replacement = {profile: {identity: {profile_id: 'synthetic'}}};
  const localFile = {size: 100, text: async () => '{}'};
  for (const [file, digest, prepare] of [
    [{size: 100, text: async () => { throw new Error('Synthetic file read failure.'); }}, 'synthetic', () => replacement],
    [localFile, 'wrong-hash', () => replacement],
    [{size: 100, text: async () => '{'}, 'synthetic', () => replacement],
    [localFile, 'synthetic', () => { throw new Error('Synthetic profile validation failure.'); }],
    [localFile, 'synthetic', () => ({profile: {identity: {profile_id: 'wrong-id'}}})]
  ]) {
    context.sha256 = async () => digest;
    context.prepareWordReferenceProfile = prepare;
    control('bnc-coca-profile').files = [file];
    await fire('bnc-coca-profile', 'change');
    assert.equal(context.wordProfiles.get('bnc-coca-1000'), retainedSelection);
    assert.equal(context.wordProfiles.get('bnc-coca-2000').profile, retainedProfile);
    assert.ok(localOptions.every(option => !option.disabled));
    assert.match(control('bnc-coca-profile-status').textContent, /検証済みの参照リストと現在の作業はそのまま保持/);
  }
  context.mweDocument = structuredClone(reviewedDocument);
  const beforeRejectedProfile = context.mweDocument;
  await fire('bnc-coca-profile', 'change');
  assert.equal(context.mweDocument, beforeRejectedProfile, 'Even a forced change event must not discard an active review');
  assert.equal(context.wordProfiles.get('bnc-coca-1000'), retainedSelection);
  fire('mwe-form', 'reset');
  context.sha256 = async () => 'synthetic';
  context.prepareWordReferenceProfile = () => replacement;
  control('bnc-coca-profile').files = [localFile];
  await fire('bnc-coca-profile', 'change');
  assert.equal(context.wordProfiles.get('bnc-coca-1000').profile, replacement);
  assert.equal(context.wordProfiles.get('bnc-coca-2000').profile, replacement);
  assert.equal(replacement.runtimeProfileSha256, 'synthetic');

  // Rejected resume files preserve input drafts and never partially import a set.
  fire('clear-mwe-document-set', 'click');
  context.restoreMweWorkspaceRecord = restoreMweWorkspaceRecord;
  context.restoreMweDocumentSetRecord = restoreMweDocumentSetRecord;
  control('mwe-text').value = 'Keep this unextracted synthetic draft.';
  control('mwe-document-id').value = 'draft-id';
  control('mwe-document-label').value = 'Draft label';
  const beforeImport = () => JSON.stringify({
    document: context.mweDocument, documents: [...context.mweDocumentSet],
    fields: ['mwe-text', 'mwe-patterns', 'word-reference', 'mwe-document-id', 'mwe-document-label']
      .map(id => control(id).value)
  });
  const preserved = beforeImport();
  context.window.confirm = () => assert.fail('Invalid files must not ask to replace a draft');
  for (const [id, record, otherKind, statusId] of [
    ['mwe-workspace-file', mweWorkspaceRecord, documentSetRecord, 'mwe-workspace-status'],
    ['mwe-document-set-file', documentSetRecord, mweWorkspaceRecord, 'mwe-document-set-status']
  ]) {
    const badHash = structuredClone(record);
    const badWorkspace = badHash.document ? badHash : badHash.documents[1].workspace;
    badWorkspace.document.text += ' Changed after saving.';
    const oldVersion = {...record, contract_version: 'unsupported'};
    for (const [sourceText, expected] of [
      ['{', /JSONとして読み込めません/], ['null', /対応する再開用JSONではありません/],
      ['[]', /対応する再開用JSONではありません/],
      [JSON.stringify(mweReviewRecord), /CSV・方法JSONからは再開できません/],
      [JSON.stringify(otherKind), /で選択してください/],
      [JSON.stringify(badHash), /保存内容の整合性/],
      [JSON.stringify(oldVersion), /互換性/]
    ]) {
      control(id).files = [{size: sourceText.length, text: async () => sourceText}];
      await fire(id, 'change');
      assert.match(control(statusId).textContent, expected);
      assert.doesNotMatch(control(statusId).textContent, /TypeError|schema_version|SHA-256|occurrence/);
      assert.equal(beforeImport(), preserved, `${id} failure must preserve current work`);
      assert.equal(control(id).value, '', 'Allow retrying the same file after an error');
    }
    control(id).files = [{size: 1, text: async () => { throw new Error('Synthetic operating-system detail.'); }}];
    await fire(id, 'change');
    assert.match(control(statusId).textContent, /端末で利用できる保存コピーを選び直して/);
    assert.equal(beforeImport(), preserved);
    control(id).files = [{size: Number.MAX_SAFE_INTEGER, text() { assert.fail('Oversized files must not be read'); }}];
    await fire(id, 'change');
    assert.match(control(statusId).textContent, /読込サイズの上限/);
    assert.equal(beforeImport(), preserved);
  }
  await assert.rejects(context.readMweResumeFile(
    {size: 1, text: async () => '{"too":"long"}'},
    {...mweContract.workspace_file, maximum_json_utf16_code_units: 5}
  ), /読込上限/);
  context.window.confirm = () => true;
  control('mwe-workspace-file').files = [{size: 1, text: async () => JSON.stringify(mweWorkspaceRecord)}];
  await fire('mwe-workspace-file', 'change');
  assert.equal(context.mweDocument.text, reviewedDocument.text, 'A valid retry must still restore normally');

  // Both restore entry points must preserve an unextracted draft when replacement is cancelled.
  context.mweDocumentSet.set('reopen', {id: 'reopen', label: 'Reopen', workspace: mweWorkspaceRecord});
  control('mwe-document-set-documents').value = 'reopen';
  control('mwe-patterns').defaultValue = patternTsv;
  for (const [id, type, statusId] of [
    ['mwe-workspace-file', 'change', 'mwe-workspace-status'],
    ['load-mwe-document', 'click', 'mwe-document-set-status']
  ]) {
    for (const draft of ['text', 'patterns']) {
      context.mweDocument = null;
      context.currentSetDocumentId = null;
      control('mwe-text').value = draft === 'text' ? 'Keep this unfinished draft.' : '';
      control('mwe-patterns').value = draft === 'patterns' ? 'Unfinished pattern draft' : patternTsv;
      const previous = beforeImport();
      let prompts = 0;
      context.window.confirm = () => { prompts++; return false; };
      await fire(id, type);
      assert.equal(prompts, 1, `${id} must ask before replacing ${draft}`);
      assert.equal(beforeImport(), previous, `${id} cancellation must preserve inputs, review and set`);
      assert.equal(context.currentSetDocumentId, null);
      assert.match(control(statusId).textContent, /cancelled.*unchanged/i);
      context.window.confirm = () => { prompts++; return true; };
      await fire(id, type);
      assert.equal(prompts, 2, 'The same file or set document can be retried after cancellation');
      assert.equal(context.mweDocument.text, reviewedDocument.text);
      assert.equal(control('mwe-patterns').value, patternTsv);
      assert.equal(context.currentSetDocumentId, id === 'load-mwe-document' ? 'reopen' : null);
    }
    for (const text of ['', reviewedDocument.text]) {
      context.mweDocument = null;
      control('mwe-text').value = text;
      control('mwe-patterns').value = patternTsv;
      context.window.confirm = () => assert.fail('Empty or identical inputs need no replacement prompt');
      await fire(id, type);
      assert.equal(context.mweDocument.text, reviewedDocument.text);
    }
  }
}

// Context expansion is a literal, read-only view, never a new annotation or HTML input.
{
  const source = readFileSync(new URL('../app.mjs', import.meta.url), 'utf8');
  const element = tag => ({
    tag, children: [], attributes: {}, handlers: {}, textContent: '', open: false,
    append(...items) {
      this.children.push(...items);
      if (tag === 'select') for (const option of items) if (option.selected) this.value = option.value;
    },
    prepend(...items) { this.children.unshift(...items); },
    replaceChildren(...items) { this.children = items; },
    setAttribute(name, value) { this.attributes[name] = value; },
    addEventListener(name, handler) { this.handlers[name] = handler; },
    querySelectorAll(selector) {
      const descendants = this.children.filter(child => typeof child === 'object')
        .flatMap(child => [child, ...child.querySelectorAll('*')]);
      return selector === '*' ? descendants : descendants.filter(child =>
        child.tag === 'input' && (selector !== 'input:checked' || child.checked));
    }
  });
  const texts = [...sampleDocument.mwe_examples.map(item => item.text),
    '“No,” she said.\n\nShe took it in. <img src=x onerror=alert(1)>',
    'Before this rather long introduction Mira took it in after a very long pause.'];
  const context = {document: {createElement: element}};
  runInNewContext(source.slice(source.indexOf('function renderOccurrenceContext('),
    source.indexOf('function setMweDecision(')), context);
  for (const text of texts) {
    context.mweDocument = {text, ...findMweCandidates(text,
      parseMwePatternTsv(examplePatterns, mweContract.occurrence_record.categories))};
    const before = JSON.stringify(context.mweDocument);
    const view = context.renderOccurrenceContext(context.mweDocument.occurrences[0]);
    const window = view.children.find(child => child.className === 'token-context');
    const members = context.mweDocument.occurrences[0].member_token_ids;
    assert.equal(window.children[0] === '…', Number(members[0].slice(1)) > 4);
    assert.equal(window.children.at(-1) === '…',
      Number(members.at(-1).slice(1)) + 3 < context.mweDocument.tokens.length);
    assert.equal(window.children.filter(child => child.className === 'token-member').length, members.length);
    const reader = view.children.find(child => child.tag === 'details');
    assert.ok(reader, 'Every candidate must offer the complete source text');
    const fullText = reader.children.find(child => child.tag === 'pre');
    assert.equal(fullText.textContent, '', 'Do not copy the full document into every collapsed card');
    assert.equal(fullText.tabIndex, 0, 'The scrollable text is keyboard reachable');
    reader.open = true;
    reader.handlers.toggle();
    assert.equal(fullText.textContent, text, 'Preserve punctuation, line breaks and literal markup exactly');
    assert.equal(fullText.children.length, 0, 'Original text must not create DOM elements');
    assert.equal(JSON.stringify(context.mweDocument), before, 'Reading must not change tokens or judgments');
    context.mweDocument = {text: 'A later document'};
    reader.handlers.toggle();
    assert.equal(fullText.textContent, text, 'An old card remains bound to its own source');
    reader.open = false;
    reader.handlers.toggle();
    assert.equal(fullText.textContent, '');
  }

  // Explain all six existing sense states without choosing, clearing or saving on the user's behalf.
  let saves = 0;
  Object.assign(context, {lookupMweSenses, mweSenseProfile, setSenseDecision() { saves++; }});
  runInNewContext(source.slice(source.indexOf('function senseReview('),
    source.indexOf('function occurrenceCard(')), context);
  const occurrence = structuredClone(reviewedDocument.occurrences[0]);
  occurrence.sense.assignment_status = 'unassigned';
  occurrence.sense.selected_sense_ids = [];
  occurrence.sense.decision = null;
  const original = JSON.stringify(occurrence);
  const panel = context.senseReview(occurrence);
  assert.equal(panel.lang, 'en');
  const state = panel.children.find(child => child.tag === 'select');
  const choices = panel.children.find(child => child.tag === 'fieldset');
  const boxes = choices.querySelectorAll('input');
  const help = panel.children.find(child => child.id === `sense-help-${occurrence.id}`);
  assert.equal(state.attributes['aria-describedby'], help.id);
  assert.equal(choices.attributes['aria-describedby'], help.id);
  assert.equal(help.attributes['aria-live'], 'polite');
  assert.deepEqual(Array.from(boxes, box => box.value), occurrence.sense.candidate_sense_ids);
  assert.match(help.textContent, /unfinished.*Selected: 0/);
  const definitions = lookupMweSenses(occurrence.canonical_form, mweSenseProfile).senses;
  choices.children.slice(1).forEach((label, index) => {
    const description = label.children[1];
    assert.equal(description.textContent, definitions[index].definitions.join('; '));
    assert.equal(description.children.at(-1).textContent, `Sense ID: ${boxes[index].value}`);
  });
  boxes[0].checked = boxes[1].checked = true;
  for (const [value, wording] of [
    ['unassigned', /Select no senses.*clears any previous/],
    ['assigned', /Select exactly one/],
    ['multiple_assigned', /at least two.*same time.*not uncertainty/],
    ['ambiguous', /at least two.*cannot distinguish.*does not assert/],
    ['abstained', /Select no senses.*cannot decide.*unfinished/],
    ['out_of_inventory', /complete list.*select no senses.*none fits/]
  ]) {
    state.value = value;
    state.handlers.change();
    assert.match(help.textContent, wording);
    assert.match(help.textContent, /Selected: 2/);
    assert.equal(boxes.filter(box => box.checked).length, 2, 'State changes must not silently clear selections');
    assert.equal(JSON.stringify(occurrence), original);
  }
  boxes[1].checked = false;
  choices.handlers.change();
  assert.match(help.textContent, /Selected: 1/);
  assert.equal(saves, 0);
  panel.children.at(-1).handlers.click();
  assert.equal(saves, 1, 'Only the explicit save control records a decision');
  const outside = context.senseReview({canonical_form: 'spill the beans',
    sense: lookupMweSenses('spill the beans', mweSenseProfile).state});
  assert.equal(outside.querySelectorAll('input').length, 0);
  assert.match(outside.children[1].textContent, /does not cover.*does not mean/);

  // All three reason fields must accept paragraphs without a rich-text editor.
  Object.assign(context, {occurrenceStatusLabels: {confirmed: 'Confirmed'},
    renderOccurrenceContext: () => element('div')});
  runInNewContext(source.slice(source.indexOf('function idiomaticityReview('),
    source.indexOf('function renderMweReview(')), context);
  const withNotes = structuredClone(reviewedDocument.occurrences[0]);
  const paragraph = 'First observation.\nA contrasting interpretation.\n日本語 🙂 <em>literal markup</em>';
  for (const record of [withNotes, withNotes.idiomaticity, withNotes.sense]) {
    record.decision = {source: 'synthetic-review', note: paragraph};
  }
  const card = context.occurrenceCard(withNotes);
  for (const prefix of ['decision-', 'idiomaticity-note-', 'sense-note-']) {
    const input = card.querySelectorAll('*').find(item => item.id === prefix + withNotes.id);
    assert.equal(input.tag, 'textarea');
    assert.equal(input.value, paragraph);
    assert.equal(input.rows, 2);
    assert.equal(input.maxLength, 500, 'Retain the existing input limit');
    assert.equal(input.className, 'review-note');
  }
}

// HTML pattern uses Unicode-sets mode, unlike the unflagged internal ID regex.
const htmlPatterns = [...readFileSync(new URL('../index.html', import.meta.url), 'utf8')
  .matchAll(/\bpattern="([^"]+)"/g)].map(match => new RegExp(`^(?:${match[1]})$`, 'v'));
assert.equal(htmlPatterns.length, 2);
for (const pattern of htmlPatterns) {
  for (const id of ['a', 'passage-01', 'Set_2.0']) assert.ok(pattern.test(id));
  for (const id of ['-a', 'two words', 'a/b', '文書', 'a|b']) assert.ok(!pattern.test(id));
}

console.log(
  `Contract verification: PASS (${fixture.cases.length} fixtures, ` +
  `${mweFixture.cases.length} MWE gold cases, ` +
  `${sampleDocument.comparison_sets.length} scenarios, ${samples.length} samples, ` +
  `${contract.workspace.relationships.length} workspace modes, exports, ` +
  `single/document-set MWE resume round-trips, draft/save/reset and page-exit guards, async snapshots and stale-operation guards, document identity/save-state guards, import failure recovery, destructive-review cancellation and independent senses)`
);
