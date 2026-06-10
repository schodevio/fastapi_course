FROM mcr.microsoft.com/devcontainers/python:3.13

USER root

# Install packages needed to build and run the application
RUN apt-get update && apt-get install -y git

# --- Custom setup
USER vscode

RUN git clone https://github.com/zsh-users/zsh-autosuggestions \
    ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions

RUN sed -ir 's/plugins=(git)/plugins=(git zsh-autosuggestions)/g' ~/.zshrc && \
    sudo chsh -s $(which zsh) $(whoami)
# ---
