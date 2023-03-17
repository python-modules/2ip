## Use Django base image
FROM registry.remote.sx/development-images/ubuntu/python:latest

## Set default Python version to use
ENV USE_PYTHON_VERSION="3.11"

## Switch to root
USER root

## Copy startup scripts to container
COPY scripts /usr/local/scripts

## Add the zsh configuration file
COPY .zshrc /home/vscode/.zshrc

## Fix zshrc permissions
RUN chown vscode:vscode /home/vscode/.zshrc

## Switch to the VS Code user
USER vscode

## Install Conda environment
RUN /home/vscode/conda/bin/conda create -q -y -n 2ip "python=${USE_PYTHON_VERSION}"

## Set the work directory
WORKDIR /code
