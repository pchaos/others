import asyncio
import numpy as np
from client.client import HDF5Client

def format_assertion_error(msg, expected, actual):
    """Formats a detailed assertion error message."""
    return f"{msg}\n" \
           f"  Expected: {np.array2string(expected, threshold=100) if isinstance(expected, np.ndarray) else expected}\n" \
           f"  Actual:   {np.array2string(actual, threshold=100) if isinstance(actual, np.ndarray) else actual}"

async def test_basic_crud(client: HDF5Client):
    """Tests basic create, write, read, update, and delete operations."""
    print("\n--- Testing Basic CRUD Operations ---")
    group_path = "/my_group"
    dataset_path = f"{group_path}/my_dataset"

    await client.create_group(group_path)

    data_to_write = np.array([1, 2, 3, 4, 5])
    await client.write(dataset_path, data_to_write)

    read_data = await client.read(dataset_path)
    print(f"Read data: {read_data}")
    assert np.array_equal(data_to_write, read_data), format_assertion_error(
        "Initial write verification failed.", data_to_write, read_data
    )

    updated_data = np.array([6, 7, 8, 9, 10])
    await client.update(dataset_path, updated_data)

    read_updated_data = await client.read(dataset_path)
    print(f"Read updated data: {read_updated_data}")
    assert np.array_equal(updated_data, read_updated_data), format_assertion_error(
        "Update verification failed.", updated_data, read_updated_data
    )

    await client.delete(dataset_path)
    read_after_delete = await client.read(dataset_path)
    print(f"Read deleted data: {read_after_delete}")
    assert read_after_delete is None, format_assertion_error(
        "Delete verification failed.", None, read_after_delete
    )

async def test_other_data_types(client: HDF5Client):
    """Tests handling of non-NumPy data types like str, float, and list."""
    print("\n--- Testing Other Data Types ---")
    group_path = "/my_group"

    string_data = "Hello HDF5!"
    string_path = f"{group_path}/string_dataset"
    await client.write(string_path, string_data)
    read_string_data = await client.read(string_path)
    print(f"Read string data: {read_string_data}")
    assert read_string_data[0] == string_data, format_assertion_error(
        "String data verification failed.", string_data, read_string_data[0]
    )

    float_data = 3.14159
    float_path = f"{group_path}/float_dataset"
    await client.write(float_path, float_data)
    read_float_data = await client.read(float_path)
    print(f"Read float data: {read_float_data}")
    assert read_float_data[0] == float_data, format_assertion_error(
        "Float data verification failed.", float_data, read_float_data[0]
    )

    list_data = [10, 20, 30, "forty", 50.0]
    list_path = f"{group_path}/list_dataset"
    await client.write(list_path, list_data)
    read_list_data = await client.read(list_path)
    print(f"Read list data: {read_list_data}")
    assert np.array_equal(read_list_data, np.array(list_data, dtype=str)), format_assertion_error(
        "List data verification failed.", np.array(list_data, dtype=str), read_list_data
    )

async def test_nested_groups(client: HDF5Client):
    """Tests creation and access of datasets in nested groups."""
    print("\n--- Testing Nested Groups ---")
    dataset_path = "/nested/group/path/nested_dataset"
    nested_data = np.array([100, 200])

    await client.create_group("/nested/group/path")
    await client.write(dataset_path, nested_data)
    read_nested_data = await client.read(dataset_path)
    print(f"Read nested data: {read_nested_data}")
    assert np.array_equal(read_nested_data, nested_data), format_assertion_error(
        "Nested group data verification failed.", nested_data, read_nested_data
    )

async def test_direct_write(client: HDF5Client):
    """Tests writing to a dataset without explicit group creation."""
    print("\n--- Testing Direct Write to Dataset ---")
    dataset_path = "/direct_dataset"
    direct_data = np.array([99, 88, 77])

    await client.write(dataset_path, direct_data)
    read_direct_data = await client.read(dataset_path)
    print(f"Read direct data: {read_direct_data}")
    assert np.array_equal(read_direct_data, direct_data), format_assertion_error(
        "Direct write verification failed.", direct_data, read_direct_data
    )

async def test_numpy_types(client: HDF5Client):
    """Tests various NumPy data types."""
    print("\n--- Testing Various NumPy Data Types ---")
    group_path = "/numpy_types"

    int32_data = np.array([100, 200, 300], dtype=np.int32)
    int32_path = f"{group_path}/int32_dataset"
    await client.write(int32_path, int32_data)
    read_int32_data = await client.read(int32_path)
    print(f"Read np.int32 data: {read_int32_data}")
    assert np.array_equal(read_int32_data, int32_data), format_assertion_error(
        "np.int32 array verification failed.", int32_data, read_int32_data
    )
    assert read_int32_data.dtype == np.int32, format_assertion_error(
        "np.int32 dtype verification failed.", np.int32, read_int32_data.dtype
    )

    float64_data = np.array([1.1, 2.2, 3.3], dtype=np.float64)
    float64_path = f"{group_path}/float64_dataset"
    await client.write(float64_path, float64_data)
    read_float64_data = await client.read(float64_path)
    print(f"Read np.float64 data: {read_float64_data}")
    assert np.array_equal(read_float64_data, float64_data), format_assertion_error(
        "np.float64 array verification failed.", float64_data, read_float64_data
    )
    assert read_float64_data.dtype == np.float64, format_assertion_error(
        "np.float64 dtype verification failed.", np.float64, read_float64_data.dtype
    )

    bool_data = np.array([True, False, True], dtype=np.bool_)
    bool_path = f"{group_path}/bool_dataset"
    await client.write(bool_path, bool_data)
    read_bool_data = await client.read(bool_path)
    print(f"Read np.bool_ data: {read_bool_data}")
    assert np.array_equal(read_bool_data, bool_data), format_assertion_error(
        "np.bool_ array verification failed.", bool_data, read_bool_data
    )
    assert read_bool_data.dtype == np.bool_, format_assertion_error(
        "np.bool_ dtype verification failed.", np.bool_, read_bool_data.dtype
    )

    str_data = np.array(["apple", "banana", "cherry"])
    str_path = f"{group_path}/str_dataset"
    await client.write(str_path, str_data)
    read_str_data = await client.read(str_path)
    print(f"Read np.str_ data: {read_str_data}")
    assert np.array_equal(read_str_data, str_data), format_assertion_error(
        "np.str_ data verification failed.", str_data, read_str_data
    )

    int64_data = np.array([1000, 2000, 3000], dtype=np.int64)
    int64_path = f"{group_path}/int64_dataset"
    await client.write(int64_path, int64_data)
    read_int64_data = await client.read(int64_path)
    print(f"Read np.int64 data: {read_int64_data}")
    assert np.array_equal(read_int64_data, int64_data), format_assertion_error(
        "np.int64 array verification failed.", int64_data, read_int64_data
    )
    assert read_int64_data.dtype == np.int64, format_assertion_error(
        "np.int64 dtype verification failed.", np.int64, read_int64_data.dtype
    )

async def test_append_operations(client: HDF5Client):
    """Tests append operations for various data types."""
    print("\n--- Testing Append Operation ---")
    group_path = "/my_group"

    append_np_path = f"{group_path}/append_dataset"
    append_data_initial = np.array([1, 2, 3])
    await client.write(append_np_path, append_data_initial)
    data_to_append = np.array([4, 5, 6])
    await client.append(append_np_path, data_to_append)
    read_appended_data = await client.read(append_np_path)
    expected_data = np.concatenate((append_data_initial, data_to_append))
    print(f"Read appended np.array data: {read_appended_data}")
    assert np.array_equal(read_appended_data, expected_data), format_assertion_error(
        "Append np.array verification failed.", expected_data, read_appended_data
    )

    append_float_path = f"{group_path}/append_float_dataset"
    await client.write(append_float_path, 3.14)
    await client.append(append_float_path, 2.718)
    read_appended_float_data = await client.read(append_float_path)
    expected_float_data = np.array([3.14, 2.718])
    print(f"Read appended float data: {read_appended_float_data}")
    assert np.allclose(read_appended_float_data, expected_float_data), format_assertion_error(
        "Append float verification failed.", expected_float_data, read_appended_float_data
    )

    append_str_path = f"{group_path}/append_str_dataset"
    await client.write(append_str_path, "hello")
    await client.append(append_str_path, "world")
    read_appended_str_data = await client.read(append_str_path)
    expected_str_data = np.array(["hello", "world"])
    print(f"Read appended string data: {read_appended_str_data}")
    assert np.array_equal(read_appended_str_data, expected_str_data), format_assertion_error(
        "Append string verification failed.", expected_str_data, read_appended_str_data
    )

async def test_insert_operations(client: HDF5Client):
    """Tests insert operations for various data types."""
    print("\n--- Testing Insert Operation ---")
    group_path = "/my_group"

    insert_np_path = f"{group_path}/insert_dataset"
    insert_data_initial = np.array([10, 20, 30, 40, 50])
    await client.write(insert_np_path, insert_data_initial)
    data_to_insert = np.array([99, 98])
    await client.insert(insert_np_path, 2, data_to_insert)
    read_inserted_data = await client.read(insert_np_path)
    expected_inserted_data = np.array([10, 20, 99, 98, 30, 40, 50])
    print(f"Read inserted np.array data: {read_inserted_data}")
    assert np.array_equal(read_inserted_data, expected_inserted_data), format_assertion_error(
        "Insert np.array verification failed.", expected_inserted_data, read_inserted_data
    )

    insert_float_path = f"{group_path}/insert_float_dataset"
    await client.write(insert_float_path, np.array([1.1, 2.2, 3.3]))
    await client.insert(insert_float_path, 1, 9.99)
    read_inserted_float_data = await client.read(insert_float_path)
    expected_float_data = np.array([1.1, 9.99, 2.2, 3.3])
    print(f"Read inserted float data: {read_inserted_float_data}")
    assert np.allclose(read_inserted_float_data, expected_float_data), format_assertion_error(
        "Insert float verification failed.", expected_float_data, read_inserted_float_data
    )

    insert_str_path = f"{group_path}/insert_str_dataset"
    await client.write(insert_str_path, ["a", "b", "d"])
    await client.insert(insert_str_path, 2, "c")
    read_inserted_str_data = await client.read(insert_str_path)
    expected_str_data = np.array(['a', 'b', 'c', 'd'])
    print(f"Read inserted string data: {read_inserted_str_data}")
    assert np.array_equal(read_inserted_str_data, expected_str_data), format_assertion_error(
        "Insert string verification failed.", expected_str_data, read_inserted_str_data
    )

async def test_structured_data(client: HDF5Client):
    """Tests handling of structured NumPy arrays with heterogeneous data types."""
    print("\n--- Testing Structured Data (Heterogeneous) ---")
    dataset_path = "/structured_dataset"

    structured_dtype = np.dtype([('id', 'i4'), ('value', 'f8'), ('label', 'S10')])
    data_to_write = np.array([(1, 3.14, b'pi'), (2, 2.718, b'e')], dtype=structured_dtype)
    await client.write(dataset_path, data_to_write)
    read_data = await client.read(dataset_path)
    print(f"Read structured data: {read_data}")
    assert np.array_equal(read_data, data_to_write), format_assertion_error(
        "Structured data verification failed.", data_to_write, read_data
    )

async def cleanup_test_data(client: HDF5Client, paths: list):
    """Deletes all data created during tests."""
    print("\n--- Cleaning up created data ---")
    for path in paths:
        await client.delete(path)

    print("\n--- Verifying cleanup ---")
    all_deleted = True
    for path in paths:
        read_data = await client.read(path)
        if read_data is not None:
            print(f"Error: Path '{path}' was not deleted.")
            all_deleted = False
    assert all_deleted, "Cleanup verification failed. Some paths were not deleted."
    print("Cleanup verification successful.")

async def main():
    """Main function to run all HDF5 client tests."""
    client = HDF5Client()
    await client.connect()

    top_level_paths_to_cleanup = [
        "/my_group",
        "/nested",
        "/numpy_types",
        "/direct_dataset",
        "/structured_dataset",
    ]

    try:
        await test_basic_crud(client)
        await test_other_data_types(client)
        await test_nested_groups(client)
        await test_direct_write(client)
        await test_numpy_types(client)
        await test_append_operations(client)
        await test_insert_operations(client)
        await test_structured_data(client)
    finally:
        await cleanup_test_data(client, top_level_paths_to_cleanup)
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())
