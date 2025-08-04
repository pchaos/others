import asyncio
import numpy as np
import pandas as pd
import pytest
from client.client import HDF5Client

# Mark all tests in this file as asyncio
pytestmark = pytest.mark.asyncio

def create_stock_data(num_rows=100, start_date_str='2023-01-01', freq='D'):
    """Creates a pandas DataFrame with simulated stock data."""
    start_date = pd.to_datetime(start_date_str)
    dates = pd.date_range(start_date, periods=num_rows, freq=freq)
    
    data = {
        'timestamp': dates.astype(np.int64),
        'open': np.random.uniform(100, 200, size=num_rows).astype(np.float32),
        'high': np.random.uniform(200, 300, size=num_rows).astype(np.float32),
        'low': np.random.uniform(50, 100, size=num_rows).astype(np.float32),
        'close': np.random.uniform(150, 250, size=num_rows).astype(np.float32),
        'volume': np.random.randint(1_000_000, 10_000_000, size=num_rows).astype(np.int64)
    }
    return pd.DataFrame(data)

def create_stock_minute_data(num_rows=240, start_date_str='2023-01-01 09:30:00'):
    """Creates a pandas DataFrame with simulated minute-level stock data."""
    return create_stock_data(num_rows=num_rows, start_date_str=start_date_str, freq='min')

def dataframe_to_structured_array(df: pd.DataFrame):
    """Converts a pandas DataFrame to a NumPy structured array."""
    struct_dtype = np.dtype([(col, df[col].dtype) for col in df.columns])
    structured_array = np.empty(len(df), dtype=struct_dtype)
    for col in df.columns:
        structured_array[col] = df[col].values
    return structured_array

def reconstruct_array_from_response(retrieved_data):
    """Helper function to reconstruct a NumPy array from a server response."""
    if isinstance(retrieved_data, dict) and b'__ndarray__' in retrieved_data:
        dtype = np.dtype([(name.decode('utf-8'), typ.decode('utf-8')) for name, typ in retrieved_data[b'dtype']])
        return np.array([tuple(row) for row in retrieved_data[b'__ndarray__']], dtype=dtype)
    return retrieved_data

async def test_save_and_load_stock_data(client: HDF5Client):
    """Tests saving and loading of simulated daily stock data."""
    stock_df = create_stock_data()
    original_data = dataframe_to_structured_array(stock_df)
    dataset_path = "/stocks/daily/AAPL"
    await client.write(dataset_path, original_data)
    retrieved_data = await client.read(dataset_path)
    retrieved_array = reconstruct_array_from_response(retrieved_data)
    assert retrieved_array is not None, "Failed to retrieve data."
    assert np.array_equal(original_data, retrieved_array), "Daily data content mismatch."

async def test_append_stock_data(client: HDF5Client):
    """Tests appending new daily stock data without deduplication."""
    stock_df_part1 = create_stock_data(num_rows=50)
    original_data_part1 = dataframe_to_structured_array(stock_df_part1)
    dataset_path = "/stocks/daily/TSLA"
    await client.write(dataset_path, original_data_part1)
    stock_df_part2 = create_stock_data(num_rows=30, start_date_str='2024-01-01')
    data_to_append = dataframe_to_structured_array(stock_df_part2)
    await client.append(dataset_path, data_to_append)
    retrieved_data = await client.read(dataset_path)
    retrieved_array = reconstruct_array_from_response(retrieved_data)
    combined_data = np.concatenate((original_data_part1, data_to_append))
    assert np.array_equal(combined_data, retrieved_array), "Appended daily data content mismatch."

async def test_append_with_deduplication(client: HDF5Client):
    """Tests appending daily stock data with deduplication."""
    initial_df = create_stock_data(num_rows=50, start_date_str='2023-01-01')
    initial_data = dataframe_to_structured_array(initial_df)
    dataset_path = "/stocks/daily/GOOG"
    await client.write(dataset_path, initial_data)
    overlap_df = create_stock_data(num_rows=40, start_date_str='2023-02-10')
    data_to_append = dataframe_to_structured_array(overlap_df)
    await client.append(dataset_path, data_to_append, deduplicate_on='timestamp')
    retrieved_data = await client.read(dataset_path)
    retrieved_array = reconstruct_array_from_response(retrieved_data)
    combined_df = pd.concat([initial_df, overlap_df]).drop_duplicates(subset=['timestamp'], keep='last')
    expected_data = dataframe_to_structured_array(combined_df.sort_values(by='timestamp').reset_index(drop=True))
    assert len(retrieved_array) == 80, "Deduplication did not result in the correct number of rows."
    assert np.array_equal(expected_data, retrieved_array), "Deduplicated daily data content mismatch."

async def test_save_and_load_minute_stock_data(client: HDF5Client):
    """Tests saving and loading of simulated minute-level stock data."""
    stock_df = create_stock_minute_data()
    original_data = dataframe_to_structured_array(stock_df)
    dataset_path = "/stocks/minute/NVDA"
    await client.write(dataset_path, original_data)
    retrieved_data = await client.read(dataset_path)
    retrieved_array = reconstruct_array_from_response(retrieved_data)
    assert retrieved_array is not None, "Failed to retrieve minute data."
    assert np.array_equal(original_data, retrieved_array), "Minute data content mismatch."

async def test_append_minute_data_with_deduplication(client: HDF5Client):
    """Tests appending minute-level stock data with deduplication."""
    initial_df = create_stock_minute_data(num_rows=120, start_date_str='2023-03-01 09:30:00')
    initial_data = dataframe_to_structured_array(initial_df)
    dataset_path = "/stocks/minute/MSFT"
    await client.write(dataset_path, initial_data)
    overlap_df = create_stock_minute_data(num_rows=60, start_date_str='2023-03-01 11:00:00')
    data_to_append = dataframe_to_structured_array(overlap_df)
    await client.append(dataset_path, data_to_append, deduplicate_on='timestamp')
    retrieved_data = await client.read(dataset_path)
    retrieved_array = reconstruct_array_from_response(retrieved_data)
    combined_df = pd.concat([initial_df, overlap_df]).drop_duplicates(subset=['timestamp'], keep='last')
    expected_data = dataframe_to_structured_array(combined_df.sort_values(by='timestamp').reset_index(drop=True))
    assert len(retrieved_array) == 150, "Deduplication on minute data resulted in incorrect row count."
    assert np.array_equal(expected_data, retrieved_array), "Deduplicated minute data content mismatch."

async def test_delete_stock_data(client: HDF5Client):
    """Tests deleting a stock dataset."""
    stock_df = create_stock_data()
    original_data = dataframe_to_structured_array(stock_df)
    dataset_path = "/stocks/daily/to_delete"
    await client.write(dataset_path, original_data)
    # Verify it exists
    assert await client.read(dataset_path) is not None, "Data not written before delete."
    # Delete it
    await client.delete(dataset_path)
    # Verify it's gone
    assert await client.read(dataset_path) is None, "Data not deleted."

async def test_update_stock_data(client: HDF5Client):
    """Tests updating/overwriting a stock dataset."""
    initial_df = create_stock_data(num_rows=10)
    initial_data = dataframe_to_structured_array(initial_df)
    dataset_path = "/stocks/daily/to_update"
    await client.write(dataset_path, initial_data)
    
    # Create new data to overwrite
    update_df = create_stock_data(num_rows=5, start_date_str='2025-01-01')
    update_data = dataframe_to_structured_array(update_df)
    
    await client.update(dataset_path, update_data)
    
    retrieved_data = await client.read(dataset_path)
    retrieved_array = reconstruct_array_from_response(retrieved_data)
    
    assert len(retrieved_array) == 5, "Update did not result in the correct number of rows."
    assert np.array_equal(update_data, retrieved_array), "Updated data content mismatch."

async def test_insert_stock_data(client: HDF5Client):
    """Tests inserting a row into a stock dataset."""
    initial_df = create_stock_data(num_rows=10, start_date_str='2023-01-01')
    initial_data = dataframe_to_structured_array(initial_df)
    dataset_path = "/stocks/daily/to_insert"
    await client.write(dataset_path, initial_data)
    
    # Create a new row to insert at index 5
    insert_df = create_stock_data(num_rows=1, start_date_str='2022-12-31')
    insert_data = dataframe_to_structured_array(insert_df)
    
    await client.insert(dataset_path, 5, insert_data)
    
    retrieved_data = await client.read(dataset_path)
    retrieved_array = reconstruct_array_from_response(retrieved_data)
    
    # Manually construct the expected array
    expected_data = np.insert(initial_data, 5, insert_data)
    
    assert len(retrieved_array) == 11, "Insert did not result in the correct number of rows."
    assert np.array_equal(expected_data, retrieved_array), "Inserted data content mismatch."