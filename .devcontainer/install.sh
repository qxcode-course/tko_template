#!/bin/bash



# Cria o arquivo de aliases, se ainda não existir

echo "" >> ~/.bashrc
echo "alias update='pip install tko --upgrade'" >> ~/.bashrc
echo "" >> ~/.bashrc

# Instala pacotes Python
pip install tko


# Instala pacotes Node.js globais
npm install -g typescript esbuild

# Instala pacotes locais
cd /workspaces
npm install --save-dev @types/node readline-sync

source .bashrc || true
