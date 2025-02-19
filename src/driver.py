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

def _ioc(command):
    return (((dir_map[command["dir"]])  << _IOC_DIRSHIFT) | \
    ((command["type"]) << _IOC_TYPESHIFT) | \
    ((command["nr"])   << _IOC_NRSHIFT) | \
    ((command["size"]) << _IOC_SIZESHIFT))
    
if __name__ == "__main__":
    libc = ctypes.CDLL(ctypes.util.find_library("libc"))
    gpu = os.open("/dev/mali0", os.O_RDWR)
    assert gpu > 0, "Error opening GPU device"
    try:
        # Simple version check
        version_check = mali_ioctl_structs.struct_kbase_ioctl_version_check()
        request = _ioc(MALI_IOCTL_MAP["KBASE_IOCTL_VERSION_CHECK"])
        libc.syscall(0x1d, ctypes.c_int(gpu), ctypes.c_ulong(request), ctypes.byref(version_check))
        print(hex(request))
        print("Mali GPU driver version")
        print(f"major={version_check.major}")
        print(f"minor={version_check.minor}")

        # set flags
        flags = mali_ioctl_structs.struct_kbase_ioctl_set_flags()
        flags.create_flags = 0x0
        request = _ioc(MALI_IOCTL_MAP["KBASE_IOCTL_SET_FLAGS"])
        print(hex(request))
        libc.syscall(0x1d, ctypes.c_int(gpu), ctypes.c_ulong(request), ctypes.byref(flags))
        print("Flags set")


        '''
         * The buffer will be filled with pairs of values, a uint32_t key identifying the
        * property followed by the value. The size of the value is identified using
        * the bottom bits of the key. The value then immediately followed the key and
        * is tightly packed (there is no padding). All keys and values are
        * little-endian.
        '''
        gpu_props = mali_ioctl_structs.struct_kbase_ioctl_get_gpuprops()
        gpu_props.size = 0x0
        request = _ioc(MALI_IOCTL_MAP["KBASE_IOCTL_GET_GPUPROPS"])
        buffer_size = libc.syscall(0x1d, ctypes.c_int(gpu), ctypes.c_ulong(request), ctypes.byref(gpu_props))
        
        print("Get GPU props")
        print(f"buffer_size={hex(buffer_size)}")
    finally:
        os.close(gpu)
