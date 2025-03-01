# tiny-mali

User space driver for Mali-G76 bifrost with the goal to run compute kernels and learn about the architecture.

## Mali-G76

Built on the Bifrost architecture.  
Compute block = quad  
Mali-G72 was 4-wide SIMD, G76 doubles to 8-wide. (Still narrow wavefront compared to AMD/NVIDIA)  
8 vec3 F32 ADDs in 3 cycles.  
int8 dot product support.  

## ioctl command structure

ioctl command encoding using `_IOC` [macro](https://sites.uclouvain.be/SystInfo/usr/include/asm-generic/ioctl.h.html)

```C
#define _IOC(dir,type,nr,size) \
        (((dir)  << _IOC_DIRSHIFT) | \
         ((type) << _IOC_TYPESHIFT) | \
         ((nr)   << _IOC_NRSHIFT) | \
         ((size) << _IOC_SIZESHIFT))
```
Bit structure
```C
parts:    dir   size  type   nr
32bits =   2  |  14  |  8  |  8
```

Example:
`0xc0048000 = IOC(0x3, 0x80, 0, 0x4)`

```C
    0b11     | 00000000000100 | 10000000  | 00000000
    dir=3    | size=0x4       | type=0x80 | nr = 0
```

Looking up the meaning of type and nr values.
type `0x80` is an identifier for `KBASE_IOCTL_TYPE` as defined [here](https://sites.uclouvain.be/SystInfo/usr/include/asm-generic/ioctl.h.html).
`nr 0` means `KBASE_IOCTL_VERSION_CHECK` (source from the [Exynos 9820 r32p1 driver ioctl includes](https://github.com/LineageOS/android_kernel_samsung_exynos9820/blob/lineage-22.1/include/uapi/gpu/arm/bv_r32p1/mali_kbase_ioctl.h))

```C
#define KBASE_IOCTL_TYPE 0x80
```

We can see commands with type `0x82`, that coresponds to a "customer extension range"
```C
#define KBASE_IOCTL_EXTRA_TYPE (KBASE_IOCTL_TYPE + 2) = 0x82
```

## ioctl map

`mali/extract_defines.py`

This tool extracts ioctl defines from mali header files. It constructs a map where the key is the define name, and the dict entry is:
```Python
{
    "type": type_num,
    "nr": nr_num,
    "payload": "struct/union name",
    "dir": "IO/IOR/IOW/IOWR"
    "size": size_of_payload,
    "encoded": ioctl_request
},
```

You can then use the generated `ioctl_map.py` to decode the sniffed ioctl requests, or to send commands.

## Sending ioctl commands

The simplest command is a version check. It returns driver major and minor versions:  

```Python
version_check = mali_ioctl_structs.struct_kbase_ioctl_version_check()
ret = gpu.ioctl(MALI_IOCTL_MAP["KBASE_IOCTL_VERSION_CHECK"]["encoded"], version_check)
assert ret == 0, f"KBASE_IOCTL_VERSION_CHECK failed"
print(f"major={version_check.major}")
print(f"minor={version_check.minor}")
```

## Writing to GPU memory

First, we have to setup the tracking page. This page needs to be mapped, otherwise the kernel won't allow `KBASE_IOCTL_MEM_ALLOC`:

```Python
tracking_page = gpu.mmap(None, 0x1000, 0, mmap.MAP_SHARED, mali_base_jm_kernel.BASE_MEM_MAP_TRACKING_HANDLE)
```

Then we can send the `ioctl`.  
This command requests 1 page of memory to be allocated with CPU write + read, and GPU read + executable protection.  
This region will probably be filled with shader executable.

```Python
mem_alloc = mali_ioctl_structs.union_kbase_ioctl_mem_alloc()
mem_alloc._in.va_pages = 1
mem_alloc._in.commit_pages = 1
mem_alloc._in.flags = mali_base_jm_kernel.BASE_MEM_PROT_CPU_RD | mali_base_jm_kernel.BASE_MEM_PROT_CPU_WR | mali_base_jm_kernel.BASE_MEM_PROT_GPU_RD |\
    mali_base_jm_kernel.BASE_MEM_PROT_GPU_EX
ret = gpu.ioctl(MALI_IOCTL_MAP["KBASE_IOCTL_MEM_ALLOC"]["encoded"], mem_alloc)
```

Map the `gpu_va` we got from the alloc:  

```Python
gpu_mem = gpu.mmap(None, 0x1000, mmap.PROT_READ | mmap.PROT_WRITE, mmap.MAP_SHARED, mem_alloc.out.gpu_va)
```

## Acronyms

CSF - Command Stream Frontend  
JM - Job Manager  
JC - Job Chain
