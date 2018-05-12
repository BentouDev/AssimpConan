#include <iostream>
#include <assimp/DefaultLogger.hpp>

int main()
{
    auto* logger = Assimp::DefaultLogger::create();
    std::cout << (void*)logger << std::endl;
    return 0;
}
