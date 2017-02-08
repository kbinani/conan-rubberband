from conans import ConanFile, CMake, tools


class RubberbandConan(ConanFile):
    name = "rubberband"
    version = "master"
    license = "GPL-2.0"
    url = "https://github.com/kbinani/conan-rubberband"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generator = "cmake"
    exports = "CMakeLists.txt"

    def source(self):
        self.run("git init")
        self.run("git remote add origin https://github.com/breakfastquay/rubberband.git")
        self.run("git fetch origin")
        self.run("git fetch origin --tags")
        self.run("git checkout %s" % self.version)

    def build(self):
        static = "-DBUILD_SHARED_LIBS=ON" if self.options.shared else ""
        cmake = CMake(self.settings)
        self.run("cmake . %s %s" % (cmake.command_line, static))
        self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", src="rubberband", dst="include/rubberband", keep_path=False)
        for ext in ["dll", "lib", "a", "dylib"]:
            self.copy("*.%s" % ext, src=".", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["rubberband"]
