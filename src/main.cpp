//
// Created by HoneyBury on 25-6-22.
//
#include <exception>
#include <iostream>

#include "cppsharp/my_lib.hpp"

int main()
{
    try
    {
        // 初始化日志
        setup_logger();

        // 调用我们的库函数
        greet("World");
        return 0;
    }
    catch (const std::exception& ex)
    {
        std::cerr << "Fatal error: " << ex.what() << '\n';
        return 1;
    }
    catch (...)
    {
        std::cerr << "Fatal error: unknown exception\n";
        return 1;
    }
}
