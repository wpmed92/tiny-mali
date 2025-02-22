from include import mali_ioctl_structs
from include.ioctl_map import MALI_IOCTL_MAP
import ctypes
import ctypes.util
import os

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

if __name__ == "__main__":
    libc = ctypes.CDLL(ctypes.util.find_library("libc"))

    # setup malloc and free
    malloc = libc.malloc
    malloc.argtypes = [ctypes.c_size_t]
    malloc.restype = ctypes.c_void_p

    free = libc.free
    free.argtypes = [ctypes.c_void_p]

    # open GPU fds
    gpu = os.open("/dev/mali0", os.O_RDWR)
    assert gpu > 0, "Error opening GPU device"

    # try a sniffed sequence
    try:
        # Simple version check
        version_check = mali_ioctl_structs.struct_kbase_ioctl_version_check()
        ioctl(gpu, "KBASE_IOCTL_VERSION_CHECK", version_check)
        print("Mali GPU driver version")
        print(f"major={version_check.major}")
        print(f"minor={version_check.minor}")

        # set flags
        flags = mali_ioctl_structs.struct_kbase_ioctl_set_flags()
        flags.create_flags = 0x0
        ioctl(gpu, "KBASE_IOCTL_SET_FLAGS", flags)
        print("Flags set")

        # get gpu props -> 1. retreive buffer size
        gpu_props = mali_ioctl_structs.struct_kbase_ioctl_get_gpuprops()
        gpu_props.size = 0x0
        buffer_size = ioctl(gpu, "KBASE_IOCTL_GET_GPUPROPS", gpu_props)
        print("Get GPU props")
        print(f"buffer_size={hex(buffer_size)}")

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
        props_buf = malloc(buffer_size)
        gpu_props.buffer = ctypes.cast(props_buf, ctypes.c_void_p).value
        gpu_props.size = buffer_size
        gpu_props.flags = 0x0
        buffer_size = ioctl(gpu, "KBASE_IOCTL_GET_GPUPROPS", gpu_props)
        print("Get GPU props")
        print(f"buffer_size={hex(buffer_size)}")

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

        free(props_buf)
    finally:
        os.close(gpu)
