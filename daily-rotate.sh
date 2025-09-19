#!/bin/bash
# Daily theme rotation via cron
# Add to crontab: 0 9 * * * /opt/html-rotator/daily-rotate.sh

# Change to script directory
cd /opt/html-rotator

# Log rotation attempt
echo "$(date): Starting daily theme rotation" >> /var/log/rotator.log

# Run single rotation
python3 /opt/html-rotator/rotator.py --once

# Log completion
echo "$(date): Daily theme rotation completed" >> /var/log/rotator.log
