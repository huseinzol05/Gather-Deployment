def mapper(_, record, writer):
    writer.emit('', record.lower())
