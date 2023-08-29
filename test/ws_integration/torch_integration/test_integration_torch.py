import pytest

local_torch = pytest.importorskip("torch")


def test_th_integration(ws_th_client):
    th = ws_th_client
    array_ptr_1 = th.tensor([[1, 2, 3], [4, 5, 6]])
    array_ptr_2 = th.tensor([[4, 5, 6], [1, 2, 3]])

    array_1 = local_torch.tensor([[1, 2, 3], [4, 5, 6]])
    array_2 = local_torch.tensor([[4, 5, 6], [1, 2, 3]])

    result_ptr = array_ptr_1 + array_ptr_2
    result = array_1 + array_2

    assert local_torch.equal(result_ptr.retrieve(), result)
