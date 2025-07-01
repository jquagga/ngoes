# micromaba
FROM ghcr.io/mamba-org/micromamba:latest@sha256:0c347cbc7a83500b2a03fc55594e1b2d775f75e458d5d9a58c50aecd752a56f9
COPY --chown=$MAMBA_USER:$MAMBA_USER environment.yml /tmp/environment.yml
COPY --chown=$MAMBA_USER:$MAMBA_USER requirements.txt /tmp/requirements.txt
RUN micromamba install -y -n base -f /tmp/environment.yml && \
    micromamba clean --all --yes

ARG MAMBA_DOCKERFILE_ACTIVATE=1
WORKDIR /app
COPY ngoes.py /app

ENTRYPOINT ["/usr/local/bin/_entrypoint.sh", "python","-u","/app/ngoes.py" ]
