# type: ignore
import ctypes, ctypes.util, struct
import mali_ioctl_structs
import pathlib, sys
from tinygrad.helpers import to_mv, getenv
from tinygrad.runtime.autogen import adreno
sys.path.append(pathlib.Path(__file__).parent.parent.parent.as_posix())

IOCTL = getenv("IOCTL", 0)

@ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.c_ulong, ctypes.c_void_p)
def ioctl(fd, request, argp):
  # flags
  if request == 0x40048001:
    flags = ctypes.cast(argp, ctypes.POINTER(mali_ioctl_structs.struct_kbase_ioctl_set_flags)).contents
    print(f"flags={hex(flags.create_flags)}")
  # gpu props
  if request == 0x40108003:
    flags = ctypes.cast(argp, ctypes.POINTER(mali_ioctl_structs.struct_kbase_ioctl_get_gpuprops)).contents
    print(f"props size={hex(flags.size)}")
  # mem alloc
  if request == 0xc0208005:
    mem_alloc_props = ctypes.cast(argp, ctypes.POINTER(mali_ioctl_structs.union_kbase_ioctl_mem_alloc)).contents
    print("____ALLOC DUMP START____")
    print("in:")
    print(f"va_pages={mem_alloc_props._in.va_pages}")
    print(f"commit_pages={mem_alloc_props._in.commit_pages}")
    print(f"extension={mem_alloc_props._in.extension}")
    print(f"flags={mem_alloc_props._in.flags}")

  ret = libc.syscall(0x1d, ctypes.c_int(fd), ctypes.c_ulong(request), ctypes.c_void_p(argp))

  if request == 0xc0208005:
    print("out:")
    print(f"gpu_va={mem_alloc_props.out.gpu_va}")
    print(f"flags={mem_alloc_props.out.flags}")
    print("____ALLOC DUMP END____")

  return ret

def install_hook(c_function, python_function):
  # AARCH64 trampoline to ioctl
  tramp = b"\x70\x00\x00\x10\x10\x02\x40\xf9\x00\x02\x1f\xd6"
  tramp += struct.pack("Q", ctypes.cast(ctypes.byref(python_function), ctypes.POINTER(ctypes.c_ulong)).contents.value)

  # get real ioctl address
  ioctl_address = ctypes.cast(ctypes.byref(c_function), ctypes.POINTER(ctypes.c_ulong))

  # hook ioctl
  libc = ctypes.CDLL(ctypes.util.find_library("libc"))
  ret = libc.mprotect(ctypes.c_ulong((ioctl_address.contents.value//0x1000)*0x1000), 0x2000, 7)
  assert ret == 0
  libc.memcpy(ioctl_address.contents, ctypes.create_string_buffer(tramp), len(tramp))

libc = ctypes.CDLL(ctypes.util.find_library("libc"))
install_hook(libc.ioctl, ioctl)

from tinygrad import Tensor

a = Tensor([1,2])
(a*3).realize()

while True:
  b = 1