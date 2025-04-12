#pragma once
#ifndef HIKYUU_CONFIG_H_
#define HIKYUU_CONFIG_H_

// clang-format off

// support serialization
#define HKU_SUPPORT_SERIALIZATION  1

#if HKU_SUPPORT_SERIALIZATION
#define HKU_SUPPORT_TEXT_ARCHIVE   0
#define HKU_SUPPORT_XML_ARCHIVE    1  //must 1 for python
#define HKU_SUPPORT_BINARY_ARCHIVE 1  //must 1 for python
#endif /* HKU_SUPPORT_SERIALIZATION*/

// 检查下标越界
#define CHECK_ACCESS_BOUND 1

// 默认激活的日志级别
#define LOG_ACTIVE_LEVEL 2

// 是否使用 spdlog
#define USE_SPDLOG_LOGGER 1

// 使用异步 logger
#define HKU_USE_SPDLOG_ASYNC_LOGGER 0

// spdlog默认日志级别
#define SPDLOG_ACTIVE_LEVEL 2

// 关闭 HKU_ASSERT
#define HKU_DISABLE_ASSERT 0

// clang-format on

#endif /* HIKYUU_CONFIG_H_ */