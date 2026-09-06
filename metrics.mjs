const tokenPattern = /(?:^|[^\p{L}\p{N}_])([A-Za-z]+(?:['’][A-Za-z]+)*)(?=$|[^\p{L}\p{N}_])/gu;
const tubelexTokenPattern = /(?:^|[^\p{L}\p{N}_])([A-Za-z]+)(?=$|[^\p{L}\p{N}_])/gu;

function requireWellFormed(value, label) {
  if (typeof value.isWellFormed !== 'function') {
    throw new Error('Unicode validation requires a current browser.');
  }
  if (!value.isWellFormed()) {
    throw new Error(`${label} contains an unpaired Unicode surrogate.`);
  }
}

export function parseJsonInput(source, maximum, label = 'JSON input') {
  if (typeof source !== 'string') throw new Error(`${label} must be text.`);
  if (source.length > maximum) {
    throw new Error(`${label} exceeds the reviewed browser limit.`);
  }
  requireWellFormed(source, label);
  try {
    return JSON.parse(source);
  } catch {
    throw new Error(`${label} is not valid JSON.`);
  }
}

export function parseBatchJson(source, maximum) {
  return parseJsonInput(source, maximum, 'Batch JSON');
}

export function tokenRecords(text) {
  return [...text.matchAll(tokenPattern)].map((match, index) => ({
    id: `t${index + 1}`,
    position: index + 1,
    surface: match[1],
    normalized: match[1].replaceAll('’', "'").toLowerCase()
  }));
}

export function tokenize(text) {
  return tokenRecords(text).map(token => token.normalized);
}

export function tokenizeForAsciiWordProfile(text) {
  if (typeof text !== 'string') throw new Error('ASCII word-profile tokenization requires text.');
  requireWellFormed(text, 'ASCII word-profile input');
  return [...text.normalize('NFKC').matchAll(tubelexTokenPattern)]
    .map(match => match[1].toLowerCase());
}

export function prepareWordReferenceProfile(profile) {
  const referenceFunction = profile?.construct?.reference_function;
  const bundled = profile?.identity?.profile_status === 'admitted' &&
    profile?.rights?.browser_delivery_permitted === true;
  const local = profile?.identity?.profile_status === 'local_only' &&
    profile?.source?.delivery_mode === 'researcher_supplied_local_file' &&
    profile?.rights?.browser_delivery_permitted === false &&
    profile?.rights?.local_user_import_permitted === true;
  if ((!bundled && !local) ||
      profile?.construct?.coverage_channel !== 'word' ||
      !['frequency_distribution', 'ranked_inventory'].includes(referenceFunction) ||
      !Array.isArray(profile.rows)) {
    throw new Error('Word reference profile is not admitted for bundled or local delivery.');
  }
  const lookup = new Map();
  if (referenceFunction === 'ranked_inventory') {
    const boundaries = profile.measurement?.band_boundaries;
    if (!Array.isArray(boundaries) || !boundaries.length || boundaries.some(
      (value, index) => !Number.isInteger(value) || value < 1 || (index && value <= boundaries[index - 1])
    )) {
      throw new Error('Ranked word reference boundaries are invalid.');
    }
    const lemmas = new Set();
    let ambiguousRows = 0;
    let previousWord = '';
    for (const [word, mappings] of profile.rows) {
      if (!/^[a-z]+$/.test(word) || word <= previousWord || !Array.isArray(mappings) ||
          !mappings.length || lookup.has(word)) {
        throw new Error('Invalid ranked word reference row.');
      }
      let previousRank = 0;
      let previousLemma = '';
      for (const [lemma, rank] of mappings) {
        if (!/^[a-z]+$/.test(lemma) || !Number.isInteger(rank) || rank < 1 ||
            rank > boundaries.at(-1) || rank < previousRank ||
            (rank === previousRank && lemma <= previousLemma)) {
          throw new Error('Invalid ranked word reference mapping.');
        }
        lemmas.add(lemma);
        previousRank = rank;
        previousLemma = lemma;
      }
      if (mappings.length > 1) ambiguousRows += 1;
      lookup.set(word, {mappings, rank: mappings[0][1]});
      previousWord = word;
    }
    if (lookup.size !== profile.table.projected_row_count ||
        lemmas.size !== profile.table.source_headword_count ||
        ambiguousRows !== profile.table.ambiguous_surface_form_count) {
      throw new Error('Ranked word reference manifest does not match its rows.');
    }
    return {profile, lookup};
  }
  if (!Number.isInteger(profile.corpus_design?.token_count)) {
    throw new Error('Frequency word reference token count is invalid.');
  }
  let previousCount = Infinity;
  let previousWord = '';
  let rank = 0;
  profile.rows.forEach((row, index) => {
    const [word, count] = row;
    if (!/^[a-z]+$/.test(word) || !Number.isInteger(count) || count < 1 ||
        count > previousCount || (count === previousCount && word <= previousWord) ||
        lookup.has(word)) {
      throw new Error(`Invalid word reference row ${index + 1}.`);
    }
    if (count < previousCount) rank = index + 1;
    lookup.set(word, {count, rank});
    previousCount = count;
    previousWord = word;
  });
  if (lookup.size !== profile.table.projected_row_count) {
    throw new Error('Word reference row count does not match its manifest.');
  }
  return {profile, lookup};
}

export function analyzeWordCoverage(text, prepared, maximumRank = null) {
  if (!(prepared?.lookup instanceof Map)) throw new Error('Prepared word profile is required.');
  const referenceFunction = prepared.profile.construct.reference_function;
  const ranked = referenceFunction === 'ranked_inventory';
  if (ranked !== Number.isInteger(maximumRank) ||
      (ranked && !prepared.profile.measurement.band_boundaries.includes(maximumRank))) {
    throw new Error('Word-profile rank cutoff is inconsistent with the selected profile.');
  }
  const tokens = tokenizeForAsciiWordProfile(text);
  const textCounts = new Map();
  for (const token of tokens) textCounts.set(token, (textCounts.get(token) || 0) + 1);
  const corpusTokens = prepared.profile.corpus_design.token_count;
  const items = [...textCounts].map(([word, textCount]) => {
    const reference = prepared.lookup.get(word);
    const status = !reference ? 'unmatched'
      : ranked && reference.rank > maximumRank ? 'beyond_cutoff' : 'matched';
    return {
      word,
      text_count: textCount,
      status,
      source_count: ranked ? null : reference?.count ?? null,
      frequency_per_million: !ranked && reference
        ? Number((reference.count / corpusTokens * 1_000_000).toFixed(6)) : null,
      frequency_rank: !ranked ? reference?.rank ?? null : null,
      head_mappings: ranked && reference
        ? reference.mappings.map(([lemma, rank]) => ({lemma, rank})) : [],
      minimum_head_rank: ranked ? reference?.rank ?? null : null,
      ambiguous_head_mapping: ranked ? Boolean(reference?.mappings.length > 1) : false
    };
  }).sort((first, second) =>
    Number(first.status === 'matched') - Number(second.status === 'matched') ||
    second.text_count - first.text_count || first.word.localeCompare(second.word)
  );
  const matchedTypes = items.filter(item => item.status === 'matched');
  const matchedTokens = matchedTypes.reduce((sum, item) => sum + item.text_count, 0);
  const unmatchedTypes = items.filter(item => item.status === 'unmatched');
  const beyondTypes = items.filter(item => item.status === 'beyond_cutoff');
  return {
    profile_id: prepared.profile.identity.profile_id,
    profile_version: prepared.profile.identity.profile_version,
    profile_title: prepared.profile.identity.title,
    reference_function: referenceFunction,
    selected_rank_cutoff: maximumRank,
    tokenizer_unit: prepared.profile.construct.unit,
    token_coverage: coverage(matchedTokens, tokens.length),
    type_coverage: coverage(matchedTypes.length, items.length),
    uncovered_token_count: tokens.length - matchedTokens,
    uncovered_type_count: items.length - matchedTypes.length,
    unmatched_token_count: unmatchedTypes.reduce((sum, item) => sum + item.text_count, 0),
    unmatched_type_count: unmatchedTypes.length,
    beyond_cutoff_token_count: beyondTypes.reduce((sum, item) => sum + item.text_count, 0),
    beyond_cutoff_type_count: beyondTypes.length,
    items
  };
}

export function wordCoverageCsv(result) {
  if (!result?.token_coverage || !Array.isArray(result.items)) {
    throw new Error('Word coverage result is required.');
  }
  const header = [
    'word', 'text_count', 'status', 'source_count', 'frequency_per_million',
    'frequency_rank', 'head_mappings', 'minimum_head_rank', 'ambiguous_head_mapping',
    'profile_id', 'profile_version', 'reference_function', 'selected_rank_cutoff'
  ];
  const rows = result.items.map(item => [
    item.word, item.text_count, item.status, item.source_count,
    item.frequency_per_million, item.frequency_rank,
    item.head_mappings.map(mapping => `${mapping.lemma}:${mapping.rank}`).join(' '),
    item.minimum_head_rank, item.ambiguous_head_mapping,
    result.profile_id, result.profile_version, result.reference_function,
    result.selected_rank_cutoff
  ]);
  return [header, ...rows].map(row => row.map(csvCell).join(',')).join('\n') + '\n';
}

export function prepareMweFormReferenceProfile(profile) {
  if (profile?.identity?.profile_status !== 'admitted' ||
      profile?.construct?.coverage_channel !== 'mwe_form' ||
      profile?.construct?.reference_function !== 'inventory_membership' ||
      !Array.isArray(profile.rows)) {
    throw new Error('MWE form reference profile is not an admitted inventory.');
  }
  const lookup = new Map();
  let previousForm = '';
  for (const [form, senseCount] of profile.rows) {
    if (typeof form !== 'string' ||
        !/^[a-z]+(?:'[a-z]+)*(?: [a-z]+(?:'[a-z]+)*)+$/.test(form) ||
        !Number.isInteger(senseCount) || senseCount < 1 || form <= previousForm ||
        lookup.has(form)) {
      throw new Error('Invalid MWE form reference row.');
    }
    lookup.set(form, senseCount);
    previousForm = form;
  }
  if (lookup.size !== profile.table.projected_row_count) {
    throw new Error('MWE form reference row count does not match its manifest.');
  }
  return {profile, lookup};
}

function normalizedCanonicalForm(value) {
  return value.trim().replaceAll('’', "'").toLowerCase().split(/\s+/).join(' ');
}

export function lookupMweForm(canonicalForm, prepared) {
  if (typeof canonicalForm !== 'string' || !(prepared?.lookup instanceof Map)) {
    throw new Error('MWE form lookup requires a canonical form and prepared profile.');
  }
  const normalized = normalizedCanonicalForm(canonicalForm);
  const matched = prepared.lookup.has(normalized);
  return {
    inventory_id: prepared.profile.identity.profile_id,
    inventory_version: prepared.profile.identity.profile_version,
    status: matched ? 'matched' : 'out_of_inventory',
    entry_id: matched ? `${normalized}#v` : null,
    sense_count: matched ? prepared.lookup.get(normalized) : null
  };
}

export function prepareMweSenseReferenceProfile(subset) {
  const projection = subset?.projection;
  const resource = subset?.resource;
  if (subset?.subset_schema_version !== '1.0.0' || !subset?.subset_id ||
      resource?.id !== 'oewn' || typeof resource.version !== 'string' ||
      !resource.artifact_sha256 || !subset?.license?.oewn ||
      projection?.part_of_speech !== 'v' || !Array.isArray(projection.senses) ||
      projection.sense_count !== projection.senses.length ||
      projection.entry_id !== `${projection.lemma}#v`) {
    throw new Error('MWE sense reference subset is invalid.');
  }
  const lemma = normalizedCanonicalForm(projection.lemma);
  if (!lemma.includes(' ') || projection.senses.length < 1) {
    throw new Error('MWE sense reference entry is invalid.');
  }
  const senseIds = new Set();
  for (const sense of projection.senses) {
    if (typeof sense?.sense_id !== 'string' || !sense.sense_id || senseIds.has(sense.sense_id) ||
        !Array.isArray(sense.definitions) || !sense.definitions.length ||
        sense.definitions.some(value => typeof value !== 'string' || !value) ||
        !Array.isArray(sense.synonyms) || !Array.isArray(sense.synset_examples) ||
        !Array.isArray(sense.entry_examples)) {
      throw new Error('MWE sense reference row is invalid.');
    }
    senseIds.add(sense.sense_id);
  }
  return {
    profile: {
      identity: {
        profile_id: subset.subset_id,
        profile_version: resource.version,
        title: `${resource.title} ${projection.entry_id} sense projection`
      },
      construct: {
        coverage_channel: 'mwe_sense',
        reference_function: 'inventory_membership',
        excluded_inferences: [
          'contextual sense truth', 'sense frequency', 'learner knowledge',
          'pedagogical importance', 'automatic word-sense disambiguation'
        ]
      },
      source: {
        artifact_sha256: resource.artifact_sha256,
        release_or_edition: resource.release_tag
      },
      rights: {
        license_identifier: `${subset.license.oewn} AND ${subset.license.underlying_wordnet}`
      }
    },
    lookup: new Map([[lemma, {entry_id: projection.entry_id, senses: projection.senses}]])
  };
}

export function lookupMweSenses(canonicalForm, prepared) {
  if (typeof canonicalForm !== 'string' || !(prepared?.lookup instanceof Map)) {
    throw new Error('MWE sense lookup requires a canonical form and prepared profile.');
  }
  const entry = prepared.lookup.get(normalizedCanonicalForm(canonicalForm));
  if (!entry) {
    return {
      state: {
        inventory_id: null, inventory_version: null, lookup_status: 'inventory_ineligible',
        candidate_sense_ids: [], assignment_status: 'inventory_ineligible',
        selected_sense_ids: [],
        decision: {
          source: 'runtime-sense-profile-scope',
          note: `The current bounded sense projection does not cover ${normalizedCanonicalForm(canonicalForm)}.`
        }
      },
      senses: []
    };
  }
  return {
    state: {
      inventory_id: prepared.profile.identity.profile_id,
      inventory_version: prepared.profile.identity.profile_version,
      lookup_status: 'matched',
      candidate_sense_ids: entry.senses.map(sense => sense.sense_id),
      assignment_status: 'unassigned', selected_sense_ids: [], decision: null
    },
    senses: entry.senses
  };
}

export function parseMwePatternTsv(source, categories, maximumRows = 500) {
  if (typeof source !== 'string' || !Array.isArray(categories)) {
    throw new Error('MWE patterns require TSV text and declared categories.');
  }
  if (source.length > 100_000) throw new Error('MWE pattern TSV exceeds 100,000 characters.');
  requireWellFormed(source, 'MWE pattern TSV');
  const rows = source.split(/\r?\n/).map(line => line.trim())
    .filter(line => line && !line.startsWith('#'));
  if (!rows.length || rows.length > maximumRows) {
    throw new Error(`MWE pattern TSV requires 1–${maximumRows} data rows.`);
  }
  const seen = new Set();
  return rows.map((row, index) => {
    const columns = row.split('\t').map(value => value.trim());
    if (columns.length !== 4) {
      throw new Error(`MWE pattern row ${index + 1} requires four tab-separated fields.`);
    }
    const [category, canonicalForm, pattern, rawMaximumGap] = columns;
    if (!categories.includes(category) || !canonicalForm || canonicalForm.length > 100) {
      throw new Error(`Invalid MWE category or canonical form at row ${index + 1}.`);
    }
    if (!pattern || pattern.length > 500) {
      throw new Error(`Invalid MWE member pattern at row ${index + 1}.`);
    }
    const maximumGap = Number(rawMaximumGap);
    if (!Number.isInteger(maximumGap) || maximumGap < 0 || maximumGap > 8) {
      throw new Error(`MWE maximum gap must be an integer from 0 to 8 at row ${index + 1}.`);
    }
    const members = pattern.split(/\s+/).filter(Boolean).map(member => {
      const alternatives = [...new Set(member.split('/').map(value => {
        const normalized = tokenize(value);
        if (normalized.length !== 1) {
          throw new Error(`Invalid MWE member alternative at row ${index + 1}.`);
        }
        return normalized[0];
      }))];
      if (!alternatives.length) {
        throw new Error(`Missing MWE member alternatives at row ${index + 1}.`);
      }
      return alternatives;
    });
    if (members.length < 2 || members.length > 5) {
      throw new Error(`MWE patterns require 2–5 member positions at row ${index + 1}.`);
    }
    const key = JSON.stringify([category, canonicalForm.toLowerCase(), members, maximumGap]);
    if (seen.has(key)) throw new Error(`Duplicate MWE pattern at row ${index + 1}.`);
    seen.add(key);
    return {
      id: `pattern-${index + 1}`,
      category,
      canonical_form: canonicalForm,
      members,
      maximum_gap: maximumGap
    };
  });
}

export function findMweCandidates(text, patterns, maximumCandidates = 500) {
  if (typeof text !== 'string' || !Array.isArray(patterns) ||
      !Number.isInteger(maximumCandidates) || maximumCandidates < 1) {
    throw new Error('MWE candidate search parameters are invalid.');
  }
  if (text.length > 100_000) throw new Error('MWE review text exceeds 100,000 characters.');
  requireWellFormed(text, 'MWE review text');
  const tokens = tokenRecords(text);
  const found = [];
  const seen = new Set();
  const add = (pattern, positions) => {
    const memberIds = positions.map(position => tokens[position].id);
    const key = JSON.stringify([pattern.category, pattern.canonical_form, memberIds]);
    if (seen.has(key)) return;
    if (found.length >= maximumCandidates) {
      throw new Error(`MWE candidate count exceeds the reviewed limit of ${maximumCandidates}.`);
    }
    seen.add(key);
    const memberSet = new Set(memberIds);
    found.push({
      id: '',
      canonical_form: pattern.canonical_form,
      category: pattern.category,
      status: 'candidate',
      member_token_ids: memberIds,
      gap_token_ids: tokens.slice(positions[0] + 1, positions.at(-1))
        .map(token => token.id).filter(id => !memberSet.has(id)),
      decision: null,
      idiomaticity: {status: 'not_assessed', decision: null},
      form_lookup: null,
      sense: null,
      candidate_source: {kind: 'user-pattern', pattern_id: pattern.id}
    });
  };
  for (const pattern of patterns) {
    const extend = positions => {
      const memberIndex = positions.length;
      if (memberIndex === pattern.members.length) return add(pattern, positions);
      const start = positions.length ? positions.at(-1) + 1 : 0;
      const end = positions.length
        ? Math.min(tokens.length, start + pattern.maximum_gap + 1)
        : tokens.length;
      for (let position = start; position < end; position += 1) {
        if (pattern.members[memberIndex].includes(tokens[position].normalized)) {
          extend([...positions, position]);
        }
      }
    };
    extend([]);
  }
  found.sort((first, second) => {
    const firstStart = Number(first.member_token_ids[0].slice(1));
    const secondStart = Number(second.member_token_ids[0].slice(1));
    return firstStart - secondStart || first.canonical_form.localeCompare(second.canonical_form);
  });
  found.forEach((occurrence, index) => { occurrence.id = `mwe-${index + 1}`; });
  return {tokens, occurrences: found};
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
  if (document.occurrences.length > contract.candidate_generation.limits.candidates_per_text) {
    throw new Error('MWE occurrence count exceeds the reviewed browser limit.');
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
      if (occurrence.decision !== null || occurrence.form_lookup || occurrence.sense ||
          occurrence.idiomaticity.status !== 'not_assessed') {
        throw new Error(`Unresolved candidate carries a terminal result: ${occurrence.id}.`);
      }
      unresolved.push(occurrence);
      continue;
    }
    if (!validMweDecision(occurrence.decision, true)) {
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
  const senseAssigned = confirmed.filter(item =>
    ['assigned', 'multiple_assigned'].includes(item.sense.assignment_status)
  ).length;
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

export function summarizeMweFormCoverage(document, contract) {
  summarizeMweDocument(document, contract);
  const confirmed = document.occurrences.filter(item => item.status === 'confirmed');
  const matched = confirmed.filter(item => item.form_lookup.status === 'matched');
  const forms = new Map();
  for (const item of confirmed) {
    const form = normalizedCanonicalForm(item.canonical_form);
    if (!forms.has(form)) forms.set(form, {occurrence_count: 0, status: item.form_lookup.status});
    const record = forms.get(form);
    record.occurrence_count += 1;
    if (record.status !== item.form_lookup.status) {
      throw new Error(`Inconsistent MWE form lookup for ${form}.`);
    }
  }
  const matchedTypes = [...forms.values()].filter(item => item.status === 'matched').length;
  return {
    occurrence_coverage: coverage(matched.length, confirmed.length),
    type_coverage: coverage(matchedTypes, forms.size),
    unmatched_forms: [...forms].filter(([, item]) => item.status !== 'matched')
      .map(([canonicalForm, item]) => ({canonical_form: canonicalForm, ...item}))
  };
}

function validMweDecision(decision, required) {
  if (!required) return decision === null;
  return ['source', 'note'].every(field =>
    typeof decision?.[field] === 'string' && decision[field].trim().length > 0
  );
}

function validateIdiomaticity(occurrence, contract) {
  const idiomaticity = occurrence.idiomaticity;
  if (!idiomaticity ||
      !contract.occurrence_record.idiomaticity_statuses.includes(idiomaticity.status) ||
      !Object.hasOwn(idiomaticity, 'decision')) {
    throw new Error(`MWE occurrence lacks idiomaticity state: ${occurrence.id}.`);
  }
  const assessed = idiomaticity.status !== 'not_assessed';
  if (!validMweDecision(idiomaticity.decision, assessed)) {
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
  const senseLookupAttempted = ['matched', 'out_of_inventory'].includes(sense.lookup_status);
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
  if (['assigned', 'multiple_assigned', 'ambiguous', 'abstained'].includes(sense.assignment_status) &&
      sense.lookup_status !== 'matched') {
    throw new Error(`Sense assignment lacks matched candidates: ${occurrence.id}.`);
  }
  const decided = sense.assignment_status !== 'unassigned';
  if (!validMweDecision(sense.decision, decided)) {
    throw new Error(`Sense decision provenance is inconsistent: ${occurrence.id}.`);
  }
  const multiple = ['multiple_assigned', 'ambiguous'].includes(sense.assignment_status);
  const selectedCount = sense.assignment_status === 'assigned' ? 1 : multiple ? 2 : 0;
  const lookupAssignmentMismatch =
    (sense.lookup_status === 'not_attempted' && sense.assignment_status !== 'unassigned') ||
    (sense.lookup_status === 'inventory_ineligible' && sense.assignment_status !== 'inventory_ineligible') ||
    (sense.lookup_status === 'out_of_inventory' && sense.assignment_status !== 'out_of_inventory') ||
    (sense.assignment_status === 'inventory_ineligible' && sense.lookup_status !== 'inventory_ineligible') ||
    (sense.assignment_status === 'out_of_inventory' &&
      !['matched', 'out_of_inventory'].includes(sense.lookup_status));
  if ((multiple && selected.length < selectedCount) ||
      (!multiple && selected.length !== selectedCount) || lookupAssignmentMismatch) {
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

function csvCell(value) {
  return `"${String(value ?? '').replaceAll('"', '""')}"`;
}

export function mweOccurrencesCsv(document, contract) {
  summarizeMweDocument(document, contract);
  const header = [
    'occurrence_id', 'canonical_form', 'category', 'status', 'member_token_ids',
    'gap_token_ids', 'candidate_source', 'decision_note', 'form_inventory_id',
    'form_inventory_version', 'form_lookup_status', 'form_entry_id', 'form_sense_count',
    'idiomaticity_status', 'idiomaticity_note', 'sense_inventory_id',
    'sense_inventory_version', 'sense_lookup_status', 'candidate_sense_ids',
    'sense_assignment_status', 'selected_sense_ids', 'sense_decision_note'
  ];
  const rows = document.occurrences.map(item => [
    item.id, item.canonical_form, item.category, item.status,
    item.member_token_ids.join(' '), item.gap_token_ids.join(' '),
    item.candidate_source?.kind, item.decision?.note, item.form_lookup?.inventory_id,
    item.form_lookup?.inventory_version, item.form_lookup?.status,
    item.form_lookup?.entry_id, item.form_lookup?.sense_count,
    item.idiomaticity.status, item.idiomaticity.decision?.note,
    item.sense?.inventory_id, item.sense?.inventory_version, item.sense?.lookup_status,
    item.sense?.candidate_sense_ids?.join(' '), item.sense?.assignment_status,
    item.sense?.selected_sense_ids?.join(' '), item.sense?.decision?.note
  ]);
  return [header, ...rows].map(row => row.map(csvCell).join(',')).join('\n') + '\n';
}

function activeProfileRecord(prepared) {
  const profile = prepared?.profile;
  if (!profile?.identity || !profile?.source || !profile?.rights) {
    throw new Error('Prepared reference profile metadata is missing.');
  }
  const localHash = prepared.runtimeProfileSha256 ?? null;
  if (profile.identity.profile_status === 'local_only' &&
      !/^[0-9a-f]{64}$/.test(localHash ?? '')) {
    throw new Error('Local reference profile runtime hash is missing.');
  }
  return {
    profile_id: profile.identity.profile_id,
    profile_version: profile.identity.profile_version,
    profile_status: profile.identity.profile_status,
    title: profile.identity.title,
    coverage_channel: profile.construct.coverage_channel,
    reference_function: profile.construct.reference_function,
    delivery_mode: profile.source.delivery_mode ?? 'bundled_browser_resource',
    runtime_profile_sha256: localHash,
    source_artifact_sha256: profile.source.artifact_sha256,
    source_release: profile.source.release_or_edition,
    license_identifier: profile.rights.license_identifier,
    excluded_inferences: profile.construct.excluded_inferences
  };
}

function requireExactIsoTimestamp(value, label) {
  const date = new Date(value);
  if (typeof value !== 'string' || !Number.isFinite(date.getTime()) ||
      date.toISOString() !== value) {
    throw new Error(`${label} must be an exact UTC ISO string.`);
  }
}

function validateMweRuntime({
  document, contract, wordProfile, wordRankCutoff, mweFormProfile, mweSenseProfile
}) {
  summarizeMweDocument(document, contract);
  const wordCoverage = analyzeWordCoverage(document.text, wordProfile, wordRankCutoff);
  for (const occurrence of document.occurrences.filter(item => item.status === 'confirmed')) {
    const expected = lookupMweForm(occurrence.canonical_form, mweFormProfile);
    if (['inventory_id', 'inventory_version', 'status', 'entry_id', 'sense_count']
      .some(key => occurrence.form_lookup[key] !== expected[key])) {
      throw new Error(`MWE form lookup does not match the active profile: ${occurrence.id}.`);
    }
    const expectedSense = lookupMweSenses(occurrence.canonical_form, mweSenseProfile).state;
    if (['inventory_id', 'inventory_version', 'lookup_status']
      .some(key => occurrence.sense[key] !== expectedSense[key]) ||
      JSON.stringify(occurrence.sense.candidate_sense_ids) !==
        JSON.stringify(expectedSense.candidate_sense_ids)) {
      throw new Error(`MWE sense lookup does not match the active profile: ${occurrence.id}.`);
    }
  }
  return wordCoverage;
}

export async function makeMweWorkspaceRecord({
  document, contract, patternSource, authorizationAttested, savedAt, wordProfileKey,
  wordProfile, wordRankCutoff, mweFormProfile, mweSenseProfile
}) {
  if (authorizationAttested !== true) {
    throw new Error('MWE workspace save requires input authorization attestation.');
  }
  document = structuredClone(document);
  if (typeof patternSource !== 'string' || typeof wordProfileKey !== 'string' ||
      !wordProfileKey) {
    throw new Error('MWE workspace metadata is missing.');
  }
  requireExactIsoTimestamp(savedAt, 'MWE workspace timestamp');
  parseMwePatternTsv(patternSource, contract.occurrence_record.categories);
  validateMweRuntime({
    document, contract, wordProfile, wordRankCutoff, mweFormProfile, mweSenseProfile
  });
  return {
    schema_version: contract.workspace_file.schema_version,
    contract_version: contract.contract_version,
    saved_at: savedAt,
    raw_content_included: true,
    input_authorization: {attested: true, independently_verified_by_app: false},
    word_profile_selection: {key: wordProfileKey, selected_rank_cutoff: wordRankCutoff},
    active_runtime_resources: [
      activeProfileRecord(wordProfile), activeProfileRecord(mweFormProfile),
      activeProfileRecord(mweSenseProfile)
    ],
    pattern_tsv: patternSource,
    document: {
      text: document.text,
      sha256_utf8: await sha256(document.text),
      occurrences: structuredClone(document.occurrences)
    }
  };
}

export async function restoreMweWorkspaceRecord({
  record, contract, authorizationAttested, wordProfileKey, wordProfile, wordRankCutoff,
  mweFormProfile, mweSenseProfile
}) {
  if (authorizationAttested !== true) {
    throw new Error('MWE workspace restore requires current input authorization attestation.');
  }
  record = structuredClone(record);
  if (record?.schema_version !== contract.workspace_file.schema_version ||
      record.contract_version !== contract.contract_version ||
      record.raw_content_included !== true || record.input_authorization?.attested !== true) {
    throw new Error('MWE workspace schema or contract does not match this app.');
  }
  requireExactIsoTimestamp(record.saved_at, 'MWE workspace timestamp');
  if (record.word_profile_selection?.key !== wordProfileKey ||
      record.word_profile_selection.selected_rank_cutoff !== wordRankCutoff) {
    throw new Error('MWE workspace word-profile selection does not match the active profile.');
  }
  const expectedResources = [
    activeProfileRecord(wordProfile), activeProfileRecord(mweFormProfile),
    activeProfileRecord(mweSenseProfile)
  ];
  const identity = resource => [
    resource?.profile_id, resource?.profile_version, resource?.profile_status,
    resource?.source_artifact_sha256, resource?.runtime_profile_sha256
  ];
  if (!Array.isArray(record.active_runtime_resources) ||
      JSON.stringify(record.active_runtime_resources.map(identity)) !==
        JSON.stringify(expectedResources.map(identity))) {
    throw new Error('MWE workspace runtime resources do not match this app.');
  }
  parseMwePatternTsv(record.pattern_tsv, contract.occurrence_record.categories);
  if (typeof record.document?.text !== 'string' ||
      record.document.text.length > contract.candidate_generation.limits.text_utf16_code_units) {
    throw new Error('MWE workspace text exceeds the reviewed browser limit.');
  }
  if (!/^[0-9a-f]{64}$/.test(record.document.sha256_utf8 || '') ||
      await sha256(record.document.text) !== record.document.sha256_utf8) {
    throw new Error('MWE workspace text SHA-256 does not match its saved review.');
  }
  const document = {
    text: record.document?.text,
    tokens: tokenRecords(record.document.text),
    occurrences: structuredClone(record.document?.occurrences)
  };
  validateMweRuntime({
    document, contract, wordProfile, wordRankCutoff,
    mweFormProfile, mweSenseProfile
  });
  return {document, patternSource: record.pattern_tsv};
}

function documentSetField(value, label, maximum, identifier = false) {
  if (typeof value !== 'string') throw new Error(`${label} must be text.`);
  requireWellFormed(value, label);
  const normalized = value.trim();
  if (!normalized || normalized.length > maximum ||
      (identifier && !/^[A-Za-z0-9][A-Za-z0-9._-]*$/.test(normalized))) {
    throw new Error(`${label} is invalid.`);
  }
  return normalized;
}

function validateMweDocumentSetEnvelope(record, contract) {
  const specification = contract.document_set_file;
  if (record?.schema_version !== specification.schema_version ||
      record.contract_version !== contract.contract_version ||
      record.raw_content_included !== true || record.input_authorization?.attested !== true) {
    throw new Error('MWE document-set schema or contract does not match this app.');
  }
  requireExactIsoTimestamp(record.saved_at, 'MWE document-set timestamp');
  const setId = documentSetField(
    record.set?.id, 'MWE document-set ID', specification.maximum_id_characters, true
  );
  const setLabel = documentSetField(
    record.set?.label, 'MWE document-set label', specification.maximum_label_characters
  );
  if (!Array.isArray(record.documents) || record.documents.length < 1 ||
      record.documents.length > specification.maximum_documents) {
    throw new Error('MWE document-set count exceeds the reviewed browser limits.');
  }
  const ids = new Set();
  let combinedTextLength = 0;
  const documents = record.documents.map((item, index) => {
    const id = documentSetField(
      item?.id, `MWE document ${index + 1} ID`, specification.maximum_id_characters, true
    );
    const label = documentSetField(
      item?.label, `MWE document ${index + 1} label`, specification.maximum_label_characters
    );
    if (ids.has(id)) throw new Error(`Duplicate MWE document ID: ${id}.`);
    ids.add(id);
    const workspace = item?.workspace;
    if (workspace?.schema_version !== contract.workspace_file.schema_version ||
        workspace.contract_version !== contract.contract_version) {
      throw new Error(`MWE document workspace contract does not match: ${id}.`);
    }
    combinedTextLength += typeof workspace.document?.text === 'string'
      ? workspace.document.text.length : specification.maximum_combined_text_characters + 1;
    return {id, label, workspace};
  });
  if (combinedTextLength > specification.maximum_combined_text_characters) {
    throw new Error('MWE document-set text exceeds the reviewed browser limit.');
  }
  return {setId, setLabel, documents};
}

export function makeMweDocumentSetRecord({
  contract, setId, setLabel, documents, savedAt, authorizationAttested
}) {
  if (authorizationAttested !== true) {
    throw new Error('MWE document-set save requires input authorization attestation.');
  }
  const record = {
    schema_version: contract.document_set_file.schema_version,
    contract_version: contract.contract_version,
    saved_at: savedAt,
    raw_content_included: true,
    input_authorization: {attested: true, independently_verified_by_app: false},
    set: {id: setId, label: setLabel},
    documents: structuredClone(documents)
  };
  const validated = validateMweDocumentSetEnvelope(record, contract);
  record.set = {id: validated.setId, label: validated.setLabel};
  record.documents = validated.documents.map(item => ({
    id: item.id, label: item.label, workspace: structuredClone(item.workspace)
  }));
  return record;
}

export async function restoreMweDocumentSetRecord({
  record, contract, authorizationAttested, wordProfiles, mweFormProfile, mweSenseProfile
}) {
  if (authorizationAttested !== true) {
    throw new Error('MWE document-set restore requires current input authorization attestation.');
  }
  if (!(wordProfiles instanceof Map)) throw new Error('MWE document-set profiles are unavailable.');
  record = structuredClone(record);
  const validated = validateMweDocumentSetEnvelope(record, contract);
  await Promise.all(validated.documents.map(async item => {
    const key = item.workspace.word_profile_selection?.key;
    const selection = wordProfiles.get(key);
    if (!selection) throw new Error(`MWE document profile is unavailable: ${item.id}.`);
    await restoreMweWorkspaceRecord({
      record: item.workspace, contract, authorizationAttested: true, wordProfileKey: key,
      wordProfile: selection.profile, wordRankCutoff: selection.maximumRank,
      mweFormProfile, mweSenseProfile
    });
  }));
  return {
    setId: validated.setId,
    setLabel: validated.setLabel,
    documents: validated.documents.map(item => ({
      id: item.id, label: item.label, workspace: structuredClone(item.workspace)
    }))
  };
}

export async function makeMweReviewRecord({
  document, contract, patternSource, tokenizer, authorizationAttested, generatedAt,
  wordProfile, wordRankCutoff, mweFormProfile, mweSenseProfile
}) {
  if (typeof patternSource !== 'string' || typeof generatedAt !== 'string') {
    throw new Error('MWE review export metadata is missing.');
  }
  if (authorizationAttested !== true) {
    throw new Error('MWE review export requires input authorization attestation.');
  }
  document = structuredClone(document);
  const wordCoverage = validateMweRuntime({
    document, contract, wordProfile, wordRankCutoff, mweFormProfile, mweSenseProfile
  });
  requireExactIsoTimestamp(generatedAt, 'MWE review timestamp');
  return {
    schema_version: '0.4.0-mwe-review',
    generated_at: generatedAt,
    contract_version: contract.contract_version,
    method: {
      candidate_generation: contract.candidate_generation,
      automatic_confirmation: false,
      tokenizer,
      categories: contract.occurrence_record.categories
    },
    active_runtime_resources: [
      activeProfileRecord(wordProfile), activeProfileRecord(mweFormProfile),
      activeProfileRecord(mweSenseProfile)
    ],
    input_authorization: {attested: true, independently_verified_by_app: false},
    text: {
      sha256_utf8: await sha256(document.text),
      mwe_token_count: document.tokens.length,
      word_profile_token_count: wordCoverage.token_coverage.denominator,
      raw_text_included: false
    },
    pattern_tsv: {
      sha256_utf8: await sha256(patternSource),
      included: false
    },
    summary: {
      review: summarizeMweDocument(document, contract),
      word_coverage: {
        profile_id: wordCoverage.profile_id,
        profile_version: wordCoverage.profile_version,
        reference_function: wordCoverage.reference_function,
        selected_rank_cutoff: wordCoverage.selected_rank_cutoff,
        tokenizer_unit: wordCoverage.tokenizer_unit,
        token_coverage: wordCoverage.token_coverage,
        type_coverage: wordCoverage.type_coverage,
        uncovered_token_count: wordCoverage.uncovered_token_count,
        uncovered_type_count: wordCoverage.uncovered_type_count,
        unmatched_token_count: wordCoverage.unmatched_token_count,
        unmatched_type_count: wordCoverage.unmatched_type_count,
        beyond_cutoff_token_count: wordCoverage.beyond_cutoff_token_count,
        beyond_cutoff_type_count: wordCoverage.beyond_cutoff_type_count,
        item_rows_included: false
      },
      mwe_form_coverage: summarizeMweFormCoverage(document, contract)
    },
    occurrences: document.occurrences.map(item => ({
      id: item.id,
      canonical_form: item.canonical_form,
      category: item.category,
      status: item.status,
      member_token_ids: item.member_token_ids,
      gap_token_ids: item.gap_token_ids,
      candidate_source: item.candidate_source,
      decision: item.decision,
      idiomaticity: item.idiomaticity,
      form_lookup: item.form_lookup,
      sense: item.sense
    })),
    limitations: [
      'surface patterns generate candidates but do not confirm MWE status',
      'the included starter patterns are not a comprehensive or pedagogically ranked inventory',
      'the selected word-profile result and OEWN MWE-form membership are separate channels and are never combined into one score',
      'OEWN form membership is not MWE frequency, occurrence truth, category, contextual sense, or pedagogical importance',
      'OEWN sense candidates are lexicographic options; only the recorded human decision concerns this context',
      'the runtime sense projection is deliberately limited to its named target entries',
      'word-profile membership or rank does not establish contextual meaning, learner knowledge, or a universal coverage threshold',
      'exact source text and pattern TSV must be preserved separately to reproduce this record'
    ]
  };
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
