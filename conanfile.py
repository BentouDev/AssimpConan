from conans import ConanFile, CMake, tools

class AssimpConan(ConanFile):
    name = "Assimp"
    version = "0.1"
    license = "MIT"
    homepage = "https://github.com/assimp/assimp"
    url = "https://github.com/BentouDev/AssimpConan"
    description = "Assimp conan package"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "cmake"

    def source(self):
        self.run("git clone https://github.com/assimp/assimp.git")
        # This small hack might be useful to guarantee proper /MT /MD linkage in MSVC
        # if the packaged project doesn't have variables to set it properly
        tools.replace_in_file("%s/CMakeLists.txt" % ("assimp"), "PROJECT( Assimp )", """PROJECT( Assimp )
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()""")

    def build(self):
        cmake = CMake(self)
        cmake.definitions["ASSIMP_BUILD_TESTS"] = "OFF"
        cmake.definitions["ASSIMP_BUILD_SAMPLES"] = "OFF"

        if self.settings.os == "Windows":
            if self.settings.compiler == "gcc":
                cmake.definitions["CONAN_CXX_FLAGS"].join("-Wa,-mbig-obj")
            #elif self.settings.compiler == "Visual Studio":
            #    cmake.definitions["CONAN_CXX_FLAGS"].append("/bigobj")

        cmake.configure(source_folder = "assimp")
        cmake.build()

    def package(self):
        # source code
        self.copy("*.h", dst="include", src="assimp/include")
        self.copy("*.hpp", dst="include", src="assimp/include")
        self.copy("*.inl", dst="include", src="assimp/include")

        # generated config.h file
        self.copy("*.h", dst="include", src="include")
        
        if self.settings.os == "Windows":
            self.copy("*.lib", dst="lib", keep_path=False)
            self.copy("*.dll", dst="bin", keep_path=False)
        else:
            self.copy("*.so", dst="lib", keep_path=False)
            self.copy("*.dylib", dst="lib", keep_path=False)
            self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self, folder="lib");

