#!/usr/bin/env python3
import os, subprocess, re
os.environ["AGENTMAIL_API_KEY"] = subprocess.run(
    ["security", "find-generic-password", "-s", "agentmail", "-a", "clark", "-w"],
    capture_output=True, text=True
).stdout.strip()

from agentmail import AgentMail
client = AgentMail()

messages = client.inboxes.messages.list(inbox_id="clark88@agentmail.to", limit=15)
for msg in messages.messages:
    full = client.inboxes.messages.get(inbox_id="clark88@agentmail.to", message_id=msg.message_id)
    subj = msg.subject or ""
    if 'iteground' in subj or 'ollaboration' in subj:
        text = full.text or full.extracted_text or ""
        html = full.html or ""
        print(f"Subject: {subj}")
        print(f"Text preview: {text[:500]}")
        links = re.findall(r'https?://[^\s<>"\']+', text)
        links += re.findall(r'href="(https?://[^"]+)"', html)
        print(f"\nAll links:")
        for link in links:
            if 'siteground' in link.lower() or 'collab' in link.lower():
                print(f"  {link}")
        print()
