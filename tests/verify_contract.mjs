import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {
  analyze, analyzeDeclaredSegments, makeExportRecord, parseBatchJson, roundedRatio, sha256,
  tokenize
} from '../metrics.mjs';

const fixtureUrl = new URL('./fixtures/metric_cases.json', import.meta.url);
const sampleUrl = new URL('../samples.json', import.meta.url);
const contractUrl = new URL('../metric_contract.json', import.meta.url);
const fixture = JSON.parse(readFileSync(fixtureUrl, 'utf8'));
const sampleDocument = JSON.parse(readFileSync(sampleUrl, 'utf8'));
const contract = JSON.parse(readFileSync(contractUrl, 'utf8'));

assert.equal(contract.contract_version, '0.1.0-probe');
assert.equal(fixture.contract_version, contract.contract_version);
for (const testCase of fixture.cases) {
  assert.deepEqual(analyze(testCase.text), testCase.expected, testCase.id);
}
assert.equal(roundedRatio(1, 128), 0.007813);

assert.equal(sampleDocument.samples_version, '0.3.0-probe');
assert.equal(sampleDocument.comparison_sets.length, 3);
const sets = Object.fromEntries(sampleDocument.comparison_sets.map(set => [set.id, set]));
const samples = sampleDocument.comparison_sets.flatMap(set => set.samples);
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

console.log(
  `Contract verification: PASS (${fixture.cases.length} fixtures, ` +
  `${sampleDocument.comparison_sets.length} scenarios, ${samples.length} samples, ` +
  `${contract.workspace.relationships.length} workspace modes, browser export)`
);
