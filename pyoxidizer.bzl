path_venv = '/Users/yamaka/Desktop/App/'
def make_exe():
    dist = default_python_distribution()
    policy = dist.make_python_packaging_policy()

    python_config = dist.make_python_interpreter_config()
    python_config.module_search_paths = ["$ORIGIN"] # sys.path[0] becomes where the binary is built.
    python_config.run_command = "from fmIDE import main;main()"

    exe = dist.to_python_executable(
        name="fmIDE",
        packaging_policy=policy,
        config=python_config,
    )

    resources = exe.read_package_root(
        path=path_venv + 'src/fmide',
        packages=['src', 'fmIDE'],
        )
    for r in resources:
        r.add_source = False
    exe.add_python_resources(resources)

    resources = exe.read_package_root(
        path=path_venv + 'lib/python3.9/site-packages',
        packages=['xlsxwriter',],
        )
    for r in resources:
        r.add_source = False
    exe.add_python_resources(resources)

    resources = exe.read_package_root(
        path=path_venv + 'src/interface',
        packages=['interface_fm','interface_fm_calculator','interface_gateway_fm','interface_keymaps',
                  'interface_mouse','interface_spreadsheet','interface_udf_builder','interface_view',
                  ],
        )
    for r in resources:
        r.add_source = False
    exe.add_python_resources(resources)

    resources = exe.read_package_root(
        path=path_venv + 'src/fm-calculator',
        packages=['fm_calculator',],
        )
    for r in resources:
        r.add_source = False
    exe.add_python_resources(resources)

    resources = exe.read_package_root(
        path=path_venv + 'src/keyboard-shortcut',
        packages=['keyboard_shortcut',],
        )
    for r in resources:
        r.add_source = False
    exe.add_python_resources(resources)

    resources = exe.read_package_root(
        path=path_venv + 'src/os-identifier',
        packages=['os_identifier',],
        )
    for r in resources:
        r.add_source = False
    exe.add_python_resources(resources)

    resources = exe.read_package_root(
        path=path_venv + 'src/rpe-to-normal',
        packages=['rpe_to_normal',],
        )
    for r in resources:
        r.add_source = False
    exe.add_python_resources(resources)

    resources = exe.read_package_root(
        path=path_venv + 'src/spreadsheet',
        packages=['spreadsheet',],
        )
    for r in resources:
        r.add_source = False
    exe.add_python_resources(resources)

    resources = exe.read_package_root(
        path=path_venv + 'src/view-tkinter',
        packages=['view_tkinter',],
        )
    for r in resources:
        r.add_source = False
    exe.add_python_resources(resources)

    resources = exe.read_package_root(
        path=path_venv + 'src/controller-mouse',
        packages=['mouse',],
        )
    for r in resources:
        r.add_source = False
    exe.add_python_resources(resources)

    exe.tcl_files_path = "lib"

    return exe

def make_embedded_resources(exe):
    return exe.to_embedded_resources()

def make_install(exe):
    files = FileManifest()
    files.add_python_resource(".", exe)
    templates = glob([
        path_venv+'src/fmide/src/Pickles/*',
        path_venv+'src/fmide/src/PicklesCommands/*',
        path_venv+'src/fmide/src/load_config_data',
                      ],
                      strip_prefix=path_venv+'src/fmide/')
    files.add_manifest(templates)

    return files

def make_msi(exe):
    return exe.to_wix_msi_builder(
        "myapp",
        "My Application",
        "1.0",
        "Alice Jones"
    )

def make_exe_for_windows(exe):
    return exe.to_wix_bundle_builder(
        "myapp",
        "My Application",
        "1.0",
        "Alice Jones"
    )

def register_code_signers():
    if not VARS.get("ENABLE_CODE_SIGNING"):
        return

set_build_path('/Users/yamaka/Desktop/new_folder')
register_code_signers()

register_target("exe", make_exe)
register_target("resources", make_embedded_resources, depends=["exe"], default_build_script=True)
register_target("install", make_install, depends=["exe"], default=True)
register_target("win", make_msi, depends=["exe"], default=True)
register_target("win2", make_exe_for_windows, depends=["exe"], default=True)

resolve_targets()
