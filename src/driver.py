from include import mali_ioctl_structs
from include.ioctl_map import MALI_IOCTL_MAP
from include import mali_base_jm_kernel
import mmap
import ctypes
import ctypes.util
import os
MAP_FAILED = ctypes.c_void_p(-1)

_IOC_SIZEBITS = 14
_IOC_NRBITS = 8
_IOC_TYPEBITS = 8
_IOC_DIRBITS  = 2

_IOC_NRSHIFT = 0
_IOC_TYPESHIFT = _IOC_NRSHIFT + _IOC_NRBITS
_IOC_SIZESHIFT = _IOC_TYPESHIFT + _IOC_TYPEBITS
_IOC_DIRSHIFT = _IOC_SIZESHIFT + _IOC_SIZEBITS

dir_map = {"IO":0, "IOW":1, "IOR":2, "IOWR":3}

gpu_properties = {
    1: "KBASE_GPUPROP_PRODUCT_ID",
    2: "KBASE_GPUPROP_VERSION_STATUS",
    3: "KBASE_GPUPROP_MINOR_REVISION",
    4: "KBASE_GPUPROP_MAJOR_REVISION",
    6: "KBASE_GPUPROP_GPU_FREQ_KHZ_MAX",
    8: "KBASE_GPUPROP_LOG2_PROGRAM_COUNTER_SIZE",
    9: "KBASE_GPUPROP_TEXTURE_FEATURES_0",
    10: "KBASE_GPUPROP_TEXTURE_FEATURES_1",
    11: "KBASE_GPUPROP_TEXTURE_FEATURES_2",
    12: "KBASE_GPUPROP_GPU_AVAILABLE_MEMORY_SIZE",
    13: "KBASE_GPUPROP_L2_LOG2_LINE_SIZE",
    14: "KBASE_GPUPROP_L2_LOG2_CACHE_SIZE",
    15: "KBASE_GPUPROP_L2_NUM_L2_SLICES",
    16: "KBASE_GPUPROP_TILER_BIN_SIZE_BYTES",
    17: "KBASE_GPUPROP_TILER_MAX_ACTIVE_LEVELS",
    18: "KBASE_GPUPROP_MAX_THREADS",
    19: "KBASE_GPUPROP_MAX_WORKGROUP_SIZE",
    20: "KBASE_GPUPROP_MAX_BARRIER_SIZE",
    21: "KBASE_GPUPROP_MAX_REGISTERS",
    22: "KBASE_GPUPROP_MAX_TASK_QUEUE",
    23: "KBASE_GPUPROP_MAX_THREAD_GROUP_SPLIT",
    24: "KBASE_GPUPROP_IMPL_TECH",
    25: "KBASE_GPUPROP_RAW_SHADER_PRESENT",
    26: "KBASE_GPUPROP_RAW_TILER_PRESENT",
    27: "KBASE_GPUPROP_RAW_L2_PRESENT",
    28: "KBASE_GPUPROP_RAW_STACK_PRESENT",
    29: "KBASE_GPUPROP_RAW_L2_FEATURES",
    30: "KBASE_GPUPROP_RAW_CORE_FEATURES",
    31: "KBASE_GPUPROP_RAW_MEM_FEATURES",
    32: "KBASE_GPUPROP_RAW_MMU_FEATURES",
    33: "KBASE_GPUPROP_RAW_AS_PRESENT",
    34: "KBASE_GPUPROP_RAW_JS_PRESENT",
    35: "KBASE_GPUPROP_RAW_JS_FEATURES_0",
    36: "KBASE_GPUPROP_RAW_JS_FEATURES_1",
    37: "KBASE_GPUPROP_RAW_JS_FEATURES_2",
    38: "KBASE_GPUPROP_RAW_JS_FEATURES_3",
    39: "KBASE_GPUPROP_RAW_JS_FEATURES_4",
    40: "KBASE_GPUPROP_RAW_JS_FEATURES_5",
    41: "KBASE_GPUPROP_RAW_JS_FEATURES_6",
    42: "KBASE_GPUPROP_RAW_JS_FEATURES_7",
    43: "KBASE_GPUPROP_RAW_JS_FEATURES_8",
    44: "KBASE_GPUPROP_RAW_JS_FEATURES_9",
    45: "KBASE_GPUPROP_RAW_JS_FEATURES_10",
    46: "KBASE_GPUPROP_RAW_JS_FEATURES_11",
    47: "KBASE_GPUPROP_RAW_JS_FEATURES_12",
    48: "KBASE_GPUPROP_RAW_JS_FEATURES_13",
    49: "KBASE_GPUPROP_RAW_JS_FEATURES_14",
    50: "KBASE_GPUPROP_RAW_JS_FEATURES_15",
    51: "KBASE_GPUPROP_RAW_TILER_FEATURES",
    52: "KBASE_GPUPROP_RAW_TEXTURE_FEATURES_0",
    53: "KBASE_GPUPROP_RAW_TEXTURE_FEATURES_1",
    54: "KBASE_GPUPROP_RAW_TEXTURE_FEATURES_2",
    55: "KBASE_GPUPROP_RAW_GPU_ID",
    56: "KBASE_GPUPROP_RAW_THREAD_MAX_THREADS",
    57: "KBASE_GPUPROP_RAW_THREAD_MAX_WORKGROUP_SIZE",
    58: "KBASE_GPUPROP_RAW_THREAD_MAX_BARRIER_SIZE",
    59: "KBASE_GPUPROP_RAW_THREAD_FEATURES",
    60: "KBASE_GPUPROP_RAW_COHERENCY_MODE",
    61: "KBASE_GPUPROP_COHERENCY_NUM_GROUPS",
    62: "KBASE_GPUPROP_COHERENCY_NUM_CORE_GROUPS",
    63: "KBASE_GPUPROP_COHERENCY_COHERENCY",
    64: "KBASE_GPUPROP_COHERENCY_GROUP_0",
    65: "KBASE_GPUPROP_COHERENCY_GROUP_1",
    66: "KBASE_GPUPROP_COHERENCY_GROUP_2",
    67: "KBASE_GPUPROP_COHERENCY_GROUP_3",
    68: "KBASE_GPUPROP_COHERENCY_GROUP_4",
    69: "KBASE_GPUPROP_COHERENCY_GROUP_5",
    70: "KBASE_GPUPROP_COHERENCY_GROUP_6",
    71: "KBASE_GPUPROP_COHERENCY_GROUP_7",
    72: "KBASE_GPUPROP_COHERENCY_GROUP_8",
    73: "KBASE_GPUPROP_COHERENCY_GROUP_9",
    74: "KBASE_GPUPROP_COHERENCY_GROUP_10",
    75: "KBASE_GPUPROP_COHERENCY_GROUP_11",
    76: "KBASE_GPUPROP_COHERENCY_GROUP_12",
    77: "KBASE_GPUPROP_COHERENCY_GROUP_13",
    78: "KBASE_GPUPROP_COHERENCY_GROUP_14",
    79: "KBASE_GPUPROP_COHERENCY_GROUP_15",
    80: "KBASE_GPUPROP_TEXTURE_FEATURES_3",
    81: "KBASE_GPUPROP_RAW_TEXTURE_FEATURES_3",
    82: "KBASE_GPUPROP_NUM_EXEC_ENGINES",
    83: "KBASE_GPUPROP_RAW_THREAD_TLS_ALLOC",
    84: "KBASE_GPUPROP_TLS_ALLOC",
    85: "KBASE_GPUPROP_RAW_GPU_FEATURES"
}

def _ioc(command):
    return (((dir_map[command["dir"]])  << _IOC_DIRSHIFT) | \
    ((command["type"]) << _IOC_TYPESHIFT) | \
    ((command["nr"])   << _IOC_NRSHIFT) | \
    ((command["size"]) << _IOC_SIZESHIFT))
    
def ioctl(fd, ioctl_name, argp):
    request = _ioc(MALI_IOCTL_MAP[ioctl_name])
    print(hex(request))
    return libc.syscall(0x1d, ctypes.c_int(fd), ctypes.c_ulong(request), ctypes.byref(argp))

def is_pointer_valid(ptr):
    """Check if a pointer is within a valid memory region in /proc/self/maps."""
    with open("/proc/self/maps", "r") as maps_file:
        for line in maps_file:
            if "/dev/mali0" in line:
                print(line)
            parts = line.split()

            if len(parts) < 2:
                continue

            addr_range, perms = parts[0], parts[1]

            if "r" not in perms:
                continue

            start, end = (int(x, 16) for x in addr_range.split('-'))
            if start <= ptr < end:
                return True

    return False

if __name__ == "__main__":
    libc = ctypes.CDLL(ctypes.util.find_library("libc"))

    libc.malloc.argtypes = [ctypes.c_size_t]
    libc.malloc.restype = ctypes.c_void_p

    libc.free.argtypes = [ctypes.c_void_p]

    libc.mmap.argtypes = [
        ctypes.c_void_p,
        ctypes.c_size_t,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int64]
    libc.mmap.restype = ctypes.c_void_p

    # open GPU fds
    gpu = os.open("/dev/mali0", os.O_RDWR)
    assert gpu > 0, "Error opening GPU device"

    # try a sniffed sequence
    try:
        # version check
        version_check = mali_ioctl_structs.struct_kbase_ioctl_version_check()
        ret = ioctl(gpu, "KBASE_IOCTL_VERSION_CHECK", version_check)
        assert ret == 0, f"KBASE_IOCTL_VERSION_CHECK failed"
        print("Mali GPU driver version")
        print(f"major={version_check.major}")
        print(f"minor={version_check.minor}")

        # set flags
        flags = mali_ioctl_structs.struct_kbase_ioctl_set_flags()
        flags.create_flags = 0
        ret = ioctl(gpu, "KBASE_IOCTL_SET_FLAGS", flags)
        assert ret == 0, f"KBASE_IOCTL_SET_FLAGS failed"
        print(f"Flags set={ret}")

        # get gpu props -> 1. retreive buffer size
        gpu_props = mali_ioctl_structs.struct_kbase_ioctl_get_gpuprops()
        gpu_props.size = 0x0
        buffer_size = ioctl(gpu, "KBASE_IOCTL_GET_GPUPROPS", gpu_props)
        assert buffer_size > 0, f"KBASE_IOCTL_GET_GPUPROPS failed: 0 buffer_size for gpu props"
        print(f"GPU props buffer_size={hex(buffer_size)}")

        # get gpu props -> 2. read the buffer
        '''
        * The buffer will be filled with pairs of values, a uint32_t key identifying the
        * property followed by the value. The size of the value is identified using
        * the bottom bits of the key. The value then immediately followed the key and
        * is tightly packed (there is no padding). All keys and values are
        * little-endian.
        * 00 = uint8_t
        * 01 = uint16_t
        * 10 = uint32_t
        * 11 = uint64_t
        '''
        gpu_props = mali_ioctl_structs.struct_kbase_ioctl_get_gpuprops()
        props_buf = libc.malloc(buffer_size)
        gpu_props.buffer = ctypes.cast(props_buf, ctypes.c_void_p).value
        gpu_props.size = buffer_size
        gpu_props.flags = 0x0
        buffer_size = ioctl(gpu, "KBASE_IOCTL_GET_GPUPROPS", gpu_props)

        with open('gpu_props.txt', 'w') as f:
            buf_ptr = ctypes.cast(props_buf, ctypes.c_void_p).value
            buf_end = buf_ptr + buffer_size
            cursor = 0
            while buf_ptr != buf_end:
                key_ptr = ctypes.cast(buf_ptr, ctypes.POINTER(ctypes.c_uint32))
                key = key_ptr.contents.value
                buf_ptr += 4
                val_size = key & 0x3
                key = key >> 2
                value = 0
                if val_size == 0:
                    value = ctypes.cast(buf_ptr, ctypes.POINTER(ctypes.c_uint8)).contents.value
                    buf_ptr += 1
                elif val_size == 1:
                    value = ctypes.cast(buf_ptr, ctypes.POINTER(ctypes.c_uint16)).contents.value
                    buf_ptr += 2
                elif val_size == 2:
                    value = ctypes.cast(buf_ptr, ctypes.POINTER(ctypes.c_uint32)).contents.value
                    buf_ptr += 4
                elif val_size == 3:
                    value = ctypes.cast(buf_ptr, ctypes.POINTER(ctypes.c_uint64)).contents.value
                    buf_ptr += 8

                f.write(f"{gpu_properties[key]}={value}\n")

        libc.free(props_buf)

        #https://github.com/LineageOS/android_kernel_samsung_exynos9820/blob/ae1152aa0a337cb3f1f02d68d83028b554245d26/drivers/gpu/arm/bv_r32p1/mali_kbase_core_linux.c#L812
        # "Don't allow memory allocation until user space has set up the tracking page"
        tracking_page = libc.mmap(None, 0x1000, 0, mmap.MAP_SHARED, gpu, mali_base_jm_kernel.BASE_MEM_MAP_TRACKING_HANDLE)
        assert tracking_page != -1, "tracking page: MAPPING FAILED"

        mem_exec = mali_ioctl_structs.struct_kbase_ioctl_mem_exec_init()
        mem_exec.va_pages = 1048576
        ret = ioctl(gpu, "KBASE_IOCTL_MEM_EXEC_INIT", mem_exec)

        # get context id
        ctx = mali_ioctl_structs.struct_kbase_ioctl_get_context_id()
        ret = ioctl(gpu, "KBASE_IOCTL_GET_CONTEXT_ID", ctx)
        print(f"ctx_id={ctx.id}")

        # test mem alloc
        # allocate a GPU executable memory region
        mem_alloc = mali_ioctl_structs.union_kbase_ioctl_mem_alloc()
        mem_alloc._in.va_pages = 1
        mem_alloc._in.commit_pages = 1
        mem_alloc._in.flags = mali_base_jm_kernel.BASE_MEM_PROT_CPU_RD | mali_base_jm_kernel.BASE_MEM_PROT_CPU_WR | mali_base_jm_kernel.BASE_MEM_PROT_GPU_RD |\
            mali_base_jm_kernel.BASE_MEM_PROT_GPU_EX
        ret = ioctl(gpu, "KBASE_IOCTL_MEM_ALLOC", mem_alloc)
        print(f"alloced mem={mem_alloc.out.gpu_va}")

        gpu_mem = libc.mmap(None, 0x1000, mmap.PROT_READ | mmap.PROT_WRITE, mmap.MAP_SHARED, gpu, mem_alloc.out.gpu_va)
        assert gpu_mem != -1, "Mapping GPU memory failed."
        assert is_pointer_valid(gpu_mem), "Invalid pointer from mmap."

        cpu_ptr = ctypes.cast(gpu_mem, ctypes.POINTER(ctypes.c_char))
        print(f"mapped pointer: {cpu_ptr}")

        # Memset to see if accessing the region works
        ctypes.memset(cpu_ptr, 0x92, 0x1000)
        print("Wrote to GPU memory")
        print(f"ptr[0]={hex(ord(cpu_ptr[0x1000-1]))}")
        print(f"ptr[0x1000-1]={hex(ord(cpu_ptr[0x1000-1]))}")

        free_argp = mali_ioctl_structs.struct_kbase_ioctl_mem_free()
        free_argp.gpu_addr = mem_alloc.out.gpu_va
        ret = ioctl(gpu, "KBASE_IOCTL_MEM_FREE", free_argp)
        assert ret != -1, "Freeing GPU memory failed"

        print("Cleanup finished.")
    finally:
        os.close(gpu)
