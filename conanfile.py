from conans import ConanFile, CMake, tools
import os, platform

assimp_version = os.getenv('ASSIMP_VERSION', '0.0')
assimp_commit = os.getenv('ASSIMP_COMMIT', '')

class AssimpConan(ConanFile):
    name = "assimp"
    license = "MIT"
    url = "https://github.com/BentouDev/AssimpConan"
    version = assimp_version
    commit = assimp_commit

    description = "Assimp conan package"
    homepage = "https://github.com/assimp/assimp"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    exports_sources = ["assimp-source/*"]

    options = {"shared": [True, False],"build_type": ["Release", "Debug", "RelWithDebInfo", "MinSizeRel"]}
    default_options = {"build_type":"MinSizeRel", "shared":"True"}

    def build_id(self):
        # Produce different package id for each configuration
        self.info_build.settings.build_type = "Any"
        self.info_build.settings.compiler = "Any"
        self.info_build.settings.arch = "Any"
        self.info_build.settings.os = "Any"

    def fix_linkage(self):
        # This small hack might be useful to guarantee proper /MT /MD linkage in MSVC
        # if the packaged project doesn't have variables to set it properly
        tools.replace_in_file("%s/CMakeLists.txt" % ("assimp-source"), "PROJECT( Assimp )", 

"""PROJECT( Assimp )
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()""")

    def build(self):
        # Workaround for conan choosing cmake embedded in Visual Studio
        if platform.system() == "Windows" and 'AZURE' in os.environ:
            cmake_path = '"C:\\Program Files\\CMake\\bin\\cmake.exe"'
            print (' [DEBUG] Forcing CMake : ' + cmake_path)
            os.environ['CONAN_CMAKE_PROGRAM'] = cmake_path

        cmake = CMake(self)
        cmake.definitions["ASSIMP_BUILD_TESTS"] = "OFF"
        cmake.definitions["ASSIMP_BUILD_SAMPLES"] = "OFF"

        if self.settings.os == "Windows":
            if self.settings.compiler == "gcc":
                cmake.definitions["CONAN_CXX_FLAGS"].join("-Wa,-mbig-obj")
            #elif self.settings.compiler == "Visual Studio":
            #    cmake.definitions["CONAN_CXX_FLAGS"].append("/bigobj")

        cmake.configure(source_folder = "assimp-source")
        cmake.build()

    def package(self):
        # source code
        self.copy("*.h", dst="include", src="assimp-source/include")
        self.copy("*.hpp", dst="include", src="assimp-source/include")
        self.copy("*.inl", dst="include", src="assimp-source/include")

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
        self.cpp_info.libs = tools.collect_libs(self, folder="lib")

