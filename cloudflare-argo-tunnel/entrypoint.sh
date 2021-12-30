#!/usr/bin/env bash

# Environment
CLOUDFLARE_DIR=/usr/local/etc/cloudflared
CONFIG_PATH=/data/options.json
url=$(jq --raw-output '.url' $CONFIG_PATH)
AccountTag=$(jq --raw-output '.account_tag' $CONFIG_PATH)
TunnelID=$(jq --raw-output '.tunnel_id' $CONFIG_PATH)
TunnelName=$(jq --raw-output '.tunnel_name' $CONFIG_PATH)
TunnelSecret=$(jq --raw-output '.tunnel_secret' $CONFIG_PATH)

#
mkdir -p $CLOUDFLARE_DIR

# Create credentials-file.json
echo "{
    \"AccountTag\":\"$AccountTag\",
    \"TunnelID\":\"$TunnelID\",
    \"TunnelName\":\"$TunnelName\",
    \"TunnelSecret\":\"$TunnelSecret\"
}" > $CLOUDFLARE_DIR/$TunnelID.json

# Create config.yaml
echo "url: $url
tunnel: $TunnelID
credentials-file: $CLOUDFLARE_DIR/$TunnelID.json" > $CLOUDFLARE_DIR/config.yaml

# Run
./cloudflared tunnel run --no-autoupdate