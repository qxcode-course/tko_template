#!/bin/bash

alias ls='eza --icons --color=always --group-directories-first'
alias ll='eza -alF --icons --color=always --group-directories-first'
alias la='eza -a --icons --color=always --group-directories-first'
alias l='eza -F --icons --color=always --group-directories-first'
alias lt='eza --tree --icons'

echo "alias update='pip install tko --upgrade'" >> /user/vscode/user_alias.sh
echo "alias play='tko play'" >> /user/vscode/user_alias.sh
echo "alias run='tko run'" >> /user/vscode/user_alias.sh
echo "" >> /user/vscode/user_alias.sh
