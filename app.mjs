import {analyze, makeExportRecord, parseBatchJson} from './metrics.mjs';

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
let comparisonSets;
let contract;
let currentExport;
let analysisRevision = 0;

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

window.addEventListener('pagehide', () => workspaceForm.reset());

relationship.addEventListener('change', updateWorkspaceMode);
relationship.addEventListener('change', () => invalidateWorkspace());
workspaceForm.addEventListener('input', () => invalidateWorkspace());

exportButton.addEventListener('click', () => {
  if (!currentExport) return;
  const url = URL.createObjectURL(new Blob(
    [JSON.stringify(currentExport, null, 2) + '\n'], {type: 'application/json'}
  ));
  const link = document.createElement('a');
  link.href = url;
  link.download = 'ldfreq-analysis.json';
  document.body.append(link);
  link.click();
  link.remove();
  setTimeout(() => URL.revokeObjectURL(url));
});

async function initialize() {
  try {
    const [samplesResponse, contractResponse] = await Promise.all([
      fetch('samples.json'), fetch('metric_contract.json')
    ]);
    if (!samplesResponse.ok || !contractResponse.ok) throw new Error('比較データを読み込めませんでした。');
    const sampleDocument = await samplesResponse.json();
    contract = await contractResponse.json();
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
    document.getElementById('analyze-button').disabled = false;
  } catch (error) {
    scenarioStatus.textContent = error.message;
    workspaceForm.querySelectorAll('input, textarea, select, button').forEach(control => {
      control.disabled = true;
    });
  }
}

initialize();
