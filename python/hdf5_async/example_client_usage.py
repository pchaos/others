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

    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())
