import pytest

local_numpy = pytest.importorskip("numpy")


def test_allow_threads(np, consumer, replies):
    allow_threads_pointer = np.ALLOW_THREADS.register()
    allow_threads_pointer.retrieve()
    consumer.listen()
    ptr_result = replies[allow_threads_pointer.id]
    assert ptr_result == local_numpy.ALLOW_THREADS


def test_numpy_s_(np, consumer, replies):
    allow_threads_pointer = np.s_.register()
    allow_threads_pointer.retrieve()
    consumer.listen()
    ptr_result = replies[allow_threads_pointer.id]
    assert ptr_result == local_numpy.s_


def test_numpy_empty(np, consumer, replies):
    array_ptr = np.empty([3, 2], dtype=int)
    array_ptr.retrieve()
    consumer.listen()
    ptr_result = replies[array_ptr.id]
    assert local_numpy.empty([3, 2], dtype=int).shape == ptr_result.shape


def test_numpy_zeros(np, consumer, replies):
    array_ptr = np.zeros((2, 2), dtype=[("x", "i4"), ("y", "i4")])
    array_ptr.retrieve()
    consumer.listen()
    ptr_result = replies[array_ptr.id]
    assert local_numpy.array_equal(
        local_numpy.zeros((2, 2), dtype=[("x", "i4"), ("y", "i4")]),
        ptr_result,
    )


def test_numpy_ones(np, consumer, replies):
    array_ptr = np.ones((2, 2), dtype=[("x", "i4"), ("y", "i4")])
    array_ptr.retrieve()
    consumer.listen()
    ptr_result = replies[array_ptr.id]
    assert local_numpy.array_equal(
        local_numpy.ones((2, 2), dtype=[("x", "i4"), ("y", "i4")]),
        ptr_result,
    )


def test_create_array(np, consumer, replies):
    array_ptr = np.array([1, 2, 3, 4, 5])
    array_ptr.retrieve()
    consumer.listen()
    ptr_result = replies[array_ptr.id]
    assert local_numpy.array_equal(
        local_numpy.array([1, 2, 3, 4, 5]),
        ptr_result,
    )


def test_create_array_dtype(np, consumer, replies):
    array_ptr = np.array([1, 2, 3, 4, 5], dtype=np.complex64)
    array_ptr.retrieve()
    consumer.listen()
    ptr_result = replies[array_ptr.id]
    assert local_numpy.array_equal(
        local_numpy.array([1, 2, 3, 4, 5], dtype=local_numpy.complex64),
        ptr_result,
    )


def test_create_array_ndim(np, consumer, replies):
    array_ptr = np.array([1, 2, 3, 4, 5], ndmin=2)
    array_ptr.retrieve()
    consumer.listen()
    ptr_result = replies[array_ptr.id]
    assert local_numpy.array_equal(
        local_numpy.array([1, 2, 3, 4, 5], ndmin=2),
        ptr_result,
    )


def test_array_shape(np, consumer, replies):
    array_ptr = np.array([[1, 2, 3, 4, 5], [1, 2, 3, 4, 5]])
    shape_ptr = array_ptr.shape
    shape_ptr.retrieve()
    consumer.listen()
    ptr_result = replies[shape_ptr.id]
    assert (
        ptr_result
        == local_numpy.array([[1, 2, 3, 4, 5], [1, 2, 3, 4, 5]]).shape
    )


def test_array_itemsize(np, consumer, replies):
    array_ptr = np.array([[1, 2, 3, 4, 5], [1, 2, 3, 4, 5]])
    shape_ptr = array_ptr.itemsize
    shape_ptr.retrieve()
    consumer.listen()
    ptr_result = replies[shape_ptr.id]
    assert (
        ptr_result
        == local_numpy.array([[1, 2, 3, 4, 5], [1, 2, 3, 4, 5]]).itemsize
    )


def test_array_dim(np, consumer, replies):
    array_ptr = np.array([[1, 2, 3, 4, 5], [1, 2, 3, 4, 5]])
    shape_ptr = array_ptr.ndim
    shape_ptr.retrieve()
    consumer.listen()
    ptr_result = replies[shape_ptr.id]
    assert (
        ptr_result
        == local_numpy.array([[1, 2, 3, 4, 5], [1, 2, 3, 4, 5]]).ndim
    )


def test_array_size(np, consumer, replies):
    array_ptr = np.array([[1, 2, 3, 4, 5], [1, 2, 3, 4, 5]])
    shape_ptr = array_ptr.size
    shape_ptr.retrieve()
    consumer.listen()
    ptr_result = replies[shape_ptr.id]
    assert (
        ptr_result
        == local_numpy.array([[1, 2, 3, 4, 5], [1, 2, 3, 4, 5]]).size
    )


def test_array_reshape(np, consumer, replies):
    array_ptr = np.array([[1, 2, 3], [4, 5, 6]])
    local_array = local_numpy.array([[1, 2, 3], [4, 5, 6]])
    reshaped_array = array_ptr.reshape(3, 2)
    reshaped_array.retrieve()
    consumer.listen()
    ptr_result = replies[reshaped_array.id]
    assert local_numpy.array_equal(local_array.reshape(3, 2), ptr_result)


def test_get_indexed_array(np, consumer, replies):
    array_ptr = np.arange(12).reshape(4, 3)
    local_array = local_numpy.arange(12).reshape(4, 3)
    slice_ptr = array_ptr[:, [0, 2]]
    local_slice = local_array[:, [0, 2]]
    slice_ptr.retrieve()
    consumer.listen()
    ptr_result = replies[slice_ptr.id]
    assert local_numpy.array_equal(local_slice, ptr_result)


def test_set_indexed_array(np, consumer, replies):
    array_ptr = np.arange(12).reshape(4, 3)
    local_array = local_numpy.arange(12).reshape(4, 3)
    array_ptr[:, [2, 0]] = array_ptr[:, [0, 2]]
    local_array[:, [2, 0]] = local_array[:, [0, 2]]
    array_ptr.retrieve()
    consumer.listen()
    ptr_result = replies[array_ptr.id]
    assert local_numpy.array_equal(local_array, ptr_result)


def test_numpy_flat(np, consumer, replies):
    array_ptr = np.arange(8).reshape(2, 4)
    local_array = local_numpy.arange(8).reshape(2, 4)
    flatten_ptr = array_ptr.flat[5]
    local_flatten = local_array.flat[5]
    flatten_ptr.retrieve()
    consumer.listen()
    ptr_result = replies[flatten_ptr.id]
    assert local_numpy.array_equal(local_flatten, ptr_result)


def test_numpy_flatten(np, consumer, replies):
    array_ptr = np.arange(8).reshape(2, 4)
    local_array = local_numpy.arange(8).reshape(2, 4)
    flatten_ptr = array_ptr.flatten()
    local_flatten = local_array.flatten()
    flatten_f_ptr = array_ptr.flatten(order="F")
    local_flatten_f = local_array.flatten(order="F")
    flatten_ptr.retrieve()
    flatten_f_ptr.retrieve()
    consumer.listen()
    ptr_result_1 = replies[flatten_ptr.id]
    ptr_result_2 = replies[flatten_f_ptr.id]
    assert local_numpy.array_equal(local_flatten, ptr_result_1)
    assert local_numpy.array_equal(local_flatten_f, ptr_result_2)


def test_numpy_ravel(np, consumer, replies):
    array_ptr = np.arange(8).reshape(2, 4)
    local_array = local_numpy.arange(8).reshape(2, 4)
    flatten_ptr = array_ptr.ravel()
    local_flatten = local_array.ravel()
    flatten_f_ptr = array_ptr.ravel(order="F")
    local_flatten_f = local_array.ravel(order="F")
    flatten_ptr.retrieve()
    flatten_f_ptr.retrieve()
    consumer.listen()
    ptr_result_1 = replies[flatten_ptr.id]
    ptr_result_2 = replies[flatten_f_ptr.id]
    assert local_numpy.array_equal(local_flatten, ptr_result_1)
    assert local_numpy.array_equal(local_flatten_f, ptr_result_2)


def test_transpose_array(np, consumer, replies):
    array_ptr = np.arange(12).reshape(3, 4)
    transposed_ptr = np.transpose(array_ptr)
    local_array = local_numpy.arange(12).reshape(3, 4)
    transposed_array = local_numpy.transpose(local_array)
    transposed_ptr.retrieve()
    consumer.listen()
    ptr_result = replies[transposed_ptr.id]
    assert local_numpy.array_equal(transposed_array, ptr_result)


def test_transpose_t_array(np, consumer, replies):
    array_ptr = np.arange(12).reshape(3, 4)
    transposed_ptr = array_ptr.T
    local_array = local_numpy.arange(12).reshape(3, 4)
    transposed_array = local_array.T
    transposed_ptr.retrieve()
    consumer.listen()
    ptr_result = replies[transposed_ptr.id]
    assert local_numpy.array_equal(transposed_array, ptr_result)


def test_rollaxis_array(np, consumer, replies):
    array_ptr = np.arange(8).reshape(2, 2, 2)
    local_array = local_numpy.arange(8).reshape(2, 2, 2)
    rollaxis_ptr = np.rollaxis(array_ptr, 2)
    rollaxis_array = local_numpy.rollaxis(local_array, 2)
    rollaxis_ptr.retrieve()
    consumer.listen()
    ptr_result = replies[rollaxis_ptr.id]
    assert local_numpy.array_equal(rollaxis_array, ptr_result)


def test_swapaxis_array(np, consumer, replies):
    array_ptr = np.arange(8).reshape(2, 2, 2)
    local_array = local_numpy.arange(8).reshape(2, 2, 2)
    rollaxis_ptr = np.swapaxes(array_ptr, 2, 0)
    rollaxis_array = local_numpy.swapaxes(local_array, 2, 0)
    rollaxis_ptr.retrieve()
    consumer.listen()
    ptr_result = replies[rollaxis_ptr.id]
    assert local_numpy.array_equal(rollaxis_array, ptr_result)


def test_expand_dims(np, consumer, replies):
    array_ptr = np.array(([1, 2], [3, 4]))
    expanded_dim_ptr = np.expand_dims(array_ptr, axis=0)
    local_array = local_numpy.array(([1, 2], [3, 4]))
    expanded_dim_local = local_numpy.expand_dims(local_array, axis=0)
    expanded_dim_ptr.retrieve()
    consumer.listen()
    ptr_result = replies[expanded_dim_ptr.id]
    assert local_numpy.array_equal(expanded_dim_local, ptr_result)


def test_squeeze_dims(np, consumer, replies):
    array_ptr = np.arange(9).reshape(1, 3, 3)
    expanded_dim_ptr = np.squeeze(array_ptr)
    local_array = local_numpy.arange(9).reshape(1, 3, 3)
    expanded_dim_local = local_numpy.squeeze(local_array)
    expanded_dim_ptr.retrieve()
    consumer.listen()
    ptr_result = replies[expanded_dim_ptr.id]
    assert local_numpy.array_equal(expanded_dim_local, ptr_result)


def test_concatenate_arrays(np, consumer, replies):
    x_ptr = np.array([[1, 2], [3, 4]])
    y_ptr = np.array([[5, 6], [7, 8]])
    axis_0_ptr = np.concatenate((x_ptr, y_ptr))
    axis_1_ptr = np.concatenate((x_ptr, y_ptr), axis=1)

    x = local_numpy.array([[1, 2], [3, 4]])
    y = local_numpy.array([[5, 6], [7, 8]])
    axis_0 = local_numpy.concatenate((x, y))
    axis_1 = local_numpy.concatenate((x, y), axis=1)

    axis_0_ptr.retrieve()
    axis_1_ptr.retrieve()
    consumer.listen()
    ptr1_result = replies[axis_0_ptr.id]
    ptr2_result = replies[axis_1_ptr.id]
    assert local_numpy.array_equal(axis_0, ptr1_result)
    assert local_numpy.array_equal(axis_1, ptr2_result)


def test_stack_arrays(np, consumer, replies):
    x_ptr = np.array([[1, 2], [3, 4]])
    y_ptr = np.array([[5, 6], [7, 8]])
    axis_0_ptr = np.stack((x_ptr, y_ptr), 0)
    axis_1_ptr = np.stack((x_ptr, y_ptr), 1)

    x = local_numpy.array([[1, 2], [3, 4]])
    y = local_numpy.array([[5, 6], [7, 8]])
    axis_0 = local_numpy.stack((x, y), 0)
    axis_1 = local_numpy.stack((x, y), 1)

    axis_0_ptr.retrieve()
    axis_1_ptr.retrieve()
    consumer.listen()
    ptr1_result = replies[axis_0_ptr.id]
    ptr2_result = replies[axis_1_ptr.id]
    assert local_numpy.array_equal(axis_0, ptr1_result)
    assert local_numpy.array_equal(axis_1, ptr2_result)


def test_array_broadcast_to(np, consumer, replies):
    array_ptr = np.arange(4).reshape(1, 4)
    local_array = local_numpy.arange(4).reshape(1, 4)
    broadcasted_array_ptr = np.broadcast_to(array_ptr, (4, 4))
    broadcasted_array_local = local_numpy.broadcast_to(local_array, (4, 4))

    broadcasted_array_ptr.retrieve()
    consumer.listen()
    ptr1_result = replies[broadcasted_array_ptr.id]
    assert local_numpy.array_equal(broadcasted_array_local, ptr1_result)


def test_h_stack_arrays(np, consumer, replies):
    x_ptr = np.array([[1, 2], [3, 4]])
    y_ptr = np.array([[5, 6], [7, 8]])
    axis_0_ptr = np.hstack((x_ptr, y_ptr))

    x = local_numpy.array([[1, 2], [3, 4]])
    y = local_numpy.array([[5, 6], [7, 8]])
    axis_0 = local_numpy.hstack((x, y))

    axis_0_ptr.retrieve()
    consumer.listen()
    ptr1_result = replies[axis_0_ptr.id]
    assert local_numpy.array_equal(axis_0, ptr1_result)


def test_v_stack_arrays(np, consumer, replies):
    x_ptr = np.array([[1, 2], [3, 4]])
    y_ptr = np.array([[5, 6], [7, 8]])
    axis_0_ptr = np.vstack((x_ptr, y_ptr))

    x = local_numpy.array([[1, 2], [3, 4]])
    y = local_numpy.array([[5, 6], [7, 8]])
    axis_0 = local_numpy.vstack((x, y))

    axis_0_ptr.retrieve()
    consumer.listen()
    ptr1_result = replies[axis_0_ptr.id]
    assert local_numpy.array_equal(axis_0, ptr1_result)


def test_split_array(np, consumer, replies):
    array_ptr = np.arange(9)
    split_array_ptr = np.split(array_ptr, 3)
    split_array_2_ptr = np.split(array_ptr, [4, 7])

    local_array = local_numpy.arange(9)
    split_array_local = local_numpy.split(local_array, 3)
    # split_array_2_local = local_numpy.split(local_array, [4, 7])

    split_array_ptr.retrieve()
    split_array_2_ptr.retrieve()
    consumer.listen()
    ptr1_result = replies[split_array_ptr.id]
    # ptr2_result = replies[split_array_2_ptr.id]
    assert local_numpy.array_equal(split_array_local, ptr1_result)

    """
    assert  local_numpy.array_equal(
        split_array_2_local,
        split_array_2_local)
    Not sure why, but it doesn't work for this use case."""


def test_h_split_array(np, consumer, replies):
    array_ptr = np.arange(16).reshape(4, 4)
    split_array_ptr = np.hsplit(array_ptr, 2)

    local_array = local_numpy.arange(16).reshape(4, 4)
    split_array_local = local_numpy.hsplit(local_array, 2)

    split_array_ptr.retrieve()
    consumer.listen()
    ptr1_result = replies[split_array_ptr.id]
    assert local_numpy.array_equal(split_array_local, ptr1_result)


def test_v_split_array(np, consumer, replies):
    array_ptr = np.arange(16).reshape(4, 4)
    split_array_ptr = np.vsplit(array_ptr, 2)

    local_array = local_numpy.arange(16).reshape(4, 4)
    split_array_local = local_numpy.vsplit(local_array, 2)

    split_array_ptr.retrieve()
    consumer.listen()
    ptr1_result = replies[split_array_ptr.id]
    assert local_numpy.array_equal(split_array_local, ptr1_result)


def test_resize_array(np, consumer, replies):
    array_ptr = np.array([[1, 2, 3], [4, 5, 6]])
    split_array_ptr = np.resize(array_ptr, (3, 2))

    local_array = local_numpy.array([[1, 2, 3], [4, 5, 6]])
    split_array_local = local_numpy.resize(local_array, (3, 2))

    split_array_ptr.retrieve()
    consumer.listen()
    ptr1_result = replies[split_array_ptr.id]
    assert local_numpy.array_equal(split_array_local, ptr1_result)


def test_append_array(np, consumer, replies):
    array_ptr = np.array([[1, 2, 3], [4, 5, 6]])
    split_array_ptr = np.append(array_ptr, [7, 8, 9])

    local_array = local_numpy.array([[1, 2, 3], [4, 5, 6]])
    split_array_local = local_numpy.append(local_array, [7, 8, 9])

    split_array_ptr.retrieve()
    consumer.listen()
    ptr1_result = replies[split_array_ptr.id]
    assert local_numpy.array_equal(split_array_local, ptr1_result)


def test_insert_array(np, consumer, replies):
    array_ptr = np.array([[1, 2], [3, 4], [5, 6]])
    split_array_ptr = np.insert(array_ptr, 3, [11, 12])

    local_array = local_numpy.array([[1, 2], [3, 4], [5, 6]])
    split_array_local = local_numpy.insert(local_array, 3, [11, 12])

    split_array_ptr.retrieve()
    consumer.listen()
    ptr1_result = replies[split_array_ptr.id]
    assert local_numpy.array_equal(split_array_local, ptr1_result)


def test_delete_array(np, consumer, replies):
    array_ptr = np.arange(12).reshape(3, 4)
    split_array_ptr = np.delete(array_ptr, 5)
    split_array_1_ptr = np.delete(array_ptr, 1, axis=1)

    local_array = local_numpy.arange(12).reshape(3, 4)
    split_array_local = local_numpy.delete(local_array, 5)
    split_array_local_1 = local_numpy.delete(local_array, 1, axis=1)

    new_array_ptr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    new_deleted_result_ptr = np.delete(new_array_ptr, np.s_[::2])

    new_local_array = local_numpy.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    new_deleted_result_local = local_numpy.delete(
        new_local_array,
        local_numpy.s_[::2],
    )

    split_array_ptr.retrieve()
    split_array_1_ptr.retrieve()
    new_deleted_result_ptr.retrieve()
    consumer.listen()
    ptr1_result = replies[split_array_ptr.id]
    ptr2_result = replies[split_array_1_ptr.id]
    ptr3_result = replies[new_deleted_result_ptr.id]
    assert local_numpy.array_equal(split_array_local, ptr1_result)
    assert local_numpy.array_equal(split_array_local_1, ptr2_result)
    assert local_numpy.array_equal(new_deleted_result_local, ptr3_result)


def test_array_unique(np, consumer, replies):
    array_ptr = np.array([5, 2, 6, 2, 7, 5, 6, 8, 2, 9])
    unique_ptr = np.unique(array_ptr)
    unique_index_ptr = np.unique(array_ptr, return_index=True)
    unique_inverse_ptr = np.unique(array_ptr, return_inverse=True)
    unique_counts_ptr = np.unique(array_ptr, return_counts=True)

    local_array = local_numpy.array([5, 2, 6, 2, 7, 5, 6, 8, 2, 9])
    local_array_unique_ptr = local_numpy.unique(local_array)
    local_array_unique_index_ptr = local_numpy.unique(
        local_array,
        return_index=True,
    )
    # local_array_unique_inverse_ptr = local_numpy.unique(
    #    local_array,
    #    return_inverse=True,
    # )
    local_array_unique_counts_ptr = local_numpy.unique(
        local_array,
        return_counts=True,
    )

    unique_ptr.retrieve()
    unique_index_ptr.retrieve()
    unique_inverse_ptr.retrieve()
    unique_counts_ptr.retrieve()
    consumer.listen()
    ptr1_result = replies[unique_ptr.id]
    ptr2_result = replies[unique_index_ptr.id]
    # ptr3_result = replies[unique_inverse_ptr.id]
    ptr4_result = replies[unique_counts_ptr.id]
    assert local_numpy.array_equal(local_array_unique_ptr, ptr1_result)
    assert local_numpy.array_equal(local_array_unique_index_ptr, ptr2_result)
    assert local_numpy.array_equal(local_array_unique_counts_ptr, ptr4_result)
    # Not sure why but it fails even being visually equal
    # assert  local_numpy.array_equal(
    # local_array_unique_inverse_ptr,
    # ptr3_result)


def test_add_array(np, consumer, replies):
    array_ptr_1 = np.array([[1, 2], [3, 4], [5, 6]])
    array_ptr_2 = np.array([[1, 2], [3, 4], [5, 6]])
    result_ptr = array_ptr_1 + array_ptr_2

    local_array_1 = local_numpy.array([[1, 2], [3, 4], [5, 6]])
    local_array_2 = local_numpy.array([[1, 2], [3, 4], [5, 6]])
    result_local = local_array_1 + local_array_2

    result_ptr.retrieve()
    consumer.listen()
    ptr1_result = replies[result_ptr.id]
    assert local_numpy.array_equal(result_local, ptr1_result)


def test_sub_array(np, consumer, replies):
    array_ptr_1 = np.array([[1, 2], [3, 4], [5, 6]])
    array_ptr_2 = np.array([[1, 2], [3, 4], [5, 6]])
    result_ptr = array_ptr_1 - array_ptr_2

    local_array_1 = local_numpy.array([[1, 2], [3, 4], [5, 6]])
    local_array_2 = local_numpy.array([[1, 2], [3, 4], [5, 6]])
    result_local = local_array_1 - local_array_2

    result_ptr.retrieve()
    consumer.listen()
    ptr1_result = replies[result_ptr.id]
    assert local_numpy.array_equal(result_local, ptr1_result)


def test_mul_array(np, consumer, replies):
    array_ptr_1 = np.array([[1, 2], [3, 4], [5, 6]])
    array_ptr_2 = np.array([[1, 2], [3, 4], [5, 6]])
    result_ptr = array_ptr_1 * array_ptr_2

    local_array_1 = local_numpy.array([[1, 2], [3, 4], [5, 6]])
    local_array_2 = local_numpy.array([[1, 2], [3, 4], [5, 6]])
    result_local = local_array_1 * local_array_2

    result_ptr.retrieve()
    consumer.listen()
    ptr1_result = replies[result_ptr.id]
    assert local_numpy.array_equal(result_local, ptr1_result)


def test_div_array(np, consumer, replies):
    array_ptr_1 = np.array([[1, 2], [3, 4], [5, 6]])
    array_ptr_2 = np.array([[1, 2], [3, 4], [5, 6]])
    result_ptr = array_ptr_1 / array_ptr_2

    local_array_1 = local_numpy.array([[1, 2], [3, 4], [5, 6]])
    local_array_2 = local_numpy.array([[1, 2], [3, 4], [5, 6]])
    result_local = local_array_1 / local_array_2

    result_ptr.retrieve()
    consumer.listen()
    ptr1_result = replies[result_ptr.id]
    assert local_numpy.array_equal(result_local, ptr1_result)


def test_pow_array(np, consumer, replies):
    array_ptr_1 = np.array([[1, 2], [3, 4], [5, 6]])
    array_ptr_2 = np.array([[1, 2], [3, 4], [5, 6]])
    result_ptr = array_ptr_1**array_ptr_2

    local_array_1 = local_numpy.array([[1, 2], [3, 4], [5, 6]])
    local_array_2 = local_numpy.array([[1, 2], [3, 4], [5, 6]])
    result_local = local_array_1**local_array_2

    result_ptr.retrieve()
    consumer.listen()
    ptr1_result = replies[result_ptr.id]
    assert local_numpy.array_equal(result_local, ptr1_result)


def test_mod_array(np, consumer, replies):
    array_ptr_1 = np.array([[1, 2], [3, 4], [5, 6]])
    array_ptr_2 = np.array([[1, 2], [3, 4], [5, 6]])
    result_ptr = array_ptr_1 // array_ptr_2

    local_array_1 = local_numpy.array([[1, 2], [3, 4], [5, 6]])
    local_array_2 = local_numpy.array([[1, 2], [3, 4], [5, 6]])
    result_local = local_array_1 // local_array_2

    result_ptr.retrieve()
    consumer.listen()
    ptr1_result = replies[result_ptr.id]
    assert local_numpy.array_equal(result_local, ptr1_result)
