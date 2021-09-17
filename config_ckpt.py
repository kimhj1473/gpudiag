from enum import Enum
from enum import auto
from define import Test

# True: Run the test / False: Skip the test
run_test = {
    Test.kernel_limits:     False,
    Test.verify_limits:     False,
    Test.l1i_linesize:      False,
    Test.icache_hierarchy:  False,
    Test.mp_and_buffers:    False,
    Test.exec_units:        True,
}

# Test configuration value definition
class CKPT(Enum):
    shared_memory_test_granularity = auto()
    max_icache_investigate_size_KiB = auto()
    nslot_timeout_multiplier = auto()
    mab_skip_num_mp_and_use = auto()
    mab_skip_bbsize_and_use = auto()
    mab_skip_shmem = auto()
    eu_latency_repeats = auto()

# Test configuration value assignment
values = {
    ## The test result related to the shared memory will have the accuracy of
    ## following granularity. Smaller value = more accurate = more time-consuming.
    ### USED IN: verify_limits, sharedmem_size
    CKPT.shared_memory_test_granularity: 1024,

    ## The icache hierarchy will be investigated up to the following size (KiB).
    ## For gpgpusim with lengauer-tarjan algorithm, 128 is recommended.
    ## Larger value = more hierarchy revealed = more time-consuming.
    ### USED IN: icache_hierarchy
    CKPT.max_icache_investigate_size_KiB: 128,

    ## Tests will determine deadlock if the sync consumes more time than
    ## (previously detected max time consumption) * (this multiplier).
    ## For simulations, 10 is enough.
    ### USED IN: mp_and_buffers
    CKPT.nslot_timeout_multiplier: 10,

    ## mp_and_buffers runs multiple tests:
    ## (1) num_mp / (2) barrier_buffer_size & warp_state_buffer_size /
    ## (3) shared_memory_size
    ## If you want to skip some test, provide the result by number.
    ## Test is run if the value <= 0.
    ### USED IN: mp_and_buffers
    CKPT.mab_skip_num_mp_and_use: 0, # if >0, skip (1) and use num_mp with this value
    CKPT.mab_skip_bbsize_and_use: 0, # if >0, skip (2) and use bbsize with this value
    CKPT.mab_skip_shmem:          0, # if >0, skip (3) (nothing will use this value)

    ## num of instruction repeats when measuring the latency
    ### USED_IN: exec_units
    CKPT.eu_latency_repeats: 32,

}

## If you want to control exec_units test, the checkpoint option is available
## in kernels/exec_units.py
### USED_IN: exec_units
