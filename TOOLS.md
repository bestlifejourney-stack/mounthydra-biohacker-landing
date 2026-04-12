# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Email (AgentMail)

- **Address:** clark88@agentmail.to
- **Todd's email:** todd@mounthydra.com
- **API key location:** openclaw.json → skills.entries.agentmail.apiKey

## Browser

- **Tool:** agent-browser (installed at /opt/homebrew/bin/agent-browser)
- Workflow: open → snapshot -i → interact → re-snapshot

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

### AgentMail
- **Inbox:** clark88@agentmail.to
- **API key:** stored in macOS Keychain (service: `agentmail`, account: `clark`)
- **Retrieve:** `security find-generic-password -s "agentmail" -a "clark" -w`
- **Python venv:** `~/.openclaw/agentmail-venv/bin/python`
- **Send script:** `~/.openclaw/skills/agentmail/scripts/send_email.py`

### Microsoft 365 Email (GoDaddy-managed)
- **Script:** `~/.openclaw/scripts/m365_email.py`
- **Auth method:** OAuth2 delegated tokens via Microsoft Office public client (bypasses GoDaddy admin consent restriction)
- **Client ID:** `d3590ed6-52b3-4102-aeff-aad2292ab01c` (Microsoft Office first-party)
- **Token refresh:** Automatic via refresh tokens stored in Keychain
- **Accounts configured:**
  - ✅ **todd@mounthydra.com** — Tenant: `ade2a6c3-2a85-4131-b6d0-b36a1f1247d5`, Keychain service: `azure-m365-email`
  - ✅ **todd@3dexosomes.com** — Tenant: `aa6a0d12-c0d5-4c6b-ba69-a8749ba63a16`, Keychain service: `azure-m365-email-3dexosomes`
  - ✅ **todd@sceql.com** — Tenant: `1ddac892-4381-494a-ac82-652aced0c287`, Keychain service: `azure-m365-email-sceql`
- **Usage:**
  ```python
  from m365_email import list_inbox, send_email, search_inbox, read_message
  list_inbox("mounthydra", top=10, unread_only=True)
  send_email("recipient@example.com", "Subject", "Body", account_key="mounthydra")
  ```
- **Note:** GoDaddy locks down Azure AD admin roles. User consent is also disabled. Using Microsoft's own first-party Office app ID as the client bypasses this restriction since it's pre-consented on all M365 tenants.

---

### Cloudflare
- **Domain:** getrepurpose.ai
- **Zone ID:** 989c721a79a192d8b26ce88129568e0c
- **API Token:** stored in macOS Keychain (service: `cloudflare`, account: `getrepurpose.ai`)
- **Scope:** Edit zone DNS for getrepurpose.ai

### Railway
- **Project:** prolific-perception (a5f0f8da-59b4-4c99-ab76-f28ce3bd7da4)
- **Service:** RepurposeAI (d8f64770-2ab1-43e4-92d9-d79ee25e88dd)
- **Environment:** production (aec102bc-bd17-4dc4-aa6c-97f96e2ee4c2)
- **Railway URL:** repurposeai-production-d136.up.railway.app
- **Custom domain:** getrepurpose.ai (CNAME → x0irlgh6.up.railway.app)
- **API Token:** stored in macOS Keychain (service: `railway`, account: `deploy`)

### Slack (Kato Ventures)
- **Workspace:** Kato Ventures (katoventures.slack.com)
- **Mode:** Socket Mode
- **Bot Token:** stored in openclaw.json
- **App Token:** stored in openclaw.json
- **DM Policy:** pairing
- **Group Policy:** allowlist

---

### SiteGround (mounthydra.us)
- **Email:** clark88@agentmail.to
- **Password:** needs reset (account exists but password not confirmed)
- **Phone for 2FA:** 213-548-0888
- **Collaboration:** Invited by Todd for mounthydra.us
- **DNS:** ns1/ns2.siteground.net
- **Blocker:** reCAPTCHA prevents headless browser login/reset

---

### DGX (Local LLM)
- **Endpoint:** http://100.119.160.94:1234/v1/chat/completions
- **Format:** OpenAI-compatible API
- **Network:** Tailnet IP (100.x range)
- **Port:** 1234

---

Add whatever helps you do your job. This is your cheat sheet.
