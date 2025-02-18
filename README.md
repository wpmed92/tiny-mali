# tiny-mali

User space driver for Mali-G76 bifrost with the goal to run compute kernels and learn about the architecture.

## Mali-G76

Built on the Bifrost architecture.
Compute block = quad
Mal-G72 was 4-wide SIMD, G76 is doubles to 8-wide. (Still narrow wavefront compared to AMD/NVIDIA)
8 vec3 F32 ADDs in 3 cycles.
int8 dot product support.
Doubles SIMD lanes compared to earlier models, has 8-wide Wavefront.

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

`#define KBASE_IOCTL_TYPE 0x80`

We can see commands with type `0x82`, that coresponds to a "customer extension range"
`#define KBASE_IOCTL_EXTRA_TYPE (KBASE_IOCTL_TYPE + 2) = 0x82`

## ioctl decode tool

`include/extract_defines.py`

This tool extracts ioctl defines from mali header files. It constructs a map where the key is the define name, and the dict entry is:
```Python
    {
        "type": type_num,
        "nr": nr_num,
        "payload": "struct/union name",
        "dir": "IO/IOR/IOW/IOWR"
    },
```

You can then use the generated `ioctl_map.py` to decode the sniffed ioctl requests.

`src/ioctl_decode.py`

usage: `PYTHONPATH="." src/ioctl_decode.py`

It import the previously generated ioctl map, loops through the given requests, and decodes them in the following form:

```Python
# request  |    dir | type | nr:DECODED_IOCTL_NAME, | size of struct/union
0x40108002 = IOC(0x1, 0x80, 2:KBASE_IOCTL_JOB_SUBMIT, 0x10)
```
## ioctl sniffing
