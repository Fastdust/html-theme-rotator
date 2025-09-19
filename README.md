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
  "interval": 3600,
  "mode": "random", 
  "backup": false
}
```

## Usage

```bash
# List available themes
python3 rotator.py --list

# Rotate once and exit
python3 rotator.py --once

# Run as daemon (continuous)
python3 rotator.py --daemon
```

That's it! Simple and effective.
