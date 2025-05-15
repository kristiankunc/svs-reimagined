FROM debian:bookworm

RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-venv git curl sudo less vim \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

ARG USERNAME=dev
RUN useradd -m -s /bin/bash $USERNAME && echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

USER $USERNAME
WORKDIR /home/$USERNAME/app

RUN python3 -m venv /home/$USERNAME/.venv
ENV PATH="/home/$USERNAME/.venv/bin:$PATH"

# Copy only requirements.txt first for caching
COPY --chown=dev:dev requirements.txt ./requirements.txt

RUN pip install --upgrade pip && pip install -r requirements.txt || true

# Copy the rest of the library source code
COPY --chown=dev:dev . .
