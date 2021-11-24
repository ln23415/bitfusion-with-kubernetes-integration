#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

__mtime__ = '2021/9/16'
import yaml

yaml_template_header = """
apiVersion: v1
kind: ConfigMap
metadata:
  name: bwki-bitfusion-client-configmap
  namespace: bwki
data:
  bitfusion-client-config.yaml: |
    BitfusionClients:
"""

dir_template_prefix = "/bitfusion/"
binary_path_template = "/usr/bin/bitfusion"
lib_path_template = "opt/bitfusion/lib/x86_64-linux-gnu/bitfusion/lib/\n"
env_variable_template = "/opt/bitfusion/lib/x86_64-linux-gnu/bitfusion/lib/"


def parse(path: str):
    with open(path) as f:
        x = yaml.load(f, Loader=yaml.FullLoader)

    return x


def mkdir_name(context: str) -> str:
    tmp = os.path.basename(context)
    return dir_template_prefix + tmp


def conver_docker(data: list) -> str:
    content = ""
    i = 0
    for v in data:
        basename = os.path.basename(v["local"])
        content += "FROM " + v["buildimage"] + " as builder" + str(i) + "\n"
        content += "COPY .temp/" + basename + " . \n"
        if v["buildimage"].startswith("ubuntu"):
            content += "RUN apt-get update && apt-get install -y ./" + basename + "\n"
        elif v["buildimage"].startswith("centos"):
            content += "RUN rpm2cpio ./" + basename + " | cpio -div \n"
        else:
            raise
        i += 1

    i = 0
    content += "FROM ubuntu:18.04 \n"

    for v in data:
        target = mkdir_name(v["local"])
        content += "RUN mkdir -p " + target + "\n"
        content += "WORKDIR " + target + "\n"
        content += """RUN mkdir bin && \\
mkdir var && \\
mkdir var/lib && \\
mkdir var/run && \\
mkdir usr && \\
mkdir usr/share && \\
mkdir usr/lib && \\
mkdir usr/bin && \\
mkdir lib && \\
mkdir lib/x86_64-linux-gnu && \\
mkdir opt && \\
mkdir opt/bitfusion  \n"""
        content += "COPY --from=builder" + str(i) + " /usr/bin/bitfusion usr/bin/  \n"
        content += "COPY --from=builder" + str(i) + " /opt/bitfusion/ opt/bitfusion  \n"
        content += "COPY --from=builder" + str(i) + " /usr/share/bitfusion usr/share/  \n"
        if v["OSVersion"].lower().startswith("ubuntu18"):
            content += "COPY resource/ubuntu18/* " + lib_path_template
        elif v["OSVersion"].lower().startswith("ubuntu20"):
            content += "COPY resource/ubuntu20/* " + lib_path_template
        elif v["OSVersion"].lower().startswith("centos7"):
            content += "COPY resource/centos7/* " + lib_path_template
        elif v["OSVersion"].lower().startswith("centos8"):
            content += "COPY resource/centos8/* " + lib_path_template
        else:
            raise
        i += 1
    return content


def conver_yaml(data: list):
    content = yaml_template_header
    for v in data:
        path = mkdir_name(v["local"])
        content += """
      - BitfusionVersion: "%s"
        OSVersion: %s
        BinaryPath: %s
        EnvVariable: %s
        """ % (v["BitfusionVersion"], v["OSVersion"],
               path + binary_path_template, path + env_variable_template)
    return content


def write(content: str, path: str):
    with open(path, "w") as f:
        f.write(content)


def build(in_put):
    os.system("rm -rf .temp")
    os.system("mkdir .temp")
    data = in_put["data"]
    for v in data:
        os.system("cp " + v["local"] + " .temp/")

    docker_content = conver_docker(data)
    write(docker_content, "Dockerfile")
    yaml_content = conver_yaml(data)
    write(yaml_content, "bitfusion-client-configmap.yaml")
    os.system("docker build -t " + in_put["imagename"] + " .")


if __name__ == '__main__':
    in_put = parse("build.yaml")
    build(in_put)
