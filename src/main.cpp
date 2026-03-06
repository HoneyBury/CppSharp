#include <exception>
#include <iostream>

#include "cppsharp/my_lib.hpp"

int main() {
    try {
        setup_logger();
        greet("World");
        return 0;
    } catch (const std::exception& ex) {
        std::cerr << "Fatal error: " << ex.what() << '\n';
        return 1;
    } catch (...) {
        std::cerr << "Fatal error: unknown exception\n";
        return 1;
    }
}
