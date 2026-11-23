# Copyright 2026 Python Language Server Contributors.

from concurrent import futures
import pytest

from pylsp_jsonrpc import exceptions
from pylsp_jsonrpc.endpoint import Endpoint


@pytest.mark.parametrize('code, error_type', [
    (-32603, exceptions.JsonRpcInternalError),
    (-32602, exceptions.JsonRpcInvalidParams),
    (0, exceptions.JsonRpcException),
    (123, exceptions.JsonRpcException),
])
def test_error_response_code(code, error_type):
    endpoint = Endpoint({}, lambda message: None, id_generator=lambda: 'request')
    try:
        future = endpoint.request('method')
        endpoint.consume({
            'jsonrpc': '2.0',
            'id': 'request',
            'error': {'code': code, 'message': 'remote failure', 'data': {'detail': 1}},
        })
        assert future.done()
        with pytest.raises(error_type) as exc_info:
            future.result(timeout=1)
        assert exc_info.type is error_type
        assert exc_info.value.to_dict() == {
            'code': code, 'message': 'remote failure', 'data': {'detail': 1},
        }
    finally:
        endpoint.shutdown()


@pytest.mark.parametrize('mode', ['direct', 'future', 'callable'])
def test_internal_handler_error_code(mode):
    messages = []

    def fail():
        raise RuntimeError('handler failure')

    def handler(_params):
        if mode == 'callable':
            return fail
        if mode == 'future':
            failed = futures.Future()
            failed.set_exception(RuntimeError('handler failure'))
            return failed
        return fail()

    endpoint = Endpoint({'method': handler}, messages.append)
    try:
        endpoint.consume({'jsonrpc': '2.0', 'id': 'request', 'method': 'method'})
        endpoint.shutdown()
        assert len(messages) == 1
        assert messages[0]['id'] == 'request'
        assert messages[0]['error']['code'] == -32603
        assert messages[0]['error']['message'] == 'RuntimeError: handler failure'
    finally:
        endpoint.shutdown()


def test_explicit_zero_code_is_preserved():
    error = exceptions.JsonRpcException('application failure', code=0)
    assert error.to_dict() == {'message': 'application failure', 'code': 0}
    assert exceptions.JsonRpcInternalError('application failure', code=0).code == 0
    assert exceptions.JsonRpcInternalError().code == -32603
