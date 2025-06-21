#ifndef MY_LIB_HPP
#define MY_LIB_HPP

#include <string>

// 使用我们的依赖库
#include <spdlog/spdlog.h>

void greet(const std::string& name);
void setup_logger();

#endif // MY_LIB_HPP