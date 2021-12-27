#!/usr/bin/env bashio

# Environment
url="$(bashio::config 'url')"
AccountTag="$(bashio::config 'account-tag')"
TunnelID="$(bashio::config 'tunnel-id')"
TunnelName="$(bashio::config 'tunnel-name')"
TunnelSecret="$(bashio::config 'tunnel-secret')"

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
./cloudflared config /data/config.yaml