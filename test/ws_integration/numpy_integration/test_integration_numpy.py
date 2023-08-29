import pytest

local_numpy = pytest.importorskip("numpy")


def test_np_integration(ws_np_client):
    np = ws_np_client
    np.ALLOW_THREADS
    x_ptr = np.array([1, 2, 3, 4, 5, 6])
    x_ptr = x_ptr + x_ptr
    assert local_numpy.array_equal(
        x_ptr.retrieve(),
        local_numpy.array([2, 4, 6, 8, 10, 12]),
    )


def test_multiple_ws_clients(ws_np_client, ws_np_client2):
    np = ws_np_client
    np2 = ws_np_client2
    np.ALLOW_THREADS
    np2.ALLOW_THREADS
    x_ptr = np.array([1, 2, 3, 4, 5, 6])
    x2_ptr = np2.array([1, 2, 3, 4, 5, 6])

    x_ptr = x_ptr + x_ptr
    x2_ptr = x2_ptr + x2_ptr

    assert local_numpy.array_equal(
        x_ptr.retrieve(),
        local_numpy.array([2, 4, 6, 8, 10, 12]),
    )
    assert local_numpy.array_equal(
        x2_ptr.retrieve(),
        local_numpy.array([2, 4, 6, 8, 10, 12]),
    )
