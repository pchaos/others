import asyncio
from client.client import HDF5Client

async def main():
    client = HDF5Client()
    await client.connect()

    try:
        # Create a group
        await client.create_group("/my_group")

        # Write data to a new dataset
        data_to_write = [1, 2, 3, 4, 5]
        await client.write("/my_group/my_dataset", data_to_write)

        # Read the data back
        response = await client.read("/my_group/my_dataset")
        read_data = response.get("data")
        print(f"Read data: {read_data}")

    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())
