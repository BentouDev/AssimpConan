conan remote add yage https://api.bintray.com/conan/bentoudev/yage
conan user -p %REPOSITORY_KEY% -r yage bentoudev
conan upload Assimp/0.1@bentoudev/yage --all -r=yage