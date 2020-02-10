FROM python:3.6-slim
MAINTAINER shankha.sinha@ust-global.com
RUN apt-get update -y \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /opt/venv
# use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
ARG REQS=base
RUN pip3 install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

FROM ubuntu:18.04
MAINTAINER shankha.sinha@ust-global.com
COPY --from=builder /opt/venv /opt/venv

# use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

RUN apt-get update -y \
    && apt-get install -y --no-install-recommends \
    python3-setuptools \
    python3-venv \
    python3-dev \
    python3-pip \
    portaudio19-dev \
    libgirepository1.0-dev \
    gcc \
    libcairo2-dev \
    pkg-config \
    libgstreamer1.0-0 \
    python3-twisted \
    python3-gst-1.0 \
    python3-pyaudio \
    gir1.2-gtk-3.0 \
    figlet \
    && rm -rf /var/lib/apt/lists/*


COPY . /cmm
WORKDIR /cmm
ENV HOME /cmm


RUN sh /$HOME/manage.sh
EXPOSE 8081

#CMD ["gunicorn", "--reload", "routes:api", "--workers=3", "--timeout", "10000", "-b :8081"]

CMD ["sh", "start_app.sh"]