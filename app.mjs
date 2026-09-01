import {
  analyze, analyzeWordCoverage, findMweCandidates, lookupMweForm, makeExportRecord,
  makeMweReviewRecord, mweOccurrencesCsv, parseBatchJson, parseMwePatternTsv,
  prepareMweFormReferenceProfile, prepareWordReferenceProfile, summarizeMweDocument,
  summarizeMweFormCoverage, wordCoverageCsv
} from './metrics.mjs';

const labels = {
  tokens: 'Tokens', types: 'Types',
  type_token_ratio: 'Type-token ratio', hapax_types: 'Hapax types'
};
const metricOrder = Object.keys(labels);
const scenarioStatus = document.getElementById('scenario-status');
const comparison = document.getElementById('comparison');
const scenario = document.getElementById('scenario');
const workspaceForm = document.getElementById('workspace-form');
const relationship = document.getElementById('relationship');
const firstInput = document.getElementById('first-input');
const secondInput = document.getElementById('second-input');
const batchInput = document.getElementById('batch-input');
const workspaceStatus = document.getElementById('workspace-status');
const workspaceResults = document.getElementById('workspace-results');
const exportButton = document.getElementById('export-json');
const mweForm = document.getElementById('mwe-form');
const mweStatus = document.getElementById('mwe-status');
const mweResults = document.getElementById('mwe-results');
let comparisonSets;
let contract;
let mweContract;
let wordProfile;
let mweFormProfile;
let currentExport;
let currentWordCoverage;
let mweDocument;
let mwePatternSource;
let nextMweId = 1;
let analysisRevision = 0;

function downloadText(filename, content, type) {
  const url = URL.createObjectURL(new Blob([content], {type}));
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.append(link);
  link.click();
  link.remove();
  setTimeout(() => URL.revokeObjectURL(url));
}

function ratioText(item) {
  return `${item.numerator}/${item.denominator} (${item.value ?? 'undefined'})`;
}

function reviewedOccurrence(occurrence, status, note) {
  const reviewed = structuredClone(occurrence);
  reviewed.status = status;
  reviewed.decision = status === 'candidate'
    ? null : {source: 'researcher-browser-review', note: note.trim()};
  reviewed.idiomaticity = {status: 'not_assessed', decision: null};
  reviewed.form_lookup = status === 'confirmed'
    ? lookupMweForm(reviewed.canonical_form, mweFormProfile) : null;
  reviewed.sense = status === 'confirmed'
    ? {
        inventory_id: null, inventory_version: null, lookup_status: 'not_attempted',
        candidate_sense_ids: [], assignment_status: 'unassigned',
        selected_sense_ids: [], decision: null
      }
    : null;
  return reviewed;
}

function renderMweTokenPicker() {
  const picker = document.getElementById('mwe-token-picker');
  picker.replaceChildren(...mweDocument.tokens.map(token => {
    const label = document.createElement('label');
    const input = document.createElement('input');
    input.type = 'checkbox';
    input.value = token.id;
    label.className = 'token-choice';
    label.append(input, ` ${token.position}:${token.surface}`);
    return label;
  }));
}

function renderOccurrenceContext(occurrence) {
  const context = document.createElement('div');
  const members = new Set(occurrence.member_token_ids);
  const gaps = new Set(occurrence.gap_token_ids);
  const positions = occurrence.member_token_ids.map(id => Number(id.slice(1)));
  const start = Math.max(0, positions[0] - 4);
  const end = Math.min(mweDocument.tokens.length, positions.at(-1) + 3);
  context.className = 'token-context';
  context.setAttribute('aria-label', 'Candidate context: bold green tokens are members; yellow tokens are gaps.');
  context.replaceChildren(...mweDocument.tokens.slice(start, end).map(token => {
    const span = document.createElement(members.has(token.id) ? 'strong' : 'span');
    if (members.has(token.id)) span.className = 'token-member';
    if (gaps.has(token.id)) span.className = 'token-gap';
    span.textContent = `${token.position}:${token.surface}`;
    return span;
  }));
  return context;
}

function setMweDecision(occurrenceId, status, noteInput) {
  const index = mweDocument.occurrences.findIndex(item => item.id === occurrenceId);
  if (index < 0) return;
  if (status !== 'candidate' && !noteInput.value.trim()) {
    noteInput.setCustomValidity('Confirm／rejectには判断根拠が必要です。');
    noteInput.reportValidity();
    return;
  }
  noteInput.setCustomValidity('');
  mweDocument.occurrences[index] = reviewedOccurrence(
    mweDocument.occurrences[index], status, noteInput.value
  );
  renderMweReview();
}

function occurrenceCard(occurrence) {
  const article = document.createElement('article');
  const heading = document.createElement('h4');
  const source = document.createElement('p');
  const formLookup = document.createElement('p');
  const controls = document.createElement('div');
  const noteField = document.createElement('div');
  const noteLabel = document.createElement('label');
  const note = document.createElement('input');
  const actions = document.createElement('div');
  article.className = 'occurrence-card';
  heading.textContent = `${occurrence.canonical_form} · ${occurrence.category} · ${occurrence.status}`;
  source.className = 'meta';
  source.textContent = occurrence.candidate_source?.kind === 'manual'
    ? 'Candidate source: manually selected members.'
    : `Candidate source: ${occurrence.candidate_source?.pattern_id || 'declared pattern'}.`;
  formLookup.className = 'meta';
  formLookup.textContent = occurrence.status === 'confirmed'
    ? occurrence.form_lookup.status === 'matched'
      ? `OEWN form inventory: matched (${occurrence.form_lookup.sense_count} inventory senses; not contextually assigned).`
      : 'OEWN form inventory: out of inventory; this does not reject the occurrence.'
    : 'OEWN form inventory: lookup begins only after confirmation.';
  noteField.className = 'field';
  noteLabel.htmlFor = `decision-${occurrence.id}`;
  noteLabel.textContent = '判断根拠';
  note.id = `decision-${occurrence.id}`;
  note.type = 'text';
  note.maxLength = 500;
  note.value = occurrence.decision?.note || '';
  note.autocomplete = 'off';
  noteField.append(noteLabel, note);
  actions.className = 'actions';
  for (const [label, status] of [
    ['Confirm', 'confirmed'], ['Reject', 'rejected'], ['未解決', 'candidate']
  ]) {
    const button = document.createElement('button');
    button.type = 'button';
    button.textContent = label;
    button.addEventListener('click', () => setMweDecision(occurrence.id, status, note));
    actions.append(button);
  }
  const remove = document.createElement('button');
  remove.type = 'button';
  remove.textContent = '削除';
  remove.addEventListener('click', () => {
    mweDocument.occurrences = mweDocument.occurrences.filter(item => item.id !== occurrence.id);
    renderMweReview();
  });
  actions.append(remove);
  controls.className = 'occurrence-controls';
  controls.append(noteField, actions);
  article.append(heading, renderOccurrenceContext(occurrence), source, formLookup, controls);
  return article;
}

function renderMweReview() {
  const summary = summarizeMweDocument(mweDocument, mweContract);
  const formCoverage = summarizeMweFormCoverage(mweDocument, mweContract);
  fillDefinitionList(document.getElementById('mwe-summary'), [
    ['MWE-review tokens', String(summary.token_count)],
    ['TUBELEX-profile tokens', String(currentWordCoverage.token_coverage.denominator)],
    ['TUBELEX word-token coverage', ratioText(currentWordCoverage.token_coverage)],
    ['TUBELEX word-type coverage', ratioText(currentWordCoverage.type_coverage)],
    ['Candidates', String(summary.candidate_occurrence_count)],
    ['Confirmed / rejected / unresolved', `${summary.confirmed_occurrence_count} / ${summary.rejected_occurrence_count} / ${summary.unresolved_occurrence_count}`],
    ['Annotation coverage', ratioText(summary.occurrence_annotation_coverage)],
    ['Confirmed member density', ratioText(summary.confirmed_member_density)],
    ['OEWN MWE-form occurrence coverage', ratioText(formCoverage.occurrence_coverage)],
    ['OEWN MWE-form type coverage', ratioText(formCoverage.type_coverage)]
  ]);
  document.getElementById('word-coverage-items').value = [
    'word\ttext_count\tstatus\tsource_count\tfrequency_per_million\tfrequency_rank',
    ...currentWordCoverage.items.map(item => [
      item.word, item.text_count, item.status, item.source_count ?? '',
      item.frequency_per_million ?? '', item.frequency_rank ?? ''
    ].join('\t'))
  ].join('\n');
  renderMweTokenPicker();
  document.getElementById('mwe-occurrences').replaceChildren(
    ...mweDocument.occurrences.map(occurrenceCard)
  );
  mweResults.hidden = false;
  mweStatus.textContent = mweDocument.occurrences.length
    ? `${mweDocument.occurrences.length}件の形式候補を表示しました。文脈を確認して判定してください。`
    : 'パターン一致はありません。tokenを選択して候補を手動追加できます。';
}

function invalidateMweReview() {
  if (!mweDocument) return;
  mweDocument = null;
  currentWordCoverage = null;
  mwePatternSource = null;
  mweResults.hidden = true;
  mweStatus.textContent = '入力を変更しました。候補を再抽出してください。';
}

mweForm.addEventListener('submit', event => {
  event.preventDefault();
  try {
    if (!document.getElementById('mwe-authorization').checked) {
      throw new Error('テキストを処理する権限の確認が必要です。');
    }
    const text = document.getElementById('mwe-text').value;
    mwePatternSource = document.getElementById('mwe-patterns').value;
    const patterns = parseMwePatternTsv(
      mwePatternSource, mweContract.occurrence_record.categories
    );
    mweDocument = {text, ...findMweCandidates(text, patterns)};
    currentWordCoverage = analyzeWordCoverage(text, wordProfile);
    if (!mweDocument.tokens.length) throw new Error('ASCII英語tokenが見つかりません。');
    nextMweId = mweDocument.occurrences.length + 1;
    renderMweReview();
  } catch (error) {
    mweDocument = null;
    currentWordCoverage = null;
    mweResults.hidden = true;
    mweStatus.textContent = error.message;
  }
});

mweForm.addEventListener('reset', () => {
  mweDocument = null;
  currentWordCoverage = null;
  mwePatternSource = null;
  mweResults.hidden = true;
  mweStatus.textContent = 'MWE入力と結果を消去しました。';
});

for (const id of ['mwe-text', 'mwe-patterns', 'mwe-authorization']) {
  document.getElementById(id).addEventListener('input', invalidateMweReview);
}

document.getElementById('add-manual-mwe').addEventListener('click', () => {
  if (!mweDocument) return;
  const selected = [...document.querySelectorAll('#mwe-token-picker input:checked')]
    .map(input => input.value);
  const canonicalForm = document.getElementById('manual-canonical-form');
  if (selected.length < 2 || !canonicalForm.value.trim()) {
    mweStatus.textContent = '手動候補には2個以上のmember tokenとcanonical formが必要です。';
    return;
  }
  const positions = selected.map(id => Number(id.slice(1)));
  const memberSet = new Set(selected);
  const duplicate = mweDocument.occurrences.some(item =>
    item.category === document.getElementById('manual-mwe-category').value &&
    item.canonical_form.toLowerCase() === canonicalForm.value.trim().toLowerCase() &&
    JSON.stringify(item.member_token_ids) === JSON.stringify(selected)
  );
  if (duplicate) {
    mweStatus.textContent = '同じcategory、canonical form、member tokenの候補が既にあります。';
    return;
  }
  mweDocument.occurrences.push({
    id: `mwe-${nextMweId++}`,
    canonical_form: canonicalForm.value.trim(),
    category: document.getElementById('manual-mwe-category').value,
    status: 'candidate',
    member_token_ids: selected,
    gap_token_ids: mweDocument.tokens.slice(positions[0], positions.at(-1) - 1)
      .map(token => token.id).filter(id => !memberSet.has(id)),
    decision: null,
    idiomaticity: {status: 'not_assessed', decision: null},
    form_lookup: null,
    sense: null,
    candidate_source: {kind: 'manual', pattern_id: null}
  });
  canonicalForm.value = '';
  renderMweReview();
});

document.getElementById('export-mwe-csv').addEventListener('click', () => {
  if (!mweDocument) return;
  downloadText(
    'ldfreq-mwe-occurrences.csv',
    mweOccurrencesCsv(mweDocument, mweContract),
    'text/csv;charset=utf-8'
  );
});

document.getElementById('export-word-coverage-csv').addEventListener('click', () => {
  if (!currentWordCoverage) return;
  downloadText(
    'ldfreq-word-coverage.csv', wordCoverageCsv(currentWordCoverage), 'text/csv;charset=utf-8'
  );
});

document.getElementById('export-mwe-json').addEventListener('click', async () => {
  if (!mweDocument) return;
  const record = await makeMweReviewRecord({
    document: mweDocument,
    contract: mweContract,
    patternSource: mwePatternSource,
    tokenizer: contract.tokenizer,
    authorizationAttested: document.getElementById('mwe-authorization').checked,
    generatedAt: new Date().toISOString(),
    wordProfile,
    mweFormProfile
  });
  downloadText('ldfreq-mwe-review.json', JSON.stringify(record, null, 2) + '\n', 'application/json');
});

function fillList(element, items) {
  element.replaceChildren(...items.map(item => {
    const li = document.createElement('li');
    li.textContent = item;
    return li;
  }));
}

function fillReferences(element, references) {
  element.replaceChildren(...Object.values(references).map(reference => {
    const li = document.createElement('li');
    const link = document.createElement('a');
    link.href = reference.url;
    link.textContent = reference.citation;
    li.append(link, ` — ${reference.supports_ja}`);
    return li;
  }));
}

function fillDefinitionList(element, rows) {
  element.replaceChildren(...rows.flatMap(([termText, definitionText, note]) => {
    const term = document.createElement('dt');
    const definition = document.createElement('dd');
    term.textContent = termText;
    definition.textContent = definitionText;
    if (note) {
      const small = document.createElement('span');
      small.className = 'metric-name';
      small.textContent = note;
      term.append(small);
    }
    return [term, definition];
  }));
}

function metricRows(result, definitions = {}) {
  return metricOrder.map(key => [labels[key], String(result[key]), definitions[key]]);
}

function sampleCard(item) {
  const computed = analyze(item.text);
  if (JSON.stringify(computed) !== JSON.stringify(item.result)) {
    throw new Error(`事前計算値が契約と一致しません: ${item.id}`);
  }
  const article = document.createElement('article');
  article.className = 'sample-card';
  const heading = document.createElement('h2');
  const text = document.createElement('div');
  const metrics = document.createElement('dl');
  const provenance = document.createElement('p');
  heading.textContent = item.label_ja;
  text.className = 'sample-text';
  text.textContent = item.text;
  fillDefinitionList(metrics, metricRows(computed, contract.metrics));
  provenance.className = 'meta';
  provenance.textContent = `Provenance: ${item.provenance.authoring_method}. Rights: ${item.provenance.rights_status}.`;
  article.append(heading, text, metrics, provenance);
  return article;
}

function signed(value, decimalPlaces = 0) {
  const rendered = decimalPlaces
    ? value.toFixed(decimalPlaces).replace(/0+$/, '').replace(/\.$/, '')
    : String(value);
  return value > 0 ? `+${rendered}` : rendered;
}

function differenceRows(first, second) {
  return [
    ['Tokens', signed(second.tokens - first.tokens)],
    ['Types', signed(second.types - first.types)],
    ['Type-token ratio', signed(second.type_token_ratio - first.type_token_ratio, 6)],
    ['Hapax types', signed(second.hapax_types - first.hapax_types)]
  ];
}

function setDependencyNote(element, first, second) {
  const strong = document.createElement('strong');
  const detail = document.createTextNode(
    first.tokens === second.tokens
      ? ' 同じtoken数では、Typesの差をtoken数で割った値がTTRの差です。'
      : ' この比較では分子と分母が同時に変わるため、TTR差を文数だけの効果として分離できません。'
  );
  strong.textContent = first.tokens === second.tokens
    ? 'TypesとTTRは独立した証拠ではありません。'
    : 'TTRはTypes ÷ Tokensです。';
  element.replaceChildren(strong, detail);
}

function renderComparison(set) {
  document.getElementById('question').textContent = set.question_ja;
  fillList(document.getElementById('held'), set.design.held_constant_ja);
  fillList(document.getElementById('uncontrolled'), set.design.not_controlled_ja);
  document.getElementById('manipulation').textContent = set.design.manipulated_ja;
  document.getElementById('interpretation').textContent = set.design.interpretation_ja;
  document.getElementById('cards').replaceChildren(...set.samples.map(sampleCard));
  const [first, second] = set.samples.map(item => analyze(item.text));
  document.getElementById('difference-direction').textContent =
    `${set.samples[1].label_ja} − ${set.samples[0].label_ja}。正負は良し悪しを意味しません。`;
  fillDefinitionList(document.getElementById('differences'), differenceRows(first, second));
  setDependencyNote(document.getElementById('dependency-note'), first, second);
  scenarioStatus.textContent = `「${set.label_ja}」を表示しました。統制範囲と限界を先に確認してください。`;
}

function updateWorkspaceMode() {
  const usesBatch = relationship.value === 'batch';
  const usesSecond = ['paired', 'independent'].includes(relationship.value);
  firstInput.hidden = usesBatch;
  for (const control of firstInput.querySelectorAll('input, textarea')) {
    control.disabled = usesBatch;
    control.setCustomValidity('');
  }
  secondInput.hidden = !usesSecond;
  for (const control of secondInput.querySelectorAll('input, textarea')) {
    control.disabled = !usesSecond;
    control.setCustomValidity('');
  }
  batchInput.hidden = !usesBatch;
  for (const control of batchInput.querySelectorAll('textarea')) {
    control.disabled = !usesBatch;
    control.setCustomValidity('');
  }
}

function invalidateWorkspace(message = '入力を変更しました。再計算してください。') {
  analysisRevision += 1;
  if (!currentExport) return;
  currentExport = null;
  exportButton.disabled = true;
  workspaceResults.hidden = true;
  workspaceStatus.textContent = message;
}

function workspaceInput(suffix) {
  return {
    id: suffix.toLowerCase(),
    label: document.getElementById(`label-${suffix}`).value,
    provenance: document.getElementById(`provenance-${suffix}`).value,
    text: document.getElementById(`text-${suffix}`).value
  };
}

function workspaceInputs() {
  if (relationship.value === 'batch') {
    return parseBatchJson(
      document.getElementById('batch-json').value,
      contract.input.max_utf16_code_units_per_batch_json
    );
  }
  const inputs = [workspaceInput('A')];
  if (['paired', 'independent'].includes(relationship.value)) inputs.push(workspaceInput('B'));
  return inputs;
}

function workspaceCard(item, pooled) {
  const article = document.createElement('article');
  article.className = 'sample-card';
  const heading = document.createElement('h3');
  const metrics = document.createElement('dl');
  const provenance = document.createElement('p');
  const digest = document.createElement('p');
  heading.textContent = pooled ? `${item.label}（全文pool）` : item.label;
  fillDefinitionList(metrics, metricRows(item.result));
  provenance.className = 'meta';
  provenance.textContent = `Source/rights: ${item.provenance}`;
  digest.className = 'hash';
  digest.textContent = `SHA-256 (UTF-8): ${item.sha256_utf8}`;
  article.append(heading, metrics, provenance, digest);
  return article;
}

function renderWorkspace(record) {
  const workspaceCards = document.getElementById('workspace-cards');
  workspaceCards.hidden = Boolean(record.batch_analysis);
  workspaceCards.replaceChildren(...(record.batch_analysis ? [] : record.inputs.map(
    item => workspaceCard(item, Boolean(record.declared_segment_analysis))
  )));
  const hasDifference = record.difference_second_minus_first !== null;
  document.getElementById('workspace-difference-panel').hidden = !hasDifference;
  if (hasDifference) {
    const [first, second] = record.inputs.map(item => item.result);
    fillDefinitionList(
      document.getElementById('workspace-differences'), differenceRows(first, second)
    );
    setDependencyNote(document.getElementById('workspace-dependency-note'), first, second);
  }
  const segmentPanel = document.getElementById('segment-panel');
  segmentPanel.hidden = !record.declared_segment_analysis;
  if (record.declared_segment_analysis) {
    const segmentAnalysis = record.declared_segment_analysis;
    const range = key => {
      const item = segmentAnalysis.distribution[key];
      return `${item.minimum} / ${item.median} / ${item.maximum}`;
    };
    fillDefinitionList(document.getElementById('segment-summary'), [
      ['Declared units', String(segmentAnalysis.segment_count)],
      ['Tokens min / median / max', range('tokens')],
      ['TTR min / median / max', range('type_token_ratio')]
    ]);
    document.getElementById('segment-rows').replaceChildren(
      ...segmentAnalysis.segments.map(segment => {
        const row = document.createElement('tr');
        const values = [
          `Unit ${segment.index}`, segment.result.tokens, segment.result.types,
          segment.result.type_token_ratio, segment.result.hapax_types
        ];
        row.replaceChildren(...values.map((value, index) => {
          const cell = document.createElement(index === 0 ? 'th' : 'td');
          if (index === 0) cell.scope = 'row';
          cell.textContent = String(value);
          return cell;
        }));
        return row;
      })
    );
  }
  const batchPanel = document.getElementById('batch-panel');
  batchPanel.hidden = !record.batch_analysis;
  if (record.batch_analysis) {
    const range = key => {
      const item = record.batch_analysis.distribution[key];
      return `${item.minimum} / ${item.median} / ${item.maximum}`;
    };
    fillDefinitionList(document.getElementById('batch-summary'), [
      ['Documents', String(record.batch_analysis.document_count)],
      ['Tokens min / median / max', range('tokens')],
      ['TTR min / median / max', range('type_token_ratio')]
    ]);
    document.getElementById('batch-rows').replaceChildren(...record.inputs.map(item => {
      const row = document.createElement('tr');
      const values = [
        `${item.id}: ${item.label}`, item.provenance, item.result.tokens, item.result.types,
        item.result.type_token_ratio, item.result.hapax_types, item.sha256_utf8
      ];
      row.replaceChildren(...values.map((value, index) => {
        const cell = document.createElement(index === 0 ? 'th' : 'td');
        if (index === 0) cell.scope = 'row';
        if (index === values.length - 1) cell.className = 'hash';
        cell.textContent = String(value);
        return cell;
      }));
      return row;
    }));
  }
  fillList(
    document.getElementById('workspace-warning-codes'),
    record.warning_codes.map(code =>
      `${code}: ${contract.workspace.warning_meanings_ja[code]}`
    )
  );
  workspaceResults.hidden = false;
}

workspaceForm.addEventListener('submit', async event => {
  event.preventDefault();
  invalidateWorkspace('再計算しています…');
  workspaceStatus.textContent = '端末内で計算しています…';
  const revision = analysisRevision;
  try {
    const inputs = workspaceInputs();
    const exportRecord = await makeExportRecord({
      contract,
      relationship: relationship.value,
      designNote: document.getElementById('design-note').value,
      contentScopeAttested: document.getElementById('rights-attestation').checked,
      inputs,
      generatedAt: new Date().toISOString()
    });
    if (revision !== analysisRevision) {
      workspaceStatus.textContent = '計算中に入力が変わりました。もう一度計算してください。';
      return;
    }
    currentExport = exportRecord;
    renderWorkspace(currentExport);
    exportButton.disabled = false;
    workspaceStatus.textContent = '計算完了。本文は送信・保存されず、JSONにも含まれません。';
  } catch (error) {
    if (revision === analysisRevision) workspaceStatus.textContent = error.message;
  }
});

workspaceForm.addEventListener('reset', () => {
  analysisRevision += 1;
  currentExport = null;
  exportButton.disabled = true;
  workspaceResults.hidden = true;
  workspaceStatus.textContent = '入力と画面上の結果を消去しました。';
  setTimeout(updateWorkspaceMode);
});

window.addEventListener('pagehide', () => {
  workspaceForm.reset();
  mweForm.reset();
});

relationship.addEventListener('change', updateWorkspaceMode);
relationship.addEventListener('change', () => invalidateWorkspace());
workspaceForm.addEventListener('input', () => invalidateWorkspace());

exportButton.addEventListener('click', () => {
  if (!currentExport) return;
  downloadText(
    'ldfreq-analysis.json', JSON.stringify(currentExport, null, 2) + '\n', 'application/json'
  );
});

async function initialize() {
  try {
    const [
      samplesResponse, contractResponse, mweContractResponse, wordProfileResponse,
      mweFormProfileResponse
    ] = await Promise.all([
      fetch('samples.json'), fetch('metric_contract.json'), fetch('mwe_contract.json'),
      fetch('resources/tubelex_en_regex_ascii_2025.json'),
      fetch('resources/oewn_2025_multiword_verbs.json')
    ]);
    if (!samplesResponse.ok || !contractResponse.ok || !mweContractResponse.ok ||
        !wordProfileResponse.ok || !mweFormProfileResponse.ok) {
      throw new Error('比較データを読み込めませんでした。');
    }
    const sampleDocument = await samplesResponse.json();
    contract = await contractResponse.json();
    mweContract = await mweContractResponse.json();
    wordProfile = prepareWordReferenceProfile(await wordProfileResponse.json());
    mweFormProfile = prepareMweFormReferenceProfile(await mweFormProfileResponse.json());
    comparisonSets = sampleDocument.comparison_sets;
    scenario.replaceChildren(...comparisonSets.map((set, index) => {
      const option = document.createElement('option');
      option.value = String(index);
      option.textContent = set.label_ja;
      return option;
    }));
    document.getElementById('contract-version').textContent =
      `Contract ${contract.contract_version} · ${contract.status}`;
    fillDefinitionList(
      document.getElementById('method'), metricOrder.map(key => [labels[key], contract.metrics[key]])
    );
    fillReferences(document.getElementById('method-references'), contract.method_references);
    for (const id of ['text-A', 'text-B']) {
      document.getElementById(id).maxLength = contract.input.max_utf16_code_units_per_text;
    }
    document.getElementById('batch-json').maxLength =
      contract.input.max_utf16_code_units_per_batch_json;
    scenario.addEventListener('change', () => renderComparison(comparisonSets[Number(scenario.value)]));
    comparison.hidden = false;
    renderComparison(comparisonSets[0]);
    updateWorkspaceMode();
    document.getElementById('mwe-analyze-button').disabled = false;
    document.getElementById('analyze-button').disabled = false;
  } catch (error) {
    scenarioStatus.textContent = error.message;
    mweStatus.textContent = error.message;
    for (const form of [mweForm, workspaceForm]) {
      form.querySelectorAll('input, textarea, select, button').forEach(control => {
        control.disabled = true;
      });
    }
  }
}

initialize();
