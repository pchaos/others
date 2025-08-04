import asyncio
import numpy as np
import pandas as pd
import pytest
from client.client import HDF5Client

# Mark all tests in this file as asyncio
pytestmark = pytest.mark.asyncio

def create_stock_data(num_rows=100, start_date_str='2023-01-01'):
    """Creates a pandas DataFrame with simulated stock data."""
    start_date = pd.to_datetime(start_date_str)
    dates = pd.date_range(start_date, periods=num_rows, freq='D')
    
    data = {
        'timestamp': dates.astype(np.int64),
        'open': np.random.uniform(100, 200, size=num_rows).astype(np.float32),
        'high': np.random.uniform(200, 300, size=num_rows).astype(np.float32),
        'low': np.random.uniform(50, 100, size=num_rows).astype(np.float32),
        'close': np.random.uniform(150, 250, size=num_rows).astype(np.float32),
        'volume': np.random.randint(1_000_000, 10_000_000, size=num_rows).astype(np.int64)
    }
    return pd.DataFrame(data)

def dataframe_to_structured_array(df: pd.DataFrame):
    """Converts a pandas DataFrame to a NumPy structured array."""
    struct_dtype = np.dtype([(col, df[col].dtype) for col in df.columns])
    structured_array = np.empty(len(df), dtype=struct_dtype)
    for col in df.columns:
        structured_array[col] = df[col].values
    return structured_array

async def test_save_and_load_stock_data(client: HDF5Client):
    """
    Tests saving and loading of simulated stock data (as a structured array).
    """
    # 1. Generate sample stock data and convert to structured array
    stock_df = create_stock_data()
    original_data = dataframe_to_structured_array(stock_df)
    dataset_path = "/stocks/AAPL"

    # 2. Save the data to the server
    await client.write(dataset_path, original_data)

    # 3. Read the data back from the server
    retrieved_data = await client.read(dataset_path)

    # 4. Verify the data
    assert retrieved_data is not None, "Failed to retrieve data. read() returned None."
    
    if isinstance(retrieved_data, dict) and b'__ndarray__' in retrieved_data:
        dtype = np.dtype([(name.decode('utf-8'), typ.decode('utf-8')) for name, typ in retrieved_data[b'dtype']])
        retrieved_array = np.array([tuple(row) for row in retrieved_data[b'__ndarray__']], dtype=dtype)
    else:
        retrieved_array = retrieved_data

    assert original_data.dtype == retrieved_array.dtype, (
        f"Data type mismatch.\n"
        f"  Expected: {original_data.dtype}\n"
        f"  Actual:   {retrieved_array.dtype}"
    )
    
    assert np.array_equal(original_data, retrieved_array), (
        f"Data content mismatch.\n"
        f"  Expected: {original_data}\n"
        f"  Actual:   {retrieved_array}"
    )
    print("Stock data saved and loaded successfully.")

async def test_append_stock_data(client: HDF5Client):
    """
    Tests appending new stock data to an existing dataset without deduplication.
    """
    # 1. Create and save initial data
    stock_df_part1 = create_stock_data(num_rows=50)
    original_data_part1 = dataframe_to_structured_array(stock_df_part1)
    dataset_path = "/stocks/TSLA"
    
    await client.write(dataset_path, original_data_part1)

    # 2. Create new data to append
    stock_df_part2 = create_stock_data(num_rows=30, start_date_str='2024-01-01') # Ensure no overlap
    data_to_append = dataframe_to_structured_array(stock_df_part2)

    # 3. Append the new data
    await client.append(dataset_path, data_to_append)

    # 4. Read the full dataset back
    retrieved_data = await client.read(dataset_path)

    # 5. Verify the combined data
    combined_data = np.concatenate((original_data_part1, data_to_append))

    if isinstance(retrieved_data, dict) and b'__ndarray__' in retrieved_data:
        dtype = np.dtype([(name.decode('utf-8'), typ.decode('utf-8')) for name, typ in retrieved_data[b'dtype']])
        retrieved_array = np.array([tuple(row) for row in retrieved_data[b'__ndarray__']], dtype=dtype)
    else:
        retrieved_array = retrieved_data

    assert combined_data.dtype == retrieved_array.dtype, (
        f"Appended data type mismatch.\n"
        f"  Expected: {combined_data.dtype}\n"
        f"  Actual:   {retrieved_array.dtype}"
    )

    assert np.array_equal(combined_data, retrieved_array), (
        f"Appended data content mismatch.\n"
        f"  Expected: {combined_data}\n"
        f"  Actual:   {retrieved_array}"
    )
    print("Stock data appended successfully.")

async def test_append_with_deduplication(client: HDF5Client):
    """
    Tests appending stock data with deduplication based on the 'timestamp' field.
    """
    # 1. Create and save initial data (e.g., 50 days of data)
    initial_df = create_stock_data(num_rows=50, start_date_str='2023-01-01')
    initial_data = dataframe_to_structured_array(initial_df)
    dataset_path = "/stocks/GOOG"
    
    await client.write(dataset_path, initial_data)

    # 2. Create new data that overlaps with the initial data
    # (e.g., 40 new days starting 10 days before the end of the initial data)
    # This creates a 10-day overlap.
    overlap_df = create_stock_data(num_rows=40, start_date_str='2023-02-10')
    data_to_append = dataframe_to_structured_array(overlap_df)

    # 3. Append the new data with deduplication enabled on 'timestamp'
    await client.append(dataset_path, data_to_append, deduplicate_on='timestamp')

    # 4. Read the data back
    retrieved_data = await client.read(dataset_path)

    # 5. Calculate the expected result locally
    combined_df = pd.concat([initial_df, overlap_df]).drop_duplicates(subset=['timestamp'], keep='last')
    combined_df = combined_df.sort_values(by='timestamp').reset_index(drop=True)
    expected_data = dataframe_to_structured_array(combined_df)

    # 6. Verify the result
    if isinstance(retrieved_data, dict) and b'__ndarray__' in retrieved_data:
        dtype = np.dtype([(name.decode('utf-8'), typ.decode('utf-8')) for name, typ in retrieved_data[b'dtype']])
        retrieved_array = np.array([tuple(row) for row in retrieved_data[b'__ndarray__']], dtype=dtype)
    else:
        retrieved_array = retrieved_data
    
    assert len(retrieved_array) == 50 + 40 - 10, "Deduplication did not result in the correct number of rows."
    
    assert expected_data.dtype == retrieved_array.dtype, (
        f"Deduplicated data type mismatch.\n"
        f"  Expected: {expected_data.dtype}\n"
        f"  Actual:   {retrieved_array.dtype}"
    )

    assert np.array_equal(expected_data, retrieved_array), (
        f"Deduplicated data content mismatch.\n"
        f"  Expected: {expected_data}\n"
        f"  Actual:   {retrieved_array}"
    )
    print("Stock data appended with deduplication successfully.")