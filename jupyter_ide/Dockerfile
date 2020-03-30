FROM debian:stretch
LABEL maintainer="calisto107"

ARG NB_USER="calisto"
ARG NB_UID="1000"
ARG NB_GID="100"

ENV DEBIAN_FRONTEND=noninteractive \
    REQUESTS_CA_BUNDLE=/etc/ssl/certs \
    PATH=/app:/opt/conda/bin:/app/jupyter/bin:/usr/local/bin:$PATH \
    CONDA_ENVS_PATH=/app \
    JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/jre \
    AWS_SHARED_CREDENTIALS_FILE=/home/dbs/aws.conf \
    PY_VERSION=python3.7 \
    PLANTUML_VERSION=1.2019.11
    #PYTHONHOME=/app/jupyter/lib/$PY_VERSION
    #PYTHONPATH=/app/jupyter/lib/$PY_VERSION

ENV APP_ROOT=/app \
    PATH=${APP_ROOT}/jupyter/bin:${PATH} \
    CONDA_DIR=/opt/conda \
    SHELL=/bin/bash \
    NB_USER=$NB_USER \
    NB_UID=$NB_UID \
    HOME=/home/$NB_USER

USER root

RUN useradd -r -u $NB_UID -g $NB_GID $NB_USER

ADD requirements.txt requirements.txt

COPY start_lab.sh /home/$NB_USER/
COPY tools /home/$NB_USER/tools/
COPY conf tmp/conf
COPY src tmp/src

# install necessary tools
 #   && curl -sL https://deb.nodesource.com/setup_6.x | bash - \
 #   && apt-get install -y npm nodejs \
RUN apt-get update \
    && apt-get install -y gcc apt-utils libcurl3-gnutls openjdk-8-jre-headless wget zip nano less curl gettext-base git graphviz \
    && chmod 770 -R /root \
    && wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh \
    && yes | /bin/bash ~/miniconda.sh -b -p /opt/conda \
    && rm ~/miniconda.sh \
    && apt-get clean \
    && conda create -p /app/jupyter --copy -q -y python=3.7 \
    && conda install -c conda-forge nodejs \
    && /app/jupyter/bin/pip install --upgrade pip==20.0.2 \
    && /app/jupyter/bin/pip install -r requirements.txt \
    && wget --quiet "http://downloads.sourceforge.net/project/plantuml/${PLANTUML_VERSION}/plantuml.${PLANTUML_VERSION}.jar" -O /app/plantuml.jar

COPY start_lab.sh /home/$NB_USER/
COPY tools /home/$NB_USER/tools/
COPY conf tmp/conf
COPY src tmp/src

RUN chmod -R 777 /app/jupyter \
    && chmod -R 777 /home/$NB_USER \
    && chmod -R u+x ${APP_ROOT} \
    && chgrp -R 0 ${APP_ROOT} \
    && chmod -R g=u ${APP_ROOT} /etc/passwd \
    && chgrp -R $NB_GID /home/$NB_USER \
    && chown -R $NB_UID /home/$NB_USER \
    && chmod -R 777 /home/$NB_USER \
    && chmod 777 /home/$NB_USER/start_lab.sh \
    && chmod 777 -R /app \
    && chmod 777 -R /tmp/conf \
    && echo "PATH=/opt/conda/bin:/app/jupyter/bin:/usr/local/bin:$PATH" >> /etc/bash.bashrc

USER $NB_UID

# install sparkmagic
RUN mkdir -p /home/$NB_USER/.jupyter \
    && jupyter nbextension enable --py --sys-prefix widgetsnbextension \
    && jupyter labextension install @jupyter-widgets/jupyterlab-manager \
    && jupyter labextension install jupyter-matplotlib \
    && /app/jupyter/bin/pip install /tmp/src/magics/custommagics \
    && mv /tmp/conf/jupyter/jupyter_notebook_config.json /home/$NB_USER/.jupyter/jupyter_notebook_config.json \
    && mv /tmp/conf/ipython /home/$NB_USER/.ipython

USER $NB_UID

CMD ["/home/calisto/start_lab.sh"]

EXPOSE 8888

WORKDIR $HOME
