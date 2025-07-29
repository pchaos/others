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

        # Update the data
        updated_data = np.array([6, 7, 8, 9, 10])
        await client.update("/my_group/my_dataset", updated_data)

        # Read the updated data
        response = await client.read("/my_group/my_dataset")
        read_data = response.get("data")
        print(f"Read updated data: {read_data}")

        # Delete the dataset
        await client.delete("/my_group/my_dataset")

        # Try to read the deleted data
        response = await client.read("/my_group/my_dataset")
        read_data = response.get("data")
        print(f"Read deleted data: {read_data}")

        print("\n--- Testing other data types ---")

        # Test string data
        string_data = "Hello HDF5!"
        await client.write("/my_group/string_dataset", string_data)
        response = await client.read("/my_group/string_dataset")
        read_string_data = response.get("data")
        print(f"Read string data: {read_string_data}")
        assert read_string_data == string_data

        # Test float data
        float_data = 3.14159
        await client.write("/my_group/float_dataset", float_data)
        response = await client.read("/my_group/float_dataset")
        read_float_data = response.get("data")
        print(f"Read float data: {read_float_data}")
        assert read_float_data == float_data

        # Test list data
        list_data = [10, 20, 30, "forty", 50.0]
        await client.write("/my_group/list_dataset", list_data)
        response = await client.read("/my_group/list_dataset")
        read_list_data = response.get("data")
        print(f"Read list data: {read_list_data}")
        assert read_list_data == list_data

        print("\n--- Testing nested groups ---")
        await client.create_group("/nested/group/path")
        nested_data = np.array([100, 200])
        await client.write("/nested/group/path/nested_dataset", nested_data)
        response = await client.read("/nested/group/path/nested_dataset")
        read_nested_data = response.get("data")
        print(f"Read nested data: {read_nested_data}")
        assert np.array_equal(read_nested_data, nested_data)

        print("\n--- Testing direct write to dataset (without explicit group creation) ---")
        direct_data = np.array([99, 88, 77])
        await client.write("/direct_dataset", direct_data)
        response = await client.read("/direct_dataset")
        read_direct_data = response.get("data")
        print(f"Read direct data: {read_direct_data}")
        assert np.array_equal(read_direct_data, direct_data)

        # Clean up
        await client.delete("/my_group/string_dataset")
        await client.delete("/my_group/float_dataset")
        await client.delete("/my_group/list_dataset")
        await client.delete("/nested/group/path/nested_dataset")
        await client.delete("/direct_dataset")
        await client.delete("/my_group") # Delete the group itself
        await client.delete("/nested") # Delete the top-level nested group

    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())
