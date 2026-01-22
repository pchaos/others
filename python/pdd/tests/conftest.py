"""
Pytest configuration and fixtures for order processing tests.
"""
import pytest
from unittest.mock import Mock, MagicMock
from selenium.webdriver.common.by import By


@pytest.fixture
def mock_driver():
    """Mock selenium webdriver for testing."""
    driver = MagicMock()
    
    # Mock find_elements to return empty list by default
    driver.find_elements.return_value = []
    
    # Mock find_element to return a mock element
    mock_element = MagicMock()
    mock_element.text = "Sample order text"
    mock_element.get_attribute.return_value = "sample-value"
    driver.find_element.return_value = mock_element
    
    return driver


@pytest.fixture
def mock_order_element():
    """Mock order element for testing parse_order."""
    element = MagicMock()
    
    # Mock sub-elements with realistic order data
    mock_shop = MagicMock()
    mock_shop.text = "测试店铺"
    element.find_element.side_effect = lambda selector: {
        By.CSS_SELECTOR + "[data-test='店铺名称']": mock_shop,
        By.CSS_SELECTOR + "p[data-test='订单状态']": MagicMock(text="待发货"),
        By.CSS_SELECTOR + "[data-test='商品名称']": MagicMock(text="测试商品"),
        By.CSS_SELECTOR + ".bJrhQPD0": MagicMock(text="规格信息"),
        By.CSS_SELECTOR + "[data-test='商品价格']": MagicMock(text="¥99.00"),
        By.CSS_SELECTOR + ".r6qvgq4W": MagicMock(text="×2"),
        By.CSS_SELECTOR + ".pdcOje4N": MagicMock(text="¥198.00"),
        By.CSS_SELECTOR + ".f2_mZxnQ p": MagicMock(text="物流信息"),
    }.get(selector, MagicMock(text=""))
    
    return element


@pytest.fixture
def sample_order_data():
    """Sample order data for testing."""
    return {
        "scrape_time": "2024-01-19T12:00:00",
        "shop_name": "测试店铺",
        "order_status": "待发货",
        "goods_name": "测试商品",
        "goods_spec": "规格信息",
        "goods_price": "99.00",
        "quantity": 2,
        "actual_pay": "198.00",
        "logistics_info": "物流信息",
        "available_actions": ["确认收货", "查看详情"]
    }


@pytest.fixture
def sample_orders_list(sample_order_data):
    """List of sample orders for testing."""
    return [
        sample_order_data,
        {
            **sample_order_data,
            "goods_name": "另一个商品",
            "order_status": "已签收"
        }
    ]


@pytest.fixture
def processor(mock_driver):
    """Create a mock processor instance for testing."""
    from pdd_order_processor import PddOrderProcessor
    processor = PddOrderProcessor(mock_driver)
    return processor
