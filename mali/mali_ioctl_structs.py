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





class struct_kbase_ioctl_version_check(Structure):
    pass

struct_kbase_ioctl_version_check._pack_ = 1 # source:False
struct_kbase_ioctl_version_check._fields_ = [
    ('major', ctypes.c_uint16),
    ('minor', ctypes.c_uint16),
]

class struct_kbase_ioctl_job_submit(Structure):
    pass

struct_kbase_ioctl_job_submit._pack_ = 1 # source:False
struct_kbase_ioctl_job_submit._fields_ = [
    ('addr', ctypes.c_uint64),
    ('nr_atoms', ctypes.c_uint32),
    ('stride', ctypes.c_uint32),
]

class struct_kbase_ioctl_soft_event_update(Structure):
    pass

struct_kbase_ioctl_soft_event_update._pack_ = 1 # source:False
struct_kbase_ioctl_soft_event_update._fields_ = [
    ('event', ctypes.c_uint64),
    ('new_status', ctypes.c_uint32),
    ('flags', ctypes.c_uint32),
]

class struct_kbase_kinstr_jm_fd_out(Structure):
    pass

struct_kbase_kinstr_jm_fd_out._pack_ = 1 # source:False
struct_kbase_kinstr_jm_fd_out._fields_ = [
    ('size', ctypes.c_uint16),
    ('version', ctypes.c_ubyte),
    ('padding', ctypes.c_ubyte * 5),
]

class struct_kbase_kinstr_jm_fd_in(Structure):
    pass

struct_kbase_kinstr_jm_fd_in._pack_ = 1 # source:False
struct_kbase_kinstr_jm_fd_in._fields_ = [
    ('count', ctypes.c_uint16),
    ('padding', ctypes.c_ubyte * 6),
]

class union_kbase_kinstr_jm_fd(Union):
    _pack_ = 1 # source:False
    _fields_ = [
    ('in', struct_kbase_kinstr_jm_fd_in),
    ('out', struct_kbase_kinstr_jm_fd_out),
     ]

class struct_kbase_ioctl_set_flags(Structure):
    pass

struct_kbase_ioctl_set_flags._pack_ = 1 # source:False
struct_kbase_ioctl_set_flags._fields_ = [
    ('create_flags', ctypes.c_uint32),
]

class struct_kbase_ioctl_get_gpuprops(Structure):
    pass

struct_kbase_ioctl_get_gpuprops._pack_ = 1 # source:False
struct_kbase_ioctl_get_gpuprops._fields_ = [
    ('buffer', ctypes.c_uint64),
    ('size', ctypes.c_uint32),
    ('flags', ctypes.c_uint32),
]

class union_kbase_ioctl_mem_alloc(Union):
    pass

class struct_inner_1(Structure):
    pass

struct_inner_1._pack_ = 1 # source:False
struct_inner_1._fields_ = [
    ('va_pages', ctypes.c_uint64),
    ('commit_pages', ctypes.c_uint64),
    ('extension', ctypes.c_uint64),
    ('flags', ctypes.c_uint64),
]

class struct_inner_2(Structure):
    pass

struct_inner_2._pack_ = 1 # source:False
struct_inner_2._fields_ = [
    ('flags', ctypes.c_uint64),
    ('gpu_va', ctypes.c_uint64),
]

union_kbase_ioctl_mem_alloc._pack_ = 1 # source:False
union_kbase_ioctl_mem_alloc._fields_ = [
    ('_in', struct_inner_1),
    ('out', struct_inner_2),
    ('PADDING_0', ctypes.c_ubyte * 16),
]

class union_kbase_ioctl_mem_query(Union):
    pass

class struct_inner_3(Structure):
    pass

struct_inner_3._pack_ = 1 # source:False
struct_inner_3._fields_ = [
    ('gpu_addr', ctypes.c_uint64),
    ('query', ctypes.c_uint64),
]

class struct_inner_4(Structure):
    pass

struct_inner_4._pack_ = 1 # source:False
struct_inner_4._fields_ = [
    ('value', ctypes.c_uint64),
]

union_kbase_ioctl_mem_query._pack_ = 1 # source:False
union_kbase_ioctl_mem_query._fields_ = [
    ('in', struct_inner_3),
    ('out', struct_inner_4),
    ('PADDING_0', ctypes.c_ubyte * 8),
]

class struct_kbase_ioctl_mem_free(Structure):
    pass

struct_kbase_ioctl_mem_free._pack_ = 1 # source:False
struct_kbase_ioctl_mem_free._fields_ = [
    ('gpu_addr', ctypes.c_uint64),
]

class struct_kbase_ioctl_hwcnt_reader_setup(Structure):
    pass

struct_kbase_ioctl_hwcnt_reader_setup._pack_ = 1 # source:False
struct_kbase_ioctl_hwcnt_reader_setup._fields_ = [
    ('buffer_count', ctypes.c_uint32),
    ('fe_bm', ctypes.c_uint32),
    ('shader_bm', ctypes.c_uint32),
    ('tiler_bm', ctypes.c_uint32),
    ('mmu_l2_bm', ctypes.c_uint32),
]

class struct_kbase_ioctl_hwcnt_enable(Structure):
    pass

struct_kbase_ioctl_hwcnt_enable._pack_ = 1 # source:False
struct_kbase_ioctl_hwcnt_enable._fields_ = [
    ('dump_buffer', ctypes.c_uint64),
    ('fe_bm', ctypes.c_uint32),
    ('shader_bm', ctypes.c_uint32),
    ('tiler_bm', ctypes.c_uint32),
    ('mmu_l2_bm', ctypes.c_uint32),
]

class struct_kbase_ioctl_hwcnt_values(Structure):
    pass

struct_kbase_ioctl_hwcnt_values._pack_ = 1 # source:False
struct_kbase_ioctl_hwcnt_values._fields_ = [
    ('data', ctypes.c_uint64),
    ('size', ctypes.c_uint32),
    ('padding', ctypes.c_uint32),
]

class struct_kbase_ioctl_disjoint_query(Structure):
    pass

struct_kbase_ioctl_disjoint_query._pack_ = 1 # source:False
struct_kbase_ioctl_disjoint_query._fields_ = [
    ('counter', ctypes.c_uint32),
]

class struct_kbase_ioctl_get_ddk_version(Structure):
    pass

struct_kbase_ioctl_get_ddk_version._pack_ = 1 # source:False
struct_kbase_ioctl_get_ddk_version._fields_ = [
    ('version_buffer', ctypes.c_uint64),
    ('size', ctypes.c_uint32),
    ('padding', ctypes.c_uint32),
]

class struct_kbase_ioctl_mem_jit_init_10_2(Structure):
    pass

struct_kbase_ioctl_mem_jit_init_10_2._pack_ = 1 # source:False
struct_kbase_ioctl_mem_jit_init_10_2._fields_ = [
    ('va_pages', ctypes.c_uint64),
]

class struct_kbase_ioctl_mem_jit_init_11_5(Structure):
    pass

struct_kbase_ioctl_mem_jit_init_11_5._pack_ = 1 # source:False
struct_kbase_ioctl_mem_jit_init_11_5._fields_ = [
    ('va_pages', ctypes.c_uint64),
    ('max_allocations', ctypes.c_ubyte),
    ('trim_level', ctypes.c_ubyte),
    ('group_id', ctypes.c_ubyte),
    ('padding', ctypes.c_ubyte * 5),
]

class struct_kbase_ioctl_mem_jit_init(Structure):
    pass

struct_kbase_ioctl_mem_jit_init._pack_ = 1 # source:False
struct_kbase_ioctl_mem_jit_init._fields_ = [
    ('va_pages', ctypes.c_uint64),
    ('max_allocations', ctypes.c_ubyte),
    ('trim_level', ctypes.c_ubyte),
    ('group_id', ctypes.c_ubyte),
    ('padding', ctypes.c_ubyte * 5),
    ('phys_pages', ctypes.c_uint64),
]

class struct_kbase_ioctl_mem_sync(Structure):
    pass

struct_kbase_ioctl_mem_sync._pack_ = 1 # source:False
struct_kbase_ioctl_mem_sync._fields_ = [
    ('handle', ctypes.c_uint64),
    ('user_addr', ctypes.c_uint64),
    ('size', ctypes.c_uint64),
    ('type', ctypes.c_ubyte),
    ('padding', ctypes.c_ubyte * 7),
]

class union_kbase_ioctl_mem_find_cpu_offset(Union):
    pass

class struct_inner_5(Structure):
    pass

struct_inner_5._pack_ = 1 # source:False
struct_inner_5._fields_ = [
    ('gpu_addr', ctypes.c_uint64),
    ('cpu_addr', ctypes.c_uint64),
    ('size', ctypes.c_uint64),
]

class struct_inner_6(Structure):
    pass

struct_inner_6._pack_ = 1 # source:False
struct_inner_6._fields_ = [
    ('offset', ctypes.c_uint64),
]

union_kbase_ioctl_mem_find_cpu_offset._pack_ = 1 # source:False
union_kbase_ioctl_mem_find_cpu_offset._fields_ = [
    ('in', struct_inner_5),
    ('out', struct_inner_6),
    ('PADDING_0', ctypes.c_ubyte * 16),
]

class struct_kbase_ioctl_get_context_id(Structure):
    pass

struct_kbase_ioctl_get_context_id._pack_ = 1 # source:False
struct_kbase_ioctl_get_context_id._fields_ = [
    ('id', ctypes.c_uint32),
]

class struct_kbase_ioctl_tlstream_acquire(Structure):
    pass

struct_kbase_ioctl_tlstream_acquire._pack_ = 1 # source:False
struct_kbase_ioctl_tlstream_acquire._fields_ = [
    ('flags', ctypes.c_uint32),
]

class struct_kbase_ioctl_mem_commit(Structure):
    pass

struct_kbase_ioctl_mem_commit._pack_ = 1 # source:False
struct_kbase_ioctl_mem_commit._fields_ = [
    ('gpu_addr', ctypes.c_uint64),
    ('pages', ctypes.c_uint64),
]

class union_kbase_ioctl_mem_alias(Union):
    pass

class struct_inner_7(Structure):
    pass

struct_inner_7._pack_ = 1 # source:False
struct_inner_7._fields_ = [
    ('flags', ctypes.c_uint64),
    ('stride', ctypes.c_uint64),
    ('nents', ctypes.c_uint64),
    ('aliasing_info', ctypes.c_uint64),
]

class struct_inner_8(Structure):
    pass

struct_inner_8._pack_ = 1 # source:False
struct_inner_8._fields_ = [
    ('flags', ctypes.c_uint64),
    ('gpu_va', ctypes.c_uint64),
    ('va_pages', ctypes.c_uint64),
]

union_kbase_ioctl_mem_alias._pack_ = 1 # source:False
union_kbase_ioctl_mem_alias._fields_ = [
    ('in', struct_inner_7),
    ('out', struct_inner_8),
    ('PADDING_0', ctypes.c_ubyte * 8),
]

class union_kbase_ioctl_mem_import(Union):
    pass

class struct_inner_9(Structure):
    pass

struct_inner_9._pack_ = 1 # source:False
struct_inner_9._fields_ = [
    ('flags', ctypes.c_uint64),
    ('phandle', ctypes.c_uint64),
    ('type', ctypes.c_uint32),
    ('padding', ctypes.c_uint32),
]

class struct_inner_10(Structure):
    pass

struct_inner_10._pack_ = 1 # source:False
struct_inner_10._fields_ = [
    ('flags', ctypes.c_uint64),
    ('gpu_va', ctypes.c_uint64),
    ('va_pages', ctypes.c_uint64),
]

union_kbase_ioctl_mem_import._pack_ = 1 # source:False
union_kbase_ioctl_mem_import._fields_ = [
    ('in', struct_inner_9),
    ('out', struct_inner_10),
]

class struct_kbase_ioctl_mem_flags_change(Structure):
    pass

struct_kbase_ioctl_mem_flags_change._pack_ = 1 # source:False
struct_kbase_ioctl_mem_flags_change._fields_ = [
    ('gpu_va', ctypes.c_uint64),
    ('flags', ctypes.c_uint64),
    ('mask', ctypes.c_uint64),
]

class struct_kbase_ioctl_stream_create(Structure):
    pass

struct_kbase_ioctl_stream_create._pack_ = 1 # source:False
struct_kbase_ioctl_stream_create._fields_ = [
    ('name', ctypes.c_char * 32),
]

class struct_kbase_ioctl_fence_validate(Structure):
    pass

struct_kbase_ioctl_fence_validate._pack_ = 1 # source:False
struct_kbase_ioctl_fence_validate._fields_ = [
    ('fd', ctypes.c_int32),
]

class struct_kbase_ioctl_mem_profile_add(Structure):
    pass

struct_kbase_ioctl_mem_profile_add._pack_ = 1 # source:False
struct_kbase_ioctl_mem_profile_add._fields_ = [
    ('buffer', ctypes.c_uint64),
    ('len', ctypes.c_uint32),
    ('padding', ctypes.c_uint32),
]

class struct_kbase_ioctl_sticky_resource_map(Structure):
    pass

struct_kbase_ioctl_sticky_resource_map._pack_ = 1 # source:False
struct_kbase_ioctl_sticky_resource_map._fields_ = [
    ('count', ctypes.c_uint64),
    ('address', ctypes.c_uint64),
]

class struct_kbase_ioctl_sticky_resource_unmap(Structure):
    pass

struct_kbase_ioctl_sticky_resource_unmap._pack_ = 1 # source:False
struct_kbase_ioctl_sticky_resource_unmap._fields_ = [
    ('count', ctypes.c_uint64),
    ('address', ctypes.c_uint64),
]

class union_kbase_ioctl_mem_find_gpu_start_and_offset(Union):
    pass

class struct_inner_11(Structure):
    pass

struct_inner_11._pack_ = 1 # source:False
struct_inner_11._fields_ = [
    ('gpu_addr', ctypes.c_uint64),
    ('size', ctypes.c_uint64),
]

class struct_inner_12(Structure):
    pass

struct_inner_12._pack_ = 1 # source:False
struct_inner_12._fields_ = [
    ('start', ctypes.c_uint64),
    ('offset', ctypes.c_uint64),
]

union_kbase_ioctl_mem_find_gpu_start_and_offset._pack_ = 1 # source:False
union_kbase_ioctl_mem_find_gpu_start_and_offset._fields_ = [
    ('in', struct_inner_11),
    ('out', struct_inner_12),
]

class union_kbase_ioctl_cinstr_gwt_dump(Union):
    pass

class struct_inner_13(Structure):
    pass

struct_inner_13._pack_ = 1 # source:False
struct_inner_13._fields_ = [
    ('addr_buffer', ctypes.c_uint64),
    ('size_buffer', ctypes.c_uint64),
    ('len', ctypes.c_uint32),
    ('padding', ctypes.c_uint32),
]

class struct_inner_14(Structure):
    pass

struct_inner_14._pack_ = 1 # source:False
struct_inner_14._fields_ = [
    ('no_of_addr_collected', ctypes.c_uint32),
    ('more_data_available', ctypes.c_ubyte),
    ('padding', ctypes.c_ubyte * 27),
]

union_kbase_ioctl_cinstr_gwt_dump._pack_ = 1 # source:False
union_kbase_ioctl_cinstr_gwt_dump._fields_ = [
    ('in', struct_inner_13),
    ('out', struct_inner_14),
]

class struct_kbase_ioctl_mem_exec_init(Structure):
    pass

struct_kbase_ioctl_mem_exec_init._pack_ = 1 # source:False
struct_kbase_ioctl_mem_exec_init._fields_ = [
    ('va_pages', ctypes.c_uint64),
]

class union_kbase_ioctl_get_cpu_gpu_timeinfo(Union):
    pass

class struct_inner_15(Structure):
    pass

struct_inner_15._pack_ = 1 # source:False
struct_inner_15._fields_ = [
    ('request_flags', ctypes.c_uint32),
    ('paddings', ctypes.c_uint32 * 7),
]

class struct_inner_16(Structure):
    pass

struct_inner_16._pack_ = 1 # source:False
struct_inner_16._fields_ = [
    ('sec', ctypes.c_uint64),
    ('nsec', ctypes.c_uint32),
    ('padding', ctypes.c_uint32),
    ('timestamp', ctypes.c_uint64),
    ('cycle_counter', ctypes.c_uint64),
]

union_kbase_ioctl_get_cpu_gpu_timeinfo._pack_ = 1 # source:False
union_kbase_ioctl_get_cpu_gpu_timeinfo._fields_ = [
    ('in', struct_inner_15),
    ('out', struct_inner_16),
]

class struct_kbase_ioctl_context_priority_check(Structure):
    pass

struct_kbase_ioctl_context_priority_check._pack_ = 1 # source:False
struct_kbase_ioctl_context_priority_check._fields_ = [
    ('priority', ctypes.c_ubyte),
]

class struct_kbase_ioctl_set_limited_core_count(Structure):
    pass

struct_kbase_ioctl_set_limited_core_count._pack_ = 1 # source:False
struct_kbase_ioctl_set_limited_core_count._fields_ = [
    ('max_core_count', ctypes.c_ubyte),
]

class struct_mali_exynos_ioctl_amigo_flags(Structure):
    pass

struct_mali_exynos_ioctl_amigo_flags._pack_ = 1 # source:False
struct_mali_exynos_ioctl_amigo_flags._fields_ = [
    ('flags', ctypes.c_uint32),
]

class struct_mali_exynos_ioctl_gts_info(Structure):
    pass

struct_mali_exynos_ioctl_gts_info._pack_ = 1 # source:False
struct_mali_exynos_ioctl_gts_info._fields_ = [
    ('util_avg', ctypes.c_uint32),
    ('hcm_mode', ctypes.c_uint32),
    ('out_data', ctypes.c_uint64 * 4),
    ('input', ctypes.c_uint64),
    ('input2', ctypes.c_uint64),
    ('freq', ctypes.c_uint64),
    ('flimit', ctypes.c_uint64),
]

class struct_mali_exynos_ioctl_hcm_pmqos(Structure):
    pass

struct_mali_exynos_ioctl_hcm_pmqos._pack_ = 1 # source:False
struct_mali_exynos_ioctl_hcm_pmqos._fields_ = [
    ('mode', ctypes.c_uint32),
]

class struct_mali_exynos_ioctl_mem_usage_add(Structure):
    pass

struct_mali_exynos_ioctl_mem_usage_add._pack_ = 1 # source:False
struct_mali_exynos_ioctl_mem_usage_add._fields_ = [
    ('gl_mem_usage', ctypes.c_uint64),
]

class struct_mali_exynos_ioctl_cmar_boost(Structure):
    pass

struct_mali_exynos_ioctl_cmar_boost._pack_ = 1 # source:False
struct_mali_exynos_ioctl_cmar_boost._fields_ = [
    ('flags', ctypes.c_uint32),
]

class struct_kbase_ioctl_slsi_egp(Structure):
    pass

struct_kbase_ioctl_slsi_egp._pack_ = 1 # source:False
struct_kbase_ioctl_slsi_egp._fields_ = [
    ('start_timestamp', ctypes.c_uint64),
    ('end_timestamp', ctypes.c_uint64),
]

class struct_kbase_ioctl_slsi_singlebuffer_boost_flags(Structure):
    pass

struct_kbase_ioctl_slsi_singlebuffer_boost_flags._pack_ = 1 # source:False
struct_kbase_ioctl_slsi_singlebuffer_boost_flags._fields_ = [
    ('flags', ctypes.c_uint32),
]

__all__ = \
    ['struct_inner_1', 'struct_inner_10', 'struct_inner_11',
    'struct_inner_12', 'struct_inner_13', 'struct_inner_14',
    'struct_inner_15', 'struct_inner_16', 'struct_inner_2',
    'struct_inner_3', 'struct_inner_4', 'struct_inner_5',
    'struct_inner_6', 'struct_inner_7', 'struct_inner_8',
    'struct_inner_9', 'struct_kbase_ioctl_context_priority_check',
    'struct_kbase_ioctl_disjoint_query',
    'struct_kbase_ioctl_fence_validate',
    'struct_kbase_ioctl_get_context_id',
    'struct_kbase_ioctl_get_ddk_version',
    'struct_kbase_ioctl_get_gpuprops',
    'struct_kbase_ioctl_hwcnt_enable',
    'struct_kbase_ioctl_hwcnt_reader_setup',
    'struct_kbase_ioctl_hwcnt_values',
    'struct_kbase_ioctl_job_submit', 'struct_kbase_ioctl_mem_commit',
    'struct_kbase_ioctl_mem_exec_init',
    'struct_kbase_ioctl_mem_flags_change',
    'struct_kbase_ioctl_mem_free', 'struct_kbase_ioctl_mem_jit_init',
    'struct_kbase_ioctl_mem_jit_init_10_2',
    'struct_kbase_ioctl_mem_jit_init_11_5',
    'struct_kbase_ioctl_mem_profile_add',
    'struct_kbase_ioctl_mem_sync', 'struct_kbase_ioctl_set_flags',
    'struct_kbase_ioctl_set_limited_core_count',
    'struct_kbase_ioctl_slsi_egp',
    'struct_kbase_ioctl_slsi_singlebuffer_boost_flags',
    'struct_kbase_ioctl_soft_event_update',
    'struct_kbase_ioctl_sticky_resource_map',
    'struct_kbase_ioctl_sticky_resource_unmap',
    'struct_kbase_ioctl_stream_create',
    'struct_kbase_ioctl_tlstream_acquire',
    'struct_kbase_ioctl_version_check',
    'struct_kbase_kinstr_jm_fd_in', 'struct_kbase_kinstr_jm_fd_out',
    'struct_mali_exynos_ioctl_amigo_flags',
    'struct_mali_exynos_ioctl_cmar_boost',
    'struct_mali_exynos_ioctl_gts_info',
    'struct_mali_exynos_ioctl_hcm_pmqos',
    'struct_mali_exynos_ioctl_mem_usage_add',
    'union_kbase_ioctl_cinstr_gwt_dump',
    'union_kbase_ioctl_get_cpu_gpu_timeinfo',
    'union_kbase_ioctl_mem_alias', 'union_kbase_ioctl_mem_alloc',
    'union_kbase_ioctl_mem_find_cpu_offset',
    'union_kbase_ioctl_mem_find_gpu_start_and_offset',
    'union_kbase_ioctl_mem_import', 'union_kbase_ioctl_mem_query',
    'union_kbase_kinstr_jm_fd']
