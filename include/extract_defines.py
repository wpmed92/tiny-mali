import re
import json
import mali_ioctl_structs
import ctypes

ioctl_map = {}

def extract_defines(kbase_ioctl_type, file_path):
    define_pattern = re.compile(r'#define\s+(KBASE_IOCTL_\S+|MALI_EXYNOS_\S+)')
    ioc_pattern = re.compile(r'^\s*_(IO|IOW|IOR|IOWR)\s*\(')

    with open(file_path, 'r') as file:
        lines = file.readlines()

    name = ""
    for line in lines:
        if define_pattern.match(line):
            name = line.strip().replace("#define ", "").replace(" \\", "")
        elif ioc_pattern.match(line):
            ioc = line.strip().split(",")
            #print(ioc)
            _dir = "IOWR" if "IOWR" in line else "IOR" if "IOR" in line else "IOW" if "IOW" in line else "IO"
            nr = int(ioc[1].replace(" ", "").replace(")", ""))
            struct_name = ioc[2].replace(")", "") if len(ioc) > 2 else ""
            #print(f"name={name}, nr={nr}, struct_name={struct_name}")
            size = 0
            if struct_name != "":
                print(struct_name)
                struct_type = getattr(mali_ioctl_structs, "_".join(struct_name[1:].split(" ")), None)
                if struct_type is not None:
                    size = ctypes.sizeof(struct_type)
            ioctl_map[name] = {"type": kbase_ioctl_type, "nr": nr, "payload": struct_name[1:], "dir": _dir, "size": size}

if __name__ == "__main__":
    file_path = 'mali_exynos_ioctl.h'
    extract_defines(0x80, 'mali_kbase_ioctl.h')
    extract_defines(0x80, 'mali_kbase_jm_ioctl.h')
    extract_defines(0x82, 'mali_exynos_ioctl.h')

    output_file = 'ioctl_map.py'
    with open(output_file, 'w') as f:
        f.write("MALI_IOCTL_MAP = ")
        json.dump(ioctl_map, f, indent=4) 
