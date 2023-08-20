import pytest

local_torch = pytest.importorskip("torch")


def test_create_tensor(th, torch_consumer, torch_replies):
    array_ptr = th.tensor([1, 2, 3])
    array_ptr.retrieve()
    torch_consumer.listen()
    ptr_result = torch_replies[array_ptr.id]
    assert local_torch.equal(ptr_result, local_torch.tensor([1, 2, 3]))


def test_add_tensor(th, torch_consumer, torch_replies):
    array_ptr_1 = th.tensor([[1, 2, 3], [4, 5, 6]])
    array_ptr_2 = th.tensor([[4, 5, 6], [1, 2, 3]])

    array_1 = local_torch.tensor([[1, 2, 3], [4, 5, 6]])
    array_2 = local_torch.tensor([[4, 5, 6], [1, 2, 3]])

    result_ptr = array_ptr_1 + array_ptr_2
    result = array_1 + array_2

    result_ptr.retrieve()
    torch_consumer.listen()
    ptr_result = torch_replies[result_ptr.id]
    assert local_torch.equal(ptr_result, result)


def test_sub_tensor(th, torch_consumer, torch_replies):
    array_ptr_1 = th.tensor([[1, 2, 3], [4, 5, 6]])
    array_ptr_2 = th.tensor([[4, 5, 6], [1, 2, 3]])

    array_1 = local_torch.tensor([[1, 2, 3], [4, 5, 6]])
    array_2 = local_torch.tensor([[4, 5, 6], [1, 2, 3]])

    result_ptr = array_ptr_1 - array_ptr_2
    result = array_1 - array_2

    result_ptr.retrieve()
    torch_consumer.listen()
    ptr_result = torch_replies[result_ptr.id]
    assert local_torch.equal(ptr_result, result)


def test_mul_tensor(th, torch_consumer, torch_replies):
    array_ptr_1 = th.tensor([[1, 2, 3], [4, 5, 6]])
    array_ptr_2 = th.tensor([[4, 5, 6], [1, 2, 3]])

    array_1 = local_torch.tensor([[1, 2, 3], [4, 5, 6]])
    array_2 = local_torch.tensor([[4, 5, 6], [1, 2, 3]])

    result_ptr = array_ptr_1 * array_ptr_2
    result = array_1 * array_2

    result_ptr.retrieve()
    torch_consumer.listen()
    ptr_result = torch_replies[result_ptr.id]
    assert local_torch.equal(ptr_result, result)


def test_div_tensor(th, torch_consumer, torch_replies):
    array_ptr_1 = th.tensor([[1, 2, 3], [4, 5, 6]])
    array_ptr_2 = th.tensor([[4, 5, 6], [1, 2, 3]])

    array_1 = local_torch.tensor([[1, 2, 3], [4, 5, 6]])
    array_2 = local_torch.tensor([[4, 5, 6], [1, 2, 3]])

    result_ptr = array_ptr_1 / array_ptr_2
    result = array_1 / array_2

    result_ptr.retrieve()
    torch_consumer.listen()
    ptr_result = torch_replies[result_ptr.id]
    assert local_torch.equal(ptr_result, result)


def test_mod_tensor(th, torch_consumer, torch_replies):
    array_ptr_1 = th.tensor([[1, 2, 3], [4, 5, 6]])
    array_ptr_2 = th.tensor([[4, 5, 6], [1, 2, 3]])

    array_1 = local_torch.tensor([[1, 2, 3], [4, 5, 6]])
    array_2 = local_torch.tensor([[4, 5, 6], [1, 2, 3]])

    result_ptr = array_ptr_1 // array_ptr_2
    result = array_1 // array_2

    result_ptr.retrieve()
    torch_consumer.listen()
    ptr_result = torch_replies[result_ptr.id]
    assert local_torch.equal(ptr_result, result)


def test_pow_tensor(th, torch_consumer, torch_replies):
    array_ptr_1 = th.tensor([[1, 2, 3], [4, 5, 6]])
    array_ptr_2 = th.tensor([[4, 5, 6], [1, 2, 3]])

    array_1 = local_torch.tensor([[1, 2, 3], [4, 5, 6]])
    array_2 = local_torch.tensor([[4, 5, 6], [1, 2, 3]])

    result_ptr = array_ptr_1**array_ptr_2
    result = array_1**array_2

    result_ptr.retrieve()
    torch_consumer.listen()
    ptr_result = torch_replies[result_ptr.id]
    assert local_torch.equal(ptr_result, result)


def test_torch_zeros(th, torch_consumer, torch_replies):
    array_ptr = th.zeros([2, 4], dtype=th.int32)
    array = local_torch.zeros([2, 4], dtype=local_torch.int32)
    array_ptr.retrieve()
    torch_consumer.listen()
    ptr_result = torch_replies[array_ptr.id]
    assert local_torch.equal(ptr_result, array)


def test_torch_ones(th, torch_consumer, torch_replies):
    array_ptr = th.ones([2, 4], dtype=th.float64, device=th.device("cpu"))
    array = local_torch.ones(
        [2, 4],
        dtype=local_torch.float64,
        device=local_torch.device("cpu"),
    )
    array_ptr.retrieve()
    torch_consumer.listen()
    ptr_result = torch_replies[array_ptr.id]
    assert local_torch.equal(ptr_result, array)


def test_torch_item(th, torch_consumer, torch_replies):
    array_ptr = th.tensor([[2.5]])
    array = local_torch.tensor([[2.5]])
    result_ptr = array_ptr.item()
    result = array.item()
    result_ptr.retrieve()
    torch_consumer.listen()
    ptr_result = torch_replies[result_ptr.id]
    assert ptr_result == result


def test_torch_arange(th, torch_consumer, torch_replies):
    array_ptr = th.arange(4, dtype=th.float)
    array = local_torch.arange(4, dtype=local_torch.float)
    array_ptr.retrieve()
    torch_consumer.listen()
    ptr_result = torch_replies[array_ptr.id]
    assert local_torch.equal(ptr_result, array)


def test_torch_reshape(th, torch_consumer, torch_replies):
    array_ptr = th.reshape(th.arange(4.0), (2, 2))
    array = local_torch.reshape(local_torch.arange(4.0), (2, 2))
    array_ptr.retrieve()
    torch_consumer.listen()
    ptr_result = torch_replies[array_ptr.id]
    assert local_torch.equal(ptr_result, array)


def test_torch_adjoint(th, torch_consumer, torch_replies):
    array_ptr = th.arange(4, dtype=th.float)
    array_ptr = th.complex(array_ptr, array_ptr).reshape(2, 2)
    array_ptr = array_ptr.adjoint()
    array = local_torch.arange(4, dtype=local_torch.float)
    array = local_torch.complex(array, array).reshape(2, 2)
    array = array.adjoint()
    array_ptr.retrieve()
    torch_consumer.listen()
    ptr_result = torch_replies[array_ptr.id]
    assert local_torch.equal(ptr_result, array)


def test_torch_argwhere(th, torch_consumer, torch_replies):
    array_ptr = th.tensor([[1, 0, 1], [0, 1, 1]])
    array_ptr = th.argwhere(array_ptr)
    array = local_torch.tensor([[1, 0, 1], [0, 1, 1]])
    array = local_torch.argwhere(array)
    array_ptr.retrieve()
    torch_consumer.listen()
    ptr_result = torch_replies[array_ptr.id]
    assert local_torch.equal(ptr_result, array)


def test_torch_cat(th, torch_consumer, torch_replies):
    array_ptr = th.ones([2, 3], dtype=th.float64)
    array_ptr = th.cat((array_ptr, array_ptr, array_ptr), 1)
    array = local_torch.ones([2, 3], dtype=local_torch.float64)
    array = local_torch.cat((array, array, array), 1)
    array_ptr.retrieve()
    torch_consumer.listen()
    ptr_result = torch_replies[array_ptr.id]
    assert local_torch.equal(ptr_result, array)


def test_torch_concat(th, torch_consumer, torch_replies):
    array_ptr = th.ones([2, 3], dtype=th.float64)
    array_ptr = th.concat((array_ptr, array_ptr, array_ptr), 1)
    array = local_torch.ones([2, 3], dtype=local_torch.float64)
    array = local_torch.concat((array, array, array), 1)
    array_ptr.retrieve()
    torch_consumer.listen()
    ptr_result = torch_replies[array_ptr.id]
    assert local_torch.equal(ptr_result, array)


def test_torch_concatenate(th, torch_consumer, torch_replies):
    array_ptr = th.ones([2, 3], dtype=th.float64)
    array_ptr = th.concatenate((array_ptr, array_ptr, array_ptr), 1)
    array = local_torch.ones([2, 3], dtype=local_torch.float64)
    array = local_torch.concatenate((array, array, array), 1)
    array_ptr.retrieve()
    torch_consumer.listen()
    ptr_result = torch_replies[array_ptr.id]
    assert local_torch.equal(ptr_result, array)


def test_torch_conj(th, torch_consumer, torch_replies):
    array_ptr = th.conj(th.tensor([-1 + 1j, -2 + 2j, 3 - 3j]))
    array = local_torch.conj(local_torch.tensor([-1 + 1j, -2 + 2j, 3 - 3j]))
    array_ptr.retrieve()
    torch_consumer.listen()
    ptr_result = torch_replies[array_ptr.id]
    assert local_torch.equal(ptr_result, array)


def test_torch_chunk(th, torch_consumer, torch_replies):
    array_ptr = th.arange(12).chunk(6)
    array = local_torch.arange(12).chunk(6)
    array_ptr.retrieve()
    torch_consumer.listen()
    ptr_result = torch_replies[array_ptr.id]
    assert len(ptr_result) == len(array)


def test_torch_dsplit(th, torch_consumer, torch_replies):
    array_ptr = th.dsplit(th.arange(16.0).reshape(2, 2, 4), 2)
    array = local_torch.dsplit(local_torch.arange(16.0).reshape(2, 2, 4), 2)
    array_ptr.retrieve()
    torch_consumer.listen()
    ptr_result = torch_replies[array_ptr.id]
    assert len(ptr_result) == len(array)


def test_torch_column_stack(th, torch_consumer, torch_replies):
    array_1_ptr = th.tensor([1, 2, 3])
    array_2_ptr = th.tensor([4, 5, 6])
    result_ptr = th.column_stack((array_1_ptr, array_2_ptr))

    array_1 = local_torch.tensor([1, 2, 3])
    array_2 = local_torch.tensor([4, 5, 6])
    result = local_torch.column_stack((array_1, array_2))

    result_ptr.retrieve()
    torch_consumer.listen()
    ptr_result = torch_replies[result_ptr.id]
    assert local_torch.equal(ptr_result, result)


def test_torch_dstack(th, torch_consumer, torch_replies):
    array_1_ptr = th.tensor([1, 2, 3])
    array_2_ptr = th.tensor([4, 5, 6])
    result_ptr = th.dstack((array_1_ptr, array_2_ptr))

    array_1 = local_torch.tensor([1, 2, 3])
    array_2 = local_torch.tensor([4, 5, 6])
    result = local_torch.dstack((array_1, array_2))

    result_ptr.retrieve()
    torch_consumer.listen()
    ptr_result = torch_replies[result_ptr.id]
    assert local_torch.equal(ptr_result, result)


def test_torch_gather(th, torch_consumer, torch_replies):
    array_ptr = th.gather(
        th.tensor([[1, 2], [3, 4]]),
        1,
        th.tensor([[0, 0], [1, 0]]),
    )
    array = local_torch.gather(
        local_torch.tensor([[1, 2], [3, 4]]),
        1,
        local_torch.tensor([[0, 0], [1, 0]]),
    )
    array_ptr.retrieve()
    torch_consumer.listen()
    ptr_result = torch_replies[array_ptr.id]
    assert local_torch.equal(ptr_result, array)


def test_torch_hsplit(th, torch_consumer, torch_replies):
    array_ptr = th.hsplit(th.arange(16.0).reshape(4, 4), 2)
    array = local_torch.hsplit(local_torch.arange(16.0).reshape(4, 4), 2)
    array_ptr.retrieve()
    torch_consumer.listen()
    ptr_result = torch_replies[array_ptr.id]
    assert len(ptr_result) == len(array)


def test_torch_hstack(th, torch_consumer, torch_replies):
    array_1_ptr = th.tensor([1, 2, 3])
    array_2_ptr = th.tensor([4, 5, 6])
    result_ptr = th.hstack((array_1_ptr, array_2_ptr))

    array_1 = local_torch.tensor([1, 2, 3])
    array_2 = local_torch.tensor([4, 5, 6])
    result = local_torch.hstack((array_1, array_2))

    result_ptr.retrieve()
    torch_consumer.listen()
    ptr_result = torch_replies[result_ptr.id]
    assert local_torch.equal(ptr_result, result)


def test_torch_movedim(th, torch_consumer, torch_replies):
    array_ptr = th.movedim(th.ones([3, 2, 1], dtype=th.float64), 1, 0)
    array = local_torch.movedim(
        local_torch.ones([3, 2, 1], dtype=local_torch.float64),
        1,
        0,
    )

    array_ptr.retrieve()
    torch_consumer.listen()
    ptr_result = torch_replies[array_ptr.id]
    assert local_torch.equal(ptr_result, array)


def test_torch_moveaxis(th, torch_consumer, torch_replies):
    array_ptr = th.moveaxis(th.ones([3, 2, 1], dtype=th.float64), 1, 0)
    array = local_torch.moveaxis(
        local_torch.ones([3, 2, 1], dtype=local_torch.float64),
        1,
        0,
    )

    array_ptr.retrieve()
    torch_consumer.listen()
    ptr_result = torch_replies[array_ptr.id]
    assert local_torch.equal(ptr_result, array)


def test_torch_split(th, torch_consumer, torch_replies):
    array_ptr = th.split(th.arange(10).reshape(5, 2), 2)
    array = local_torch.split(local_torch.arange(10).reshape(5, 2), 2)

    array_ptr.retrieve()
    torch_consumer.listen()
    ptr_result = torch_replies[array_ptr.id]
    assert len(ptr_result) == len(array)


def test_torch_squeeze(th, torch_consumer, torch_replies):
    array_ptr = th.squeeze(th.arange(10).reshape(5, 2))
    array = local_torch.squeeze(local_torch.arange(10).reshape(5, 2))

    array_ptr.retrieve()
    torch_consumer.listen()
    ptr_result = torch_replies[array_ptr.id]
    assert local_torch.equal(ptr_result, array)


def test_torch_swapdims(th, torch_consumer, torch_replies):
    array_ptr = th.swapdims(
        th.tensor(
            [
                [[0, 1], [2, 3]],
                [[4, 5], [6, 7]],
            ],
        ),
        0,
        1,
    )
    array = local_torch.swapdims(
        local_torch.tensor(
            [
                [[0, 1], [2, 3]],
                [[4, 5], [6, 7]],
            ],
        ),
        0,
        1,
    )

    array_ptr.retrieve()
    torch_consumer.listen()
    ptr_result = torch_replies[array_ptr.id]
    assert local_torch.equal(ptr_result, array)


def test_torch_t(th, torch_consumer, torch_replies):
    array_ptr = th.t(th.ones([2, 3]))
    array = local_torch.t(local_torch.ones([2, 3]))

    array_ptr.retrieve()
    torch_consumer.listen()
    ptr_result = torch_replies[array_ptr.id]
    assert local_torch.equal(ptr_result, array)


def test_torch_transpose(th, torch_consumer, torch_replies):
    array_ptr = th.transpose(th.ones([2, 3]), 0, 1)
    array = local_torch.transpose(local_torch.ones([2, 3]), 0, 1)

    array_ptr.retrieve()
    torch_consumer.listen()
    ptr_result = torch_replies[array_ptr.id]
    assert local_torch.equal(ptr_result, array)


def test_torch_unbind(th, torch_consumer, torch_replies):
    array_ptr = th.unbind(th.tensor([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))
    array = local_torch.unbind(
        local_torch.tensor(
            [
                [1, 2, 3],
                [4, 5, 6],
                [7, 8, 9],
            ],
        ),
    )

    array_ptr.retrieve()
    torch_consumer.listen()
    ptr_result = torch_replies[array_ptr.id]
    assert len(ptr_result) == len(array)


def test_torch_unsqueeze(th, torch_consumer, torch_replies):
    array_ptr = th.unsqueeze(th.tensor([1, 2, 3, 4]), 1)
    array = local_torch.unsqueeze(local_torch.tensor([1, 2, 3, 4]), 1)

    array_ptr.retrieve()
    torch_consumer.listen()
    ptr_result = torch_replies[array_ptr.id]
    assert local_torch.equal(ptr_result, array)


def test_torch_vsplit(th, torch_consumer, torch_replies):
    array_ptr = th.vsplit(th.arange(16.0).reshape(4, 4), [3, 6])
    array = local_torch.vsplit(local_torch.arange(16.0).reshape(4, 4), [3, 6])

    array_ptr.retrieve()
    torch_consumer.listen()
    ptr_result = torch_replies[array_ptr.id]
    assert len(ptr_result) == len(array)
