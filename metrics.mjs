const tokenPattern = /(?:^|[^\p{L}\p{N}_])([A-Za-z]+(?:['’][A-Za-z]+)*)(?=$|[^\p{L}\p{N}_])/gu;

function requireWellFormed(value, label) {
  if (typeof value.isWellFormed !== 'function') {
    throw new Error('Unicode validation requires a current browser.');
  }
  if (!value.isWellFormed()) {
    throw new Error(`${label} contains an unpaired Unicode surrogate.`);
  }
}

export function parseBatchJson(source, maximum) {
  if (typeof source !== 'string') throw new Error('Batch JSON must be text.');
  if (source.length > maximum) {
    throw new Error('Batch JSON exceeds the reviewed browser limit.');
  }
  requireWellFormed(source, 'Batch JSON');
  try {
    return JSON.parse(source);
  } catch {
    throw new Error('Batch JSON is not valid JSON.');
  }
}

export function tokenize(text) {
  return [...text.matchAll(tokenPattern)].map(match =>
    match[1].replaceAll('’', "'").toLowerCase()
  );
}

export function roundedRatio(numerator, denominator) {
  if (denominator === 0) return 0;
  const scale = 1_000_000;
  let quotient = Math.floor(numerator * scale / denominator);
  const remainder = numerator * scale % denominator;
  if (remainder * 2 >= denominator) quotient += 1;
  return quotient / scale;
}

export function analyze(text) {
  const tokens = tokenize(text);
  const counts = new Map();
  for (const token of tokens) counts.set(token, (counts.get(token) || 0) + 1);
  return {
    tokens: tokens.length,
    types: counts.size,
    type_token_ratio: roundedRatio(counts.size, tokens.length),
    hapax_types: [...counts.values()].filter(count => count === 1).length
  };
}

function coverage(numerator, denominator) {
  return {numerator, denominator, value: denominator ? roundedRatio(numerator, denominator) : null};
}

export function summarizeMweDocument(document, contract) {
  if (!document || typeof document.text !== 'string' || !Array.isArray(document.tokens) ||
      !Array.isArray(document.occurrences)) {
    throw new Error('MWE document requires token and occurrence arrays.');
  }
  const normalized = tokenize(document.text);
  const tokenIds = new Set();
  document.tokens.forEach((token, index) => {
    const surfaceTokens = typeof token.surface === 'string' ? tokenize(token.surface) : [];
    if (typeof token.id !== 'string' || !token.id || typeof token.surface !== 'string' ||
        token.position !== index + 1 || token.normalized !== normalized[index] ||
        surfaceTokens.length !== 1 || surfaceTokens[0] !== token.normalized) {
      throw new Error('MWE token records do not match canonical tokenization.');
    }
    if (tokenIds.has(token.id)) throw new Error(`Duplicate MWE token ID: ${token.id}.`);
    tokenIds.add(token.id);
  });
  if (normalized.length !== document.tokens.length) {
    throw new Error('MWE token records do not match canonical tokenization.');
  }
  const positionById = new Map(document.tokens.map(token => [token.id, token.position]));
  const occurrenceIds = new Set();
  const confirmed = [];
  const rejected = [];
  const unresolved = [];
  for (const occurrence of document.occurrences) {
    if (typeof occurrence.id !== 'string' || !occurrence.id ||
        typeof occurrence.canonical_form !== 'string' || !occurrence.canonical_form.trim()) {
      throw new Error('MWE occurrence identity is missing.');
    }
    if (occurrenceIds.has(occurrence.id)) {
      throw new Error(`Duplicate MWE occurrence ID: ${occurrence.id}.`);
    }
    occurrenceIds.add(occurrence.id);
    if (!contract.occurrence_record.statuses.includes(occurrence.status)) {
      throw new Error(`Unknown MWE occurrence status: ${occurrence.status}.`);
    }
    if (!contract.occurrence_record.categories.includes(occurrence.category)) {
      throw new Error(`Unknown MWE category: ${occurrence.category}.`);
    }
    validateIdiomaticity(occurrence, contract);
    const members = occurrence.member_token_ids;
    const gaps = occurrence.gap_token_ids;
    if (!Array.isArray(members) || members.length < 2 || new Set(members).size !== members.length) {
      throw new Error(`MWE occurrence ${occurrence.id} requires unique member tokens.`);
    }
    if (!Array.isArray(gaps) || new Set(gaps).size !== gaps.length) {
      throw new Error(`MWE occurrence ${occurrence.id} requires unique gap tokens.`);
    }
    for (const id of [...members, ...gaps]) {
      if (!tokenIds.has(id)) throw new Error(`Unknown token ID in ${occurrence.id}: ${id}.`);
    }
    const memberPositions = members.map(id => positionById.get(id));
    if (memberPositions.some((position, index) => index && position <= memberPositions[index - 1])) {
      throw new Error(`MWE members are not in document order: ${occurrence.id}.`);
    }
    // ponytail: scan each occurrence span; index tokens only if corpus benchmarks require it.
    const expectedGaps = document.tokens
      .slice(memberPositions[0], memberPositions.at(-1) - 1)
      .map(token => token.id).filter(id => !members.includes(id));
    if (JSON.stringify(gaps) !== JSON.stringify(expectedGaps)) {
      throw new Error(`MWE gap tokens do not match the member span: ${occurrence.id}.`);
    }
    if (occurrence.status === 'candidate') {
      if (occurrence.decision || occurrence.form_lookup || occurrence.sense ||
          occurrence.idiomaticity.status !== 'not_assessed') {
        throw new Error(`Unresolved candidate carries a terminal result: ${occurrence.id}.`);
      }
      unresolved.push(occurrence);
      continue;
    }
    if (!occurrence.decision?.source || !occurrence.decision?.note) {
      throw new Error(`MWE decision provenance is missing: ${occurrence.id}.`);
    }
    if (occurrence.status === 'rejected') {
      if (occurrence.form_lookup || occurrence.sense) {
        throw new Error(`Rejected occurrence carries an inventory result: ${occurrence.id}.`);
      }
      rejected.push(occurrence);
      continue;
    }
    validateConfirmedOccurrence(occurrence, contract);
    confirmed.push(occurrence);
  }

  const memberIds = new Set(confirmed.flatMap(occurrence => occurrence.member_token_ids));
  const formMatched = confirmed.filter(item => item.form_lookup.status === 'matched').length;
  const senseMatched = confirmed.filter(item => item.sense.lookup_status === 'matched').length;
  const senseAssigned = confirmed.filter(item => item.sense.assignment_status === 'assigned').length;
  const senseStatuses = Object.fromEntries(
    contract.occurrence_record.sense_assignment_statuses.map(status => [
      status, confirmed.filter(item => item.sense.assignment_status === status).length
    ])
  );
  const idiomaticityStatuses = Object.fromEntries(
    contract.occurrence_record.idiomaticity_statuses.map(status => [
      status,
      document.occurrences.filter(item => item.idiomaticity.status === status).length
    ])
  );
  const idiomaticityAssessed = document.occurrences.length - idiomaticityStatuses.not_assessed;
  return {
    token_count: document.tokens.length,
    candidate_occurrence_count: document.occurrences.length,
    confirmed_occurrence_count: confirmed.length,
    rejected_occurrence_count: rejected.length,
    unresolved_occurrence_count: unresolved.length,
    confirmed_member_token_count: memberIds.size,
    confirmed_member_density: coverage(memberIds.size, document.tokens.length),
    occurrence_annotation_coverage: coverage(
      confirmed.length + rejected.length, document.occurrences.length
    ),
    idiomaticity_annotation_coverage: coverage(
      idiomaticityAssessed, document.occurrences.length
    ),
    idiomaticity_status_counts: idiomaticityStatuses,
    form_inventory_coverage: coverage(formMatched, confirmed.length),
    sense_inventory_coverage: coverage(senseMatched, confirmed.length),
    sense_assignment_coverage: coverage(senseAssigned, senseMatched),
    sense_assignment_status_counts: senseStatuses
  };
}

function validateIdiomaticity(occurrence, contract) {
  const idiomaticity = occurrence.idiomaticity;
  if (!idiomaticity ||
      !contract.occurrence_record.idiomaticity_statuses.includes(idiomaticity.status) ||
      !Object.hasOwn(idiomaticity, 'decision')) {
    throw new Error(`MWE occurrence lacks idiomaticity state: ${occurrence.id}.`);
  }
  const assessed = idiomaticity.status !== 'not_assessed';
  if (assessed !== Boolean(idiomaticity.decision?.source && idiomaticity.decision?.note)) {
    throw new Error(`Idiomaticity decision provenance is inconsistent: ${occurrence.id}.`);
  }
}

function validateConfirmedOccurrence(occurrence, contract) {
  const form = occurrence.form_lookup;
  const sense = occurrence.sense;
  if (!form || !contract.occurrence_record.form_lookup_statuses.includes(form.status)) {
    throw new Error(`Confirmed occurrence lacks form lookup: ${occurrence.id}.`);
  }
  const formLookupAttempted = form.status !== 'not_attempted';
  if (formLookupAttempted !== Boolean(form.inventory_id && form.inventory_version)) {
    throw new Error(`Form inventory identity is inconsistent: ${occurrence.id}.`);
  }
  if ((form.status === 'matched') !== Boolean(form.entry_id)) {
    throw new Error(`Form lookup result is inconsistent: ${occurrence.id}.`);
  }
  if (!sense || !contract.occurrence_record.sense_lookup_statuses.includes(sense.lookup_status) ||
      !contract.occurrence_record.sense_assignment_statuses.includes(sense.assignment_status)) {
    throw new Error(`Confirmed occurrence lacks sense state: ${occurrence.id}.`);
  }
  if (!Object.hasOwn(sense, 'decision')) {
    throw new Error(`Sense decision field is missing: ${occurrence.id}.`);
  }
  const senseLookupAttempted = sense.lookup_status !== 'not_attempted';
  if (senseLookupAttempted !== Boolean(sense.inventory_id && sense.inventory_version)) {
    throw new Error(`Sense inventory identity is inconsistent: ${occurrence.id}.`);
  }
  const candidates = sense.candidate_sense_ids;
  const selected = sense.selected_sense_ids;
  if (!Array.isArray(candidates) || !Array.isArray(selected) ||
      new Set(candidates).size !== candidates.length || new Set(selected).size !== selected.length ||
      selected.some(id => !candidates.includes(id))) {
    throw new Error(`Sense candidates are inconsistent: ${occurrence.id}.`);
  }
  if ((sense.lookup_status === 'matched') !== (candidates.length > 0)) {
    throw new Error(`Sense lookup result is inconsistent: ${occurrence.id}.`);
  }
  if (['assigned', 'ambiguous', 'abstained'].includes(sense.assignment_status) &&
      sense.lookup_status !== 'matched') {
    throw new Error(`Sense assignment lacks matched candidates: ${occurrence.id}.`);
  }
  const decided = ['assigned', 'ambiguous', 'abstained'].includes(sense.assignment_status);
  if (decided !== Boolean(sense.decision?.source && sense.decision?.note)) {
    throw new Error(`Sense decision provenance is inconsistent: ${occurrence.id}.`);
  }
  const selectedCount = sense.assignment_status === 'assigned'
    ? 1 : sense.assignment_status === 'ambiguous' ? 2 : 0;
  if ((sense.assignment_status === 'ambiguous' && selected.length < selectedCount) ||
      (sense.assignment_status !== 'ambiguous' && selected.length !== selectedCount) ||
      (sense.assignment_status === 'out_of_inventory') !==
        (sense.lookup_status === 'out_of_inventory')) {
    throw new Error(`Sense assignment is inconsistent: ${occurrence.id}.`);
  }
}

export function resultDifference(first, second) {
  return Object.fromEntries(
    Object.keys(first).map(key => [
      key, Number((second[key] - first[key]).toFixed(6))
    ])
  );
}

function median(values) {
  const sorted = [...values].sort((first, second) => first - second);
  const middle = Math.floor(sorted.length / 2);
  const value = sorted.length % 2
    ? sorted[middle]
    : (sorted[middle - 1] + sorted[middle]) / 2;
  return Number(value.toFixed(6));
}

function summarizeResults(results) {
  return Object.fromEntries(Object.keys(results[0]).map(key => {
    const values = results.map(result => result[key]);
    return [key, {minimum: Math.min(...values), median: median(values), maximum: Math.max(...values)}];
  }));
}

export function analyzeDeclaredSegments(text, maximum) {
  const lines = text.split(/\r?\n/).filter(line => line.trim());
  if (lines.length < 2) {
    throw new Error('Declared-segment mode requires at least two non-empty lines.');
  }
  if (lines.length > maximum) {
    throw new Error('Declared-segment count exceeds the reviewed browser limit.');
  }
  const segments = lines.map((line, index) => ({
    index: index + 1,
    utf8_bytes: new TextEncoder().encode(line).length,
    raw_text_included: false,
    result: analyze(line)
  }));
  return {
    boundary_rule: 'researcher-declared non-empty lines in input order',
    distribution_summary: 'unweighted minimum, median, and maximum across declared lines',
    segment_count: segments.length,
    distribution: summarizeResults(segments.map(segment => segment.result)),
    segments
  };
}

export async function sha256(text) {
  if (typeof text !== 'string') throw new Error('SHA-256 input must be text.');
  requireWellFormed(text, 'SHA-256 input');
  if (!globalThis.crypto?.subtle) {
    throw new Error('SHA-256 requires HTTPS or localhost in a modern browser.');
  }
  const digest = await globalThis.crypto.subtle.digest(
    'SHA-256', new TextEncoder().encode(text)
  );
  return [...new Uint8Array(digest)]
    .map(byte => byte.toString(16).padStart(2, '0')).join('');
}

export async function makeExportRecord({
  contract, relationship, designNote, contentScopeAttested, inputs, generatedAt
}) {
  if (!contract.workspace.relationships.includes(relationship)) {
    throw new Error('Unsupported comparison relationship.');
  }
  if (!Array.isArray(inputs)) throw new Error('Inputs must be an array.');
  if (relationship === 'batch') {
    if (inputs.length < 2 || inputs.length > contract.input.max_documents_per_batch) {
      throw new Error('Batch document count exceeds the reviewed browser limits.');
    }
  } else {
    const expectedInputs = ['single', 'declared-segments'].includes(relationship) ? 1 : 2;
    if (inputs.length !== expectedInputs) throw new Error('Wrong number of inputs.');
  }
  if (typeof designNote !== 'string' || !designNote.trim()) {
    throw new Error('Missing sampling/comparison design note.');
  }
  requireWellFormed(designNote, 'Sampling/comparison design note');
  if (designNote.length > contract.input.max_utf16_code_units_per_design_note) {
    throw new Error('Design note exceeds the reviewed browser limit.');
  }
  if (contentScopeAttested !== true) {
    throw new Error('Content-scope attestation is required.');
  }
  if (typeof generatedAt !== 'string') throw new Error('Missing generated-at timestamp.');
  const generatedDate = new Date(generatedAt);
  if (!Number.isFinite(generatedDate.getTime()) || generatedDate.toISOString() !== generatedAt) {
    throw new Error('Generated-at timestamp must be an exact UTC ISO string.');
  }

  for (const [index, input] of inputs.entries()) {
    if (!input || typeof input !== 'object' || Array.isArray(input)) {
      throw new Error(`Input ${index + 1} must be an object.`);
    }
    for (const key of ['id', 'label', 'provenance', 'text']) {
      if (typeof input[key] !== 'string' || !input[key].trim()) {
        throw new Error(`Missing input field at item ${index + 1}: ${key}.`);
      }
      requireWellFormed(input[key], `Input ${index + 1} ${key}`);
    }
    const itemName = input.id.trim();
    if (input.text.length > contract.input.max_utf16_code_units_per_text) {
      throw new Error(`Input text exceeds the reviewed browser limit: ${itemName}.`);
    }
    if (input.label.length > contract.input.max_utf16_code_units_per_label) {
      throw new Error(`Input label exceeds the reviewed browser limit: ${itemName}.`);
    }
    if (input.id.length > contract.input.max_utf16_code_units_per_id) {
      throw new Error(`Input ID exceeds the reviewed browser limit: item ${index + 1}.`);
    }
    if (input.provenance.length > contract.input.max_utf16_code_units_per_provenance) {
      throw new Error(`Input provenance exceeds the reviewed browser limit: ${itemName}.`);
    }
  }
  const ids = inputs.map(input => input.id.trim());
  const duplicateId = ids.find((id, index) => ids.indexOf(id) !== index);
  if (duplicateId) throw new Error(`Duplicate input ID: ${duplicateId}.`);
  if (relationship === 'batch') {
    const combinedLength = inputs.reduce((sum, input) => sum + input.text.length, 0);
    if (combinedLength > contract.input.max_combined_utf16_code_units_per_batch) {
      throw new Error('Combined batch text exceeds the reviewed browser limit.');
    }
  }

  const reviewedInputs = await Promise.all(inputs.map(async input => {
    return {
      id: input.id.trim(),
      label: input.label.trim(),
      provenance: input.provenance.trim(),
      sha256_utf8: await sha256(input.text),
      utf8_bytes: new TextEncoder().encode(input.text).length,
      raw_text_included: false,
      result: analyze(input.text)
    };
  }));

  const emptyInput = reviewedInputs.find(input => input.result.tokens === 0);
  if (relationship === 'batch' && emptyInput) {
    throw new Error(`Batch document has no recognized tokens: ${emptyInput.id}.`);
  }

  const warningCodes = ['descriptive-only', 'ttr-length-sensitive'];
  if (emptyInput) {
    warningCodes.push('no-recognized-tokens');
  }
  if (['paired', 'independent'].includes(relationship)) {
    warningCodes.push(
      reviewedInputs[0].result.tokens === reviewedInputs[1].result.tokens
        ? 'types-and-ttr-algebraically-dependent-at-fixed-length'
        : 'cross-length-difference-confounded'
    );
    if (relationship === 'independent') warningCodes.push('independent-texts-not-causal');
  }
  const declaredSegmentAnalysis = relationship === 'declared-segments'
    ? analyzeDeclaredSegments(
      inputs[0].text, contract.input.max_declared_segments_per_text
    )
    : null;
  if (declaredSegmentAnalysis) {
    warningCodes.push(
      'researcher-declared-segments',
      'segments-not-independent-observations',
      'pooled-and-segment-statistics-not-equivalent'
    );
    if (
      declaredSegmentAnalysis.segments.some(segment => segment.result.tokens === 0) &&
      !warningCodes.includes('no-recognized-tokens')
    ) {
      warningCodes.push('no-recognized-tokens');
    }
  }
  const batchAnalysis = relationship === 'batch'
    ? {
        document_count: reviewedInputs.length,
        distribution_summary: 'unweighted minimum, median, and maximum across documents',
        distribution: summarizeResults(reviewedInputs.map(input => input.result))
      }
    : null;
  if (batchAnalysis) {
    warningCodes.push('batch-documents-not-independent', 'batch-summary-unweighted');
  }

  return {
    schema_version: contract.workspace.export_schema_version,
    generated_at: generatedAt,
    contract_version: contract.contract_version,
    relationship,
    relationship_meaning: contract.workspace.relationship_meanings[relationship],
    sampling_and_comparison_design: designNote.trim(),
    content_scope_attested: true,
    attestation_scope: contract.workspace.required_attestation,
    method: {
      project_license: contract.project_license,
      construct: contract.scope.construct,
      claims: contract.scope.claims,
      excluded_inferences: contract.scope.excluded_inferences,
      limitations: contract.limitations,
      input_language: contract.scope.input_language,
      external_resource_dependencies: contract.external_resource_dependencies,
      tokenizer: contract.tokenizer,
      metrics: contract.metrics,
      method_references: contract.method_references,
      metric_reference_ids: contract.metric_reference_ids,
      reference_scope: contract.reference_scope,
      rounding: contract.rounding
    },
    inputs: reviewedInputs,
    declared_segment_analysis: declaredSegmentAnalysis,
    batch_analysis: batchAnalysis,
    difference_second_minus_first: ['paired', 'independent'].includes(relationship)
      ? resultDifference(reviewedInputs[0].result, reviewedInputs[1].result)
      : null,
    warning_codes: warningCodes,
    warning_meanings_ja: Object.fromEntries(warningCodes.map(code => [
      code, contract.workspace.warning_meanings_ja[code]
    ]))
  };
}
