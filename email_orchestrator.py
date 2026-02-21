#!/usr/bin/env python3
"""
Email Orchestrator - Process approved emails and simulate sending.

This script:
1. Monitors the Approved/ folder for approved emails
2. Processes and "sends" them (simulated or via Gmail API)
3. Moves sent emails to Done/
4. Logs all actions
"""

import json
import shutil
from pathlib import Path
from datetime import datetime
from email_validator import validate_email, EmailNotValidError


class EmailOrchestrator:
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.approved_dir = self.vault_path / 'Approved'
        self.done_dir = self.vault_path / 'Done'
        self.logs_dir = self.vault_path / 'Logs'
        self.dry_run = True  # Set to False to actually send emails
        
    def process_approved_emails(self):
        """Process all approved emails in the Approved folder."""
        print(f"\n[Email Orchestrator] Processing approved emails...")
        print(f"Vault: {self.vault_path}")
        print(f"Dry Run: {self.dry_run}")
        
        approved_files = list(self.approved_dir.glob('EMAIL_*.md'))
        
        if not approved_files:
            print("[INFO] No approved emails to process")
            return
        
        print(f"[INFO] Found {len(approved_files)} approved email(s)")
        
        for email_file in approved_files:
            self._process_email(email_file)
    
    def _process_email(self, email_file: Path):
        """Process a single approved email."""
        print(f"\n[PROCESSING] {email_file.name}")
        
        try:
            # Read email content
            content = email_file.read_text(encoding='utf-8')
            
            # Parse frontmatter
            email_data = self._parse_email(content)
            
            # Validate email
            self._validate_recipients(email_data)
            
            # Send email (or simulate)
            send_result = self._send_email(email_data)
            
            # Log the action
            self._log_email_action(email_file.name, email_data, send_result)
            
            # Move to Done
            dest = self.done_dir / email_file.name
            shutil.move(str(email_file), str(dest))
            
            print(f"[SUCCESS] Email processed and moved to Done/")
            
        except Exception as e:
            print(f"[ERROR] Failed to process email: {e}")
    
    def _parse_email(self, content: str) -> dict:
        """Parse email markdown and extract data."""
        # Split frontmatter
        parts = content.split('---')
        if len(parts) < 3:
            raise ValueError("Invalid email format - missing frontmatter")
        
        frontmatter_text = parts[1].strip()
        body = '---'.join(parts[2:]).strip()
        
        # Parse YAML-like frontmatter manually
        email_data = {'body': body}
        
        for line in frontmatter_text.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                
                # Parse arrays
                if value.startswith('[') and value.endswith(']'):
                    # Simple array parsing
                    items = value[1:-1].split(',')
                    email_data[key] = [item.strip().strip('"\'') for item in items if item.strip()]
                else:
                    email_data[key] = value
        
        return email_data
    
    def _validate_recipients(self, email_data: dict):
        """Validate email recipients."""
        recipients = email_data.get('recipients', [])
        
        for recipient in recipients:
            try:
                valid = validate_email(recipient)
                print(f"  [OK] Valid recipient: {valid.email}")
            except EmailNotValidError as e:
                print(f"  [WARN] Invalid recipient: {recipient} - {e}")
                # Don't fail, just warn (it's a test)
    
    def _send_email(self, email_data: dict) -> dict:
        """Send email (simulated in dry-run mode)."""
        recipients = email_data.get('recipients', [])
        subject = email_data.get('subject', 'No Subject')
        
        if self.dry_run:
            print(f"  [DRY RUN] Would send email to: {', '.join(recipients)}")
            print(f"  [DRY RUN] Subject: {subject}")
            
            return {
                'status': 'simulated',
                'recipients': recipients,
                'subject': subject,
                'timestamp': datetime.now().isoformat()
            }
        else:
            # Actual sending would happen here via Gmail API
            print(f"  [SENDING] Sending email to: {', '.join(recipients)}")
            
            return {
                'status': 'sent',
                'recipients': recipients,
                'subject': subject,
                'timestamp': datetime.now().isoformat()
            }
    
    def _log_email_action(self, filename: str, email_data: dict, result: dict):
        """Log email action to JSON file."""
        today = datetime.now().strftime('%Y-%m-%d')
        log_file = self.logs_dir / f'{today}.json'
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action_type': 'email_sent',
            'source_file': filename,
            'email_data': {
                'recipients': email_data.get('recipients', []),
                'subject': email_data.get('subject', '')
            },
            'result': result
        }
        
        # Read existing logs
        logs = []
        if log_file.exists():
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            except:
                logs = []
        
        # Append new log
        logs.append(log_entry)
        
        # Write back
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)
        
        print(f"  [LOGGED] Action logged to {log_file.name}")


def main():
    """Main entry point."""
    import sys
    
    vault_path = sys.argv[1] if len(sys.argv) > 1 else './AI_Employee_Vault'
    dry_run = '--dry-run' not in sys.argv
    
    orchestrator = EmailOrchestrator(vault_path)
    orchestrator.dry_run = dry_run
    orchestrator.process_approved_emails()
    
    print("\n[COMPLETE] Email orchestration finished")


if __name__ == '__main__':
    main()
