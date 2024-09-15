# -*- coding=utf-8 -*-

import time

import pytest
from run_limited import limit_calls, limit_calls_with_waiting


@limit_calls(max_calls=3, period=5)
def my_test_function():
    return "Called"


@limit_calls_with_waiting(max_calls=3, period=5)
def my_test_function_with_waiting():
    return "Called"


@pytest.mark.run(order=1)  # 添加标记以确保不并行
def test_limit_calls():
    for _ in range(3):
        assert my_test_function() == "Called"

    assert my_test_function() is None  # 超过调用次数限制


@pytest.mark.run(order=2)  # 添加标记以确保不并行
def test_limit_calls_with_waiting():
    decorated_function = limit_calls_with_waiting(max_calls=2, period=5)(my_test_function_with_waiting)

    for _ in range(4):
        assert decorated_function() == "Called"

    start_time = time.time()
    # assert decorated_function() is None  # 超过调用次数限制
    assert decorated_function() == "Called"  # 应该可以再次调用
    time.sleep(5)  # 等待时间段结束
    assert decorated_function() == "Called"  # 应该可以再次调用
