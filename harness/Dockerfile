FROM debian:bookworm-slim@sha256:734a72b3d6142a71993b4bc580ca01d8ca687f77a2c422d96a961d3376b179bc
ARG DEBIAN_FRONTEND=noninteractive
ARG EXTRA_APT=""
ARG EXTRA_PIP=""
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 TZ=UTC PATH=/opt/venv/bin:$PATH
RUN printf 'Acquire::Retries "2"; Acquire::http::Timeout "30"; Acquire::https::Timeout "30"; Acquire::Check-Valid-Until "false";\n' > /etc/apt/apt.conf.d/80bounded \
 && timeout 180 apt-get update \
 && timeout 900 apt-get install -y --no-install-recommends \
    ca-certificates=20230311+deb12u1 \
    python3=3.11.2-1+b1 python3-venv=3.11.2-1+b1 \
    python3-pil=9.4.0-1.1+deb12u1 python3-reportlab=3.6.12-1+deb12u1 \
    python3-markdown=3.4.1-2+deb12u1 \
    ghostscript=10.0.0~dfsg-11+deb12u9 qpdf=11.3.0-1+deb12u1 \
    poppler-utils=22.12.0-2+deb12u3 chromium=156.0.8078.79-1~deb12u1 \
    fonts-dejavu-core=2.37-6 fonts-liberation=1:1.07.4-11 ${EXTRA_APT} \
 && python3 -m venv --system-site-packages /opt/venv \
 && timeout 180 /opt/venv/bin/pip install --no-cache-dir --retries 2 --timeout 30 pypdf==5.1.0 ${EXTRA_PIP} \
 && dpkg-query -W -f='${Package}\t${Version}\n' > /opt/packages.tsv \
 && rm -rf /var/lib/apt/lists/*
