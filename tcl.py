import os
import subprocess
import string


def get_project_paths(project_path):
    project_dir = os.path.dirname(project_path)
    project_name = os.path.basename(project_dir)

    bit_path = os.path.join(project_dir, f"{project_name}.runs", "impl_1",
                            f"TM_ov5642_BPF_SPF.bit").replace(os.sep, '/')
    mcs_path = os.path.join(project_dir, f"{project_name}.runs", "impl_1",
                            f"TM_ov5642_BPF_SPF.mcs").replace(os.sep, '/')

    return project_dir, project_name, bit_path, mcs_path


def generate_tcl(project_path, bit_path, mcs_path, device="xc7a100t_0", memory_device="mt25ql128-spi-x1_x2_x4", template_path="run.tcl.tpl", tcl_path="run.tcl"):
    with open(template_path, "r", encoding="utf-8") as f:
        template = string.Template(f.read())
        result = template.substitute(
            project_path=project_path, bit_path=bit_path,
            mcs_path=mcs_path, device=device, memory_device=memory_device)
        with open(tcl_path, "w", encoding="utf-8") as f:
            f.write(result)


def run_tcl(tcl_path="run.tcl"):
    p = subprocess.Popen(
        f"vivado -mode batch -source {tcl_path}",
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        shell=True, universal_newlines=True)
    return p
