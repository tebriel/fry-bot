#!/bin/bash

set -euo pipefail

if [ -n "$PERSONAL_TF_API_KEY" ]; then
    echo "Configuring terraform creds..."
    mkdir -p "$HOME/.terraform.d/"
    cp /workspaces/fry-bot/.devcontainer/credentials.tfrc.json.example "$HOME/.terraform.d/credentials.tfrc.json"
    # shellcheck disable=SC2016
    sed -i -e 's/$TERRAFORM_API_KEY/'"$PERSONAL_TF_API_KEY"'/' "$HOME/.terraform.d/credentials.tfrc.json"

    pushd /workspaces/fry-bot/infrastructure
    terraform init
    popd
fi
