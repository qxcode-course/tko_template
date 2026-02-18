#!/usr/bin/env bash
set -euo pipefail

# ==============================
# Configurações
# ==============================

GO_VERSION="go1.26.0"
GO_ARCH="linux-amd64"
GO_TAR="${GO_VERSION}.${GO_ARCH}.tar.gz"
GO_URL="https://go.dev/dl/${GO_TAR}"
CACHE_DIR="${HOME}/.cache/dev-setup"

# ==============================
# Utilidades
# ==============================

log() {
    echo -e "\n==> $1"
}

command_exists() {
    command -v "$1" >/dev/null 2>&1
}

ensure_path_export() {
    local line='export PATH=$PATH:/usr/local/go/bin'
    local file="$1"

    [[ -f "$file" ]] || touch "$file"
    grep -qxF "$line" "$file" || echo "$line" >> "$file"
}

install_vscode_extensions() {
    command_exists code || return 0

    mapfile -t installed < <(code --list-extensions)

    for ext in "$@"; do
        if printf '%s\n' "${installed[@]}" | grep -qx "$ext"; then
            echo "✓ $ext já instalada"
        else
            echo "→ Instalando $ext"
            code --install-extension "$ext"
        fi
    done
}

# ==============================
# Setup básico
# ==============================

setup_basic() {
    log "Instalando ferramentas básicas"

    if command_exists pipx; then
        if pipx list | grep -qE 'package tko '; then
            echo "→ Atualizando tko"
            pipx upgrade tko
        else
            echo "→ Instalando tko"
            pipx install tko
        fi
    else
        echo "pipx não encontrado. Pulando instalação do tko."
    fi

    install_vscode_extensions \
        usernamehw.errorlens \
        bierner.markdown-preview-github-styles \
        tamasfe.even-better-toml

    echo "✓ Básico concluído"
}


# ==============================
# Python
# ==============================

setup_python() {
    log "Configurando ambiente Python"

    mkdir -p .vscode
    cat > .vscode/settings.json <<EOF
{
  "python.analysis.typeCheckingMode": "strict",
  "python.analysis.diagnosticMode": "workspace"
}
EOF

    install_vscode_extensions ms-python.python

    echo "✓ Python configurado"
}

# ==============================
# TypeScript
# ==============================

setup_typescript() {
    log "Configurando ambiente TypeScript"

    if command_exists npm; then
        npm install -g typescript esbuild
        npm install --save-dev @types/node readline-sync
    else
        echo "npm não encontrado. Pulando configuração TypeScript."
    fi

    echo "✓ TypeScript configurado"
}

# ==============================
# Go
# ==============================

setup_go() {
    log "Instalando Go ${GO_VERSION}"

    mkdir -p "${CACHE_DIR}"
    GO_FILE="${CACHE_DIR}/${GO_TAR}"

    if [[ ! -f "${GO_FILE}" ]]; then
        log "Baixando ${GO_TAR}"
        if command_exists curl; then
            curl -fsSL "${GO_URL}" -o "${GO_FILE}"
        else
            echo "curl não encontrado."
            exit 1
        fi
    else
        log "Usando arquivo em cache"
    fi

    sudo rm -rf /usr/local/go
    sudo tar -C /usr/local -xzf "${GO_FILE}"

    ensure_path_export ~/.profile
    ensure_path_export ~/.bashrc

    install_vscode_extensions golang.Go

    echo "✓ Go instalado"
}

# ==============================
# Execução
# ==============================

echo "========================================"
echo "   Setup de Ambiente de Desenvolvimento"
echo "========================================"

echo "1) Python"
echo "2) TypeScript"
echo "3) Golang"
echo "4) Apenas básico"

read -rp "Escolha [1-4]: " choice

setup_basic

case "${choice}" in
    1) setup_python ;;
    2) setup_typescript ;;
    3) setup_go ;;
    4) echo "Somente básico aplicado." ;;
    *) echo "Opção inválida. Apenas básico aplicado." ;;
esac

echo -e "\n✓ Setup concluído"
