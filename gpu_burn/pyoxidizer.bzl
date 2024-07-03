PYTHON_VERSION = "3.8"

def make_gpu_burn_script():
    dist = default_python_distribution(python_version = PYTHON_VERSION)

    policy = dist.make_python_packaging_policy()
    policy.resources_location_fallback = "filesystem-relative:lib"

    python_config = dist.make_python_interpreter_config()
    python_config.run_command = "from gpu_burn_script import main; main()"

    exe = dist.to_python_executable(
        name = "gpu_burn_script",
        packaging_policy = policy,
        config = python_config,
    )

    exe.add_python_resources(exe.read_package_root(CWD, ["gpu_burn_script"]))

    return exe

def make_gpu_burn_epilog_parser():
    dist = default_python_distribution(python_version = PYTHON_VERSION)

    policy = dist.make_python_packaging_policy()
    policy.resources_location_fallback = "filesystem-relative:lib"

    python_config = dist.make_python_interpreter_config()
    python_config.run_command = "from gpu_burn_epilog_parser import main; main()"

    exe = dist.to_python_executable(
        name = "gpu_burn_epilog_parser",
        packaging_policy = policy,
        config = python_config,
    )

    exe.add_python_resources(exe.read_package_root(CWD, ["gpu_burn_epilog_parser"]))

    return exe

register_target("gpu_burn_epilog_parser", make_gpu_burn_epilog_parser)
register_target("gpu_burn_script", make_gpu_burn_script)

resolve_targets()
