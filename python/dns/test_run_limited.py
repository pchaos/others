# -*- coding=utf-8 -*-

import time

from run_limited import limit_calls, limit_calls_with_waiting


@limit_calls(max_calls=3, period=5)
def my_test_function():
    return "Called"


@limit_calls_with_waiting(max_calls=3, period=5)
def my_test_function_with_waiting():
    return "Called"


# @pytest.mark.run(order=1)  # 添加标记以确保不并行测试
def test_limit_calls():
    """
    测试限制调用次数的函数。

    这个测试函数验证了被装饰的函数在指定时间段内的调用次数限制。
    首先，它调用被装饰的函数三次，验证每次调用都返回预期的结果。
    然后，它再次调用被装饰的函数，验证调用次数超过限制后返回None。
    """
    for _ in range(3):
        assert my_test_function() == "Called"

    assert my_test_function() is None  # 超过调用次数限制

# @pytest.mark.run(order=2)  # 添加标记以确保不并行测试
def test_limit_calls_with_waiting():
    """
    测试带等待的限制调用次数的函数。

    这个测试函数验证了被装饰的函数在指定时间段内的调用次数限制，并且在时间段结束后是否可以再次调用。
    首先，它调用被装饰的函数四次，验证每次调用都返回预期的结果，尽管调用次数超过限制。
    然后，它等待时间段结束，并验证在时间段结束后是否可以再次调用被装饰的函数。
    """
    decorated_function = limit_calls_with_waiting(max_calls=2, period=5)(my_test_function_with_waiting)

    for _ in range(4):
        assert decorated_function() == "Called"

    start_time = time.time()
    # assert decorated_function() is None  # 超过调用次数限制
    assert decorated_function() == "Called"  # 应该可以再次调用
    time.sleep(5)  # 等待时间段结束
    assert decorated_function() == "Called"  # 应该可以再次调用