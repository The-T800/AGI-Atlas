const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

const template = fs.readFileSync(path.join(__dirname, '../src/agi_atlas/templates/index.html'), 'utf8');
const helpers = template.slice(template.indexOf('function capabilityLink('), template.indexOf('function benchmarkEvidence('));

function context(selection = {}) {
  const field = { level: 'field', id: '17', domain: '3' };
  const subfield = { level: 'subfield', id: '1702', domain: '3', field: '17' };
  const topic = { level: 'topic', id: 'T10201', domain: '3', field: '17', subfield: '1702' };
  const ctx = vm.createContext({
    subjectState: { domain: '', field: '', subfield: '', query: '', capability: '', ...selection },
    subjectNodes: new Map([field, subfield, topic].map(n => [n.level + ':' + n.id, n])),
    byBench: new Map(),
    repGroup: () => undefined,
  });
  vm.runInContext(helpers, ctx);
  return { ctx, topic };
}

const link = (level, id, capability = 'perception') => ({ target_level: level, target_id: id, capability_id: capability });

test('subfield selection preserves broad field links as context', () => {
  const { ctx, topic } = context({ subfield: '1702' });
  assert.equal(ctx.linkScope(link('field', '17'), [topic]), 'context');
  assert.equal(ctx.linkScope(link('topic', 'T10201'), [topic]), 'linked');
  ctx.subjectNodes.set('field:27', { level: 'field', id: '27', domain: '4' });
  assert.equal(ctx.linkScope(link('field', '27'), [topic]), null);
});

test('topic search separates exact task links, ancestors and unassigned tasks', () => {
  const { ctx, topic } = context({ query: 'T10201' });
  assert.equal(ctx.linkScope(link('topic', 'T10201'), [topic]), 'linked');
  assert.equal(ctx.linkScope(link('field', '17'), [topic]), 'context');
  assert.equal(ctx.linkScope(link('unassigned', ''), [topic]), null);
  assert.equal(ctx.linkScope(link('field', '17'), []), null);
});

test('capability selection applies to both exact evidence and context', () => {
  const { ctx, topic } = context({ query: 'T10201', capability: 'reasoning' });
  assert.equal(ctx.linkScope(link('topic', 'T10201'), [topic]), null);
  assert.equal(ctx.linkScope(link('field', '17', 'reasoning'), [topic]), 'context');
  assert.equal(ctx.capabilityLink(link('topic', 'T10201')), false);
});

test('unassigned evidence is separated from subject evidence', () => {
  const { ctx } = context();
  assert.equal(ctx.linkScope(link('unassigned', ''), []), 'unassigned');
  ctx.subjectState.field = '17';
  assert.equal(ctx.linkScope(link('unassigned', ''), []), null);
});

test('recent evidence in a nonrepresentative group is found without merging groups', () => {
  const { ctx } = context();
  const old = { version: 'A', records: [{ score: 99, freshness: 'historical' }] };
  const recent = { version: 'B', records: [{ score: 90, freshness: 'undated' }, { score: 80, freshness: 'recent' }] };
  ctx.byBench.set('gpqa', [old, recent]);
  ctx.repGroup = () => old;
  assert.equal(ctx.evidenceGroup('gpqa'), recent);
  assert.equal(ctx.freshRecord(ctx.evidenceGroup('gpqa')).score, 80);
  old.records[0].freshness = 'recent';
  assert.equal(ctx.evidenceGroup('gpqa'), old);
  ctx.repGroup = () => undefined;
  assert.equal(ctx.evidenceGroup('missing'), undefined);
});
