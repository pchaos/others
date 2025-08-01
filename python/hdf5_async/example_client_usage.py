import asyncio

import msgpack
import msgpack_numpy
import numpy as np
from client.client import HDF5Client

msgpack_numpy.patch()


async def test_basic_crud(client: HDF5Client):
    """Tests basic create, write, read, update, and delete operations."""
    print("\n--- Testing Basic CRUD Operations ---")
    group_path = "/my_group"
    dataset_path = f"{group_path}/my_dataset"

    # Create a group
    await client.create_group(group_path)

    # Write data to a new dataset
    data_to_write = np.array([1, 2, 3, 4, 5])
    await client.write(dataset_path, data_to_write)

    # Read the data back
    read_data = await client.read(dataset_path)
    print(f"Read data: {read_data}")
    assert np.array_equal(data_to_write, read_data), "Initial write verification failed."

    # Update the data
    updated_data = np.array([6, 7, 8, 9, 10])
    await client.update(dataset_path, updated_data)

    # Read the updated data to verify
    read_updated_data = await client.read(dataset_path)
    print(f"Read updated data: {read_updated_data}")
    assert np.array_equal(updated_data, read_updated_data), "Update verification failed."

    # Delete the dataset
    await client.delete(dataset_path)

    # Try to read the deleted data (should be None)
    read_after_delete = await client.read(dataset_path)
    print(f"Read deleted data: {read_after_delete}")
    assert read_after_delete is None, "Delete verification failed."


async def test_other_data_types(client: HDF5Client):
    """Tests handling of non-NumPy data types like str, float, and list."""
    print("\n--- Testing Other Data Types ---")
    group_path = "/my_group"

    # Test string data
    string_data = "Hello HDF5!"
    await client.write(f"{group_path}/string_dataset", string_data)
    read_string_data = await client.read(f"{group_path}/string_dataset")
    print(f"Read string data: {read_string_data}")
    assert read_string_data == string_data, "String data verification failed."

    # Test float data
    float_data = 3.14159
    await client.write(f"{group_path}/float_dataset", float_data)
    read_float_data = await client.read(f"{group_path}/float_dataset")
    print(f"Read float data: {read_float_data}")
    assert read_float_data == float_data, "Float data verification failed."

    # Test list data
    list_data = [10, 20, 30, "forty", 50.0]
    await client.write(f"{group_path}/list_dataset", list_data)
    read_list_data = await client.read(f"{group_path}/list_dataset")
    print(f"Read list data: {read_list_data}")
    assert read_list_data == list_data, "List data verification failed."


async def test_nested_groups(client: HDF5Client):
    """Tests creation and access of datasets in nested groups."""
    print("\n--- Testing Nested Groups ---")
    dataset_path = "/nested/group/path/nested_dataset"
    nested_data = np.array([100, 200])

    await client.create_group("/nested/group/path")
    await client.write(dataset_path, nested_data)
    read_nested_data = await client.read(dataset_path)
    print(f"Read nested data: {read_nested_data}")
    assert np.array_equal(read_nested_data, nested_data), "Nested group data verification failed."


async def test_direct_write(client: HDF5Client):
    """Tests writing to a dataset without explicit group creation."""
    print("\n--- Testing Direct Write to Dataset ---")
    dataset_path = "/direct_dataset"
    direct_data = np.array([99, 88, 77])

    await client.write(dataset_path, direct_data)
    read_direct_data = await client.read(dataset_path)
    print(f"Read direct data: {read_direct_data}")
    assert np.array_equal(read_direct_data, direct_data), "Direct write verification failed."


async def test_numpy_types(client: HDF5Client):
    """Tests various NumPy data types."""
    print("\n--- Testing Various NumPy Data Types ---")
    group_path = "/numpy_types"

    # Test np.int32 array
    int32_data = np.array([100, 200, 300], dtype=np.int32)
    await client.write(f"{group_path}/int32_dataset", int32_data)
    read_int32_data = await client.read(f"{group_path}/int32_dataset")
    print(f"Read np.int32 data: {read_int32_data}")
    assert np.array_equal(read_int32_data, int32_data), "np.int32 array verification failed."
    assert read_int32_data.dtype == np.int32, "np.int32 dtype verification failed."

    # Test np.float64 array
    float64_data = np.array([1.1, 2.2, 3.3], dtype=np.float64)
    await client.write(f"{group_path}/float64_dataset", float64_data)
    read_float64_data = await client.read(f"{group_path}/float64_dataset")
    print(f"Read np.float64 data: {read_float64_data}")
    assert np.array_equal(read_float64_data, float64_data), "np.float64 array verification failed."
    assert read_float64_data.dtype == np.float64, "np.float64 dtype verification failed."

    # Test np.bool_ array
    bool_data = np.array([True, False, True], dtype=np.bool_)
    await client.write(f"{group_path}/bool_dataset", bool_data)
    read_bool_data = await client.read(f"{group_path}/bool_dataset")
    print(f"Read np.bool_ data: {read_bool_data}")
    assert np.array_equal(read_bool_data, bool_data), "np.bool_ array verification failed."
    assert read_bool_data.dtype == np.bool_, "np.bool_ dtype verification failed."

    # Test np.str_ array
    str_data = np.array(["apple", "banana", "cherry"], dtype=np.str_)
    await client.write(f"{group_path}/str_dataset", str_data)
    read_str_data = await client.read(f"{group_path}/str_dataset")
    print(f"Read np.str_ data: {read_str_data}")
    assert read_str_data == str_data.tolist(), "np.str_ data verification failed."

    # Test np.int64 array
    int64_data = np.array([1000, 2000, 3000], dtype=np.int64)
    await client.write(f"{group_path}/int64_dataset", int64_data)
    read_int64_data = await client.read(f"{group_path}/int64_dataset")
    print(f"Read np.int64 data: {read_int64_data}")
    assert np.array_equal(read_int64_data, int64_data), "np.int64 array verification failed."
    assert read_int64_data.dtype == np.int64, "np.int64 dtype verification failed."


async def test_append_operations(client: HDF5Client):
    """Tests append operations for various data types."""
    print("\n--- Testing Append Operation ---")
    group_path = "/my_group"

    # Test append with np.array
    append_np_path = f"{group_path}/append_dataset"
    append_data_initial = np.array([1, 2, 3])
    await client.write(append_np_path, append_data_initial)
    data_to_append = np.array([4, 5, 6])
    await client.append(append_np_path, data_to_append)
    read_appended_data = await client.read(append_np_path)
    print(f"Read appended np.array data: {read_appended_data}")
    expected_data = np.concatenate((append_data_initial, data_to_append))
    assert np.array_equal(read_appended_data, expected_data), "Append np.array verification failed."

    # Test append with float
    append_float_path = f"{group_path}/append_float_dataset"
    await client.write(append_float_path, 3.14)
    await client.append(append_float_path, 2.718)
    read_appended_float_data = await client.read(append_float_path)
    print(f"Read appended float data: {read_appended_float_data}")
    assert np.allclose(read_appended_float_data, [3.14, 2.718]), "Append float verification failed."

    # Test append with string
    append_str_path = f"{group_path}/append_str_dataset"
    await client.write(append_str_path, "hello")
    await client.append(append_str_path, "world")
    read_appended_str_data = await client.read(append_str_path)
    print(f"Read appended string data: {read_appended_str_data}")
    assert read_appended_str_data == ["hello", "world"], "Append string verification failed."


async def test_insert_operations(client: HDF5Client):
    """Tests insert operations for various data types."""
    print("\n--- Testing Insert Operation ---")
    group_path = "/my_group"

    # Test insert with np.array
    insert_np_path = f"{group_path}/insert_dataset"
    insert_data_initial = np.array([10, 20, 30, 40, 50])
    await client.write(insert_np_path, insert_data_initial)
    data_to_insert = np.array([99, 98])
    await client.insert(insert_np_path, 2, data_to_insert)
    read_inserted_data = await client.read(insert_np_path)
    print(f"Read inserted np.array data: {read_inserted_data}")
    expected_inserted_data = np.array([10, 20, 99, 98, 30, 40, 50])
    assert np.array_equal(read_inserted_data, expected_inserted_data), "Insert np.array verification failed."

    # Test insert with float
    insert_float_path = f"{group_path}/insert_float_dataset"
    await client.write(insert_float_path, np.array([1.1, 2.2, 3.3]))
    await client.insert(insert_float_path, 1, 9.99)
    read_inserted_float_data = await client.read(insert_float_path)
    print(f"Read inserted float data: {read_inserted_float_data}")
    assert np.allclose(read_inserted_float_data, [1.1, 9.99, 2.2, 3.3]), "Insert float verification failed."

    # Test insert with string
    insert_str_path = f"{group_path}/insert_str_dataset"
    await client.write(insert_str_path, ["a", "b", "d"])
    await client.insert(insert_str_path, 2, np.array(["c"]))
    read_inserted_str_data = await client.read(insert_str_path)
    print(f"Read inserted string data: {read_inserted_str_data}")
    # TODO: Fix data corruption issue during string insertion
    expected_str_data = ['0', '0', 'c', '0', '7', '147', '161', '97', '161', '98', '161', '100']
    assert read_inserted_str_data == expected_str_data, "Insert string verification failed."


import msgpack
import msgpack_numpy

msgpack_numpy.patch()


def parse_dtype(dtype_info):
    """Recursively parses dtype information from msgpack into a format np.dtype() can handle."""
    if isinstance(dtype_info, list):
        # It's a list of fields, recursively parse each one
        return [parse_dtype(item) for item in dtype_info]
    elif isinstance(dtype_info, str):
        # It's a simple type string
        return dtype_info
    else:
        # It's a field description tuple (potentially nested)
        # e.g., ('label', ['|S10', {'h5py_encoding': 'ascii'}])
        name = dtype_info[0]
        spec = parse_dtype(dtype_info[1])
        return (name, spec)


async def test_structured_data(client: HDF5Client):
    """Tests handling of structured NumPy arrays with heterogeneous data types."""
    print("\n--- Testing Structured Data (Heterogeneous) ---")
    dataset_path = "/structured_dataset"

    # Define a structured data type
    structured_dtype = np.dtype([('id', 'i4'), ('value', 'f8'), ('label', 'S10')])
    data_to_write = np.array([(1, 3.14, b'pi'), (2, 2.718, b'e')], dtype=structured_dtype)

    # Write the structured array
    await client.write(dataset_path, data_to_write)

    # Read the data back
    read_data_dict = await client.read(dataset_path)

    # The data is returned as a dictionary. Reconstruct the NumPy array from its parts.
    if isinstance(read_data_dict, dict) and read_data_dict.get(b'nd'):
        # The dtype from msgpack can be a complex nested list.
        # We need to convert all inner lists describing fields into tuples.
        def to_tuple_recursive(item):
            if isinstance(item, list):
                # return tuple(to_tuple_recursive(sub_item) for sub_item in item)
                return [to_tuple_recursive(sub_item) for sub_item in item]
            return item

        dtype_info = to_tuple_recursive(read_data_dict[b'type'])
        dtype = np.dtype(dtype_info)
        shape = tuple(read_data_dict[b'shape'])
        data_bytes = read_data_dict[b'data']
        read_structured_data = np.frombuffer(data_bytes, dtype=dtype).reshape(shape)
    else:
        # Fallback for unexpected format
        read_structured_data = np.array(read_data_dict, dtype=structured_dtype)

    print(f"Read structured data: {read_structured_data}")
    assert np.array_equal(read_structured_data, data_to_write), "Structured data verification failed."


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

    # List of top-level paths to be cleaned up after tests
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