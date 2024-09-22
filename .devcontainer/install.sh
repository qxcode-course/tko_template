#!/bin/bash



# Cria o arquivo de aliases, se ainda não existir

echo "" >> ~/.bashrc
echo "alias ls='eza --icons --color=always --group-directories-first'" >> ~/.bashrc
echo "alias ll='eza -alF --icons --color=always --group-directories-first'" >> ~/.bashrc
echo "alias update='pip install tko --upgrade'" >> ~/.bashrc
echo "alias play='tko play'" >> ~/.bashrc
echo "alias run='tko run'" >> ~/.bashrc
echo "" >> ~/.bashrc

# Instala pacotes via apt
sudo apt-get update
sudo apt-get install -y graphviz

# Instala eza
wget -c https://github.com/eza-community/eza/releases/latest/download/eza_x86_64-unknown-linux-gnu.tar.gz -O - | tar xz
sudo chmod +x eza
sudo chown root:root eza
sudo mv eza /usr/local/bin/eza

# Instala pacotes Python
pip install tko
tko config --root .
tko config --lang ts
tko config --hud 0

# Baixa e instala a FiraCode Nerd Font
#mkdir -p ~/.local/share/fonts
#cd ~/.local/share/fonts
#rm -rf myfont
#curl -fLo "myfont.zip" https://github.com/ryanoasis/nerd-fonts/releases/download/v3.2.1/ComicShannsMono.zip
#unzip myfont.zip -d myfont
#rm myfont.zip
#fc-cache -fv  # Atualiza o cache de fontes

# Instala pacotes Node.js globais
npm install -g typescript esbuild

# Instala pacotes locais
cd /workspaces
npm install --save-dev @types/node readline-sync

source .bashrc || true
