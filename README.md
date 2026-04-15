# Zenna

## What is it?

Very new packet manager (C++ packet manager). Would you mind making packet manager with parasite relationship with conan
and vcpkg?

## How to start:

Create config.zen file with configuration

Example:

```
profile.name = hello
profile.version = 0.1
profile.requires = qt
profile.build_systems = cmake
profile.build_types = build
```

## Goal of using Zenna:

You do not care about conan file config and write simple Zenna config file.

## How it will work:

Zenna config -> conanfile -> cmake (or other) profile -> make (or other build system) -> your sad code :(

It can be something like:

```
                        Zenna config
                        /           \
                    VCPKG           Conan (build, release or something)
                                        |
                                make, cmake, meson
```

Yes, more config files for the brave of Emperor