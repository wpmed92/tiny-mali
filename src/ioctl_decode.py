from include.ioctl_map import MALI_IOCTL_MAP
# MALI IOCTL SNIFFING FOR FUN

# bits
_IOC_SIZEBITS = 14
_IOC_NRBITS = 8
_IOC_TYPEBITS = 8
_IOC_DIRBITS  = 2

# shift
_IOC_NRSHIFT = 0
_IOC_TYPESHIFT = _IOC_NRSHIFT + _IOC_NRBITS
_IOC_SIZESHIFT = _IOC_TYPESHIFT + _IOC_TYPEBITS
_IOC_DIRSHIFT = _IOC_SIZESHIFT + _IOC_SIZEBITS

# masks
_IOC_NRMASK  = ((1 << _IOC_NRBITS)-1)
_IOC_TYPEMASK  = ((1 << _IOC_TYPEBITS)-1)
_IOC_SIZEMASK  = ((1 << _IOC_SIZEBITS)-1)
_IOC_DIRMASK   = ((1 << _IOC_DIRBITS)-1)

if __name__ == "__main__":
    requests = [
        (4, 3221520384, 548757042140),
        (4, 1074036737, 548757042416),
        (4, 1074823171, 548757042280),
        (4, 1074823171, 548757042280),
        (4, 1074298918, 548757042560),
        (4, 2147778577, 548757042528),
        (4, 3223355397, 548757042384),
        (4, 3223355397, 548757041184),
        (4, 3223355397, 548757041056),
        (4, 3223355397, 548757041056),
        (4, 3223355397, 548757041840),
        (4, 3223355397, 548757041792),
        (4, 3223355397, 548757044048),
        (4, 1074823195, 516297481064),
        (4, 1074299395, 516297481072),
        (4, 3223355397, 548757041920),
        (4, 3223355397, 548757042432),
        (4, 1074823195, 516297481064),
        (4, 1074299395, 516297481072),
        (4, 1074823195, 516297481064),
        (4, 1074299395, 516297481072),
        (4, 1074823195, 516297481064),
        (4, 1074299395, 516297481072),
        (4, 3223355397, 548757041920),
        (4, 3223355397, 516258744128),
        (4, 1074823170, 516258744504),
        (4, 1074823195, 516297481064),
        (4, 1074299395, 516297481072),
        (4, 1074823195, 516297481064),
        (4, 1074299395, 516297481072),
        (4, 1074823195, 516297481064),
        (4, 1074299395, 516297481072),
        (4, 1074823195, 516297481064),
        (4, 1074299395, 516297481072),
        (4, 1074823195, 516297481064),
        (4, 1074299395, 516297481072),
        (4, 1074823195, 516297481064),
        (4, 1074299395, 516297481072),
        (4, 1074823195, 516297481064),
        (4, 1074299395, 516297481072),
    ]

    def get_name(dir, _type, nr):
        dir_map = ["IO", "IOW", "IOR", "IOWR"]
        for key, value in MALI_IOCTL_MAP.items():
            if value["dir"] == dir_map[dir] and _type == value["type"] and nr == value["nr"]:
                return key
        raise RuntimeError(f"could find IOCTL for dir={dir}, type={_type}, nr={nr}")
            

    def decode_ioc(req):
       nr = (req >> _IOC_NRSHIFT)&_IOC_NRMASK
       _type = (req >> _IOC_TYPESHIFT)&_IOC_TYPEMASK
       _dir = (req >> _IOC_DIRSHIFT)&_IOC_DIRMASK
       return f"{hex(req)} = IOC({hex(_dir)}, {hex(_type)}, {nr}:{get_name(_dir, _type, nr)}, {hex((req >> _IOC_SIZESHIFT)&_IOC_SIZEMASK)})"

    for req in requests:
        print(decode_ioc(req[1]))
    