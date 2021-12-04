#!/usr/bin/env bash

set -euo pipefail

SUBSCRIPTION_ID=$(az account show --query id --output tsv)

az ad sp create-for-rbac --name "fry-bot-sp" --role contributor \
    --scopes /subscriptions/${SUBSCRIPTION_ID}/resourceGroups/fry-bot \
    --sdk-auth