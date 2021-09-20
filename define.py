from enum import Enum
from enum import auto

class Test(Enum):
    kernel_limits = auto()
    l1i_linesize = auto()
    icache_hierarchy = auto()
    mp_and_buffers = auto()
    functional_units = auto()
    dcache_hierarchy = auto()

class Feature(Enum):
    warp_size = auto()
    limit_threads_per_block = auto()
    limit_threads_per_grid = auto()
    limit_sharedmem_per_block = auto()
    limit_registers_per_thread = auto()
    limit_registers_per_block = auto()
    # generated by kernel_limits, used in mp_and_buffers
    LRpB_test_info0 = auto() # [num_tests, min_tested_R, Reg_unit]
    LRpB_test_data0 = auto() # array of max_b at min_tested_R+i*Reg_unit
    LRpB_test_info1 = auto() # [num_tests, min_tested_R, Reg_unit]
    LRpB_test_data1 = auto() # array of max_b at min_tested_R+i*Reg_unit

    l1i_linesize = auto()
    icache_capacities = auto()
    icache_linesizes = auto()

    num_mp = auto()
    barrier_buffer_size = auto()
    warp_state_buffer_size = auto()
    shared_memory_size = auto()
    shared_memory_alloc_unit = auto()
    register_file_size = auto()
    register_file_alloc_unit = auto()
    scalar_register_file_size = auto()
    scalar_register_file_alloc_unit = auto()
    vector_register_file_size = auto()
    vector_register_file_alloc_unit = auto()

    dcache_capacities = auto()
    dcache_linesizes = auto()
    dcache_latencies = auto()
