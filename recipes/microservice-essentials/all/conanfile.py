from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain
from conan.tools.files import get, copy
from conan.tools.build import cross_building, check_min_cppstd
import os

required_conan_version = ">=1.53.0"

class MicroserviceEssentials(ConanFile):
    name = "microservice-essentials"    
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/seboste/microservice-essentials"
    license = "MIT"    
    description = """microservice-essentials is a portable, independent C++ library that takes care of typical recurring concerns that occur in microservice development."""
    topics = ("microservices", "cloud-native", "request-handling")
    settings = "os", "compiler", "arch", "build_type"
    generators = "CMakeDeps", "CMakeToolchain"    
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "build_testing": [True, False],
        "build_examples": [True, False]        
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "build_testing": False,
        "build_examples": False
    }

    def requirements(self):
        if self.options.build_examples:
            self.requires("cpp-httplib/0.12.4")
            self.requires("nlohmann_json/3.11.2")
            self.requires("openssl/3.1.0")
            self.requires("grpc/1.50.1")
        if self.options.build_testing:
            self.requires("catch2/3.3.2")
            self.requires("nlohmann_json/3.11.2")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def build(self):
        cmake = CMake(self)        
        cmake.configure()
        cmake.build()

    def generate(self):
        tc = CMakeToolchain(self)    
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def validate(self):
        if self.settings.compiler.get_safe("cppstd"):
            check_min_cppstd(self, 17)
    
    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def package(self):
        copy(self, "LICENSE", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses"))
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["microservice-essentials"]
        if self.settings.os != "Windows":
            self.cpp_info.system_libs = ["pthread"]

    def test(self):
        if not cross_building(self):
            bin_path = os.path.join("bin", "test_package")
            self.run(bin_path, run_environment=True)
