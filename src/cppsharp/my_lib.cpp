#include "cppsharp/my_lib.hpp"

#include <fmt/core.h>
#include <spdlog/spdlog.h>

void greet(const std::string& name) {
    std::string message = fmt::format("Hello, {}! Welcome to our modern C++ project.", name);
    spdlog::info(message);
}

void setup_logger() {
    spdlog::set_level(spdlog::level::debug);
    spdlog::set_pattern("[%Y-%m-%d %H:%M:%S.%e] [%^%l%$] %v");
}
