FROM ubuntu:18.04 as builder
MAINTAINER shankha.shuvro@hotmail.com

RUN apt-get update -y \
    && apt-get install -y --no-install-recommends \
    python3-setuptools \
    python3-venv \
    python3-dev \
    python3-pip \
    figlet \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /opt/venv
# use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
ARG REQS=base
RUN pip3 install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

FROM ubuntu:18.04
MAINTAINER shankha.shuvro@hotmail.com
COPY --from=builder /opt/venv /opt/venv

# use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

RUN apt-get update -y \
    && apt-get install -y --no-install-recommends \
    python3-setuptools \
    python3-venv \
    python3-dev \
    python3-pip \
    figlet \
    && rm -rf /var/lib/apt/lists/*


COPY . /cmm
WORKDIR /cmm
ENV HOME /cmm


RUN sh /$HOME/manage.sh
EXPOSE 8081

#CMD ["gunicorn", "--reload", "routes:api", "--workers=3", "--timeout", "10000", "-b :8081"]

CMD ["sh", "start_app.sh"]