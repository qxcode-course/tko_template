#!/usr/bin/env bash
set -e

code --install-extension ms-python.python

# garante que a pasta exista
mkdir -p .vscode

# sobrescreve o settings.json
cat > .vscode/settings.json <<'EOF'
{
    "python.analysis.typeCheckingMode": "strict"
}
EOF
