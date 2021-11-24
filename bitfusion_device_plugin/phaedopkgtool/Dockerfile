FROM ubuntu:18.04 as builder0
COPY .temp/bitfusion-client-ubuntu1804_4.0.1-5_amd64.deb . 
RUN apt-get update && apt-get install -y ./bitfusion-client-ubuntu1804_4.0.1-5_amd64.deb
FROM ubuntu:20.04 as builder1
COPY .temp/bitfusion-client-ubuntu2004_4.0.1-5_amd64.deb . 
RUN apt-get update && apt-get install -y ./bitfusion-client-ubuntu2004_4.0.1-5_amd64.deb
FROM centos:7 as builder2
COPY .temp/bitfusion-client-centos7-4.0.1-5.x86_64.rpm . 
RUN rpm2cpio ./bitfusion-client-centos7-4.0.1-5.x86_64.rpm | cpio -div 
FROM centos:8 as builder3
COPY .temp/bitfusion-client-centos8-4.0.1-5.x86_64.rpm . 
RUN rpm2cpio ./bitfusion-client-centos8-4.0.1-5.x86_64.rpm | cpio -div 
FROM ubuntu:18.04 
RUN mkdir -p /bitfusion/bitfusion-client-ubuntu1804_4.0.1-5_amd64.deb
WORKDIR /bitfusion/bitfusion-client-ubuntu1804_4.0.1-5_amd64.deb
RUN mkdir bin && \
mkdir var && \
mkdir var/lib && \
mkdir var/run && \
mkdir usr && \
mkdir usr/share && \
mkdir usr/lib && \
mkdir usr/bin && \
mkdir lib && \
mkdir lib/x86_64-linux-gnu && \
mkdir opt && \
mkdir opt/bitfusion  
COPY --from=builder0 /usr/bin/bitfusion usr/bin/  
COPY --from=builder0 /opt/bitfusion/ opt/bitfusion  
COPY --from=builder0 /usr/share/bitfusion usr/share/  
COPY resource/ubuntu18/* opt/bitfusion/lib/x86_64-linux-gnu/bitfusion/lib/
RUN mkdir -p /bitfusion/bitfusion-client-ubuntu2004_4.0.1-5_amd64.deb
WORKDIR /bitfusion/bitfusion-client-ubuntu2004_4.0.1-5_amd64.deb
RUN mkdir bin && \
mkdir var && \
mkdir var/lib && \
mkdir var/run && \
mkdir usr && \
mkdir usr/share && \
mkdir usr/lib && \
mkdir usr/bin && \
mkdir lib && \
mkdir lib/x86_64-linux-gnu && \
mkdir opt && \
mkdir opt/bitfusion  
COPY --from=builder1 /usr/bin/bitfusion usr/bin/  
COPY --from=builder1 /opt/bitfusion/ opt/bitfusion  
COPY --from=builder1 /usr/share/bitfusion usr/share/  
COPY resource/ubuntu20/* opt/bitfusion/lib/x86_64-linux-gnu/bitfusion/lib/
RUN mkdir -p /bitfusion/bitfusion-client-centos7-4.0.1-5.x86_64.rpm
WORKDIR /bitfusion/bitfusion-client-centos7-4.0.1-5.x86_64.rpm
RUN mkdir bin && \
mkdir var && \
mkdir var/lib && \
mkdir var/run && \
mkdir usr && \
mkdir usr/share && \
mkdir usr/lib && \
mkdir usr/bin && \
mkdir lib && \
mkdir lib/x86_64-linux-gnu && \
mkdir opt && \
mkdir opt/bitfusion  
COPY --from=builder2 /usr/bin/bitfusion usr/bin/  
COPY --from=builder2 /opt/bitfusion/ opt/bitfusion  
COPY --from=builder2 /usr/share/bitfusion usr/share/  
COPY resource/centos7/* opt/bitfusion/lib/x86_64-linux-gnu/bitfusion/lib/
RUN mkdir -p /bitfusion/bitfusion-client-centos8-4.0.1-5.x86_64.rpm
WORKDIR /bitfusion/bitfusion-client-centos8-4.0.1-5.x86_64.rpm
RUN mkdir bin && \
mkdir var && \
mkdir var/lib && \
mkdir var/run && \
mkdir usr && \
mkdir usr/share && \
mkdir usr/lib && \
mkdir usr/bin && \
mkdir lib && \
mkdir lib/x86_64-linux-gnu && \
mkdir opt && \
mkdir opt/bitfusion  
COPY --from=builder3 /usr/bin/bitfusion usr/bin/  
COPY --from=builder3 /opt/bitfusion/ opt/bitfusion  
COPY --from=builder3 /usr/share/bitfusion usr/share/  
COPY resource/centos8/* opt/bitfusion/lib/x86_64-linux-gnu/bitfusion/lib/
