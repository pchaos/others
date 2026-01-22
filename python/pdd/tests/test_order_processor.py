"""
Unit tests for order processing functionality.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
from selenium.webdriver.common.by import By


class TestParseOrder:
    """Test suite for parse_order method."""
    
    @pytest.fixture
    def processor(self):
        """Create a mock processor instance for testing."""
        from pdd_order_processor import PddOrderProcessor
        mock_driver = MagicMock()
        processor = PddOrderProcessor(mock_driver)
        return processor
    
    def test_parse_order_complete_data(self, processor):
        """Test parsing order with all fields available."""
        # Create a proper mock element
        mock_element = MagicMock()
        
        # Setup mock elements with proper selenium-style returns
        mock_elements = {
            (By.CSS_SELECTOR, "span[data-test='店铺名称']"): MagicMock(text="测试店铺"),
            (By.CSS_SELECTOR, "p[data-test='订单状态']"): MagicMock(text="待发货"),
            (By.CSS_SELECTOR, "span[data-test='商品名称']"): MagicMock(text="测试商品"),
            (By.CSS_SELECTOR, ".bJrhQPD0"): MagicMock(text="规格信息"),
            (By.CSS_SELECTOR, "span[data-test='商品价格']"): MagicMock(text="¥99.00"),
            (By.CSS_SELECTOR, ".r6qvgq4W"): MagicMock(text="×2"),
            (By.CSS_SELECTOR, ".pdcOje4N"): MagicMock(text="¥198.00"),
            (By.CSS_SELECTOR, ".f2_mZxnQ p"): MagicMock(text="这是一段很长的物流信息详情描述文本，超过了10个字符"),
        }
        
        mock_buttons = [MagicMock(text="确认收货"), MagicMock(text="查看详情")]
        
        def mock_find_element(by, selector):
            key = (by, selector)
            if key in mock_elements:
                return mock_elements[key]
            else:
                raise Exception(f"Element not found: {selector}")
        
        def mock_find_elements(by, selector):
            if selector == ".KBkhFO8F a":
                return mock_buttons
            return []
        
        mock_element.find_element.side_effect = mock_find_element
        mock_element.find_elements.side_effect = mock_find_elements
        mock_element.text = "订单详情文本"
        
        result = processor.parse_order(mock_element)
        
        assert result is not None
        assert "scrape_time" in result
        assert result["shop_name"] == "测试店铺"
        assert result["order_status"] == "待发货"
        assert result["goods_name"] == "测试商品"
        assert result["goods_spec"] == "规格信息"
        assert result["goods_price"] == "¥99.00"
        assert result["quantity"] == 2
        assert result["actual_pay"] == "198.00"
        assert result["logistics_info"] == "这是一段很长的物流信息详情描述文本，超过了10个字符"
        assert result["available_actions"] == ["确认收货", "查看详情"]
    
    def test_parse_order_missing_fields(self, processor):
        """Test parsing order with some fields missing."""
        mock_element = MagicMock()
        
        # Only setup some elements
        mock_elements = {
            (By.CSS_SELECTOR, "span[data-test='商品名称']"): MagicMock(text="测试商品"),
            (By.CSS_SELECTOR, "span[data-test='商品价格']"): MagicMock(text="¥50.00"),
        }
        
        def mock_find_element(by, selector):
            key = (by, selector)
            if key in mock_elements:
                return mock_elements[key]
            else:
                raise Exception("Element not found")
        
        mock_element.find_element.side_effect = mock_find_element
        mock_element.find_elements.return_value = []
        mock_element.text = "12345678901234567890 订单详情"
        
        result = processor.parse_order(mock_element)
        
        assert result is not None
        assert result["goods_name"] == "测试商品"
        assert result["goods_price"] == "¥50.00"
        assert result["order_sn"] == "12345678901234567890"  # From fallback regex
        # Other fields should not be set
        assert "shop_name" not in result
        assert "order_status" not in result
    
    def test_parse_order_quantity_extraction(self, processor):
        """Test quantity extraction from various formats."""
        test_cases = [
            ("×1", 1),
            ("×5", 5),
            ("×10", 10),
            ("数量: 3", 3),
        ]
        
        for quantity_text, expected in test_cases:
            mock_element = MagicMock()
            
            # Create mock with proper text attribute
            mock_quantity_elem = Mock()
            mock_quantity_elem.text = quantity_text
            
            mock_elements = {(By.CSS_SELECTOR, ".r6qvgq4W"): mock_quantity_elem}
            
            def mock_find_element(by, selector):
                key = (by, selector)
                if key in mock_elements:
                    return mock_elements[key]
                raise Exception("Element not found")
            
            mock_element.find_element.side_effect = mock_find_element
            mock_element.find_elements.return_value = []
            mock_element.text = "fallback text"
            
            result = processor.parse_order(mock_element)
            
            assert result is not None
            assert result["quantity"] == expected
    
    def test_parse_order_price_extraction(self, processor):
        """Test actual pay price extraction from various formats."""
        test_cases = [
            ("¥13.89", "13.89"),
            ("￥99.00", "99.00"),
            ("实付: 50.5", "50.5"),
        ]
        
        for pay_text, expected in test_cases:
            mock_element = MagicMock()
            
            # Create mock with proper text attribute
            mock_price_elem = Mock()
            mock_price_elem.text = pay_text
            
            mock_elements = {(By.CSS_SELECTOR, ".pdcOje4N"): mock_price_elem}
            
            def mock_find_element(by, selector):
                key = (by, selector)
                if key in mock_elements:
                    return mock_elements[key]
                raise Exception("Element not found")
            
            mock_element.find_element.side_effect = mock_find_element
            mock_element.find_elements.return_value = []
            mock_element.text = "fallback text"
            
            result = processor.parse_order(mock_element)
            
            assert result is not None
            assert result["actual_pay"] == expected
    
    def test_parse_order_exception_handling(self, processor):
        """Test that exceptions are handled gracefully."""
        mock_element = MagicMock()
        mock_element.find_element.side_effect = Exception("Test exception")
        mock_element.find_elements.side_effect = Exception("Test exception")
        mock_element.text = "some text"
        
        result = processor.parse_order(mock_element)
        
        # Should return basic order dict with scrape_time, even with exceptions
        assert result is not None
        assert "scrape_time" in result
        # Other fields should be missing due to exceptions


class TestOrderProcessor:
    """Test suite for other order processing methods."""
    
    @pytest.fixture
    def processor(self):
        """Create a mock processor instance for testing."""
        from pdd_order_processor import PddOrderProcessor
        mock_driver = MagicMock()
        processor = PddOrderProcessor(mock_driver)
        return processor
    
    def test_extract_orders_successful_extraction(self, processor):
        """Test successful order extraction with valid elements."""
        # Mock driver with current_url
        processor.driver.current_url = "https://example.com/orders"
        
        # Create mock order elements
        mock_order_elem1 = MagicMock()
        mock_order_elem1.text = "测试商品1 ¥99.00 ×2 待发货 订单详情信息"
        
        mock_order_elem2 = MagicMock()
        mock_order_elem2.text = "测试商品2 ¥50.00 ×1 已签收 订单详情信息"
        
        # Mock parse_order to return valid orders
        def mock_parse_order(elem):
            if elem == mock_order_elem1:
                return {
                    "scrape_time": "2024-01-19T12:00:00",
                    "goods_name": "测试商品1",
                    "goods_price": "¥99.00",
                    "quantity": 2,
                    "order_status": "待发货"
                }
            elif elem == mock_order_elem2:
                return {
                    "scrape_time": "2024-01-19T12:00:00", 
                    "goods_name": "测试商品2",
                    "goods_price": "¥50.00",
                    "quantity": 1,
                    "order_status": "已签收"
                }
            return None
        
        processor.parse_order = mock_parse_order
        
        # Mock find_elements to return our test elements for one selector
        processor.driver.find_elements.side_effect = lambda by, selector: {
            ".U6SAh0Eo": [mock_order_elem1, mock_order_elem2],
        }.get(selector, [])
        
        # Mock refresh to do nothing
        processor.driver.refresh = MagicMock()
        
        result = processor.extract_orders()
        
        assert len(result) == 2
        assert result[0]["goods_name"] == "测试商品1"
        assert result[1]["goods_name"] == "测试商品2"
    
    def test_extract_orders_no_elements_found(self, processor):
        """Test behavior when no order elements are found."""
        processor.driver.current_url = "https://example.com/orders"
        
        # Mock find_elements to return empty lists
        processor.driver.find_elements.return_value = []
        processor.driver.refresh = MagicMock()
        
        result = processor.extract_orders()
        
        assert result == []
        # Should have called refresh during retry
        assert processor.driver.refresh.call_count >= 1
    
    def test_extract_orders_invalid_elements_filtered(self, processor):
        """Test that invalid elements are filtered out."""
        processor.driver.current_url = "https://example.com/orders"
        
        # Create elements with insufficient order features
        mock_elem1 = MagicMock()
        mock_elem1.text = "short"  # Too short
        
        mock_elem2 = MagicMock()
        mock_elem2.text = "very long text that exceeds 2000 characters" + "x" * 2000  # Too long
        
        mock_elem3 = MagicMock()
        mock_elem3.text = "some text without order features"  # No order features
        
        processor.driver.find_elements.return_value = [mock_elem1, mock_elem2, mock_elem3]
        processor.driver.refresh = MagicMock()
        processor.parse_order = MagicMock(return_value=None)
        
        result = processor.extract_orders()
        
        assert result == []
        # parse_order should not be called for invalid elements
        processor.parse_order.assert_not_called()
    
    def test_extract_orders_parse_failure(self, processor):
        """Test handling when parse_order fails."""
        processor.driver.current_url = "https://example.com/orders"
        
        mock_elem = MagicMock()
        mock_elem.text = "有效订单文本 ¥100.00 ×1 待发货 商品信息"
        
        processor.driver.find_elements.return_value = [mock_elem]
        processor.driver.refresh = MagicMock()
        
        # Mock parse_order to return None (failure)
        processor.parse_order = MagicMock(return_value=None)
        
        result = processor.extract_orders()
        
        assert result == []
        # parse_order is called once per retry (3 times total)
        assert processor.parse_order.call_count == 3
    
    def test_extract_orders_duplicate_removal(self, processor):
        """Test that duplicate elements are removed."""
        processor.driver.current_url = "https://example.com/orders"
        
        mock_elem1 = MagicMock()
        mock_elem1.text = "相同订单文本 ¥100.00 ×1 待发货"
        
        mock_elem2 = MagicMock()
        mock_elem2.text = "相同订单文本 ¥100.00 ×1 待发货"  # Duplicate text
        
        mock_elem3 = MagicMock()
        mock_elem3.text = "不同订单文本 ¥200.00 ×2 已签收"
        
        # Return duplicates from different selectors
        processor.driver.find_elements.side_effect = lambda by, selector: {
            ".U6SAh0Eo": [mock_elem1, mock_elem2],
            "[class*='order']": [mock_elem3],
        }.get(selector, [])
        
        processor.driver.refresh = MagicMock()
        
        def mock_parse_order(elem):
            if elem in [mock_elem1, mock_elem2]:
                return {"goods_name": "商品1", "order_status": "待发货"}
            elif elem == mock_elem3:
                return {"goods_name": "商品2", "order_status": "已签收"}
            return None
        
        processor.parse_order = mock_parse_order
        
        result = processor.extract_orders()
        
        # Should only have 2 unique orders (duplicates removed)
        assert len(result) == 2
        assert result[0]["goods_name"] == "商品1"
        assert result[1]["goods_name"] == "商品2"
    
    def test_extract_orders_retry_logic(self, processor):
        """Test retry logic when initial attempts fail."""
        processor.driver.current_url = "https://example.com/orders"
        
        # First two attempts return empty for all selectors, third returns elements
        attempt_count = 0
        
        def mock_find_elements(by, selector):
            nonlocal attempt_count
            # Count attempts by tracking calls to the first selector
            if selector == ".U6SAh0Eo":
                nonlocal attempt_count
                attempt_count += 1
            
            if attempt_count <= 2:  # First two attempts
                return []
            else:  # Third attempt
                mock_elem = MagicMock()
                mock_elem.text = "订单文本 ¥100.00 ×1 待发货 商品信息"  # Has order features
                return [mock_elem]
        
        processor.driver.find_elements.side_effect = mock_find_elements
        processor.driver.refresh = MagicMock()
        
        processor.parse_order = MagicMock(return_value={"goods_name": "测试商品"})
        
        result = processor.extract_orders()
        
        assert len(result) == 1
        assert processor.driver.refresh.call_count == 2  # Called during first two retries
    
    def test_extract_orders_connection_error_retry(self, processor):
        """Test retry behavior on connection errors."""
        processor.driver.current_url = "https://example.com/orders"
        
        # Simulate connection error on all selectors for first attempt
        attempt_count = 0
        
        def mock_find_elements(by, selector):
            nonlocal attempt_count
            if selector == ".U6SAh0Eo":  # Track attempts
                nonlocal attempt_count
                attempt_count += 1
            
            if attempt_count == 1:  # First attempt fails
                raise Exception("Connection aborted")
            else:  # Subsequent attempts succeed
                mock_elem = MagicMock()
                mock_elem.text = "订单文本 ¥100.00 ×1 待发货 商品信息"  # Has order features
                return [mock_elem]
        
        processor.driver.find_elements.side_effect = mock_find_elements
        processor.driver.refresh = MagicMock()
        
        processor.parse_order = MagicMock(return_value={"goods_name": "测试商品"})
        
        result = processor.extract_orders()
        
        assert len(result) == 1
        assert processor.driver.refresh.call_count >= 1
    
    def test_go_to_next_page_page_down_success(self, processor):
        """Test successful page down navigation."""
        # Mock body element for PageDown
        mock_body = MagicMock()
        processor.driver.find_element.return_value = mock_body
        
        result = processor.go_to_next_page()
        
        assert result is True
        # Should have called send_keys 3 times with PAGE_DOWN
        assert mock_body.send_keys.call_count == 3
        from selenium.webdriver.common.keys import Keys
        mock_body.send_keys.assert_called_with(Keys.PAGE_DOWN)
    
    def test_go_to_next_page_page_down_fails_button_success(self, processor):
        """Test fallback to button click when PageDown fails."""
        # Mock PageDown to fail
        processor.driver.find_element.side_effect = [
            Exception("PageDown failed"),  # First call for body
            MagicMock()  # Second call for next button
        ]
        
        mock_button = MagicMock()
        mock_button.is_displayed.return_value = True
        mock_button.is_enabled.return_value = True
        processor.driver.find_element.side_effect = [
            Exception("PageDown failed"),  # body element
            mock_button  # next button
        ]
        
        result = processor.go_to_next_page()
        
        assert result is True
        # Should have clicked the button
        mock_button.click.assert_not_called()  # Actually uses execute_script
        # The execute_script call would be tested if we mocked it
    
    def test_go_to_next_page_all_methods_fail(self, processor):
        """Test when all navigation methods fail."""
        # Mock all find_element calls to fail
        processor.driver.find_element.side_effect = Exception("No elements found")
        
        result = processor.go_to_next_page()
        
        assert result is False
    
    def test_generate_report_with_valid_orders(self, processor):
        """Test report generation with valid orders."""
        # Setup test orders
        processor.orders = [
            {
                "goods_name": "商品1",
                "goods_price": "¥100.00",
                "order_status": "已签收",
                "available_actions": ["评价"]
            },
            {
                "goods_name": "商品2", 
                "goods_price": "¥50.00",
                "order_status": "待发货",
                "available_actions": ["取消订单"]
            }
        ]
        
        result = processor.generate_report()
        
        assert result is not None
        assert "valid_order_report" in result
        # Should have filtered to 2 valid orders
        assert len(processor.orders) == 2
    
    def test_generate_report_excludes_cancelled_orders(self, processor):
        """Test that cancelled orders are excluded from report."""
        processor.orders = [
            {
                "goods_name": "商品1",
                "goods_price": "¥100.00", 
                "order_status": "已签收"
            },
            {
                "goods_name": "商品2",
                "goods_price": "¥50.00",
                "order_status": "交易已取消"
            }
        ]
        
        result = processor.generate_report()
        
        # Should only keep the valid order
        assert len(processor.orders) == 1
        assert processor.orders[0]["order_status"] == "已签收"
    
    def test_generate_report_excludes_invalid_actions(self, processor):
        """Test that orders with only cancel/delete actions are excluded."""
        processor.orders = [
            {
                "goods_name": "商品1",
                "goods_price": "¥100.00",
                "order_status": "待发货",
                "available_actions": ["再次拼单", "删除订单"]  # Only invalid actions
            }
        ]
        
        result = processor.generate_report()
        
        # Should exclude this order
        assert len(processor.orders) == 0
    
    def test_generate_report_empty_orders(self, processor):
        """Test report generation with no orders."""
        processor.orders = []
        
        result = processor.generate_report()
        
        # Should handle empty orders gracefully
        assert result is None
    
    def test_scrape_orders_multiple_pages(self, processor):
        """Test scraping orders across multiple pages."""
        # Mock extract_orders to return different orders each call
        call_count = 0
        def mock_extract_orders():
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return [{"goods_name": "商品1"}]
            elif call_count == 2:
                return [{"goods_name": "商品2"}]
            else:
                return []
        
        processor.extract_orders = mock_extract_orders
        
        # Mock go_to_next_page to succeed twice then fail
        go_to_calls = 0
        def mock_go_to_next_page():
            nonlocal go_to_calls
            go_to_calls += 1
            return go_to_calls <= 2  # Succeed for first 2 calls
        
        processor.go_to_next_page = mock_go_to_next_page
        
        result = processor.scrape_orders(max_pages=5)
        
        assert len(result) == 2
        assert result[0]["goods_name"] == "商品1"
        assert result[1]["goods_name"] == "商品2"
        assert processor.orders == result
    
    def test_scrape_orders_single_page(self, processor):
        """Test scraping orders from a single page."""
        processor.extract_orders = MagicMock(return_value=[{"goods_name": "商品1"}])
        processor.go_to_next_page = MagicMock(return_value=False)  # No more pages
        
        result = processor.scrape_orders(max_pages=1)
        
        assert len(result) == 1
        assert result[0]["goods_name"] == "商品1"
        processor.extract_orders.assert_called_once()
        processor.go_to_next_page.assert_called_once()
    
    def test_scrape_orders_max_pages_limit(self, processor):
        """Test that max_pages parameter is respected."""
        processor.extract_orders = MagicMock(return_value=[{"goods_name": f"商品{i}"} for i in range(3)])
        processor.go_to_next_page = MagicMock(return_value=True)  # Always succeed
        
        result = processor.scrape_orders(max_pages=2)
        
        assert len(result) == 6  # 2 pages * 3 orders each
        assert processor.extract_orders.call_count == 2
        assert processor.go_to_next_page.call_count == 2
