# para desinstalar o go caso tenha baixado anteriormente
sudo rm -rf /usr/local/go

# para desisntalar o go caso tenha baixado via apt
sudo apt remove --purge golang-go -y
sudo apt autoremove -y

# para instalar a versão mais nova
versao='go1.24.2.linux-amd64.tar.gz'
wget https://go.dev/dl/$versao
sudo tar -C /usr/local -xzf $versao
rm $versao

#check export before insert in .profile
if ! grep -q "export PATH=\$PATH:/usr/local/go/bin" ~/.profile; then
  echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.profile
fi

# #check export before insert in .bashrc
# if ! grep -q "export PATH=\$PATH:/usr/local/go/bin" ~/.bashrc; then
#   echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
# fi

# if ! grep -q "export PATH=\$PATH:/usr/local/go/bin" /etc/profile.d/meu_path.sh; then
#   echo 'export PATH=$PATH:/usr/local/go/bin' | sudo tee /etc/profile.d/meu_path.sh
# fi



echo "reinicie o terminal com Control D"

