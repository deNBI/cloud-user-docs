# Install latest CUDA version

This short guide will demonstrate how to install the latest CUDA version on your **CentOS** VM with access to GPU resources (e.g. P100 GPU).

First of all make sure that your VM is up to date and reboot the VM if a kernel update was installed.

```bash
sudo yum update -y && sudo reboot
```

We will install the EPEL repository because it contains the dkms package which we will need to install the NVIDIA drivers.

```bash
sudo yum install epel-release -y
```

Now we install the following packages to allow the installation of CUDA and the GPU drivers.

```bash
sudo yum install kernel-devel-`uname -r` kernel-headers-`uname -r` pciutils dkms wget -y
```

As the CentOS repositories do not provide any CUDA versions we have to add the official NVIDIA CUDA repository. Therefore visit the [NVIDIA CUDA repository](https://developer.download.nvidia.com/compute/cuda/repos/rhel7/x86_64/) and choose the (**rhel7**) CUDA version you want to install. We will download the rpm with wget and install it via yum.

```bash
wget https://developer.download.nvidia.com/compute/cuda/repos/rhel7/x86_64/cuda-repo-rhel7-10.2.89-1.x86_64.rpm
sudo yum install cuda-repo-rhel7-10.2.89-1.x86_64.rpm -y
```

In the last step we will install the latest CUDA package and reboot the VM.
```bash
sudo yum install cuda -y && sudo reboot
```

Now You can use `nvidia-smi` to validate if the installation was successfully.

```
$ nvidia-smi
Mon Apr 27 14:18:12 2020       
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 440.64.00    Driver Version: 440.64.00    CUDA Version: 10.2     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|===============================+======================+======================|
|   0  Tesla P100-PCIE...  Off  | 00000000:00:05.0 Off |                    0 |
| N/A   29C    P0    27W / 250W |      0MiB / 16280MiB |      4%      Default |
+-------------------------------+----------------------+----------------------+

+-----------------------------------------------------------------------------+
| Processes:                                                       GPU Memory |
|  GPU       PID   Type   Process name                             Usage      |
|=============================================================================|
|  No running processes found                                                 |
+-----------------------------------------------------------------------------+
```
