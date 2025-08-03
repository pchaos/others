# tests/test_e2e.py
import pytest
import numpy as np
import asyncio
from client.client import HDF5Client

@pytest.fixture
def test_path(request):
    """
    为每个测试函数创建一个唯一的顶级组名，以隔离测试。
    例如，'test_basic_crud' -> '/test_basic_crud'
    """
    return f"/{request.node.name}"

@pytest.mark.asyncio
async def test_basic_crud(client, test_path):
    """Tests basic create, write, read, update, and delete operations."""
    dataset_path = f"{test_path}/my_dataset"

    # Group creation is implicit in client.write, so this is optional
    await client.create_group(test_path)

    data_to_write = np.array([1, 2, 3, 4, 5])
    await client.write(dataset_path, data_to_write)

    read_data = await client.read(dataset_path)
    assert np.array_equal(data_to_write, read_data)

    updated_data = np.array([6, 7, 8, 9, 10])
    await client.update(dataset_path, updated_data)

    read_updated_data = await client.read(dataset_path)
    assert np.array_equal(updated_data, read_updated_data)

    await client.delete(dataset_path)
    read_after_delete = await client.read(dataset_path)
    assert read_after_delete is None

@pytest.mark.asyncio
async def test_other_data_types(client, test_path):
    """Tests handling of non-NumPy data types like str, float, and list."""
    # String
    string_data = "Hello HDF5!"
    await client.write(f"{test_path}/string_dataset", string_data)
    read_string_data = await client.read(f"{test_path}/string_dataset")
    assert read_string_data[0] == string_data

    # Float
    float_data = 3.14159
    await client.write(f"{test_path}/float_dataset", float_data)
    read_float_data = await client.read(f"{test_path}/float_dataset")
    assert read_float_data[0] == float_data

    # List
    list_data = [10, 20, 30, "forty", 50.0]
    await client.write(f"{test_path}/list_dataset", list_data)
    read_list_data = await client.read(f"{test_path}/list_dataset")
    assert np.array_equal(read_list_data, np.array(list_data, dtype=str))

@pytest.mark.asyncio
async def test_nested_groups(client, test_path):
    """Tests creation and access of datasets in nested groups."""
    dataset_path = f"{test_path}/group/path/nested_dataset"
    nested_data = np.array([100, 200])

    await client.create_group(f"{test_path}/group/path")
    await client.write(dataset_path, nested_data)
    read_nested_data = await client.read(dataset_path)
    assert np.array_equal(read_nested_data, nested_data)

@pytest.mark.asyncio
async def test_direct_write(client, test_path):
    """Tests writing to a dataset without explicit group creation."""
    dataset_path = f"{test_path}/direct_dataset"
    direct_data = np.array([99, 88, 77])

    # The server should handle creating the dataset and any parent groups implicitly
    await client.write(dataset_path, direct_data)
    read_direct_data = await client.read(dataset_path)
    assert np.array_equal(read_direct_data, direct_data)

@pytest.mark.asyncio
async def test_numpy_types(client, test_path):
    """Tests various NumPy data types."""
    test_cases = [
        ("int32", np.array([100, 200, 300], dtype=np.int32)),
        ("float64", np.array([1.1, 2.2, 3.3], dtype=np.float64)),
        ("bool", np.array([True, False, True], dtype=np.bool_)),
        ("str", np.array(["apple", "banana", "cherry"])),
        ("int64", np.array([1000, 2000, 3000], dtype=np.int64)),
    ]

    for name, data in test_cases:
        path = f"{test_path}/{name}_dataset"
        await client.write(path, data)
        read_data = await client.read(path)
        assert np.array_equal(read_data, data)
        assert read_data.dtype == data.dtype

@pytest.mark.asyncio
async def test_append_operations(client, test_path):
    """Tests append operations."""
    dataset_path = f"{test_path}/dataset"
    
    initial_data = np.array([1, 2, 3])
    await client.write(dataset_path, initial_data)
    
    data_to_append = np.array([4, 5, 6])
    await client.append(dataset_path, data_to_append)
    
    read_data = await client.read(dataset_path)
    expected_data = np.concatenate((initial_data, data_to_append))
    assert np.array_equal(read_data, expected_data)

@pytest.mark.asyncio
async def test_insert_operations(client, test_path):
    """Tests insert operations."""
    dataset_path = f"{test_path}/dataset"
    
    initial_data = np.array([10, 20, 50, 60])
    await client.write(dataset_path, initial_data)
    
    data_to_insert = np.array([30, 40])
    await client.insert(dataset_path, 2, data_to_insert)
    
    read_data = await client.read(dataset_path)
    expected_data = np.array([10, 20, 30, 40, 50, 60])
    assert np.array_equal(read_data, expected_data)

@pytest.mark.asyncio
async def test_structured_data(client, test_path):
    """Tests handling of structured NumPy arrays."""
    dataset_path = f"{test_path}/structured_dataset"

    structured_dtype = np.dtype([('id', 'i4'), ('value', 'f8'), ('label', 'S10')])
    data_to_write = np.array([(1, 3.14, b'pi'), (2, 2.718, b'e')], dtype=structured_dtype)
    
    await client.write(dataset_path, data_to_write)
    read_data = await client.read(dataset_path)
    assert np.array_equal(read_data, data_to_write)

@pytest.mark.asyncio
async def test_compression(client, test_path):
    """Tests per-path compression settings for all write operations."""
    data = np.arange(1000)

    # Test write with compression
    compressed_path = f"{test_path}/compressed_write"
    await client.write(compressed_path, data, compression='gzip')
    read_compressed_data = await client.read(compressed_path)
    assert np.array_equal(data, read_compressed_data)

    # Test write without compression
    uncompressed_path = f"{test_path}/uncompressed_write"
    await client.write(uncompressed_path, data, compression=None)
    read_uncompressed_data = await client.read(uncompressed_path)
    assert np.array_equal(data, read_uncompressed_data)

    # Test append with compression (on new file)
    append_path = f"{test_path}/compressed_append"
    await client.append(append_path, data, compression='gzip')
    await client.append(append_path, data) # Second append inherits compression
    read_append_data = await client.read(append_path)
    assert np.array_equal(np.concatenate((data, data)), read_append_data)

    # Test insert with compression (on new file)
    insert_path = f"{test_path}/compressed_insert"
    await client.insert(insert_path, 0, data, compression='gzip')
    await client.insert(insert_path, 0, data) # Second insert inherits
    read_insert_data = await client.read(insert_path)
    assert np.array_equal(np.concatenate((data, data)), read_insert_data)

@pytest.mark.asyncio
async def test_large_data(client, test_path):
    """Tests handling of large datasets."""
    dataset_path = f"{test_path}/large_dataset"
    
    large_data = np.random.rand(500, 500)
    await client.write(dataset_path, large_data)
    
    read_data = await client.read(dataset_path)
    assert np.array_equal(large_data, read_data)

@pytest.mark.asyncio
async def test_concurrent_requests(hdf5_server, test_path):
    """Tests handling of multiple concurrent requests."""
    _, host, port = hdf5_server

    async def single_request(path, data):
        client = HDF5Client(host, port)
        await client.connect()
        try:
            await client.write(path, data)
            read_data = await client.read(path)
            assert np.array_equal(data, read_data)
        finally:
            await client.close()

    paths = [f"{test_path}/concurrent_{i}" for i in range(5)]  # Reduced for speed
    data_to_write = [np.random.rand(10) for _ in range(5)]

    tasks = [single_request(path, data) for path, data in zip(paths, data_to_write)]
    await asyncio.gather(*tasks)

@pytest.mark.asyncio
async def test_error_handling(client, test_path):
    """Tests server's response to invalid requests."""
    # Reading a non-existent dataset
    non_existent_path = f"{test_path}/non_existent"
    read_result = await client.read(non_existent_path)
    assert read_result is None

    # Writing to an invalid path (e.g., root)
    with pytest.raises(Exception):
        await client.write('/', np.array([1, 2, 3]))

    # Invalid operation
    invalid_op_result = await client.request({'command': 'invalid_op'})
    assert invalid_op_result['status'] == 'error'
    assert 'Unknown command' in invalid_op_result['message']