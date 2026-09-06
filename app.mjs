import {
  analyze, analyzeWordCoverage, findMweCandidates, lookupMweForm, lookupMweSenses,
  makeExportRecord, makeMweDocumentSetRecord, makeMweReviewRecord, makeMweWorkspaceRecord,
  mweOccurrencesCsv, parseBatchJson, parseJsonInput,
  parseMwePatternTsv, prepareMweFormReferenceProfile, prepareMweSenseReferenceProfile,
  prepareWordReferenceProfile, restoreMweDocumentSetRecord, restoreMweWorkspaceRecord, sha256,
  summarizeMweDocument, summarizeMweFormCoverage, wordCoverageCsv
} from './metrics.mjs';

const localBncCocaProfile = {
  id: 'bnc-coca-level6-v1.0.0-first-2k-local',
  size: 366120,
  sha256: 'ebd06548187988eb1a61ab967cc39c01461023043ee7aef427606e5bf508f138'
};

const labels = {
  tokens: 'Tokens', types: 'Types',
  type_token_ratio: 'Type-token ratio', hapax_types: 'Hapax types'
};
const occurrenceStatusLabels = {
  candidate: '未確定（候補）', confirmed: '成立（利用者確認済み）', rejected: '不成立（利用者確認済み）'
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
const mweDocumentSetForm = document.getElementById('mwe-document-set-form');
const mweStatus = document.getElementById('mwe-status');
const mweResults = document.getElementById('mwe-results');
let comparisonSets;
let contract;
let mweContract;
let wordProfiles;
let currentWordProfile;
let currentWordRankCutoff = null;
let mweFormProfile;
let mweSenseProfile;
let currentExport;
let currentWordCoverage;
let mweDocument;
let mwePatternSource;
let nextMweId = 1;
let mweDocumentSetIdentity;
let mweDocumentSet = new Map();
let currentSetDocumentId;
let mweDocumentDirty = false;
let mweRevision = 0;
let analysisRevision = 0;
let clearingOnPageExit = false;

function warnOnPageExit(event) {
  event.preventDefault();
  event.returnValue = true;
}

function updatePageExitWarning() {
  const hasWork = mweDocument || currentExport || mweDocumentSet.size ||
    [mweForm, mweDocumentSetForm, workspaceForm].some(form =>
      [...form.querySelectorAll('input[type="text"], textarea:not([readonly])')]
        .some(input => input.value !== input.defaultValue));
  // Downloads cannot confirm a saved file: retain protection while work is present.
  window[hasWork ? 'addEventListener' : 'removeEventListener']('beforeunload', warnOnPageExit);
}

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

function pendingMweEdits() {
  if (!mweDocument) return [];
  const edits = [];
  const input = id => document.getElementById(id);
  const add = (label, fields) => {
    const changed = fields.find(([control, saved]) => control &&
      (control.type === 'checkbox' ? control.checked !== saved : control.value.trim() !== saved?.trim()));
    if (changed) edits.push({label, control: changed[0]});
  };
  mweDocument.occurrences.forEach((occurrence, index) => {
    const label = `候補${index + 1}「${occurrence.canonical_form}」`;
    add(`${label}の成立判断`, [
      [input(`decision-${occurrence.id}`), occurrence.decision?.note || '']
    ]);
    add(`${label}の慣用性`, [
      [input(`idiomaticity-${occurrence.id}`), occurrence.idiomaticity.status],
      [input(`idiomaticity-note-${occurrence.id}`), occurrence.idiomaticity.decision?.note || '']
    ]);
    const senseStatus = input(`sense-status-${occurrence.id}`);
    const choices = senseStatus?.closest('.sense-review').querySelectorAll('input[type="checkbox"]') || [];
    add(`${label}の語義`, [
      [senseStatus, occurrence.sense?.assignment_status],
      [input(`sense-note-${occurrence.id}`), occurrence.sense?.decision?.note || ''],
      ...[...choices].map(choice => [choice, occurrence.sense.selected_sense_ids.includes(choice.value)])
    ]);
  });
  add('手動候補の追加', [
    [input('manual-canonical-form'), ''],
    ...[...document.querySelectorAll('#mwe-token-picker input')].map(choice => [choice, false])
  ]);
  return edits;
}

function focusMweEdit(control) {
  const details = control.closest('details');
  if (details) details.open = true;
  control.focus();
  control.scrollIntoView({block: 'center'});
}

function updateMwePendingEdits() {
  updatePageExitWarning();
  const edits = pendingMweEdits();
  const current = document.getElementById('mwe-current-document-status');
  current.textContent = !mweDocument ? '現在開いているレビューはありません。'
    : !currentSetDocumentId ? '現在のレビューは文書セットに未追加です。'
      : `現在の文書：${currentSetDocumentId}。` + (mweDocumentDirty
        ? '編集内容を文書セットへ追加／更新してください。'
        : '記録済みのレビューと文書名は、ページのメモリ内のセットに反映済みです。');
  if (edits.length) current.textContent += '画面に未記録の編集があります。各欄で記録してからセットを更新してください。';
  document.getElementById('mwe-pending-edits').hidden = !edits.length;
  document.getElementById('mwe-pending-status').textContent = edits.length
    ? `${edits.length}項目に未記録の編集があります。` : '';
  const list = document.getElementById('mwe-pending-list');
  const keys = JSON.stringify(edits.map(edit => [edit.label, edit.control.id || edit.control.value]));
  // Keep return buttons in place when blur/change repeats the same edit list.
  if (list.dataset.editKeys === keys) return edits;
  list.dataset.editKeys = keys;
  list.replaceChildren(...edits.map(edit => {
    const item = document.createElement('li');
    const button = document.createElement('button');
    button.type = 'button';
    button.textContent = `${edit.label}へ戻る`;
    button.addEventListener('click', () => focusMweEdit(edit.control));
    item.append(button);
    return item;
  }));
  return edits;
}

function ensureMweEditsRecorded() {
  const edits = updateMwePendingEdits();
  if (!edits.length) return true;
  mweStatus.textContent = '保存を中止しました。未記録の編集を各欄で記録するか、編集前の値に戻してください。未確定の候補自体はそのまま保存できます。';
  focusMweEdit(edits[0].control);
  return false;
}

function lockMweSourceInputs(locked) {
  for (const id of [
    'mwe-text', 'mwe-patterns', 'word-reference', 'mwe-authorization',
    'bnc-coca-profile', 'mwe-workspace-file', 'mwe-analyze-button'
  ]) document.getElementById(id).disabled = locked;
}

function reviewedOccurrence(occurrence, status, note) {
  const reviewed = structuredClone(occurrence);
  const previousStatus = reviewed.status;
  reviewed.status = status;
  reviewed.decision = status === 'candidate'
    ? null : {source: 'researcher-browser-review', note: note.trim()};
  if (status === 'candidate') {
    reviewed.idiomaticity = {status: 'not_assessed', decision: null};
    reviewed.form_lookup = null;
    reviewed.sense = null;
  } else {
    if (previousStatus === 'candidate') {
      reviewed.idiomaticity = {status: 'not_assessed', decision: null};
    }
    reviewed.form_lookup = status === 'confirmed'
      ? lookupMweForm(reviewed.canonical_form, mweFormProfile) : null;
    reviewed.sense = status === 'confirmed'
      ? previousStatus === 'confirmed'
        ? reviewed.sense
        : lookupMweSenses(reviewed.canonical_form, mweSenseProfile).state
      : null;
  }
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
    noteInput.setCustomValidity('成立／不成立の記録には判断根拠が必要です。');
    noteInput.reportValidity();
    return;
  }
  noteInput.setCustomValidity('');
  const previousStatus = mweDocument.occurrences[index].status;
  const card = noteInput.closest('.occurrence-card');
  const discardsDrafts = previousStatus !== status && pendingMweEdits().some(edit =>
    edit.control !== noteInput && card.contains(edit.control)
  );
  const resetsDecision = status === 'candidate' &&
    (previousStatus !== 'candidate' || noteInput.value.trim());
  const removesSense = previousStatus === 'confirmed' && status === 'rejected';
  if (resetsDecision || removesSense || discardsDrafts) {
    const effect = resetsDecision
      ? '成立判断・慣用性・語義の記録と、この候補の入力途中の編集を消去して未確定に戻します。'
      : removesSense
        ? '不成立として記録し、語義の記録と、この候補の慣用性・語義の入力途中の編集を消去します。記録済みの慣用性は保持します。'
        : '成立として記録し、この候補の入力途中の慣用性・語義の編集を消去します。';
    if (!window.confirm(`「${mweDocument.occurrences[index].canonical_form}」について、${effect}続けますか？`)) return;
  }
  mweRevision += 1;
  mweDocument.occurrences[index] = reviewedOccurrence(
    mweDocument.occurrences[index], status, noteInput.value
  );
  if (previousStatus !== status) {
    noteInput.closest('.occurrence-card').replaceWith(
      occurrenceCard(mweDocument.occurrences[index])
    );
    document.getElementById(`decision-${occurrenceId}-${status}`).focus();
  } else {
    noteInput.value = mweDocument.occurrences[index].decision?.note || '';
  }
  renderMweReviewSummary();
}

function setIdiomaticity(occurrenceId, statusSelect, noteInput) {
  const occurrence = mweDocument.occurrences.find(item => item.id === occurrenceId);
  if (!occurrence || occurrence.status === 'candidate') return;
  const assessed = statusSelect.value !== 'not_assessed';
  if (assessed && !noteInput.value.trim()) {
    noteInput.setCustomValidity('Idiomaticityの判断根拠が必要です。');
    noteInput.reportValidity();
    return;
  }
  noteInput.setCustomValidity('');
  if (!assessed && (occurrence.idiomaticity.status !== 'not_assessed' || noteInput.value.trim()) &&
      !window.confirm(`「${occurrence.canonical_form}」の慣用性を未判定に戻し、その判断根拠を消去しますか？成立判断と語義の記録・入力途中の編集は保持します。`)) return;
  mweRevision += 1;
  occurrence.idiomaticity = {
    status: statusSelect.value,
    decision: assessed
      ? {source: 'researcher-browser-review', note: noteInput.value.trim()}
      : null
  };
  noteInput.value = occurrence.idiomaticity.decision?.note || '';
  renderMweReviewSummary();
}

function setSenseDecision(occurrenceId, statusSelect, choices, noteInput) {
  const occurrence = mweDocument.occurrences.find(item => item.id === occurrenceId);
  if (!occurrence || occurrence.status !== 'confirmed' ||
      occurrence.sense.lookup_status !== 'matched') return;
  const status = statusSelect.value;
  const selected = [...choices.querySelectorAll('input:checked')].map(input => input.value);
  const multiple = ['multiple_assigned', 'ambiguous'].includes(status);
  const requiredCount = status === 'assigned' ? 1 : multiple ? 2 : 0;
  const wrongCount = multiple
    ? selected.length < requiredCount : selected.length !== requiredCount;
  if (wrongCount) {
    statusSelect.setCustomValidity(
      status === 'assigned' ? 'Assignedは語義を1件選択します。'
        : multiple ? '複数語義の判定では語義を2件以上選択します。'
          : '未判定／棄権／該当語義なしでは語義を選択しません。'
    );
    statusSelect.reportValidity();
    return;
  }
  const decided = status !== 'unassigned';
  if (decided && !noteInput.value.trim()) {
    noteInput.setCustomValidity('語義判断または棄権の根拠が必要です。');
    noteInput.reportValidity();
    return;
  }
  statusSelect.setCustomValidity('');
  noteInput.setCustomValidity('');
  if (!decided && (occurrence.sense.assignment_status !== 'unassigned' || noteInput.value.trim()) &&
      !window.confirm(`「${occurrence.canonical_form}」の語義を未判定に戻し、その判断・棄権の根拠を消去しますか？成立判断と慣用性は保持します。`)) return;
  mweRevision += 1;
  occurrence.sense.assignment_status = status;
  occurrence.sense.selected_sense_ids = selected;
  occurrence.sense.decision = decided
    ? {source: 'researcher-browser-review', note: noteInput.value.trim()}
    : null;
  noteInput.value = occurrence.sense.decision?.note || '';
  renderMweReviewSummary();
}

function idiomaticityReview(occurrence) {
  const fieldset = document.createElement('fieldset');
  const legend = document.createElement('legend');
  const statusLabel = document.createElement('label');
  const status = document.createElement('select');
  const noteLabel = document.createElement('label');
  const note = document.createElement('input');
  const apply = document.createElement('button');
  legend.textContent = '文脈内のidiomaticity（構造category・語義とは別）';
  status.id = `idiomaticity-${occurrence.id}`;
  statusLabel.htmlFor = status.id;
  statusLabel.textContent = '判定';
  for (const [value, label] of Object.entries({
    not_assessed: '未判定', idiomatic: '慣用的', literal: '字義通り', ambiguous: '判断が曖昧'
  })) {
    const option = document.createElement('option');
    option.value = value;
    option.textContent = label;
    option.selected = occurrence.idiomaticity.status === value;
    status.append(option);
  }
  note.id = `idiomaticity-note-${occurrence.id}`;
  note.type = 'text';
  note.maxLength = 500;
  note.autocomplete = 'off';
  note.value = occurrence.idiomaticity.decision?.note || '';
  noteLabel.htmlFor = note.id;
  noteLabel.textContent = '判断根拠';
  apply.type = 'button';
  apply.textContent = 'Idiomaticityを保存';
  apply.addEventListener('click', () => setIdiomaticity(occurrence.id, status, note));
  fieldset.className = 'review-fieldset';
  fieldset.append(legend, statusLabel, status, noteLabel, note, apply);
  return fieldset;
}

function senseReview(occurrence) {
  const details = document.createElement('details');
  const summary = document.createElement('summary');
  const lookup = lookupMweSenses(occurrence.canonical_form, mweSenseProfile);
  details.className = 'sense-review';
  if (occurrence.sense.lookup_status !== 'matched') {
    summary.textContent = occurrence.sense.lookup_status === 'inventory_ineligible'
      ? 'Contextual sense：現行参照範囲の対象外'
      : occurrence.sense.lookup_status === 'out_of_inventory'
        ? 'Contextual sense：候補なし'
        : 'Contextual sense：未検索';
    const note = document.createElement('p');
    note.className = 'meta';
    note.textContent = occurrence.sense.lookup_status === 'inventory_ineligible'
      ? '現在読み込まれている参照語義の適用範囲外です。語義が存在しないという判定ではありません。'
      : '完全な参照範囲を検索した結果です。';
    details.append(summary, note);
    return details;
  }
  summary.textContent = `OEWN contextual sense review（${lookup.senses.length}候補）`;
  const warning = document.createElement('p');
  warning.className = 'meta';
  warning.textContent = '辞書候補は文脈上の正解、頻度、学習者知識を決めません。';
  const statusLabel = document.createElement('label');
  const status = document.createElement('select');
  status.id = `sense-status-${occurrence.id}`;
  statusLabel.htmlFor = status.id;
  statusLabel.textContent = '語義判定';
  const senseLabels = {
    unassigned: '未判定',
    assigned: '1語義',
    multiple_assigned: '複数語義が同時成立',
    ambiguous: '複数候補間で曖昧',
    abstained: '判断を棄権',
    out_of_inventory: '該当語義なし'
  };
  for (const value of Object.keys(senseLabels)) {
    const option = document.createElement('option');
    option.value = value;
    option.textContent = senseLabels[value];
    option.selected = occurrence.sense.assignment_status === value;
    status.append(option);
  }
  const choices = document.createElement('fieldset');
  const choicesLegend = document.createElement('legend');
  choicesLegend.textContent = '候補語義';
  choices.className = 'sense-choices';
  choices.append(choicesLegend);
  lookup.senses.forEach((sense, index) => {
    const label = document.createElement('label');
    const input = document.createElement('input');
    const description = document.createElement('span');
    input.id = `sense-${occurrence.id}-${index + 1}`;
    input.type = 'checkbox';
    input.value = sense.sense_id;
    input.checked = occurrence.sense.selected_sense_ids.includes(sense.sense_id);
    description.textContent = `${sense.sense_id} — ${sense.definitions.join('; ')}`;
    const example = [...sense.entry_examples, ...sense.synset_examples][0];
    if (example) description.append(document.createElement('br'), `例: ${example}`);
    label.className = 'sense-choice';
    label.append(input, description);
    choices.append(label);
  });
  const noteLabel = document.createElement('label');
  const note = document.createElement('input');
  note.id = `sense-note-${occurrence.id}`;
  note.type = 'text';
  note.maxLength = 500;
  note.autocomplete = 'off';
  note.value = occurrence.sense.decision?.note || '';
  noteLabel.htmlFor = note.id;
  noteLabel.textContent = '判断／棄権の根拠';
  const apply = document.createElement('button');
  apply.type = 'button';
  apply.textContent = 'Contextual senseを保存';
  apply.addEventListener('click', () => {
    setSenseDecision(occurrence.id, status, choices, note);
  });
  details.append(summary, warning, statusLabel, status, choices, noteLabel, note, apply);
  return details;
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
  heading.textContent = `${occurrence.canonical_form} · ${occurrence.category} · ${occurrenceStatusLabels[occurrence.status]}`;
  source.className = 'meta';
  source.textContent = occurrence.candidate_source?.kind === 'manual'
    ? '候補の追加方法：利用者が構成語を選択。'
    : `候補の追加方法：指定パターンとの一致（${occurrence.candidate_source?.pattern_id || '利用者指定'}）。`;
  formLookup.className = 'meta';
  formLookup.textContent = occurrence.status === 'confirmed'
    ? occurrence.form_lookup.status === 'matched'
      ? `OEWNに同じ表現が収録されています（辞書語義${occurrence.form_lookup.sense_count}件）。文脈上の語義を確定するものではありません。`
      : 'OEWNの参照範囲に同じ表現はありません。この用例が不成立という意味ではありません。'
    : 'OEWNとの照合は、利用者が成立を確認した後に行います。';
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
    ['成立として記録', 'confirmed'], ['不成立として記録', 'rejected'], ['未確定に戻す', 'candidate']
  ]) {
    const button = document.createElement('button');
    button.id = `decision-${occurrence.id}-${status}`;
    button.type = 'button';
    button.textContent = label;
    button.addEventListener('click', () => setMweDecision(occurrence.id, status, note));
    actions.append(button);
  }
  const remove = document.createElement('button');
  remove.type = 'button';
  remove.textContent = '削除';
  remove.addEventListener('click', () => {
    if (!window.confirm(`「${occurrence.canonical_form}」のこの候補を、記録済みの判断・根拠と入力途中の編集を含めて削除しますか？他の候補は変更しません。`)) return;
    const nextFocus = article.nextElementSibling?.querySelector('button') ||
      article.previousElementSibling?.querySelector('button') ||
      document.getElementById('add-manual-mwe');
    mweRevision += 1;
    mweDocument.occurrences = mweDocument.occurrences.filter(item => item.id !== occurrence.id);
    article.remove();
    nextFocus.focus();
    renderMweReviewSummary();
  });
  actions.append(remove);
  controls.className = 'occurrence-controls';
  controls.append(noteField, actions);
  article.append(heading, renderOccurrenceContext(occurrence), source, formLookup, controls);
  if (occurrence.status !== 'candidate') article.append(idiomaticityReview(occurrence));
  if (occurrence.status === 'confirmed') article.append(senseReview(occurrence));
  return article;
}

function renderMweReview() {
  renderMweTokenPicker();
  document.getElementById('mwe-occurrences').replaceChildren(
    ...mweDocument.occurrences.map(occurrenceCard)
  );
  renderMweReviewSummary();
}

function renderMweReviewSummary() {
  const summary = summarizeMweDocument(mweDocument, mweContract);
  const formCoverage = summarizeMweFormCoverage(mweDocument, mweContract);
  const wordProfileLabel = currentWordCoverage.selected_rank_cutoff
    ? `${currentWordCoverage.profile_title} first ${currentWordCoverage.selected_rank_cutoff}`
    : currentWordCoverage.profile_title;
  fillDefinitionList(document.getElementById('mwe-summary'), [
    ['MWE-review tokens', String(summary.token_count)],
    ['Word-profile tokens', String(currentWordCoverage.token_coverage.denominator)],
    [`${wordProfileLabel} token coverage`, ratioText(currentWordCoverage.token_coverage)],
    [`${wordProfileLabel} type coverage`, ratioText(currentWordCoverage.type_coverage)],
    ['候補の総数', String(summary.candidate_occurrence_count)],
    ['成立 / 不成立 / 未確定', `${summary.confirmed_occurrence_count} / ${summary.rejected_occurrence_count} / ${summary.unresolved_occurrence_count}`],
    ['Annotation coverage', ratioText(summary.occurrence_annotation_coverage)],
    ['Idiomaticity annotation coverage', ratioText(summary.idiomaticity_annotation_coverage)],
    ['Confirmed member density', ratioText(summary.confirmed_member_density)],
    ['OEWN MWE-form occurrence coverage', ratioText(formCoverage.occurrence_coverage)],
    ['OEWN MWE-form type coverage', ratioText(formCoverage.type_coverage)],
    ['OEWN target-sense inventory coverage', ratioText(summary.sense_inventory_coverage)],
    ['Contextual sense assignment coverage', ratioText(summary.sense_assignment_coverage)]
  ]);
  document.getElementById('word-coverage-items').value = [
    'word\ttext_count\tstatus\tsource_count\tfrequency_per_million\tfrequency_rank\thead_mappings\tminimum_head_rank',
    ...currentWordCoverage.items.map(item => [
      item.word, item.text_count, item.status, item.source_count ?? '',
      item.frequency_per_million ?? '', item.frequency_rank ?? '',
      item.head_mappings.map(mapping => `${mapping.lemma}:${mapping.rank}`).join(' '),
      item.minimum_head_rank ?? ''
    ].join('\t'))
  ].join('\n');
  mweResults.hidden = false;
  mweDocumentDirty = true;
  lockMweSourceInputs(true);
  mweStatus.textContent = mweDocument.occurrences.length
    ? `${mweDocument.occurrences.length}件中、成立${summary.confirmed_occurrence_count}件・不成立${summary.rejected_occurrence_count}件・未確定${summary.unresolved_occurrence_count}件です。判定は利用者によるもので、自動判定ではありません。本文の変更・再抽出には、作業をファイルに保存してから入力と結果を消去してください。`
    : '指定パターンとの一致はありません。句動詞・イディオムが存在しないという判定ではありません。構成語を選択して候補を手動追加できます。本文の変更には、必要な作業をファイルに保存してから入力と結果を消去してください。';
  updateMwePendingEdits();
}

function invalidateMweReview() {
  if (!mweDocument) return;
  mweDocument = null;
  currentSetDocumentId = null;
  mweDocumentDirty = false;
  currentWordCoverage = null;
  currentWordProfile = null;
  currentWordRankCutoff = null;
  mwePatternSource = null;
  mweResults.hidden = true;
  mweStatus.textContent = '入力を変更しました。候補を再抽出してください。';
}

async function readMweResumeFile(file, specification) {
  if (!file || file.size > specification.maximum_json_file_bytes) {
    throw new Error('再開用JSONが選択されていないか、読込サイズの上限を超えています。');
  }
  let source;
  try {
    source = await file.text();
  } catch {
    throw new Error('ファイルを読み取れませんでした。端末で利用できる保存コピーを選び直してください。');
  }
  let record;
  try {
    record = parseJsonInput(source, specification.maximum_json_utf16_code_units);
  } catch {
    throw new Error('ファイルをJSONとして読み込めませんでした。内容や読込上限を確認し、元のファイルを書き換えずに別の保存コピーを選び直してください。');
  }
  if (record?.schema_version !== specification.schema_version) {
    if (record?.schema_version === mweContract.workspace_file.schema_version) {
      throw new Error('これは1文書の再開用JSONです。「保存した再開用JSONを開く」で選択してください。');
    }
    if (record?.schema_version === mweContract.document_set_file.schema_version) {
      throw new Error('これは文書セットJSONです。「MWE文書セットJSONを再開」で選択してください。');
    }
    throw new Error('このファイルは対応する再開用JSONではありません。CSV・方法JSONからは再開できません。再開用の保存コピーと、保存時のアプリを確認してください。');
  }
  return record;
}

function mweResumeValidationError() {
  return new Error('保存内容の整合性、またはこのアプリ・参照リストとの互換性を確認できませんでした。ファイルは書き換えず、別の保存コピーか保存時のアプリを確認してください。ローカル参照リストが必要な作業は、先に同じリストを読み込んでください。');
}

document.getElementById('bnc-coca-profile').addEventListener('change', async event => {
  const revision = ++mweRevision;
  const [file] = event.target.files;
  event.target.value = '';
  const status = document.getElementById('bnc-coca-profile-status');
  if (mweDocument) {
    status.textContent = '現在のレビューを保存し、入力と結果を消去してから参照リストを読み込んでください。現在のレビューと参照リストは変更していません。';
    return;
  }
  try {
    if (!file || file.size !== localBncCocaProfile.size) {
      throw new Error('指定されたBNC/COCAローカルprofileのサイズが一致しません。');
    }
    const source = await file.text();
    if (revision !== mweRevision) return;
    const runtimeHash = await sha256(source);
    if (revision !== mweRevision) return;
    if (runtimeHash !== localBncCocaProfile.sha256) {
      throw new Error('指定されたBNC/COCAローカルprofileのSHA-256が一致しません。');
    }
    const profile = prepareWordReferenceProfile(
      parseJsonInput(source, localBncCocaProfile.size, 'Local word profile JSON')
    );
    if (profile.profile.identity.profile_id !== localBncCocaProfile.id) {
      throw new Error('指定されたローカルprofile IDが一致しません。');
    }
    profile.runtimeProfileSha256 = runtimeHash;
    wordProfiles.set('bnc-coca-1000', {profile, maximumRank: 1});
    wordProfiles.set('bnc-coca-2000', {profile, maximumRank: 2});
    for (const option of document.querySelectorAll('#word-reference option[data-local-profile]')) {
      option.disabled = false;
    }
    status.textContent = `BNC/COCA first-2K profileを端末内で検証しました。SHA-256: ${runtimeHash}`;
  } catch {
    if (revision !== mweRevision) return;
    status.textContent = 'BNC/COCA参照リストを読み込めませんでした。指定されたファイルを選び直してください。' +
      (wordProfiles.has('bnc-coca-1000')
        ? '検証済みの参照リストと現在の作業はそのまま保持しています。'
        : '現在の作業はそのまま保持しています。参照リストはまだ利用できません。');
  }
});

async function restoreWorkspaceToPage(record, revision) {
  const wordProfileKey = record?.word_profile_selection?.key;
  const selection = wordProfiles.get(wordProfileKey);
  if (!selection) {
    throw new Error('作業JSONで使った参照リストを利用できません。ローカルBNC/COCAの作業では、先に同じ参照リストを読み込んでください。それ以外は、保存コピーと保存時のアプリを確認してください。');
  }
  const restored = await restoreMweWorkspaceRecord({
    record, contract: mweContract, authorizationAttested: true, wordProfileKey,
    wordProfile: selection.profile, wordRankCutoff: selection.maximumRank,
    mweFormProfile, mweSenseProfile
  }).catch(() => { throw mweResumeValidationError(); });
  if (revision !== mweRevision) return;
  document.getElementById('mwe-text').value = restored.document.text;
  document.getElementById('mwe-patterns').value = restored.patternSource;
  document.getElementById('word-reference').value = wordProfileKey;
  mweDocument = restored.document;
  mwePatternSource = restored.patternSource;
  currentWordProfile = selection.profile;
  currentWordRankCutoff = selection.maximumRank;
  currentWordCoverage = analyzeWordCoverage(
    restored.document.text, selection.profile, selection.maximumRank
  );
  nextMweId = 1;
  const occurrenceIds = new Set(mweDocument.occurrences.map(item => item.id));
  while (occurrenceIds.has(`mwe-${nextMweId}`)) nextMweId += 1;
  renderMweReview();
}

document.getElementById('mwe-workspace-file').addEventListener('change', async event => {
  const revision = ++mweRevision;
  const [file] = event.target.files;
  // Keep the File, not the selection: allow retrying it without late cleanup.
  event.target.value = '';
  const status = document.getElementById('mwe-workspace-status');
  try {
    if (mweDocument) {
      throw new Error('現在のMWEレビューを保存または消去してから、別の作業JSONを読み込んでください。');
    }
    if (!document.getElementById('mwe-authorization').checked) {
      throw new Error('作業JSONの読込前に、現在の処理権限を確認してください。');
    }
    const record = await readMweResumeFile(file, mweContract.workspace_file);
    if (revision !== mweRevision) return;
    await restoreWorkspaceToPage(record, revision);
    if (revision !== mweRevision) return;
    currentSetDocumentId = null;
    status.textContent = `MWE作業JSONを再開しました（保存時刻 ${record.saved_at}）。`;
  } catch (error) {
    if (revision === mweRevision) status.textContent = error.message;
  }
});

mweForm.addEventListener('submit', event => {
  event.preventDefault();
  if (mweDocument) {
    mweStatus.textContent = '現在のレビューを保護するため、再抽出しませんでした。作業をファイルに保存してから入力と結果を消去してください。';
    return;
  }
  mweRevision += 1;
  try {
    if (!document.getElementById('mwe-authorization').checked) {
      throw new Error('テキストを処理する権限の確認が必要です。');
    }
    const text = document.getElementById('mwe-text').value;
    mwePatternSource = document.getElementById('mwe-patterns').value;
    const wordSelection = wordProfiles.get(document.getElementById('word-reference').value);
    if (!wordSelection) throw new Error('通常語の参照profileを選択してください。');
    currentWordProfile = wordSelection.profile;
    currentWordRankCutoff = wordSelection.maximumRank;
    const patterns = parseMwePatternTsv(
      mwePatternSource, mweContract.occurrence_record.categories
    );
    mweDocument = {text, ...findMweCandidates(text, patterns)};
    currentWordCoverage = analyzeWordCoverage(text, currentWordProfile, currentWordRankCutoff);
    if (!mweDocument.tokens.length) throw new Error('ASCII英語tokenが見つかりません。');
    nextMweId = mweDocument.occurrences.length + 1;
    renderMweReview();
  } catch (error) {
    mweDocument = null;
    currentWordCoverage = null;
    currentWordProfile = null;
    currentWordRankCutoff = null;
    mweResults.hidden = true;
    mweStatus.textContent = error.message;
  }
});

mweForm.addEventListener('reset', event => {
  const hasWork = mweDocument || document.getElementById('mwe-text').value ||
    document.getElementById('mwe-patterns').value !== document.getElementById('mwe-patterns').defaultValue;
  if (!clearingOnPageExit && hasWork && !window.confirm(
    '現在の文書の入力とレビュー（未記録の編集を含む）を消去しますか？必要な作業は先に再開用JSONへ保存してください。文書セットとダウンロード済みファイルは消去されません。'
  )) {
    event.preventDefault();
    return;
  }
  mweRevision += 1;
  lockMweSourceInputs(false);
  mweDocument = null;
  currentSetDocumentId = null;
  mweDocumentDirty = false;
  currentWordCoverage = null;
  currentWordProfile = null;
  currentWordRankCutoff = null;
  mwePatternSource = null;
  mweResults.hidden = true;
  mweStatus.textContent = 'MWE入力と結果を消去しました。';
  document.getElementById('bnc-coca-profile-status').textContent =
    wordProfiles?.has('bnc-coca-1000')
      ? '検証済みBNC/COCA profileはこのsessionのメモリ内で引き続き利用できます。'
      : 'BNC/COCAローカルprofileは未読込です。';
  document.getElementById('mwe-workspace-status').textContent =
    '作業JSONはまだ読み込まれていません。';
  document.getElementById('mwe-document-id').value = '';
  document.getElementById('mwe-document-id').disabled = false;
  document.getElementById('mwe-document-label').value = '';
  updateMwePendingEdits();
});

for (const id of ['mwe-text', 'mwe-patterns', 'mwe-authorization']) {
  document.getElementById(id).addEventListener('input', invalidateMweReview);
}
document.getElementById('word-reference').addEventListener('change', invalidateMweReview);
mweForm.addEventListener('input', updateMwePendingEdits);
mweForm.addEventListener('change', updateMwePendingEdits);
// Capture before file-input handlers take their revision; drafts also cancel old work.
for (const form of [mweForm, mweDocumentSetForm]) {
  for (const type of ['input', 'change']) {
    form.addEventListener(type, () => { mweRevision += 1; }, true);
  }
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
  mweRevision += 1;
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
  for (const input of document.querySelectorAll('#mwe-token-picker input:checked')) {
    input.checked = false;
  }
  document.getElementById('mwe-occurrences').append(
    occurrenceCard(mweDocument.occurrences.at(-1))
  );
  renderMweReviewSummary();
});

document.getElementById('export-mwe-csv').addEventListener('click', () => {
  if (!mweDocument || !ensureMweEditsRecorded()) return;
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
  if (!mweDocument || !ensureMweEditsRecorded()) return;
  const revision = mweRevision;
  try {
    const record = await makeMweReviewRecord({
      document: mweDocument,
      contract: mweContract,
      patternSource: mwePatternSource,
      tokenizer: contract.tokenizer,
      authorizationAttested: document.getElementById('mwe-authorization').checked,
      generatedAt: new Date().toISOString(),
      wordProfile: currentWordProfile,
      wordRankCutoff: currentWordRankCutoff,
      mweFormProfile,
      mweSenseProfile
    });
    if (revision !== mweRevision) return;
    downloadText('ldfreq-mwe-review.json', JSON.stringify(record, null, 2) + '\n', 'application/json');
  } catch (error) {
    if (revision === mweRevision) mweStatus.textContent = error.message;
  }
});

document.getElementById('export-mwe-workspace').addEventListener('click', async () => {
  if (!mweDocument || !ensureMweEditsRecorded()) return;
  const revision = mweRevision;
  try {
    const record = await makeMweWorkspaceRecord({
      document: mweDocument, contract: mweContract, patternSource: mwePatternSource,
      authorizationAttested: document.getElementById('mwe-authorization').checked,
      savedAt: new Date().toISOString(),
      wordProfileKey: document.getElementById('word-reference').value,
      wordProfile: currentWordProfile, wordRankCutoff: currentWordRankCutoff,
      mweFormProfile, mweSenseProfile
    });
    if (revision !== mweRevision) return;
    downloadText(
      'ldfreq-mwe-workspace.json', JSON.stringify(record, null, 2) + '\n', 'application/json'
    );
    document.getElementById('mwe-workspace-status').textContent =
      '原文・判断・根拠を含む再開用JSONのダウンロードを開始しました。保存先とファイルを確認してください。自動保存は行いません。';
  } catch (error) {
    if (revision === mweRevision) {
      document.getElementById('mwe-workspace-status').textContent = error.message;
    }
  }
});

function renderMweDocumentSet(selectedId = '') {
  const picker = document.getElementById('mwe-document-set-documents');
  const placeholder = document.createElement('option');
  placeholder.value = '';
  placeholder.textContent = mweDocumentSet.size
    ? '文書を選択してください' : 'セット内に文書はありません';
  picker.replaceChildren(placeholder, ...[...mweDocumentSet.values()].map(item => {
    const option = document.createElement('option');
    option.value = item.id;
    option.textContent = `${item.id} — ${item.label}`;
    return option;
  }));
  picker.value = selectedId && mweDocumentSet.has(selectedId) ? selectedId : '';
  document.getElementById('load-mwe-document').disabled = !picker.value;
  document.getElementById('export-mwe-document-set').disabled = !mweDocumentSet.size;
  document.getElementById('clear-mwe-document-set').disabled = !mweDocumentSet.size;
  document.getElementById('mwe-document-set-id').disabled = Boolean(mweDocumentSet.size);
  document.getElementById('mwe-document-set-label').disabled = Boolean(mweDocumentSet.size);
  document.getElementById('mwe-document-id').disabled = Boolean(currentSetDocumentId);
  updateMwePendingEdits();
}

function documentSetDocuments(map = mweDocumentSet) {
  return [...map.values()].map(item => ({
    id: item.id, label: item.label, workspace: item.workspace
  }));
}

mweDocumentSetForm.addEventListener('submit', event => event.preventDefault());

document.getElementById('save-mwe-document').addEventListener('click', async () => {
  const revision = mweRevision;
  const status = document.getElementById('mwe-document-set-status');
  try {
    if (!mweDocument) throw new Error('先に現在の文書を抽出・レビューしてください。');
    if (!ensureMweEditsRecorded()) return;
    if (!document.getElementById('mwe-authorization').checked) {
      throw new Error('文書セットへ保存する前に、現在の処理権限を確認してください。');
    }
    const setId = document.getElementById('mwe-document-set-id').value;
    const setLabel = document.getElementById('mwe-document-set-label').value;
    const documentId = document.getElementById('mwe-document-id').value.trim();
    const documentLabel = document.getElementById('mwe-document-label').value;
    if (currentSetDocumentId && currentSetDocumentId !== documentId) {
      throw new Error('開いている文書のIDは変更できません。現在の文書IDを確認してください。');
    }
    if (mweDocumentSet.has(documentId) && currentSetDocumentId !== documentId) {
      throw new Error(`同じ文書IDが既にあります: ${documentId}。`);
    }
    const savedAt = new Date().toISOString();
    const workspace = await makeMweWorkspaceRecord({
      document: mweDocument, contract: mweContract, patternSource: mwePatternSource,
      authorizationAttested: true, savedAt,
      wordProfileKey: document.getElementById('word-reference').value,
      wordProfile: currentWordProfile, wordRankCutoff: currentWordRankCutoff,
      mweFormProfile, mweSenseProfile
    });
    if (revision !== mweRevision) return;
    const proposed = new Map(mweDocumentSet);
    proposed.set(documentId, {id: documentId, label: documentLabel, workspace});
    const validated = makeMweDocumentSetRecord({
      contract: mweContract, setId, setLabel, documents: documentSetDocuments(proposed),
      savedAt, authorizationAttested: true
    });
    mweDocumentSetIdentity = validated.set;
    mweDocumentSet = new Map(validated.documents.map(item => [item.id, item]));
    currentSetDocumentId = documentId;
    mweDocumentDirty = false;
    document.getElementById('mwe-document-set-id').value = validated.set.id;
    document.getElementById('mwe-document-set-label').value = validated.set.label;
    document.getElementById('mwe-document-id').value = documentId;
    document.getElementById('mwe-document-label').value = mweDocumentSet.get(documentId).label;
    renderMweDocumentSet(documentId);
    status.textContent = `${documentId}をページのメモリ内のセットへ追加・更新しました（${mweDocumentSet.size}件）。端末のファイルには未保存です。「文書セットをファイルに保存」でダウンロードしてください。`;
  } catch (error) {
    if (revision === mweRevision) status.textContent = error.message;
  }
});

document.getElementById('mwe-document-set-documents').addEventListener('change', event => {
  document.getElementById('load-mwe-document').disabled = !event.target.value;
});

document.getElementById('mwe-document-label').addEventListener('input', () => {
  if (mweDocument) mweDocumentDirty = true;
  updateMwePendingEdits();
});

document.getElementById('load-mwe-document').addEventListener('click', async () => {
  const revision = ++mweRevision;
  const status = document.getElementById('mwe-document-set-status');
  try {
    if (mweDocument) {
      throw new Error('必要なレビューを文書セットへ追加／更新した後、「MWE入力と結果を消去」で現在のレビューを閉じてから別文書を開いてください。');
    }
    if (!document.getElementById('mwe-authorization').checked) {
      throw new Error('文書を開く前に、現在の処理権限を確認してください。');
    }
    const id = document.getElementById('mwe-document-set-documents').value;
    const item = mweDocumentSet.get(id);
    if (!item) throw new Error('開く文書を選択してください。');
    await restoreWorkspaceToPage(item.workspace, revision);
    if (revision !== mweRevision) return;
    currentSetDocumentId = id;
    mweDocumentDirty = false;
    document.getElementById('mwe-document-id').value = item.id;
    document.getElementById('mwe-document-label').value = item.label;
    renderMweDocumentSet(id);
    status.textContent = `${item.id}を文書セットから開きました。`;
  } catch (error) {
    if (revision === mweRevision) status.textContent = error.message;
  }
});

document.getElementById('mwe-document-set-file').addEventListener('change', async event => {
  const revision = ++mweRevision;
  const [file] = event.target.files;
  event.target.value = '';
  const status = document.getElementById('mwe-document-set-status');
  try {
    if (mweDocument || mweDocumentSet.size) {
      throw new Error('現在のレビューと文書セットを保存・消去してから別セットを読み込んでください。');
    }
    if (!document.getElementById('mwe-authorization').checked) {
      throw new Error('文書セットの読込前に、現在の処理権限を確認してください。');
    }
    const record = await readMweResumeFile(file, mweContract.document_set_file);
    if (revision !== mweRevision) return;
    const restored = await restoreMweDocumentSetRecord({
      record, contract: mweContract, authorizationAttested: true, wordProfiles,
      mweFormProfile, mweSenseProfile
    }).catch(() => { throw mweResumeValidationError(); });
    if (revision !== mweRevision) return;
    mweDocumentSetIdentity = {id: restored.setId, label: restored.setLabel};
    mweDocumentSet = new Map(restored.documents.map(item => [item.id, item]));
    document.getElementById('mwe-document-set-id').value = restored.setId;
    document.getElementById('mwe-document-set-label').value = restored.setLabel;
    renderMweDocumentSet();
    status.textContent = `${restored.setId}を検証しました（${mweDocumentSet.size}件）。`;
  } catch (error) {
    if (revision === mweRevision) status.textContent = error.message;
  }
});

document.getElementById('export-mwe-document-set').addEventListener('click', () => {
  const status = document.getElementById('mwe-document-set-status');
  try {
    if (!ensureMweEditsRecorded()) return;
    if (mweDocumentDirty) {
      throw new Error('現在のレビュー変更を先に文書セットへ保存してください。');
    }
    const record = makeMweDocumentSetRecord({
      contract: mweContract,
      setId: mweDocumentSetIdentity?.id,
      setLabel: mweDocumentSetIdentity?.label,
      documents: documentSetDocuments(), savedAt: new Date().toISOString(),
      authorizationAttested: document.getElementById('mwe-authorization').checked
    });
    downloadText(
      `ldfreq-mwe-document-set-${record.set.id}.json`,
      JSON.stringify(record, null, 2) + '\n', 'application/json'
    );
    status.textContent = `原文を含む${record.documents.length}件の文書セットJSONのダウンロードを開始しました。保存先とファイルを確認してください。`;
  } catch (error) {
    status.textContent = error.message;
  }
});

document.getElementById('clear-mwe-document-set').addEventListener('click', () => {
  const status = document.getElementById('mwe-document-set-status');
  if (!window.confirm('現在の文書セットをこのページのメモリから消去しますか？')) return;
  mweRevision += 1;
  mweDocumentSet.clear();
  mweDocumentSetIdentity = null;
  currentSetDocumentId = null;
  mweDocumentDirty = Boolean(mweDocument);
  for (const id of [
    'mwe-document-set-id', 'mwe-document-set-label', 'mwe-document-id', 'mwe-document-label'
  ]) document.getElementById(id).value = '';
  document.getElementById('mwe-document-id').disabled = false;
  renderMweDocumentSet();
  status.textContent = '文書セットをこのページのメモリから消去しました。';
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

workspaceForm.addEventListener('reset', event => {
  const hasWork = currentExport || [...workspaceForm.querySelectorAll('input[type="text"], textarea')]
    .some(input => input.value !== input.defaultValue);
  if (!clearingOnPageExit && hasWork && !window.confirm(
    '基本集計の入力と画面上の結果を消去しますか？ダウンロード済みファイルは消去されません。'
  )) {
    event.preventDefault();
    return;
  }
  analysisRevision += 1;
  currentExport = null;
  exportButton.disabled = true;
  workspaceResults.hidden = true;
  workspaceStatus.textContent = '入力と画面上の結果を消去しました。';
  setTimeout(updateWorkspaceMode);
});

window.addEventListener('pagehide', () => {
  clearingOnPageExit = true;
  try {
    workspaceForm.reset();
    mweForm.reset();
  } finally {
    clearingOnPageExit = false;
  }
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
      ngslProfileResponse, mweFormProfileResponse, mweSenseProfileResponse
    ] = await Promise.all([
      fetch('samples.json'), fetch('metric_contract.json'), fetch('mwe_contract.json'),
      fetch('resources/tubelex_en_regex_ascii_2025.json'),
      fetch('resources/ngsl_1_2_ascii_forms.json'),
      fetch('resources/oewn_2025_multiword_verbs.json'),
      fetch('resources/oewn_take_in_2025.json')
    ]);
    if (!samplesResponse.ok || !contractResponse.ok || !mweContractResponse.ok ||
        !wordProfileResponse.ok || !ngslProfileResponse.ok || !mweFormProfileResponse.ok ||
        !mweSenseProfileResponse.ok) {
      throw new Error('比較データを読み込めませんでした。');
    }
    const sampleDocument = await samplesResponse.json();
    contract = await contractResponse.json();
    mweContract = await mweContractResponse.json();
    const tubelexProfile = prepareWordReferenceProfile(await wordProfileResponse.json());
    const ngslProfile = prepareWordReferenceProfile(await ngslProfileResponse.json());
    wordProfiles = new Map([
      ['tubelex', {profile: tubelexProfile, maximumRank: null}],
      ['ngsl-1000', {profile: ngslProfile, maximumRank: 1000}],
      ['ngsl-2000', {profile: ngslProfile, maximumRank: 2000}],
      ['ngsl-full', {profile: ngslProfile, maximumRank: 2809}]
    ]);
    mweFormProfile = prepareMweFormReferenceProfile(await mweFormProfileResponse.json());
    mweSenseProfile = prepareMweSenseReferenceProfile(await mweSenseProfileResponse.json());
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
    document.getElementById('bnc-coca-profile').disabled = false;
    document.getElementById('mwe-workspace-file').disabled = false;
    for (const control of mweDocumentSetForm.querySelectorAll('input, select, button')) {
      control.disabled = false;
    }
    renderMweDocumentSet();
    document.getElementById('analyze-button').disabled = false;
  } catch (error) {
    scenarioStatus.textContent = error.message;
    mweStatus.textContent = error.message;
    for (const form of [mweForm, mweDocumentSetForm, workspaceForm]) {
      form.querySelectorAll('input, textarea, select, button').forEach(control => {
        control.disabled = true;
      });
    }
  }
}

// Refresh after form handlers and native reset defaults.
for (const form of [mweForm, mweDocumentSetForm, workspaceForm]) {
  for (const type of ['input', 'change', 'reset', 'submit']) {
    form.addEventListener(type, () => {
      if (type === 'reset') setTimeout(updatePageExitWarning);
      else queueMicrotask(updatePageExitWarning);
    });
  }
}

initialize();
