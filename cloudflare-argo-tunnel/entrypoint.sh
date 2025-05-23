#!/usr/bin/env bash

# Environment
CONFIG_PATH=/data/options.json
url=$(jq --raw-output '.url' $CONFIG_PATH)
AccountTag=$(jq --raw-output '.account_tag' $CONFIG_PATH)
TunnelID=$(jq --raw-output '.tunnel_id' $CONFIG_PATH)
TunnelName=$(jq --raw-output '.tunnel_name' $CONFIG_PATH)
TunnelSecret=$(jq --raw-output '.tunnel_secret' $CONFIG_PATH)

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
./cloudflared tunnel --config /data/config.yaml --no-autoupdate run