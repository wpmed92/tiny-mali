MALI_IOCTL_MAP = {
    "KBASE_IOCTL_SET_FLAGS": {
        "type": 128,
        "nr": 1,
        "payload": "struct kbase_ioctl_set_flags",
        "dir": "IOW"
    },
    "KBASE_IOCTL_GET_GPUPROPS": {
        "type": 128,
        "nr": 3,
        "payload": "struct kbase_ioctl_get_gpuprops",
        "dir": "IOW"
    },
    "KBASE_IOCTL_MEM_ALLOC": {
        "type": 128,
        "nr": 5,
        "payload": "union kbase_ioctl_mem_alloc",
        "dir": "IOWR"
    },
    "KBASE_IOCTL_MEM_QUERY": {
        "type": 128,
        "nr": 6,
        "payload": "union kbase_ioctl_mem_query",
        "dir": "IOWR"
    },
    "KBASE_IOCTL_MEM_FREE": {
        "type": 128,
        "nr": 7,
        "payload": "struct kbase_ioctl_mem_free",
        "dir": "IOW"
    },
    "KBASE_IOCTL_HWCNT_READER_SETUP": {
        "type": 128,
        "nr": 8,
        "payload": "struct kbase_ioctl_hwcnt_reader_setup",
        "dir": "IOW"
    },
    "KBASE_IOCTL_HWCNT_ENABLE": {
        "type": 128,
        "nr": 9,
        "payload": "struct kbase_ioctl_hwcnt_enable",
        "dir": "IOW"
    },
    "KBASE_IOCTL_HWCNT_DUMP": {
        "type": 128,
        "nr": 10,
        "payload": "",
        "dir": "IO"
    },
    "KBASE_IOCTL_HWCNT_CLEAR": {
        "type": 128,
        "nr": 11,
        "payload": "",
        "dir": "IO"
    },
    "KBASE_IOCTL_HWCNT_SET": {
        "type": 128,
        "nr": 32,
        "payload": "struct kbase_ioctl_hwcnt_values",
        "dir": "IOW"
    },
    "KBASE_IOCTL_DISJOINT_QUERY": {
        "type": 128,
        "nr": 12,
        "payload": "struct kbase_ioctl_disjoint_query",
        "dir": "IOR"
    },
    "KBASE_IOCTL_GET_DDK_VERSION": {
        "type": 128,
        "nr": 13,
        "payload": "struct kbase_ioctl_get_ddk_version",
        "dir": "IOW"
    },
    "KBASE_IOCTL_MEM_JIT_INIT_10_2": {
        "type": 128,
        "nr": 14,
        "payload": "struct kbase_ioctl_mem_jit_init_10_2",
        "dir": "IOW"
    },
    "KBASE_IOCTL_MEM_JIT_INIT_11_5": {
        "type": 128,
        "nr": 14,
        "payload": "struct kbase_ioctl_mem_jit_init_11_5",
        "dir": "IOW"
    },
    "KBASE_IOCTL_MEM_JIT_INIT": {
        "type": 128,
        "nr": 14,
        "payload": "struct kbase_ioctl_mem_jit_init",
        "dir": "IOW"
    },
    "KBASE_IOCTL_MEM_SYNC": {
        "type": 128,
        "nr": 15,
        "payload": "struct kbase_ioctl_mem_sync",
        "dir": "IOW"
    },
    "KBASE_IOCTL_MEM_FIND_CPU_OFFSET": {
        "type": 128,
        "nr": 16,
        "payload": "union kbase_ioctl_mem_find_cpu_offset",
        "dir": "IOWR"
    },
    "KBASE_IOCTL_GET_CONTEXT_ID": {
        "type": 128,
        "nr": 17,
        "payload": "struct kbase_ioctl_get_context_id",
        "dir": "IOR"
    },
    "KBASE_IOCTL_TLSTREAM_ACQUIRE": {
        "type": 128,
        "nr": 18,
        "payload": "struct kbase_ioctl_tlstream_acquire",
        "dir": "IOW"
    },
    "KBASE_IOCTL_TLSTREAM_FLUSH": {
        "type": 128,
        "nr": 19,
        "payload": "",
        "dir": "IO"
    },
    "KBASE_IOCTL_MEM_COMMIT": {
        "type": 128,
        "nr": 20,
        "payload": "struct kbase_ioctl_mem_commit",
        "dir": "IOW"
    },
    "KBASE_IOCTL_MEM_ALIAS": {
        "type": 128,
        "nr": 21,
        "payload": "union kbase_ioctl_mem_alias",
        "dir": "IOWR"
    },
    "KBASE_IOCTL_MEM_IMPORT": {
        "type": 128,
        "nr": 22,
        "payload": "union kbase_ioctl_mem_import",
        "dir": "IOWR"
    },
    "KBASE_IOCTL_MEM_FLAGS_CHANGE": {
        "type": 128,
        "nr": 23,
        "payload": "struct kbase_ioctl_mem_flags_change",
        "dir": "IOW"
    },
    "KBASE_IOCTL_STREAM_CREATE": {
        "type": 128,
        "nr": 24,
        "payload": "struct kbase_ioctl_stream_create",
        "dir": "IOW"
    },
    "KBASE_IOCTL_FENCE_VALIDATE": {
        "type": 128,
        "nr": 25,
        "payload": "struct kbase_ioctl_fence_validate",
        "dir": "IOW"
    },
    "KBASE_IOCTL_MEM_PROFILE_ADD": {
        "type": 128,
        "nr": 27,
        "payload": "struct kbase_ioctl_mem_profile_add",
        "dir": "IOW"
    },
    "KBASE_IOCTL_STICKY_RESOURCE_MAP": {
        "type": 128,
        "nr": 29,
        "payload": "struct kbase_ioctl_sticky_resource_map",
        "dir": "IOW"
    },
    "KBASE_IOCTL_STICKY_RESOURCE_UNMAP": {
        "type": 128,
        "nr": 30,
        "payload": "struct kbase_ioctl_sticky_resource_unmap",
        "dir": "IOW"
    },
    "KBASE_IOCTL_MEM_FIND_GPU_START_AND_OFFSET": {
        "type": 128,
        "nr": 31,
        "payload": "union kbase_ioctl_mem_find_gpu_start_and_offset",
        "dir": "IOWR"
    },
    "KBASE_IOCTL_CINSTR_GWT_START": {
        "type": 128,
        "nr": 33,
        "payload": "",
        "dir": "IO"
    },
    "KBASE_IOCTL_CINSTR_GWT_STOP": {
        "type": 128,
        "nr": 34,
        "payload": "",
        "dir": "IO"
    },
    "KBASE_IOCTL_CINSTR_GWT_DUMP": {
        "type": 128,
        "nr": 35,
        "payload": "union kbase_ioctl_cinstr_gwt_dump",
        "dir": "IOWR"
    },
    "KBASE_IOCTL_MEM_EXEC_INIT": {
        "type": 128,
        "nr": 38,
        "payload": "struct kbase_ioctl_mem_exec_init",
        "dir": "IOW"
    },
    "KBASE_IOCTL_GET_CPU_GPU_TIMEINFO": {
        "type": 128,
        "nr": 50,
        "payload": "union kbase_ioctl_get_cpu_gpu_timeinfo",
        "dir": "IOWR"
    },
    "KBASE_IOCTL_CONTEXT_PRIORITY_CHECK": {
        "type": 128,
        "nr": 54,
        "payload": "struct kbase_ioctl_context_priority_check",
        "dir": "IOWR"
    },
    "KBASE_IOCTL_SET_LIMITED_CORE_COUNT": {
        "type": 128,
        "nr": 55,
        "payload": "struct kbase_ioctl_set_limited_core_count",
        "dir": "IOW"
    },
    "KBASE_IOCTL_TLSTREAM_STATS": {
        "type": 128,
        "nr": 2,
        "payload": "struct kbase_ioctl_tlstream_stats",
        "dir": "IOR"
    },
    "KBASE_IOCTL_VERSION_CHECK": {
        "type": 128,
        "nr": 0,
        "payload": "struct kbase_ioctl_version_check",
        "dir": "IOWR"
    },
    "KBASE_IOCTL_JOB_SUBMIT": {
        "type": 128,
        "nr": 2,
        "payload": "struct kbase_ioctl_job_submit",
        "dir": "IOW"
    },
    "KBASE_IOCTL_POST_TERM": {
        "type": 128,
        "nr": 4,
        "payload": "",
        "dir": "IO"
    },
    "KBASE_IOCTL_SOFT_EVENT_UPDATE": {
        "type": 128,
        "nr": 28,
        "payload": "struct kbase_ioctl_soft_event_update",
        "dir": "IOW"
    },
    "KBASE_IOCTL_KINSTR_JM_FD": {
        "type": 128,
        "nr": 51,
        "payload": "union kbase_kinstr_jm_fd",
        "dir": "IOWR"
    },
    "KBASE_IOCTL_VERSION_CHECK_RESERVED": {
        "type": 128,
        "nr": 52,
        "payload": "struct kbase_ioctl_version_check",
        "dir": "IOWR"
    },
    "MALI_EXYNOS_IOCTL_AMIGO_FLAGS": {
        "type": 130,
        "nr": 0,
        "payload": "struct mali_exynos_ioctl_amigo_flags",
        "dir": "IOR"
    },
    "MALI_EXYNOS_IOCTL_READ_GTS_INFO": {
        "type": 130,
        "nr": 1,
        "payload": "struct mali_exynos_ioctl_gts_info",
        "dir": "IOR"
    },
    "MALI_EXYNOS_IOCTL_HCM_PMQOS": {
        "type": 130,
        "nr": 2,
        "payload": "struct mali_exynos_ioctl_hcm_pmqos",
        "dir": "IOW"
    },
    "MALI_EXYNOS_IOCTL_MEM_USAGE_ADD": {
        "type": 130,
        "nr": 3,
        "payload": "struct mali_exynos_ioctl_mem_usage_add",
        "dir": "IOW"
    },
    "MALI_EXYNOS_IOCTL_CMAR_BOOST": {
        "type": 130,
        "nr": 4,
        "payload": "struct mali_exynos_ioctl_cmar_boost",
        "dir": "IOW"
    },
    "KBASE_IOCTL_SLSI_EGP": {
        "type": 130,
        "nr": 5,
        "payload": "struct kbase_ioctl_slsi_egp",
        "dir": "IOW"
    },
    "KBASE_IOCTL_SLSI_SINGLEBUFFER_BOOST_FLAGS": {
        "type": 130,
        "nr": 46,
        "payload": "struct kbase_ioctl_slsi_singlebuffer_boost_flags",
        "dir": "IOW"
    }
}