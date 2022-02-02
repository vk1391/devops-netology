1.  - более менее собрал но еластик ругается на отсутсвие javа ES_JAVA_HOME
```
FROM centos:7

RUN yum update -y && yum install java-11-openjdk wget perl-Digest-SHA yum install nano sudo -y
ENV PATH=/usr/lib:/usr/lib/jvm/jre-11/bin:$PATH
RUN wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.17.0-linux-x86_64.tar.gz
RUN wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.17.0-linux-x86_64.tar.gz.sha512
RUN shasum -a 512 -c elasticsearch-7.17.0-linux-x86_64.tar.gz.sha512
RUN tar -xzf elasticsearch-7.17.0-linux-x86_64.tar.gz
RUN cd elasticsearch-7.17.0/
#RUN RUN echo '1234' | passwd root
RUN groupadd elasticsearch && useradd -g elasticsearch elasticsearch && usermod -a -G wheel elasticsearch
USER elasticsearch
ENV ES_JAVA_HOME=/elasticsearch-7.17.0/jdk
ENV ES_HOME=/elasticsearch-7.17.0
CMD ["./elasticsearch-7.17.0/bin/elasticsearch"]
