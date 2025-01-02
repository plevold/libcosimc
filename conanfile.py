import os

from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, CMakeDeps, cmake_layout


class LibCosimCConan(ConanFile):
    name = "libcosimc"
    author = "osp"
    exports = "version.txt"
    scm = {
        "type": "git",
        "url": "auto",
        "revision": "auto"
    }
    settings = "os", "compiler", "build_type", "arch"

    def requirements(self):
        self.tool_requires("cmake/[>=3.19]")
        self.requires("libcosim/0.10.4@osp/stable")

    def layout(self):
        cmake_layout(self)

    def generate(self):
        # TODO: Remove?
        # Copy dependencies to the folder where executables (tests, mainly)
        # will be placed, so it's easier to run them.
        # bindir = os.path.join(
        #     self.build_folder,
        #     "output",
        #     str(self.settings.build_type).lower(),
        #     "bin")
        # for dep in self.dependencies.values():
        #     for depdir in dep.cpp_info.bindirs:
        #         copy(self, "*.dll", depdir, bindir, keep_path=False)
        #         copy(self, "*.pdb", depdir, bindir, keep_path=False)
        #         copy(self, "proxyfmu*", depdir, bindir, keep_path=False)

        # Generate CMake toolchain file
        tc = CMakeToolchain(self)
        tc.cache_variables["LIBCOSIMC_USING_CONAN"] = "ON"
        tc.generate()
        CMakeDeps(self).generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        cmake.build(target="doc")

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["cosimc"]
