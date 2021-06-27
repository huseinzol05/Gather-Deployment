def mapper(_, text, writer):
    for word in text.split():
        writer.emit(word, '1')


def reducer(word, icounts, writer):
    writer.emit(word, sum(map(int, icounts)))


def combiner(word, icounts, writer):
    writer.count('combiner calls', 1)
    reducer(word, icounts, writer)
