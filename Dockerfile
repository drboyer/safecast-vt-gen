FROM openjdk:8
ENV SPARK_VERSION "2.3.1"
ENV SPARK_PACKAGE spark-${SPARK_VERSION}-bin-hadoop2.7.tgz
RUN cd /opt && \
    curl -O https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/${SPARK_PACKAGE} && \
    tar xzf $SPARK_PACKAGE && \
    rm $SPARK_PACKAGE
ENV PATH $PATH:/opt/spark-${SPARK_VERSION}-bin-hadoop2.7/bin
WORKDIR /usr/local/src/spark