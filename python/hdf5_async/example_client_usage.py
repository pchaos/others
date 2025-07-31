import asyncio

import numpy as np
from client.client import HDF5Client


async def main():
    client = HDF5Client()
    await client.connect()

    try:
        # Create a group
        await client.create_group("/my_group")

        # Write data to a new dataset
        data_to_write = np.array([1, 2, 3, 4, 5])
        await client.write("/my_group/my_dataset", data_to_write)

        # Read the data back
        response = await client.read("/my_group/my_dataset")
        read_data = response.get("data")
        print(f"Read data: {read_data}")
        assert np.array_equal(data_to_write, read_data), f"Initial write verification failed. Expected: {data_to_write}, Got: {read_data}"

        # Update the data
        updated_data = np.array([6, 7, 8, 9, 10])
        await client.update("/my_group/my_dataset", updated_data)

        # Read the updated data to verify
        response = await client.read("/my_group/my_dataset")
        read_updated_data = response.get("data")
        print(f"Read updated data: {read_updated_data}")
        assert np.array_equal(updated_data, read_updated_data), f"Update verification failed. Expected: {updated_data}, Got: {read_updated_data}"

        # Delete the dataset
        await client.delete("/my_group/my_dataset")

        # Try to read the deleted data (should fail)
        response = await client.read("/my_group/my_dataset")
        read_after_delete = response.get("data")
        print(f"Read deleted data: {read_after_delete}")
        assert read_after_delete is None, f"Delete verification failed. Expected None, but got: {read_after_delete}"

        print("\n--- Testing other data types ---")

        # Test string data
        string_data = "Hello HDF5!"
        await client.write("/my_group/string_dataset", string_data)
        response = await client.read("/my_group/string_dataset")
        read_string_data = response.get("data")
        print(f"Read string data: {read_string_data}")
        assert read_string_data == string_data, f"String data verification failed. Expected: '{string_data}', Got: '{read_string_data}'"

        # Test float data
        float_data = 3.14159
        await client.write("/my_group/float_dataset", float_data)
        response = await client.read("/my_group/float_dataset")
        read_float_data = response.get("data")
        print(f"Read float data: {read_float_data}")
        assert read_float_data == float_data, f"Float data verification failed. Expected: {float_data}, Got: {read_float_data}"

        # Test list data
        list_data = [10, 20, 30, "forty", 50.0]
        await client.write("/my_group/list_dataset", list_data)
        response = await client.read("/my_group/list_dataset")
        read_list_data = response.get("data")
        print(f"Read list data: {read_list_data}")
        assert read_list_data == list_data, f"List data verification failed. Expected: {list_data}, Got: {read_list_data}"

        print("\n--- Testing nested groups ---")
        await client.create_group("/nested/group/path")
        nested_data = np.array([100, 200])
        await client.write("/nested/group/path/nested_dataset", nested_data)
        response = await client.read("/nested/group/path/nested_dataset")
        read_nested_data = response.get("data")
        print(f"Read nested data: {read_nested_data}")
        assert np.array_equal(read_nested_data, nested_data), f"Nested group data verification failed. Expected: {nested_data}, Got: {read_nested_data}"

        print("\n--- Testing direct write to dataset (without explicit group creation) ---")
        direct_data = np.array([99, 88, 77])
        await client.write("/direct_dataset", direct_data)
        response = await client.read("/direct_dataset")
        read_direct_data = response.get("data")
        print(f"Read direct data: {read_direct_data}")
        assert np.array_equal(read_direct_data, direct_data), f"Direct write verification failed. Expected: {direct_data}, Got: {read_direct_data}"

        print("\n--- Testing various NumPy data types ---")

        # Test np.int32 array
        int32_data = np.array([100, 200, 300], dtype=np.int32)
        await client.write("/numpy_types/int32_dataset", int32_data)
        response = await client.read("/numpy_types/int32_dataset")
        read_int32_data = response.get("data")
        print(f"Read np.int32 data: {read_int32_data}")
        assert np.array_equal(read_int32_data, int32_data), f"np.int32 array verification failed. Expected: {int32_data}, Got: {read_int32_data}"
        assert read_int32_data.dtype == np.int32, f"np.int32 dtype verification failed. Expected: {np.int32}, Got: {read_int32_data.dtype}"

        # Test np.float64 array
        float64_data = np.array([1.1, 2.2, 3.3], dtype=np.float64)
        await client.write("/numpy_types/float64_dataset", float64_data)
        response = await client.read("/numpy_types/float64_dataset")
        read_float64_data = response.get("data")
        print(f"Read np.float64 data: {read_float64_data}")
        assert np.array_equal(read_float64_data, float64_data), f"np.float64 array verification failed. Expected: {float64_data}, Got: {read_float64_data}"
        assert read_float64_data.dtype == np.float64, f"np.float64 dtype verification failed. Expected: {np.float64}, Got: {read_float64_data.dtype}"

        # Test np.bool_ array
        bool_data = np.array([True, False, True], dtype=np.bool_)
        await client.write("/numpy_types/bool_dataset", bool_data)
        response = await client.read("/numpy_types/bool_dataset")
        read_bool_data = response.get("data")
        print(f"Read np.bool_ data: {read_bool_data}")
        assert np.array_equal(read_bool_data, bool_data), f"np.bool_ array verification failed. Expected: {bool_data}, Got: {read_bool_data}"
        assert read_bool_data.dtype == np.bool_, f"np.bool_ dtype verification failed. Expected: {np.bool_}, Got: {read_bool_data.dtype}"

        # Test np.str_ array
        str_data = np.array(["apple", "banana", "cherry"], dtype=np.str_)
        await client.write("/numpy_types/str_dataset", str_data)
        response = await client.read("/numpy_types/str_dataset")
        read_str_data = response.get("data")
        print(f"Read np.str_ data: {read_str_data}")
        assert isinstance(read_str_data, list), f"np.str_ type verification failed. Expected: list, Got: {type(read_str_data)}"
        assert read_str_data == str_data.tolist(), f"np.str_ data verification failed. Expected: {str_data.tolist()}, Got: {read_str_data}"

        print("\n--- Testing append operation ---")
        append_data_initial = np.array([1, 2, 3])
        await client.write("/my_group/append_dataset", append_data_initial)
        response = await client.read("/my_group/append_dataset")
        read_append_data = response.get("data")
        print(f"Read initial append data: {read_append_data}")
        assert np.array_equal(read_append_data, append_data_initial), f"Initial append data verification failed. Expected: {append_data_initial}, Got: {read_append_data}"

        # Append new data
        data_to_append = np.array([4, 5, 6])
        await client.append("/my_group/append_dataset", data_to_append)
        response = await client.read("/my_group/append_dataset")
        read_appended_data = response.get("data")
        print(f"Read appended data: {read_appended_data}")
        expected_data = np.concatenate((append_data_initial, data_to_append))
        assert np.array_equal(read_appended_data, expected_data), f"Append operation verification failed. Expected: {expected_data}, Got: {read_appended_data}"

        print("\n--- Testing insert operation ---")
        insert_data_initial = np.array([10, 20, 30, 40, 50])
        await client.write("/my_group/insert_dataset", insert_data_initial)
        data_to_insert = np.array([99, 98])
        await client.insert("/my_group/insert_dataset", 2, data_to_insert)
        response = await client.read("/my_group/insert_dataset")
        read_inserted_data = response.get("data")
        print(f"Read inserted data: {read_inserted_data}")
        expected_inserted_data = np.array([10, 20, 99, 98, 30, 40, 50])
        assert np.array_equal(read_inserted_data, expected_inserted_data), f"Insert operation verification failed. Expected: {expected_inserted_data}, Got: {read_inserted_data}"


        # Clean up
        print("\n--- Cleaning up created data ---")
        await client.delete("/my_group/string_dataset")
        await client.delete("/my_group/float_dataset")
        await client.delete("/my_group/list_dataset")
        await client.delete("/my_group/append_dataset")
        await client.delete("/my_group/insert_dataset")
        await client.delete("/nested/group/path/nested_dataset")
        await client.delete("/direct_dataset")
        await client.delete("/numpy_types/int32_dataset")
        await client.delete("/numpy_types/float64_dataset")
        await client.delete("/numpy_types/bool_dataset")
        await client.delete("/numpy_types/str_dataset")
        await client.delete("/my_group")  # Delete the group itself
        await client.delete("/nested")  # Delete the top-level nested group
        await client.delete("/numpy_types")  # Delete the numpy types group

        # Verify cleanup
        print("\n--- Verifying cleanup ---")
        paths_to_check = [
            "/my_group",
            "/nested",
            "/numpy_types",
            "/direct_dataset",
            "/my_group/my_dataset",  # Was deleted earlier
            "/my_group/string_dataset", # Was in a group that is now deleted
        ]
        all_deleted = True
        for path in paths_to_check:
            response = await client.read(path)
            if response.get("data") is not None:
                print(f"Error: Path {path} was not deleted.")
                all_deleted = False
        assert all_deleted, "Cleanup verification failed. Some paths were not deleted."
        print("Cleanup verification successful.")

    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())