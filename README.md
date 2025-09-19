# HTML Theme Rotator

Simple tool that automatically rotates through theme folders, copying their entire contents to your web directory.

## What it does

1. **Finds theme folders** - Looks in the `themes/` directory
2. **Picks one randomly** - Selects a theme folder  
3. **Copies everything** - Copies all files from that theme to your web server directory

## Quick Setup

```bash
# Install
sudo ./setup.sh

# Run once
python3 rotator.py --once

# Run continuously  
python3 rotator.py --daemon
```

## Files

- `rotator.py` - Main script
- `config.json` - Configuration
- `themes/` - Put your theme folders here
- `setup.sh` - Installation script

## Configuration

Edit `config.json`:
```json
{
  "themes_dir": "themes",
  "output_dir": "/var/www/html",
  "interval": 86400,
  "mode": "random", 
  "backup": false
}
```

**Interval options:**
- `3600` = 1 hour
- `86400` = 24 hours (daily)
- `604800` = 7 days (weekly)

## Usage

**Option 1: Manual rotation**
```bash
# List available themes
python3 rotator.py --list

# Rotate once and exit
python3 rotator.py --once
```

**Option 2: Continuous service**
```bash
# Run as daemon (continuous)
python3 rotator.py --daemon

# Or via systemd
sudo systemctl start html-rotator
```

**Option 3: Daily cron job (recommended)**
```bash
# Add to crontab for daily rotation at 9 AM
(crontab -l 2>/dev/null; echo "0 9 * * * /opt/html-rotator/daily-rotate.sh") | crontab -

# Test the daily script
sudo /opt/html-rotator/daily-rotate.sh
```

## Testing Daily Rotation

**1. Test the script manually:**
```bash
sudo /opt/html-rotator/daily-rotate.sh
```

**2. Check if cron job is scheduled:**
```bash
# View current crontab
crontab -l

# Should show: 0 9 * * * /opt/html-rotator/daily-rotate.sh
```

**3. Monitor rotation in logs:**
```bash
# Watch real-time logs
tail -f /var/log/rotator.log

# Check recent rotations
tail -20 /var/log/rotator.log
```

**4. Test with different time (for immediate testing):**
```bash
# Add a test rotation for next minute
echo "$(date -d '+1 minute' +'%M %H * * *') /opt/html-rotator/daily-rotate.sh" | crontab -
```

That's it! Simple and effective.
