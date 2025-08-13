import matplotlib.pyplot as plt
import numpy as np

def kalman_filter_with_momentum(prices, q_price_noise=0.05, q_velocity_noise=0.1, r_measurement_noise=10.0):
    """
    使用包含动量（速度）的卡尔曼滤波器来平滑价格数据。
    这个模型假设价格的变化不仅是随机的，还包含一个速度分量，即价格变化的趋势。

    参数:
    - prices (np.array or list): 观测到的价格序列，例如每日收盘价。
    - q_price_noise (float): 过程噪声中价格分量的方差。这代表了模型对价格随机波动的假设。
    - q_velocity_noise (float): 过程噪声中速度分量的方差。这代表了模型对速度（趋势）随机变化的假设。
    - r_measurement_noise (float): 测量噪声的方差。这代表了观测值（如收盘价）与其背后真实价格之间差异的期望大小。

    返回:
    - np.array: 经过卡尔曼滤波平滑后的价格估计序列。
    """
    # --- 1. 定义卡尔曼滤波器的核心矩阵 ---

    # 状态向量 x 定义为 [price, velocity]，即 [价格, 价格变化速度]
    # 这是一个二阶模型，因为它同时考虑了位置（价格）和速度。

    # 状态转移矩阵 F:
    # 描述了状态如何从一个时间步演变到下一个时间步（没有噪声的情况下）。
    # new_price = 1 * old_price + 1 * old_velocity
    # new_velocity = 0 * old_price + 1 * old_velocity
    # 这个矩阵假设价格以当前速度呈线性变化。
    F = np.array([[1, 1], [0, 1]])

    # 观测矩阵 H:
    # 描述了如何从状态向量中获得观测值。
    # observed_price = 1 * price + 0 * velocity
    # 我们只能直接观测到价格，而无法直接观测到速度。
    H = np.array([[1, 0]])

    # 过程噪声协方差矩阵 Q:
    # 描述了状态转移模型的不确定性（噪声）。
    # 它假设价格和速度的噪声是独立的（非对角线元素为0）。
    # q_price_noise: 价格本身的随机波动。
    # q_velocity_noise: 速度（趋势）的随机波动。
    Q = np.array([[q_price_noise, 0], [0, q_velocity_noise]])

    # 测量噪声协方差矩阵 R:
    # 描述了测量过程中的不确定性。
    # r_measurement_noise: 观测值的噪声方差。值越大，说明我们越不信任观测值。
    R = np.array([[r_measurement_noise]])

    # --- 2. 初始化状态和协方差 ---

    # 初始状态 x:
    # - 初始价格：使用观测序列的第一个值。
    # - 初始速度：假设为0，因为我们没有先验信息。
    initial_price = prices[0]
    x = np.array([[initial_price], [0.0]])

    # 初始误差协方差矩阵 P:
    # 表示我们对初始状态估计的不确定性。
    # 使用一个对角矩阵，并设置较大的值（例如100），表示我们对初始状态的估计非常不确定。
    # 滤波器会随着时间的推移迅速收敛。
    P = np.eye(2) * 100

    # 用于存储每个时间步滤波后的价格估计
    kalman_predictions = []

    # --- 3. 循环执行滤波过程 ---
    for price in prices:
        # --- 预测步骤 (Prediction) ---
        # 基于上一时刻的状态，预测当前时刻的状态和误差协方差。

        # 预测状态：x_pred = F * x_last
        x_pred = F @ x
        # 预测误差协方差：P_pred = F * P_last * F^T + Q
        P_pred = F @ P @ F.T + Q

        # --- 更新步骤 (Update) ---
        # 基于当前时刻的观测值，修正预测的状态。

        # 测量值
        measurement = np.array([[price]])
        # 测量残差 y: 实际观测值与预测观测值之差
        y = measurement - H @ x_pred
        # 残差的协方差 S: H * P_pred * H^T + R
        S = H @ P_pred @ H.T + R
        # 卡尔曼增益 K: P_pred * H^T * S^-1
        # K 决定了我们应该在多大程度上相信测量残差。
        # K 值大，说明我们更相信观测值；K 值小，说明我们更相信模型的预测。
        K = P_pred @ H.T @ np.linalg.inv(S)
        # 更新状态估计: x_new = x_pred + K * y
        x = x_pred + K @ y
        # 更新误差协方差: P_new = (I - K * H) * P_pred
        P = (np.eye(F.shape[0]) - K @ H) @ P_pred

        # 存储当前时刻滤波后的价格部分
        kalman_predictions.append(x[0, 0])

    return np.array(kalman_predictions)


def kalman_filter_with_acceleration(prices, q_price_noise=0.05, q_velocity_noise=0.1, q_acceleration_noise=0.1, r_measurement_noise=10.0):
    """
    使用包含加速度的卡尔曼滤波器来平滑价格数据。
    这是一个三阶模型，假设价格运动包含位置、速度和加速度。

    参数:
    - prices (np.array or list): 观测到的价格序列。
    - q_price_noise (float): 过程噪声中价格分量的方差。
    - q_velocity_noise (float): 过程噪声中速度分量的方差。
    - q_acceleration_noise (float): 过程噪声中加速度分量的方差。
    - r_measurement_noise (float): 测量噪声的方差。

    返回:
    - tuple(np.array, np.array, np.array): (滤波后的价格, 速度, 加速度)序列。
    """
    # --- 1. 定义三阶卡尔曼滤波器的核心矩阵 ---

    # 状态向量 x 定义为 [price, velocity, acceleration]
    # 状态转移矩阵 F:
    # new_price = 1*p + 1*v + 0.5*a
    # new_velocity = 0*p + 1*v + 1*a
    # new_acceleration = 0*p + 0*v + 1*a
    F = np.array([[1, 1, 0.5], [0, 1, 1], [0, 0, 1]])

    # 观测矩阵 H: 我们只能观测到价格
    # observed_price = 1*p + 0*v + 0*a
    H = np.array([[1, 0, 0]])

    # 过程噪声协方差 Q:
    Q = np.diag([q_price_noise, q_velocity_noise, q_acceleration_noise])**2

    # 测量噪声协方差 R:
    R = np.array([[r_measurement_noise]])

    # --- 2. 初始化状态和协方差 ---
    initial_price = prices[0]
    # 初始状态 [price, velocity, acceleration]
    x = np.array([[initial_price], [0.0], [0.0]])
    # 初始误差协方差
    P = np.eye(3) * 100

    # 存储结果
    kalman_prices = []
    kalman_velocities = []
    kalman_accelerations = []

    # --- 3. 循环执行滤波过程 ---
    for price in prices:
        # 预测
        x_pred = F @ x
        P_pred = F @ P @ F.T + Q

        # 更新
        measurement = np.array([[price]])
        y = measurement - H @ x_pred
        S = H @ P_pred @ H.T + R
        K = P_pred @ H.T @ np.linalg.inv(S)
        x = x_pred + K @ y
        P = (np.eye(F.shape[0]) - K @ H) @ P_pred

        # 存储结果
        kalman_prices.append(x[0, 0])
        kalman_velocities.append(x[1, 0])
        kalman_accelerations.append(x[2, 0])

    return np.array(kalman_prices), np.array(kalman_velocities), np.array(kalman_accelerations)


# --- 主执行部分 ---
if __name__ == "__main__":
    # --- 1. 模拟生成更真实的股票数据 ---
    np.random.seed(42)
    num_days = 252 # 模拟一年的交易日
    initial_price = 100.0
    
    # 创建时间轴
    t = np.arange(num_days)
    
    # a. 长期趋势 (一个缓慢的年度周期)
    long_term_period = num_days
    long_term_amplitude = 20
    long_term_trend = long_term_amplitude * np.sin(2 * np.pi * t / long_term_period)
    
    # b. 短期波动 (多个较快的月度周期)
    short_term_period = 30 # 大约一个月的周期
    short_term_amplitude = 5
    short_term_waves = short_term_amplitude * np.sin(2 * np.pi * t / short_term_period)
    
    # c. 整体向上漂移
    drift = 0.1 * t
    
    # d. 组合成“真实”价格
    true_price = initial_price + long_term_trend + short_term_waves + drift
    
    # e. 增加测量噪声，得到我们能“观测”到的价格
    measurement_noise_std = 2.5 # 测量噪声的标准差
    observed_price = true_price + np.random.normal(0, measurement_noise_std, num_days)


    # --- 2. 调用两个不同的卡尔曼滤波函数 ---
    
    # 调用原始的二阶模型（仅速度）
    # 注意：这里的噪声参数是需要我们为滤波器“猜测”的，它们不一定等于模拟时使用的噪声
    filtered_prices_mom = kalman_filter_with_momentum(
        observed_price,
        q_price_noise=0.1,      # 调高一点，因为价格波动更复杂
        q_velocity_noise=0.2,   # 调高一点
        r_measurement_noise=measurement_noise_std**2 # 假设我们知道测量设备的精度
    )

    # 调用新增的三阶模型（含加速度）
    filtered_prices_acc, filtered_vel, filtered_acc = kalman_filter_with_acceleration(
        observed_price,
        q_price_noise=0.1,
        q_velocity_noise=0.2,
        q_acceleration_noise=0.5, # 加速度的噪声，需要调整
        r_measurement_noise=measurement_noise_std**2
    )

    # --- 3. 将所有结果合并到一个图中进行可视化 ---
    # 设置matplotlib以正确显示中文字符
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    
    # 创建一个包含3个子图的图表
    fig, axs = plt.subplots(3, 1, figsize=(14, 12), sharex=True, gridspec_kw={'height_ratios': [3, 1, 1]})
    
    # --- 子图1: 价格对比 ---
    axs[0].plot(true_price, 'g-', linewidth=2, label='“真实”价格 (无法观测)')
    axs[0].plot(observed_price, 'bo', markersize=3, alpha=0.5, label='每日收盘价 (观测值)')
    axs[0].plot(filtered_prices_mom, 'r-', linewidth=2, label='卡尔曼滤波 (速度模型)')
    axs[0].plot(filtered_prices_acc, 'm--', linewidth=2.5, label='卡尔曼滤波 (加速度模型)')
    axs[0].set_title('卡尔曼滤波在模拟波动价格上的应用')
    axs[0].set_ylabel('价格')
    axs[0].legend()
    axs[0].grid(True)
    
    # --- 子图2: 估计的速度 ---
    axs[1].plot(filtered_vel, 'c-', label='估计的速度 (来自加速度模型)')
    axs[1].axhline(0, color='gray', linestyle='--')
    axs[1].set_ylabel('速度')
    axs[1].legend()
    axs[1].grid(True)
    
    # --- 子图3: 估计的加速度 ---
    axs[2].plot(filtered_acc, 'orange', label='估计的加速度 (来自加速度模型)')
    axs[2].axhline(0, color='gray', linestyle='--')
    axs[2].set_xlabel('天数')
    axs[2].set_ylabel('加速度')
    axs[2].legend()
    axs[2].grid(True)
    
    plt.tight_layout()
    plt.show()
