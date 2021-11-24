# PhaedoPkgTools

## Introduced
Provides a way to make the image of initContainer, that is bitfusion client image, in this bitfusion-with-kubernetes-integration project.
## Prerequisites
- python3 + pip3
- docker
- Ensure that the host can connect to the Internet

## Usage
Fistly, install the dependencies by the following command:
```bash
pip3 install -r requirements.txt
```
Go to Bitfusion's website to download the Bitfusion Clients package that needs to be packaged into the image. Here is the link: <http://devrepo.wdc.bf.eng.vmware.com/releases/packages/>

Here, we select Bitfusion Client 4.0.1-5 Ubuntu 18, Ubuntu 20, Centos 7, and Centos 8 OS versions as examples

1.Download these packages to current foler
```
├── bitfusion-client-centos7-4.0.1-5.x86_64.rpm
├── bitfusion-client-centos8-4.0.1-5.x86_64.rpm
├── bitfusion-client-ubuntu1804_4.0.1-5_amd64.deb
├── bitfusion-client-ubuntu2004_4.0.1-5_amd64.deb

```

2.Modify the build.yaml file
There are some parameters in build.yaml file.
- `imagename` indicates the image-name:tag of the generated image
- `OSVersion` indicates the corresponding operating system version of a Bitfusion Client package
- `BitfusionVersion` indicates the version of the Bitfusion Client. The value should be computed by `(major version of Bitfusion Client) x 100`, for example, for bitfusion client 4.0.1, BitfusionVersion is 401.
- `buildimage` specifies on which os version that the Bitfusion Client will be installed. The value could be revealed by the filename of the bitfusion client package. For example, for bitfusion-client-ubuntu1804.0.1-5_amd64.deb, `buildimage` parameter is `ubuntu1804`.
- `local` indicates the path of a bitfusion client package.
```yaml

imagename: bitfusion-client:example
data:
  - OSVersion: ubuntu18
    BitfusionVersion: 401
    buildimage: ubuntu:18.04
    local: bitfusion-client-ubuntu1804_4.0.1-5_amd64.deb
  - OSVersion: ubuntu20
    BitfusionVersion: 401
    buildimage: ubuntu:20.04
    local: bitfusion-client-ubuntu2004_4.0.1-5_amd64.deb
  - OSVersion: centos7
    BitfusionVersion: 401
    buildimage: centos:7
    local: bitfusion-client-centos7-4.0.1-5.x86_64.rpm
  - OSVersion: centos8
    BitfusionVersion: 401
    buildimage: centos:8
    local: bitfusion-client-centos8-4.0.1-5.x86_64.rpm
```
3. Run the following command to build the bitfusion client image.
```bash
python3 build.py
```
Three things will be generated:
- Dockerfile: use it to build the final image.
- bitfusion-client-configmap.yaml: This file determines the final location of the Bitfusion Client execution binary files in the image is going to build. 
- Bitfusion-client image, whose image name and tag are pre-defined by `imagename` paramter in build.yaml.

Then you can publish the final Bitfusion-client image to target registry. 


