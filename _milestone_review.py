import config
from ingest import load_documents
from chunker import split_documents
from store import search
from gate import check
import questions

corpus = config.CORPUS
chunks = split_documents(load_documents(corpus))
lengths = [len(c.text) for c in chunks]
print('chunk_count', len(chunks))
print('avg_len', sum(lengths) / len(lengths))
print('short_under_200', sum(1 for x in lengths if x < 200))
print('short_under_800', sum(1 for x in lengths if x < 800))
print('longest', max(lengths), 'shortest', min(lengths))
print('--- questions ---')
for q in questions.QUESTIONS:
    r = search(q['question'], top_k=5, corpus=corpus)
    best = min((x.distance for x in r), default=None)
    print(q['question'][:55].replace('\n', ' '), '=> hits', len(r), 'best', best)
print('--- out_of_scope ---')
for q in questions.OUT_OF_SCOPE:
    r = search(q, top_k=5, corpus=corpus)
    d = check(r)
    print(q[:25], '=> hits', len(r), 'best', round(d.best_distance, 3), 'passed', d.passed)
