# -*- coding: utf-8 -*-
#
# TARGET arch is: []
# WORD_SIZE is: 8
# POINTER_SIZE is: 8
# LONGDOUBLE_SIZE is: 8
#
import ctypes


class AsDictMixin:
    @classmethod
    def as_dict(cls, self):
        result = {}
        if not isinstance(self, AsDictMixin):
            # not a structure, assume it's already a python object
            return self
        if not hasattr(cls, "_fields_"):
            return result
        # sys.version_info >= (3, 5)
        # for (field, *_) in cls._fields_:  # noqa
        for field_tuple in cls._fields_:  # noqa
            field = field_tuple[0]
            if field.startswith('PADDING_'):
                continue
            value = getattr(self, field)
            type_ = type(value)
            if hasattr(value, "_length_") and hasattr(value, "_type_"):
                # array
                if not hasattr(type_, "as_dict"):
                    value = [v for v in value]
                else:
                    type_ = type_._type_
                    value = [type_.as_dict(v) for v in value]
            elif hasattr(value, "contents") and hasattr(value, "_type_"):
                # pointer
                try:
                    if not hasattr(type_, "as_dict"):
                        value = value.contents
                    else:
                        type_ = type_._type_
                        value = type_.as_dict(value.contents)
                except ValueError:
                    # nullptr
                    value = None
            elif isinstance(value, AsDictMixin):
                # other structure
                value = type_.as_dict(value)
            result[field] = value
        return result


class Structure(ctypes.Structure, AsDictMixin):

    def __init__(self, *args, **kwds):
        # We don't want to use positional arguments fill PADDING_* fields

        args = dict(zip(self.__class__._field_names_(), args))
        args.update(kwds)
        super(Structure, self).__init__(**args)

    @classmethod
    def _field_names_(cls):
        if hasattr(cls, '_fields_'):
            return (f[0] for f in cls._fields_ if not f[0].startswith('PADDING'))
        else:
            return ()

    @classmethod
    def get_type(cls, field):
        for f in cls._fields_:
            if f[0] == field:
                return f[1]
        return None

    @classmethod
    def bind(cls, bound_fields):
        fields = {}
        for name, type_ in cls._fields_:
            if hasattr(type_, "restype"):
                if name in bound_fields:
                    if bound_fields[name] is None:
                        fields[name] = type_()
                    else:
                        # use a closure to capture the callback from the loop scope
                        fields[name] = (
                            type_((lambda callback: lambda *args: callback(*args))(
                                bound_fields[name]))
                        )
                    del bound_fields[name]
                else:
                    # default callback implementation (does nothing)
                    try:
                        default_ = type_(0).restype().value
                    except TypeError:
                        default_ = None
                    fields[name] = type_((
                        lambda default_: lambda *args: default_)(default_))
            else:
                # not a callback function, use default initialization
                if name in bound_fields:
                    fields[name] = bound_fields[name]
                    del bound_fields[name]
                else:
                    fields[name] = type_()
        if len(bound_fields) != 0:
            raise ValueError(
                "Cannot bind the following unknown callback(s) {}.{}".format(
                    cls.__name__, bound_fields.keys()
            ))
        return cls(**fields)


class Union(ctypes.Union, AsDictMixin):
    pass





_UAPI_BASE_JM_KERNEL_H_ = True # macro
BASE_MEM_PROT_CPU_RD = (1<<0) # macro
BASE_MEM_PROT_CPU_WR = (1<<1) # macro
BASE_MEM_PROT_GPU_RD = (1<<2) # macro
BASE_MEM_PROT_GPU_WR = (1<<3) # macro
BASE_MEM_PROT_GPU_EX = (1<<4) # macro
BASEP_MEM_PERMANENT_KERNEL_MAPPING = (1<<5) # macro
BASE_MEM_GPU_VA_SAME_4GB_PAGE = (1<<6) # macro
BASEP_MEM_NO_USER_FREE = (1<<7) # macro
BASE_MEM_RESERVED_BIT_8 = (1<<8) # macro
BASE_MEM_GROW_ON_GPF = (1<<9) # macro
BASE_MEM_COHERENT_SYSTEM = (1<<10) # macro
BASE_MEM_COHERENT_LOCAL = (1<<11) # macro
BASE_MEM_CACHED_CPU = (1<<12) # macro
BASE_MEM_SAME_VA = (1<<13) # macro
BASE_MEM_NEED_MMAP = (1<<14) # macro
BASE_MEM_COHERENT_SYSTEM_REQUIRED = (1<<15) # macro
BASE_MEM_PROTECTED = (1<<16) # macro
BASE_MEM_DONT_NEED = (1<<17) # macro
BASE_MEM_IMPORT_SHARED = (1<<18) # macro
BASE_MEM_RESERVED_BIT_19 = (1<<19) # macro
BASE_MEM_TILER_ALIGN_TOP = (1<<20) # macro
BASE_MEM_UNCACHED_GPU = (1<<21) # macro
BASEP_MEM_GROUP_ID_SHIFT = 22 # macro
BASE_MEM_GROUP_ID_MASK = (0xF<<22) # macro
BASE_MEM_IMPORT_SYNC_ON_MAP_UNMAP = (1<<26) # macro
BASE_MEM_FLAG_MAP_FIXED = (1<<27) # macro
BASE_MEM_KERNEL_SYNC = (1<<28) # macro
BASEP_MEM_PERFORM_JIT_TRIM = (1<<29) # macro
BASE_MEM_FLAGS_NR_BITS = 30 # macro
BASEP_MEM_FLAGS_KERNEL_ONLY = ((1<<5)|(1<<7)|(1<<27)|(1<<29)) # macro
BASE_MEM_FLAGS_OUTPUT_MASK = (1<<14) # macro
BASE_MEM_FLAGS_INPUT_MASK = (((1<<30)-1)&~(1<<14)) # macro
BASE_MEM_FLAGS_RESERVED = ((1<<8)|(1<<19)) # macro
BASEP_MEM_INVALID_HANDLE = (0<<12) # macro
BASE_MEM_MMU_DUMP_HANDLE = (1<<12) # macro
BASE_MEM_TRACE_BUFFER_HANDLE = (2<<12) # macro
BASE_MEM_MAP_TRACKING_HANDLE = (3<<12) # macro
BASEP_MEM_WRITE_ALLOC_PAGES_HANDLE = (4<<12) # macro
BASE_MEM_COOKIE_BASE = (64<<12) # macro
# BASE_MEM_FIRST_FREE_ADDRESS = ((BITS_PER_LONG<<12)+(64<<12)) # macro
BASE_JIT_ALLOC_MEM_TILER_ALIGN_TOP = (1<<0) # macro
BASE_JIT_ALLOC_HEAP_INFO_IS_SIZE = (1<<1) # macro
BASE_JIT_ALLOC_VALID_FLAGS = ((1<<0)|(1<<1)) # macro
BASE_CONTEXT_CREATE_FLAG_NONE = (0) # macro
BASE_CONTEXT_CCTX_EMBEDDED = (1<<0) # macro
BASE_CONTEXT_SYSTEM_MONITOR_SUBMIT_DISABLED = (1<<1) # macro
BASEP_CONTEXT_MMU_GROUP_ID_SHIFT = (3) # macro
BASEP_CONTEXT_MMU_GROUP_ID_MASK = (0xF<<(3)) # macro
BASEP_CONTEXT_CREATE_KERNEL_FLAGS = ((1<<1)|(0xF<<(3))) # macro
BASEP_CONTEXT_CREATE_ALLOWED_FLAGS = ((1<<0)|((1<<1)|(0xF<<(3)))) # macro
BASEP_CONTEXT_FLAG_JOB_DUMP_DISABLED = ((1<<31)) # macro
BASE_TLSTREAM_ENABLE_LATENCY_TRACEPOINTS = (1<<0) # macro
BASE_TLSTREAM_JOB_DUMPING_ENABLED = (1<<1) # macro
BASE_TLSTREAM_FLAGS_MASK = ((1<<0)|(1<<1)) # macro
BASE_JD_ATOM_COUNT = 256 # macro
BASE_JD_RP_COUNT = (256) # macro
BASE_JD_SOFT_EVENT_SET = (1) # macro
BASE_JD_SOFT_EVENT_RESET = (0) # macro
BASE_JD_DEP_TYPE_INVALID = (0) # macro
BASE_JD_DEP_TYPE_DATA = (1<<0) # macro
BASE_JD_DEP_TYPE_ORDER = (1<<1) # macro
BASE_JD_REQ_DEP = (0) # macro
BASE_JD_REQ_FS = (1<<0) # macro
BASE_JD_REQ_CS = (1<<1) # macro
BASE_JD_REQ_T = (1<<2) # macro
BASE_JD_REQ_CF = (1<<3) # macro
BASE_JD_REQ_V = (1<<4) # macro
BASE_JD_REQ_FS_AFBC = (1<<13) # macro
BASE_JD_REQ_EVENT_COALESCE = (1<<5) # macro
BASE_JD_REQ_COHERENT_GROUP = (1<<6) # macro
BASE_JD_REQ_PERMON = (1<<7) # macro
BASE_JD_REQ_EXTERNAL_RESOURCES = (1<<8) # macro
BASE_JD_REQ_SOFT_JOB = (1<<9) # macro
BASE_JD_REQ_SOFT_DUMP_CPU_GPU_TIME = ((1<<9)|0x1) # macro
BASE_JD_REQ_SOFT_FENCE_TRIGGER = ((1<<9)|0x2) # macro
BASE_JD_REQ_SOFT_FENCE_WAIT = ((1<<9)|0x3) # macro
BASE_JD_REQ_SOFT_EVENT_WAIT = ((1<<9)|0x5) # macro
BASE_JD_REQ_SOFT_EVENT_SET = ((1<<9)|0x6) # macro
BASE_JD_REQ_SOFT_EVENT_RESET = ((1<<9)|0x7) # macro
BASE_JD_REQ_SOFT_DEBUG_COPY = ((1<<9)|0x8) # macro
BASE_JD_REQ_SOFT_JIT_ALLOC = ((1<<9)|0x9) # macro
BASE_JD_REQ_SOFT_JIT_FREE = ((1<<9)|0xa) # macro
BASE_JD_REQ_SOFT_EXT_RES_MAP = ((1<<9)|0xb) # macro
BASE_JD_REQ_SOFT_EXT_RES_UNMAP = ((1<<9)|0xc) # macro
BASE_JD_REQ_ONLY_COMPUTE = (1<<10) # macro
BASE_JD_REQ_SPECIFIC_COHERENT_GROUP = (1<<11) # macro
BASE_JD_REQ_EVENT_ONLY_ON_FAILURE = (1<<12) # macro
BASEP_JD_REQ_EVENT_NEVER = (1<<14) # macro
BASE_JD_REQ_SKIP_CACHE_START = (1<<15) # macro
BASE_JD_REQ_SKIP_CACHE_END = (1<<16) # macro
BASE_JD_REQ_JOB_SLOT = (1<<17) # macro
BASE_JD_REQ_START_RENDERPASS = (1<<18) # macro
BASE_JD_REQ_END_RENDERPASS = (1<<19) # macro
BASE_JD_REQ_LIMITED_CORE_MASK = (1<<20) # macro
BASE_JD_REQ_ATOM_TYPE = ((1<<0)|(1<<1)|(1<<2)|(1<<3)|(1<<4)|(1<<9)|(1<<10)) # macro
BASEP_JD_REQ_RESERVED = (~(BASE_JD_REQ_ATOM_TYPE|(1<<8)|(1<<12)|(1<<14)|(1<<5)|(1<<6)|(1<<11)|(1<<13)|(1<<7)|(1<<15)|(1<<16)|(1<<17)|(1<<18)|(1<<19)|(1<<20))) # macro
BASE_JD_REQ_SOFT_JOB_TYPE = ((1<<9)|0x1f) # macro
def BASE_JD_REQ_SOFT_JOB_OR_DEP(core_req):  # macro
   return (((core_req)&(1<<9)) or ((core_req)&((1<<0)|(1<<1)|(1<<2)|(1<<3)|(1<<4)|(1<<9)|(1<<10)))==(0))  
BASE_JD_PRIO_MEDIUM = (0) # macro
BASE_JD_PRIO_HIGH = (1) # macro
BASE_JD_PRIO_LOW = (2) # macro
BASE_JD_PRIO_REALTIME = (3) # macro
BASE_JD_NR_PRIO_LEVELS = 4 # macro
base_context_create_flags = ctypes.c_uint32
class struct_base_jd_udata(Structure):
    pass

struct_base_jd_udata._pack_ = 1 # source:False
struct_base_jd_udata._fields_ = [
    ('blob', ctypes.c_uint64 * 2),
]

base_jd_dep_type = ctypes.c_ubyte
base_jd_core_req = ctypes.c_uint32

# values for enumeration 'kbase_jd_atom_state'
kbase_jd_atom_state__enumvalues = {
    0: 'KBASE_JD_ATOM_STATE_UNUSED',
    1: 'KBASE_JD_ATOM_STATE_QUEUED',
    2: 'KBASE_JD_ATOM_STATE_IN_JS',
    3: 'KBASE_JD_ATOM_STATE_HW_COMPLETED',
    4: 'KBASE_JD_ATOM_STATE_COMPLETED',
}
KBASE_JD_ATOM_STATE_UNUSED = 0
KBASE_JD_ATOM_STATE_QUEUED = 1
KBASE_JD_ATOM_STATE_IN_JS = 2
KBASE_JD_ATOM_STATE_HW_COMPLETED = 3
KBASE_JD_ATOM_STATE_COMPLETED = 4
kbase_jd_atom_state = ctypes.c_uint32 # enum
base_atom_id = ctypes.c_ubyte
class struct_base_dependency(Structure):
    pass

struct_base_dependency._pack_ = 1 # source:False
struct_base_dependency._fields_ = [
    ('atom_id', ctypes.c_ubyte),
    ('dependency_type', ctypes.c_ubyte),
]

class struct_base_jd_fragment(Structure):
    pass

struct_base_jd_fragment._pack_ = 1 # source:False
struct_base_jd_fragment._fields_ = [
    ('norm_read_norm_write', ctypes.c_uint64),
    ('norm_read_forced_write', ctypes.c_uint64),
    ('forced_read_forced_write', ctypes.c_uint64),
    ('forced_read_norm_write', ctypes.c_uint64),
]

base_jd_prio = ctypes.c_ubyte
class struct_base_jd_atom_v2(Structure):
    pass

struct_base_jd_atom_v2._pack_ = 1 # source:False
struct_base_jd_atom_v2._fields_ = [
    ('jc', ctypes.c_uint64),
    ('udata', struct_base_jd_udata),
    ('extres_list', ctypes.c_uint64),
    ('nr_extres', ctypes.c_uint16),
    ('jit_id', ctypes.c_ubyte * 2),
    ('pre_dep', struct_base_dependency * 2),
    ('atom_number', ctypes.c_ubyte),
    ('prio', ctypes.c_ubyte),
    ('device_nr', ctypes.c_ubyte),
    ('jobslot', ctypes.c_ubyte),
    ('core_req', ctypes.c_uint32),
    ('renderpass_id', ctypes.c_ubyte),
    ('padding', ctypes.c_ubyte * 7),
]

class struct_base_jd_atom(Structure):
    pass

struct_base_jd_atom._pack_ = 1 # source:False
struct_base_jd_atom._fields_ = [
    ('seq_nr', ctypes.c_uint64),
    ('jc', ctypes.c_uint64),
    ('udata', struct_base_jd_udata),
    ('extres_list', ctypes.c_uint64),
    ('nr_extres', ctypes.c_uint16),
    ('jit_id', ctypes.c_ubyte * 2),
    ('pre_dep', struct_base_dependency * 2),
    ('atom_number', ctypes.c_ubyte),
    ('prio', ctypes.c_ubyte),
    ('device_nr', ctypes.c_ubyte),
    ('jobslot', ctypes.c_ubyte),
    ('core_req', ctypes.c_uint32),
    ('renderpass_id', ctypes.c_ubyte),
    ('padding', ctypes.c_ubyte * 7),
]

base_jd_atom = struct_base_jd_atom

# values for enumeration 'enum_mali_base_jm_kernel_h_884'
enum_mali_base_jm_kernel_h_884__enumvalues = {
    32768: 'BASE_JD_SW_EVENT_KERNEL',
    16384: 'BASE_JD_SW_EVENT',
    8192: 'BASE_JD_SW_EVENT_SUCCESS',
    0: 'BASE_JD_SW_EVENT_JOB',
    2048: 'BASE_JD_SW_EVENT_BAG',
    4096: 'BASE_JD_SW_EVENT_INFO',
    6144: 'BASE_JD_SW_EVENT_RESERVED',
    6144: 'BASE_JD_SW_EVENT_TYPE_MASK',
}
BASE_JD_SW_EVENT_KERNEL = 32768
BASE_JD_SW_EVENT = 16384
BASE_JD_SW_EVENT_SUCCESS = 8192
BASE_JD_SW_EVENT_JOB = 0
BASE_JD_SW_EVENT_BAG = 2048
BASE_JD_SW_EVENT_INFO = 4096
BASE_JD_SW_EVENT_RESERVED = 6144
BASE_JD_SW_EVENT_TYPE_MASK = 6144
enum_mali_base_jm_kernel_h_884 = ctypes.c_uint32 # enum

# values for enumeration 'base_jd_event_code'
base_jd_event_code__enumvalues = {
    0: 'BASE_JD_EVENT_RANGE_HW_NONFAULT_START',
    0: 'BASE_JD_EVENT_NOT_STARTED',
    1: 'BASE_JD_EVENT_DONE',
    3: 'BASE_JD_EVENT_STOPPED',
    4: 'BASE_JD_EVENT_TERMINATED',
    8: 'BASE_JD_EVENT_ACTIVE',
    64: 'BASE_JD_EVENT_RANGE_HW_NONFAULT_END',
    64: 'BASE_JD_EVENT_RANGE_HW_FAULT_OR_SW_ERROR_START',
    64: 'BASE_JD_EVENT_JOB_CONFIG_FAULT',
    65: 'BASE_JD_EVENT_JOB_POWER_FAULT',
    66: 'BASE_JD_EVENT_JOB_READ_FAULT',
    67: 'BASE_JD_EVENT_JOB_WRITE_FAULT',
    68: 'BASE_JD_EVENT_JOB_AFFINITY_FAULT',
    72: 'BASE_JD_EVENT_JOB_BUS_FAULT',
    80: 'BASE_JD_EVENT_INSTR_INVALID_PC',
    81: 'BASE_JD_EVENT_INSTR_INVALID_ENC',
    82: 'BASE_JD_EVENT_INSTR_TYPE_MISMATCH',
    83: 'BASE_JD_EVENT_INSTR_OPERAND_FAULT',
    84: 'BASE_JD_EVENT_INSTR_TLS_FAULT',
    85: 'BASE_JD_EVENT_INSTR_BARRIER_FAULT',
    86: 'BASE_JD_EVENT_INSTR_ALIGN_FAULT',
    88: 'BASE_JD_EVENT_DATA_INVALID_FAULT',
    89: 'BASE_JD_EVENT_TILE_RANGE_FAULT',
    90: 'BASE_JD_EVENT_STATE_FAULT',
    96: 'BASE_JD_EVENT_OUT_OF_MEMORY',
    127: 'BASE_JD_EVENT_UNKNOWN',
    128: 'BASE_JD_EVENT_DELAYED_BUS_FAULT',
    136: 'BASE_JD_EVENT_SHAREABILITY_FAULT',
    193: 'BASE_JD_EVENT_TRANSLATION_FAULT_LEVEL1',
    194: 'BASE_JD_EVENT_TRANSLATION_FAULT_LEVEL2',
    195: 'BASE_JD_EVENT_TRANSLATION_FAULT_LEVEL3',
    196: 'BASE_JD_EVENT_TRANSLATION_FAULT_LEVEL4',
    200: 'BASE_JD_EVENT_PERMISSION_FAULT',
    209: 'BASE_JD_EVENT_TRANSTAB_BUS_FAULT_LEVEL1',
    210: 'BASE_JD_EVENT_TRANSTAB_BUS_FAULT_LEVEL2',
    211: 'BASE_JD_EVENT_TRANSTAB_BUS_FAULT_LEVEL3',
    212: 'BASE_JD_EVENT_TRANSTAB_BUS_FAULT_LEVEL4',
    216: 'BASE_JD_EVENT_ACCESS_FLAG',
    16384: 'BASE_JD_EVENT_MEM_GROWTH_FAILED',
    16385: 'BASE_JD_EVENT_TIMED_OUT',
    16386: 'BASE_JD_EVENT_JOB_CANCELLED',
    16387: 'BASE_JD_EVENT_JOB_INVALID',
    16388: 'BASE_JD_EVENT_PM_EVENT',
    18435: 'BASE_JD_EVENT_BAG_INVALID',
    23551: 'BASE_JD_EVENT_RANGE_HW_FAULT_OR_SW_ERROR_END',
    24576: 'BASE_JD_EVENT_RANGE_SW_SUCCESS_START',
    24576: 'BASE_JD_EVENT_PROGRESS_REPORT',
    26624: 'BASE_JD_EVENT_BAG_DONE',
    28672: 'BASE_JD_EVENT_DRV_TERMINATED',
    31743: 'BASE_JD_EVENT_RANGE_SW_SUCCESS_END',
    49152: 'BASE_JD_EVENT_RANGE_KERNEL_ONLY_START',
    49152: 'BASE_JD_EVENT_REMOVED_FROM_NEXT',
    49153: 'BASE_JD_EVENT_END_RP_DONE',
    56319: 'BASE_JD_EVENT_RANGE_KERNEL_ONLY_END',
}
BASE_JD_EVENT_RANGE_HW_NONFAULT_START = 0
BASE_JD_EVENT_NOT_STARTED = 0
BASE_JD_EVENT_DONE = 1
BASE_JD_EVENT_STOPPED = 3
BASE_JD_EVENT_TERMINATED = 4
BASE_JD_EVENT_ACTIVE = 8
BASE_JD_EVENT_RANGE_HW_NONFAULT_END = 64
BASE_JD_EVENT_RANGE_HW_FAULT_OR_SW_ERROR_START = 64
BASE_JD_EVENT_JOB_CONFIG_FAULT = 64
BASE_JD_EVENT_JOB_POWER_FAULT = 65
BASE_JD_EVENT_JOB_READ_FAULT = 66
BASE_JD_EVENT_JOB_WRITE_FAULT = 67
BASE_JD_EVENT_JOB_AFFINITY_FAULT = 68
BASE_JD_EVENT_JOB_BUS_FAULT = 72
BASE_JD_EVENT_INSTR_INVALID_PC = 80
BASE_JD_EVENT_INSTR_INVALID_ENC = 81
BASE_JD_EVENT_INSTR_TYPE_MISMATCH = 82
BASE_JD_EVENT_INSTR_OPERAND_FAULT = 83
BASE_JD_EVENT_INSTR_TLS_FAULT = 84
BASE_JD_EVENT_INSTR_BARRIER_FAULT = 85
BASE_JD_EVENT_INSTR_ALIGN_FAULT = 86
BASE_JD_EVENT_DATA_INVALID_FAULT = 88
BASE_JD_EVENT_TILE_RANGE_FAULT = 89
BASE_JD_EVENT_STATE_FAULT = 90
BASE_JD_EVENT_OUT_OF_MEMORY = 96
BASE_JD_EVENT_UNKNOWN = 127
BASE_JD_EVENT_DELAYED_BUS_FAULT = 128
BASE_JD_EVENT_SHAREABILITY_FAULT = 136
BASE_JD_EVENT_TRANSLATION_FAULT_LEVEL1 = 193
BASE_JD_EVENT_TRANSLATION_FAULT_LEVEL2 = 194
BASE_JD_EVENT_TRANSLATION_FAULT_LEVEL3 = 195
BASE_JD_EVENT_TRANSLATION_FAULT_LEVEL4 = 196
BASE_JD_EVENT_PERMISSION_FAULT = 200
BASE_JD_EVENT_TRANSTAB_BUS_FAULT_LEVEL1 = 209
BASE_JD_EVENT_TRANSTAB_BUS_FAULT_LEVEL2 = 210
BASE_JD_EVENT_TRANSTAB_BUS_FAULT_LEVEL3 = 211
BASE_JD_EVENT_TRANSTAB_BUS_FAULT_LEVEL4 = 212
BASE_JD_EVENT_ACCESS_FLAG = 216
BASE_JD_EVENT_MEM_GROWTH_FAILED = 16384
BASE_JD_EVENT_TIMED_OUT = 16385
BASE_JD_EVENT_JOB_CANCELLED = 16386
BASE_JD_EVENT_JOB_INVALID = 16387
BASE_JD_EVENT_PM_EVENT = 16388
BASE_JD_EVENT_BAG_INVALID = 18435
BASE_JD_EVENT_RANGE_HW_FAULT_OR_SW_ERROR_END = 23551
BASE_JD_EVENT_RANGE_SW_SUCCESS_START = 24576
BASE_JD_EVENT_PROGRESS_REPORT = 24576
BASE_JD_EVENT_BAG_DONE = 26624
BASE_JD_EVENT_DRV_TERMINATED = 28672
BASE_JD_EVENT_RANGE_SW_SUCCESS_END = 31743
BASE_JD_EVENT_RANGE_KERNEL_ONLY_START = 49152
BASE_JD_EVENT_REMOVED_FROM_NEXT = 49152
BASE_JD_EVENT_END_RP_DONE = 49153
BASE_JD_EVENT_RANGE_KERNEL_ONLY_END = 56319
base_jd_event_code = ctypes.c_uint32 # enum
class struct_base_jd_event_v2(Structure):
    pass

struct_base_jd_event_v2._pack_ = 1 # source:False
struct_base_jd_event_v2._fields_ = [
    ('event_code', base_jd_event_code),
    ('atom_number', ctypes.c_ubyte),
    ('PADDING_0', ctypes.c_ubyte * 3),
    ('udata', struct_base_jd_udata),
]

class struct_base_dump_cpu_gpu_counters(Structure):
    pass

struct_base_dump_cpu_gpu_counters._pack_ = 1 # source:False
struct_base_dump_cpu_gpu_counters._fields_ = [
    ('system_time', ctypes.c_uint64),
    ('cycle_counter', ctypes.c_uint64),
    ('sec', ctypes.c_uint64),
    ('usec', ctypes.c_uint32),
    ('padding', ctypes.c_ubyte * 36),
]

__all__ = \
    ['BASEP_CONTEXT_CREATE_ALLOWED_FLAGS',
    'BASEP_CONTEXT_CREATE_KERNEL_FLAGS',
    'BASEP_CONTEXT_FLAG_JOB_DUMP_DISABLED',
    'BASEP_CONTEXT_MMU_GROUP_ID_MASK',
    'BASEP_CONTEXT_MMU_GROUP_ID_SHIFT', 'BASEP_JD_REQ_EVENT_NEVER',
    'BASEP_JD_REQ_RESERVED', 'BASEP_MEM_FLAGS_KERNEL_ONLY',
    'BASEP_MEM_GROUP_ID_SHIFT', 'BASEP_MEM_INVALID_HANDLE',
    'BASEP_MEM_NO_USER_FREE', 'BASEP_MEM_PERFORM_JIT_TRIM',
    'BASEP_MEM_PERMANENT_KERNEL_MAPPING',
    'BASEP_MEM_WRITE_ALLOC_PAGES_HANDLE',
    'BASE_CONTEXT_CCTX_EMBEDDED', 'BASE_CONTEXT_CREATE_FLAG_NONE',
    'BASE_CONTEXT_SYSTEM_MONITOR_SUBMIT_DISABLED',
    'BASE_JD_ATOM_COUNT', 'BASE_JD_DEP_TYPE_DATA',
    'BASE_JD_DEP_TYPE_INVALID', 'BASE_JD_DEP_TYPE_ORDER',
    'BASE_JD_EVENT_ACCESS_FLAG', 'BASE_JD_EVENT_ACTIVE',
    'BASE_JD_EVENT_BAG_DONE', 'BASE_JD_EVENT_BAG_INVALID',
    'BASE_JD_EVENT_DATA_INVALID_FAULT',
    'BASE_JD_EVENT_DELAYED_BUS_FAULT', 'BASE_JD_EVENT_DONE',
    'BASE_JD_EVENT_DRV_TERMINATED', 'BASE_JD_EVENT_END_RP_DONE',
    'BASE_JD_EVENT_INSTR_ALIGN_FAULT',
    'BASE_JD_EVENT_INSTR_BARRIER_FAULT',
    'BASE_JD_EVENT_INSTR_INVALID_ENC',
    'BASE_JD_EVENT_INSTR_INVALID_PC',
    'BASE_JD_EVENT_INSTR_OPERAND_FAULT',
    'BASE_JD_EVENT_INSTR_TLS_FAULT',
    'BASE_JD_EVENT_INSTR_TYPE_MISMATCH',
    'BASE_JD_EVENT_JOB_AFFINITY_FAULT', 'BASE_JD_EVENT_JOB_BUS_FAULT',
    'BASE_JD_EVENT_JOB_CANCELLED', 'BASE_JD_EVENT_JOB_CONFIG_FAULT',
    'BASE_JD_EVENT_JOB_INVALID', 'BASE_JD_EVENT_JOB_POWER_FAULT',
    'BASE_JD_EVENT_JOB_READ_FAULT', 'BASE_JD_EVENT_JOB_WRITE_FAULT',
    'BASE_JD_EVENT_MEM_GROWTH_FAILED', 'BASE_JD_EVENT_NOT_STARTED',
    'BASE_JD_EVENT_OUT_OF_MEMORY', 'BASE_JD_EVENT_PERMISSION_FAULT',
    'BASE_JD_EVENT_PM_EVENT', 'BASE_JD_EVENT_PROGRESS_REPORT',
    'BASE_JD_EVENT_RANGE_HW_FAULT_OR_SW_ERROR_END',
    'BASE_JD_EVENT_RANGE_HW_FAULT_OR_SW_ERROR_START',
    'BASE_JD_EVENT_RANGE_HW_NONFAULT_END',
    'BASE_JD_EVENT_RANGE_HW_NONFAULT_START',
    'BASE_JD_EVENT_RANGE_KERNEL_ONLY_END',
    'BASE_JD_EVENT_RANGE_KERNEL_ONLY_START',
    'BASE_JD_EVENT_RANGE_SW_SUCCESS_END',
    'BASE_JD_EVENT_RANGE_SW_SUCCESS_START',
    'BASE_JD_EVENT_REMOVED_FROM_NEXT',
    'BASE_JD_EVENT_SHAREABILITY_FAULT', 'BASE_JD_EVENT_STATE_FAULT',
    'BASE_JD_EVENT_STOPPED', 'BASE_JD_EVENT_TERMINATED',
    'BASE_JD_EVENT_TILE_RANGE_FAULT', 'BASE_JD_EVENT_TIMED_OUT',
    'BASE_JD_EVENT_TRANSLATION_FAULT_LEVEL1',
    'BASE_JD_EVENT_TRANSLATION_FAULT_LEVEL2',
    'BASE_JD_EVENT_TRANSLATION_FAULT_LEVEL3',
    'BASE_JD_EVENT_TRANSLATION_FAULT_LEVEL4',
    'BASE_JD_EVENT_TRANSTAB_BUS_FAULT_LEVEL1',
    'BASE_JD_EVENT_TRANSTAB_BUS_FAULT_LEVEL2',
    'BASE_JD_EVENT_TRANSTAB_BUS_FAULT_LEVEL3',
    'BASE_JD_EVENT_TRANSTAB_BUS_FAULT_LEVEL4',
    'BASE_JD_EVENT_UNKNOWN', 'BASE_JD_NR_PRIO_LEVELS',
    'BASE_JD_PRIO_HIGH', 'BASE_JD_PRIO_LOW', 'BASE_JD_PRIO_MEDIUM',
    'BASE_JD_PRIO_REALTIME', 'BASE_JD_REQ_ATOM_TYPE',
    'BASE_JD_REQ_CF', 'BASE_JD_REQ_COHERENT_GROUP', 'BASE_JD_REQ_CS',
    'BASE_JD_REQ_DEP', 'BASE_JD_REQ_END_RENDERPASS',
    'BASE_JD_REQ_EVENT_COALESCE', 'BASE_JD_REQ_EVENT_ONLY_ON_FAILURE',
    'BASE_JD_REQ_EXTERNAL_RESOURCES', 'BASE_JD_REQ_FS',
    'BASE_JD_REQ_FS_AFBC', 'BASE_JD_REQ_JOB_SLOT',
    'BASE_JD_REQ_LIMITED_CORE_MASK', 'BASE_JD_REQ_ONLY_COMPUTE',
    'BASE_JD_REQ_PERMON', 'BASE_JD_REQ_SKIP_CACHE_END',
    'BASE_JD_REQ_SKIP_CACHE_START', 'BASE_JD_REQ_SOFT_DEBUG_COPY',
    'BASE_JD_REQ_SOFT_DUMP_CPU_GPU_TIME',
    'BASE_JD_REQ_SOFT_EVENT_RESET', 'BASE_JD_REQ_SOFT_EVENT_SET',
    'BASE_JD_REQ_SOFT_EVENT_WAIT', 'BASE_JD_REQ_SOFT_EXT_RES_MAP',
    'BASE_JD_REQ_SOFT_EXT_RES_UNMAP',
    'BASE_JD_REQ_SOFT_FENCE_TRIGGER', 'BASE_JD_REQ_SOFT_FENCE_WAIT',
    'BASE_JD_REQ_SOFT_JIT_ALLOC', 'BASE_JD_REQ_SOFT_JIT_FREE',
    'BASE_JD_REQ_SOFT_JOB', 'BASE_JD_REQ_SOFT_JOB_TYPE',
    'BASE_JD_REQ_SPECIFIC_COHERENT_GROUP',
    'BASE_JD_REQ_START_RENDERPASS', 'BASE_JD_REQ_T', 'BASE_JD_REQ_V',
    'BASE_JD_RP_COUNT', 'BASE_JD_SOFT_EVENT_RESET',
    'BASE_JD_SOFT_EVENT_SET', 'BASE_JD_SW_EVENT',
    'BASE_JD_SW_EVENT_BAG', 'BASE_JD_SW_EVENT_INFO',
    'BASE_JD_SW_EVENT_JOB', 'BASE_JD_SW_EVENT_KERNEL',
    'BASE_JD_SW_EVENT_RESERVED', 'BASE_JD_SW_EVENT_SUCCESS',
    'BASE_JD_SW_EVENT_TYPE_MASK', 'BASE_JIT_ALLOC_HEAP_INFO_IS_SIZE',
    'BASE_JIT_ALLOC_MEM_TILER_ALIGN_TOP',
    'BASE_JIT_ALLOC_VALID_FLAGS', 'BASE_MEM_CACHED_CPU',
    'BASE_MEM_COHERENT_LOCAL', 'BASE_MEM_COHERENT_SYSTEM',
    'BASE_MEM_COHERENT_SYSTEM_REQUIRED', 'BASE_MEM_COOKIE_BASE',
    'BASE_MEM_DONT_NEED', 'BASE_MEM_FLAGS_INPUT_MASK',
    'BASE_MEM_FLAGS_NR_BITS', 'BASE_MEM_FLAGS_OUTPUT_MASK',
    'BASE_MEM_FLAGS_RESERVED', 'BASE_MEM_FLAG_MAP_FIXED',
    'BASE_MEM_GPU_VA_SAME_4GB_PAGE', 'BASE_MEM_GROUP_ID_MASK',
    'BASE_MEM_GROW_ON_GPF', 'BASE_MEM_IMPORT_SHARED',
    'BASE_MEM_IMPORT_SYNC_ON_MAP_UNMAP', 'BASE_MEM_KERNEL_SYNC',
    'BASE_MEM_MAP_TRACKING_HANDLE', 'BASE_MEM_MMU_DUMP_HANDLE',
    'BASE_MEM_NEED_MMAP', 'BASE_MEM_PROTECTED',
    'BASE_MEM_PROT_CPU_RD', 'BASE_MEM_PROT_CPU_WR',
    'BASE_MEM_PROT_GPU_EX', 'BASE_MEM_PROT_GPU_RD',
    'BASE_MEM_PROT_GPU_WR', 'BASE_MEM_RESERVED_BIT_19',
    'BASE_MEM_RESERVED_BIT_8', 'BASE_MEM_SAME_VA',
    'BASE_MEM_TILER_ALIGN_TOP', 'BASE_MEM_TRACE_BUFFER_HANDLE',
    'BASE_MEM_UNCACHED_GPU',
    'BASE_TLSTREAM_ENABLE_LATENCY_TRACEPOINTS',
    'BASE_TLSTREAM_FLAGS_MASK', 'BASE_TLSTREAM_JOB_DUMPING_ENABLED',
    'KBASE_JD_ATOM_STATE_COMPLETED',
    'KBASE_JD_ATOM_STATE_HW_COMPLETED', 'KBASE_JD_ATOM_STATE_IN_JS',
    'KBASE_JD_ATOM_STATE_QUEUED', 'KBASE_JD_ATOM_STATE_UNUSED',
    '_UAPI_BASE_JM_KERNEL_H_', 'base_atom_id',
    'base_context_create_flags', 'base_jd_atom', 'base_jd_core_req',
    'base_jd_dep_type', 'base_jd_event_code', 'base_jd_prio',
    'enum_mali_base_jm_kernel_h_884', 'kbase_jd_atom_state',
    'struct_base_dependency', 'struct_base_dump_cpu_gpu_counters',
    'struct_base_jd_atom', 'struct_base_jd_atom_v2',
    'struct_base_jd_event_v2', 'struct_base_jd_fragment',
    'struct_base_jd_udata']
