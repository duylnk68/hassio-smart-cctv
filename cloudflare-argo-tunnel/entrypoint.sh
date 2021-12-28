#!/usr/bin/env bash

# Environment
CONFIG_PATH=/data/options.json
url="$(jq --raw-output '.url' $CONFIG_PATH)
AccountTag=$(jq --raw-output '.account-tag' $CONFIG_PATH)
TunnelID=$(jq --raw-output '.tunnel-id' $CONFIG_PATH)
TunnelName=$(jq --raw-output '.tunnel-name' $CONFIG_PATH)
TunnelSecret=$(jq --raw-output '.tunnel-secret' $CONFIG_PATH)

# Create credentials-file.json
echo "{
    \"AccountTag\":\"$AccountTag\",
    \"TunnelID\":\"$TunnelID\",
    \"TunnelName\":\"$TunnelName\",
    \"TunnelSecret\":\"$TunnelSecret\"
}" > /data/$TunnelID.json

# Create config.yaml
echo "url: $url
tunnel: $TunnelID
credentials-file: /data/$TunnelID.json" > /data/config.yaml

# Run
./cloudflared config /data/config.yaml tunnel run