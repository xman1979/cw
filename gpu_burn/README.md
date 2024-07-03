# gpu-burn
Multi-GPU CUDA stress test

# Building
To build GPU Burn:

```bash
make
# for devfair
make CUDAPATH=$CUDA_HOME
```

To remove artifacts built by GPU Burn:

`make clean`

GPU Burn builds with a default Compute Capability of 5.0.
To override this with a different value:

`make COMPUTE=<compute capability value>`

CFLAGS can be added when invoking make to add to the default
list of compiler flags:

`make CFLAGS=-Wall`

LDFLAGS can be added when invoking make to add to the default
list of linker flags:

`make LDFLAGS=-lmylib`

NVCCFLAGS can be added when invoking make to add to the default
list of nvcc flags:

`make NVCCFLAGS=-ccbin <path to host compiler>`

CUDAPATH can be added to point to a non standard install or
specific version of the cuda toolkit (default is
/usr/local/cuda):

`make CUDAPATH=/usr/local/cuda-<version>`

CCPATH can be specified to point to a specific gcc (default is
/usr/bin):

`make CCPATH=/usr/local/bin`

# Usage

    GPU Burn
    Usage: gpu_burn [OPTIONS] [TIME]

    -m X    Use X MB of memory.
    -m N%   Use N% of the available GPU memory.  Default is 90%
    -d      Use doubles
    -tc     Try to use Tensor cores
    -l      Lists all GPUs in the system
    -i N    Execute only on GPU N
    -c FILE Use FILE as compare kernel.  Default is compare.ptx
    -h      Show this help message

    Examples:
      gpu-burn -d 3600 # burns all GPUs with doubles for an hour
      gpu-burn -m 50% # burns using 50135133120f the available GPU memory
      gpu-burn -l # list GPUs
      gpu-burn -i 2 # burns only GPU of index 2
