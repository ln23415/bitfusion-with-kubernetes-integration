# PhaedoPkgTools

## 介绍
提供一种制作 [bitfusion-with-kubernetes-integration](https://github.com/vmware/bitfusion-with-kubernetes-integration/tree/main/bitfusion_device_plugin) 项目中initContainer的image的方式
## 前提条件
- python3 + pip3
- docker
- 确保主机可以连接到互联网

## 使用方式
先安装项目所使用依赖包
```bash
pip3 install -r requirement.txt
```
到Bitfusion的网站下载所需要打包到image中的Bitfusion客户端版本。这里提供了Bitfusion安装教程https://docs.vmware.com/en/VMware-vSphere-Bitfusion/index.html

这里我们选择Bitfusion Client 4.0.1-5的Ubuntu 18， Ubuntu 20， Centos 7， Centos8四种OS版本作为示例演示  

1.下载所对应的安装包到本地
```
├── bitfusion-client-centos7-4.0.1-5.x86_64.rpm
├── bitfusion-client-centos8-4.0.1-5.x86_64.rpm
├── bitfusion-client-ubuntu1804_4.0.1-5_amd64.deb
├── bitfusion-client-ubuntu2004_4.0.1-5_amd64.deb

```
2.修改build.yaml文件  
此文件作为程序运行所需要的的参数传入，不同的key代表了不同的意思
- imagename 代表最终生成的image的名称  
- OSVersion 表示所对应的安装包适配的操作系统版本
- BitfusionVersion 代表Bitfusion Client的版本，这里用整数表示是为了和bitfusion-with-kubernetes-integration项目中的规则保持一直。取值规则为版本号 X 100，比如要生成4.0.1版本的时候就写401
- buildimage 说明需要安装Bitfusion Client的系统版本，这个值可以在所下载的安装文件中找到，比如文件名为bitfusion-client-ubuntu1804_4.0.1-5_amd64.deb，其中ubuntu1804就是对应的构建版本
- local 代表了安装包的为止，可以使用相对路径也可以使用绝对路径
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
3. 使用下面命令运行项目
```bash
python3 build.py
```  
在构建image之前会生成两个文件
- Dockerfile 通过检验Dockerfile可以查看image的构建步骤
- bitfusion-client-configmap.yaml 查看此文件可以确定Bitfusion客户端安装包最终对应到image中的位置，请不要对这个文件进行修改
## 输出内容
输出的内容包括 
- image 名称为bitfusion-client:example的镜像，这个名称是自定义的。
- Dockerfile 用来构建image使用
- bitfusion-client-configmap.yaml 需要替换bitfusion-with-kubernetes-integration项目中对应的文件，bitfusion-client-configmap.yaml文件记录了image中不同版本客户端的位置信息

## 在Device Plugin中使用

在只有一个K8S节点的前提下

需要将当前所输出的image的名称替换为原image的名称。例如目前bitfusion-with-kubernetes-integration项目所使用的initContainer名称为bitfusiondeviceplugin/bitfusion-client:0.2.2，我们所输出的image名称为bitfusion-client:example，需要运行下面命令使我们的image替换掉原来的image 
```bash
docker rmi bitfusiondeviceplugin/bitfusion-client:0.2.2
docker tag bitfusion-client:example bitfusiondeviceplugin/bitfusion-client:0.2.2
```
然后使用我们所输出的bitfusion-client-configmap.yaml文件替换掉[bitfusion-with-kubernetes-integration]项目中[bitfusion-with-kubernetes-integration/bitfusion_device_plugin/webhook/deployment/bitfusion-client-configmap.yaml]此路径下的[bitfusion-client-configmap.yaml]文件

做好以上两步内容后，运行下面命令对[bitfusion-with-kubernetes-integration]项目进行重新部署。在[bitfusion-with-kubernetes-integration/bitfusion_device_plugin/]路径下运行
```bash
make deploy
```
到此，我们的单节点替换就完成了，如果存在多个K8S节点的情况下，需要到每个节点上重复替换image的操作，可以参考bitfusion-with-kubernetes-integration项目readme中的安装方式二进行部署和替换
