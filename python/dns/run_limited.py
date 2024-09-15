# -*- coding=utf-8 -*-
"""限制调用频率
示例代码:
@limit_calls(max_calls=4, period=60)
def my_function():
    print("函数被调用")

# 测试调用
for _ in range(9):
    my_function()
    time.sleep(9)  # 每10秒调用一次
"""

import time

def limit_calls(max_calls, period):
    """
    限制函数在指定时间段内的调用次数。

    Args:
        max_calls (int): 在指定时间段内允许的最大调用次数。
        period (float): 时间段长度，以秒为单位。

    Returns:
        callable: 一个装饰器函数，用于限制被装饰函数的调用次数。
    """
    def decorator(func):
        """
        装饰器函数，用于限制被装饰函数的调用次数。

        Args:
            func (callable): 需要被限制调用次数的函数。

        Returns:
            callable: 一个包装了原始函数的新函数，用于限制调用次数。
        """
        last_called = [0]  # 使用列表以便在内部修改
        call_count = [0]

        def wrapper(*args, **kwargs):
            """
            包装了原始函数的新函数，用于限制调用次数。

            Args:
                *args: 传递给原始函数的位置参数。
                *kwargs: 传递给原始函数的关键字参数。

            Returns:
                Any: 如果调用次数未达到限制，则返回原始函数的返回值；否则，返回None。
            """
            current_time = time.time()
            if current_time - last_called[0] > period:
                last_called[0] = current_time
                call_count[0] = 0
            
            if call_count[0] < max_calls:
                call_count[0] += 1
                return func(*args, **kwargs)
            else:
                print("超过调用次数限制")
                return None

        return wrapper
    return decorator

def limit_calls_with_waiting(max_calls, period):
    """
    限制函数在指定时间段内的调用次数，并在达到限制时等待直到时间段结束。

    Args:
        max_calls (int): 在指定时间段内允许的最大调用次数。
        period (float): 时间段长度，以秒为单位。

    Returns:
        callable: 一个装饰器函数，用于限制被装饰函数的调用次数，并在达到限制时等待。
    """
    def decorator(func):
        """
        装饰器函数，用于限制被装饰函数的调用次数，并在达到限制时等待。

        Args:
            func (callable): 需要被限制调用次数的函数。

        Returns:
            callable: 一个包装了原始函数的新函数，用于限制调用次数，并在达到限制时等待。
        """
        last_called = [0]  # 使用列表以便在内部修改
        call_count = [0]

        def wrapper(*args, **kwargs):
            """
            包装了原始函数的新函数，用于限制调用次数，并在达到限制时等待。

            Args:
                *args: 传递给原始函数的位置参数。
                *kwargs: 传递给原始函数的关键字参数。

            Returns:
                Any: 如果调用次数未达到限制，则返回原始函数的返回值；否则，返回None。
            """
            current_time = time.time()
            if current_time - last_called[0] > period:
                last_called[0] = current_time
                call_count[0] = 0
            
            if call_count[0] < max_calls:
                call_count[0] += 1
                return func(*args, **kwargs)
            else:
                while call_count[0] >= max_calls:
                    time.sleep(1)
                    current_time = time.time()
                    if current_time - last_called[0] > period:
                        last_called[0] = current_time
                        call_count[0] = 0
                return func(*args, **kwargs)

        return wrapper
    return decorator
