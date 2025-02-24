from include import mali_base_jm_kernel

def get_flag(flag, bit):
    return 1 if flag&bit else 0
if __name__ == "__main__":
    decode = False
    with open("./dump/ioctl_mem_alloc_dump.txt", "r", encoding="utf-8") as file:
        for line in file:
            if "____ALLOC DUMP START____" in line:
                decode = True
            if "flags=" in line and decode:
                flag = int(line.split("=")[1].strip())
                print(f"flag={hex(flag), bin(flag)}")
                print(f"CPU_READ={get_flag(flag, mali_base_jm_kernel.BASE_MEM_PROT_CPU_RD)}")
                print(f"CPU_WRITE={get_flag(flag, mali_base_jm_kernel.BASE_MEM_PROT_CPU_WR)}")
                print(f"GPU_READ={get_flag(flag, mali_base_jm_kernel.BASE_MEM_PROT_GPU_RD)}")
                print(f"GPU_WRITE={get_flag(flag, mali_base_jm_kernel.BASE_MEM_PROT_GPU_WR)}")
                print(f"GPU_EX={get_flag(flag, mali_base_jm_kernel.BASE_MEM_PROT_GPU_EX)}")
