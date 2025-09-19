#!/bin/bash

# HTML Theme Rotator - Simple Setup Script

set -e

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root (use sudo)"
   exit 1
fi

echo "HTML Theme Rotator Setup"
echo "======================"

# Install to /opt
INSTALL_DIR="/opt/html-rotator"
echo "Installing to $INSTALL_DIR..."

# Create directories
mkdir -p $INSTALL_DIR
mkdir -p /var/log

# Copy files
cp rotator.py $INSTALL_DIR/
cp config.json $INSTALL_DIR/
cp -r themes $INSTALL_DIR/

# Set permissions
chmod +x $INSTALL_DIR/rotator.py
chown -R root:root $INSTALL_DIR

# Create systemd service
cat > /etc/systemd/system/html-rotator.service << EOF
[Unit]
Description=HTML Theme Rotator
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$INSTALL_DIR
ExecStart=/usr/bin/python3 $INSTALL_DIR/rotator.py --daemon
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and enable service
systemctl daemon-reload
systemctl enable html-rotator

echo ""
echo "Installation complete!"
echo ""
echo "Commands:"
echo "  sudo systemctl start html-rotator    # Start service"
echo "  sudo systemctl stop html-rotator     # Stop service" 
echo "  sudo systemctl status html-rotator   # Check status"
echo "  python3 $INSTALL_DIR/rotator.py --list  # List themes"
echo "  python3 $INSTALL_DIR/rotator.py --once  # Run once"
echo ""
echo "Configuration: $INSTALL_DIR/config.json"
echo "Themes folder: $INSTALL_DIR/themes/"
echo "Log file: /var/log/rotator.log"
