# GPUDiag
Systematic reverse-engineering diagnosis tool for GPUs.
made by Hyoungjoo Kim, Seoul Nat'l University, 2021

## Requirements
~~~shell
sudo apt install -y python3 pip
pip3 install matplotlib
~~~

## How to use
~~~shell
# set config_env.py
# set config_ckpt.py
python3 gpudiag.py
~~~
If you want to clean build & result files,
~~~shell
sudo python3 clean.py
~~~

### Using with gpgpusim
You should prepare gpgpusim-compatible environment first.
The Dockerfile at dockerfiles/gpgpusim is tested.

The following modifications should be applied to the gpgpusim.
- Because gpgpusim 4.0.1 uses a naive algorithm in finding dominators,
icache_hierarchy test is too slow. Please modify it using
lengauer_tarjan_dominator_tree in boost.org
- NOTE: the default config uses modified gpgpusim.config at 
configs/tested-cfgs/SM75_RTX2060_notperfect, which was 
modified as non-perfect icache, 4 SMs, and 8KiB L1I$.

Download and build gpgpu-sim.
Download gpudiag.
~~~shell
cd workdir
ls # >> gpgpusim/ gpudiag/
sudo docker run --rm -it -v $PWD/gpgpusim:/gpgpusim \
    -v $PWD/gpudiag:/gpudiag -w /gpudiag gpgpusim_image
## edit config_env.py to match the environment
python3 gpudiag
~~~

### Using with gem5-apu
You should prepare gem5-apu-compatible environment first.
The Dockerfile at dockerfiles/gem5 is tested.

The following modifications should be applied to the gem5.
- Because gem5 21.1.0 don't have s_memtime instruction implemented, 
you may have to implement it manually.
- My repo at https://github.com/kimhj1473/zolp_gem5.git is tested.
- If you modified it yourself, you may have to change config_env.py
run_command.

Download and build gem5.
Download gpudiag.
~~~shell
cd workdir
ls # >> gem5/ gpudiag/
sudo docker run --rm -it -v $PWD/gem5:/gem5 \
    -v $PWD/gpudiag:/gpudiag -w /gpudiag gem5gcn_image
## edit config_env.py to match the environment
python3 gpudiag
~~~

## Modifying tests
The enum for the possible featuers and tests are defined in define.py
The python will compile the test at tests/test.cpp,
using the kernel code build/manufacturer/test/test.h
generated by kernels/test.py