# syntax=docker/dockerfile:1
FROM python:3.11-slim

# Install base tools (can also add: curl, git, docker CLI, kubectl, etc.)
RUN apt-get update && apt-get install -y \
    build-essential curl git && \
    rm -rf /var/lib/apt/lists/*

# Install Node.js via nvm or official LTS
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs

# Install Pants / Bazel / Nx CLI globally
RUN npm install -g nx
RUN curl -LO https://github.com/bazelbuild/bazel/releases/download/6.4.0/bazel-6.4.0-linux-x86_64 && \
    chmod +x bazel-6.4.0-linux-x86_64 && mv bazel-6.4.0-linux-x86_64 /usr/local/bin/bazel

WORKDIR /app
COPY . .

CMD ["/bin/bash"]
