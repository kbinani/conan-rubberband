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
        # Build both Debug and Release in one package id for Windows.
        build_types = ["Debug", "Release"] if self.settings.os == "Windows" else [self.settings.build_type]
        for build_type in build_types:
            settings = self.settings
            settings.build_type = build_type
            cmake = CMake(settings)
            self.run("cmake . %s %s" % (cmake.command_line, static))
            self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", src="rubberband", dst="include", keep_path=False)
        if self.settings.os == "Windows":
            for build_type in ["Debug", "Release"]:
                self.copy("*.dll", src=build_type, dst="lib/%s" % build_type, keep_path=False)
                self.copy("*.lib", src=build_type, dst="lib/%s" % build_type, keep_path=False)
        else:
            self.copy("*.a", src=".", dst="lib", keep_path=False)
            self.copy("*.dylib", src=".", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["rubberband"]

    def conan_info(self):
        if self.settings.os == "Windows":
            # This will make package id same for both "Debug" and "Release".
            self.info.settings.build_type = "DebugAndRelease"
