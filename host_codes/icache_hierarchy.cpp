// MANUFACTURER=1 (nvidia), =0 (amd)
#define MANUFACTURER
#define REPORT_FILE
#define KERNEL_FILE

#define ckpt_max_icache_investigate_KiB
#define ckpt_icache_investigate_interval_B

#include "gpudiag_runtime.h"

int main(int argc, char **argv) {
    GDInit();

    const int num_iters = ICACHE_MAX_REPEATS / ICACHE_INTERVAL;
    float data[num_iters];

    uint64_t hres, *dres;
    GDMalloc(&dres, sizeof(uint64_t));
    for (int i=0; i<num_iters; i++) {
        GDLaunchKernel(measure_icache[i], dim3(1), dim3(1), 0, 0, dres);
        GDSynchronize();
        GDMemcpyDToH(&hres, dres, sizeof(uint64_t));
        data[i] = (float)hres / (float)((i+1)*ICACHE_INTERVAL);
    }
    GDFree(dres);

    // analyze
    int max_level = 20;
    uint64_t capacity[max_level];
    int current_level = 0;
    float current_level_time = data[0];
    float current_level_mean_slope = data[1] - data[0];
    for (int i=1; i<num_iters; i++) {
        if (current_level_time < 0) {
            // waiting the slope to be flat again..
            if (data[i] - data[i-1] < 1.5 * current_level_mean_slope) {
                // flat again!
                current_level_time = data[i];
                current_level_mean_slope = data[i] - data[i-1];
                continue;
            }
        } 
        if (data[i] > 1.5 * current_level_time) {
            // new hierarchy detected
            current_level++;
            capacity[current_level-1] = ICACHE_INSTSIZE_A +
                ICACHE_INSTSIZE_B * ICACHE_INTERVAL * i-1;
            current_level_time = -1;
            continue;
        }
        current_level_time = (current_level_time + data[i]) / 2.0f;
        current_level_mean_slope = (current_level_mean_slope + data[i]-data[i-1]) / 2.0f;
    }
    int max_observed_level = current_level;
    for (int i=0; i<max_observed_level; i++) {
        // round the value to the nearest multiple of 1024
        capacity[i] = (capacity[i] + 512) / 1024 * 1024;
    }
    uint64_t capacity_removed_redunduncy[max_level];
    capacity_removed_redunduncy[0] = capacity[0]; current_level = 0;
    if (max_observed_level > 0) {
        for (int i=1; i<max_observed_level; i++) {
            if (capacity[i] > capacity_removed_redunduncy[current_level]) {
                capacity_removed_redunduncy[current_level+1] = capacity[i];
                current_level++;
            }
        }
        max_observed_level = current_level+1;
    }

    // write
    write_init("icache_hierarchy");
    write_graph_data("Icache hierarchy", num_iters, "inst. size(B)",
        ICACHE_INSTSIZE_A + ICACHE_INSTSIZE_B * ICACHE_INTERVAL,
        ICACHE_INSTSIZE_B * ICACHE_INTERVAL,
        "total time / repeat", data);
    if (max_observed_level > 0)
        write_values("icache_capacities", capacity, max_observed_level);
    else {
        write_line("## Only 1 level is observed, L1I capacity is at least following.");
        write_value("icache_capacities", ICACHE_INSTSIZE_A + num_iters * 
            ICACHE_INTERVAL * ICACHE_INSTSIZE_B);
    }

    return 0;
}