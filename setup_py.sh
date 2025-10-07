#!/usr/bin/env bash

mkdir -p .vscode
cat > .vscode/settings.json <<EOF
{
    "python.analysis.typeCheckingMode": "strict",
    "python.analysis.diagnosticMode": "workspace"
}
EOF

code --install-extension ms-python.python