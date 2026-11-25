# Copyright 2021- Python Language Server Contributors.

from io import BytesIO
from unittest import mock

import pytest

from pylsp_jsonrpc.streams import JsonRpcStreamReader, JsonRpcStreamWriter


@pytest.mark.parametrize('chunk_size', [1, 7])
def test_writer_short_writes(chunk_size):
    class ShortWriter(BytesIO):
        def write(self, data):
            return super().write(data[:chunk_size])

    stream = ShortWriter()
    stream.flush = mock.Mock()
    writer = JsonRpcStreamWriter(stream, ensure_ascii=False)
    messages = [{'id': 1, 'result': 'caf\u00e9'}, {'id': 2, 'result': '\u96ea'}]
    for message in messages:
        writer.write(message)
    assert stream.flush.call_count == len(messages)
    stream.seek(0)
    received = []
    JsonRpcStreamReader(stream).listen(received.append)
    assert received == messages


@pytest.mark.parametrize('written', [0, None])
def test_writer_short_writes_without_progress(written, caplog):
    stream = BytesIO()
    stream.write = mock.Mock(return_value=written)
    stream.flush = mock.Mock()
    JsonRpcStreamWriter(stream).write({'id': 1})
    stream.write.assert_called_once()
    stream.flush.assert_not_called()
    assert 'Output stream made no progress' in caplog.text
