#!/bin/sh

if [ ! -f /tmp/Caddyfile ]; then
    echo "No Caddyfile found, generating default one."
    cat <<EOF > /tmp/Caddyfile
:80 {
    respond "Welcome to Caddy"
}
EOF
fi

exec caddy run --config /tmp/Caddyfile --adapter caddyfile
