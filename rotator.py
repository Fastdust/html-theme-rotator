#!/usr/bin/env python3
"""
HTML Theme Rotator - Simple version
Rotates through theme folders, copying entire contents to web directory
"""

import os
import sys
import json
import time
import shutil
import random
import argparse
import logging
from pathlib import Path

class HTMLRotator:
    def __init__(self, config_file="config.json"):
        self.config = self.load_config(config_file)
        self.themes_dir = self.config.get("themes_dir", "themes")
        self.output_dir = self.config.get("output_dir", "/var/www/html")
        self.interval = self.config.get("interval", 3600)
        self.mode = self.config.get("mode", "random")
        self.backup = self.config.get("backup", True)
        self.current_index = 0
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('rotator.log'),
                logging.StreamHandler()
            ]
        )
    
    def load_config(self, config_file):
        """Load configuration from JSON file"""
        if not os.path.exists(config_file):
            return {}
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def find_themes(self):
        """Find all theme directories"""
        themes_path = Path(self.themes_dir)
        if not themes_path.exists():
            logging.error(f"Themes directory not found: {self.themes_dir}")
            return []
        
        themes = []
        for item in themes_path.iterdir():
            if item.is_dir():
                # Check if directory contains files
                if any(item.iterdir()):
                    themes.append(str(item))
        
        if not themes:
            logging.warning(f"No theme directories found in {self.themes_dir}")
        else:
            logging.info(f"Found {len(themes)} themes: {[Path(t).name for t in themes]}")
        
        return themes
    
    def backup_current(self):
        """Create backup of current deployment"""
        if not self.backup or not os.path.exists(self.output_dir):
            return
        
        try:
            backup_dir = f"backup_{int(time.time())}"
            shutil.copytree(self.output_dir, backup_dir)
            logging.info(f"Backup created: {backup_dir}")
        except Exception as e:
            logging.warning(f"Backup failed: {e}")
    
    def deploy_theme(self, theme_path):
        """Deploy theme to output directory"""
        try:
            # Create backup
            self.backup_current()
            
            # Clear output directory
            if os.path.exists(self.output_dir):
                for item in os.listdir(self.output_dir):
                    item_path = os.path.join(self.output_dir, item)
                    if os.path.isfile(item_path):
                        os.remove(item_path)
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)
            else:
                os.makedirs(self.output_dir)
            
            # Copy theme files
            files_copied = 0
            for item in os.listdir(theme_path):
                src = os.path.join(theme_path, item)
                dst = os.path.join(self.output_dir, item)
                
                if os.path.isfile(src):
                    shutil.copy2(src, dst)
                    files_copied += 1
                elif os.path.isdir(src):
                    shutil.copytree(src, dst)
                    files_copied += 1
            
            theme_name = Path(theme_path).name
            logging.info(f"Deployed theme '{theme_name}' - {files_copied} items copied")
            return True
            
        except Exception as e:
            logging.error(f"Deployment failed: {e}")
            return False
    
    def rotate_once(self):
        """Perform one rotation"""
        themes = self.find_themes()
        if not themes:
            return False
        
        # Select theme
        if self.mode == "random":
            selected = random.choice(themes)
        else:  # sequential
            selected = themes[self.current_index % len(themes)]
            self.current_index = (self.current_index + 1) % len(themes)
        
        return self.deploy_theme(selected)
    
    def list_themes(self):
        """List all available themes"""
        themes = self.find_themes()
        if themes:
            print("Available themes:")
            for i, theme in enumerate(themes, 1):
                theme_name = Path(theme).name
                file_count = len(list(Path(theme).iterdir()))
                print(f"  {i}. {theme_name} ({file_count} files)")
        else:
            print("No themes found")
    
    def run_daemon(self):
        """Run continuously with specified interval"""
        logging.info(f"Starting daemon mode (interval: {self.interval}s)")
        
        try:
            while True:
                if self.rotate_once():
                    logging.info("Rotation successful")
                else:
                    logging.error("Rotation failed")
                
                time.sleep(self.interval)
                
        except KeyboardInterrupt:
            logging.info("Daemon stopped by user")
        except Exception as e:
            logging.error(f"Daemon error: {e}")

def main():
    parser = argparse.ArgumentParser(description="HTML Theme Rotator")
    parser.add_argument("--once", action="store_true", help="Run once and exit")
    parser.add_argument("--daemon", action="store_true", help="Run as daemon")
    parser.add_argument("--list", action="store_true", help="List available themes")
    parser.add_argument("--config", default="config.json", help="Config file path")
    
    args = parser.parse_args()
    
    rotator = HTMLRotator(args.config)
    
    if args.list:
        rotator.list_themes()
    elif args.once:
        if rotator.rotate_once():
            print("Rotation completed successfully")
        else:
            print("Rotation failed")
    elif args.daemon:
        rotator.run_daemon()
    else:
        print("HTML Theme Rotator")
        print("Usage:")
        print("  --once    Run single rotation")
        print("  --daemon  Run continuously") 
        print("  --list    List available themes")
        print("  --config  Specify config file")

if __name__ == "__main__":
    main()
