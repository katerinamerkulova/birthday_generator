import io
import re
from random import uniform
from collections import defaultdict

r_alphabet = re.compile(u'[а-яёА-Я0-9-]+|[.,:;?!]+')
data = io.open('file.txt', encoding="utf-8")

def gen_lines(data):
    for line in data:
        yield line.lower()

def gen_tokens(lines):
    for line in lines:
        for token in r_alphabet.findall(line):
            yield token

def gen_trigrams(tokens):
    t0, t1 = '$', '$'
    for t2 in tokens:
        yield t0, t1, t2
        if t2 in '.!?':
            yield t1, t2, '$'
            yield t2, '$','$'
            t0, t1 = '$', '$'
        else:
            t0, t1 = t1, t2

def train():
    lines = gen_lines(data)
    tokens = gen_tokens(lines)
    trigrams = gen_trigrams(tokens)

    bi, tri = defaultdict(lambda: 0.0), defaultdict(lambda: 0.0)

    for t0, t1, t2 in trigrams:
        bi[t0, t1] += 1
        tri[t0, t1, t2] += 1

    model = {}
    for (t0, t1, t2), freq in iter(tri.items()):
        if (t0, t1) in model:
            model[t0, t1].append((t2, freq/bi[t0, t1]))
        else:
            model[t0, t1] = [(t2, freq/bi[t0, t1])]
    return model

model = train()

def generate_sentence():
    phrase = ''
    t0, t1 = '$', '$'
    while 1:
        t0, t1 = t1, unirand(model[t0, t1])
        if t1 == '$': break
        if 'днём рождения' in phrase and (t0 == 'днём' or t0 == 'днем') and t1 == 'рождения': continue
        if 'днем рождения' in phrase and (t0 == 'днём' or t0 == 'днем') and t1 == 'рождения': continue
        if t1 in ('.!?,;:') or t0 == '$':
            phrase += t1
        else:
            phrase += ' ' + t1
    if phrase[-9:] != 'рождения!':
        print(phrase.capitalize())
        generate_sentence()
    return ''

def unirand(seq):
    sum_, freq_ = 0, 0
    for item, freq in seq:
        sum_ += freq
    rnd = uniform(0, sum_)
    for token, freq in seq:
        freq_ += freq
        if rnd < freq_:
            return token
        