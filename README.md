# Emoji Name Changer for Instagram & Facebook

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A simple Python script to update your Instagram display name (with or without emojis) and automatically sync it to your linked Facebook profile. It uses Facebook's Accounts Center API via session cookies for automation. **Use at your own risk—see warnings below.**

## Features
- **Name Updates**: Change Instagram display name directly (supports emojis/Unicode, min 1 character).
- **Bidirectional Sync**: Syncs the new name from Instagram to Facebook (and vice versa via SSO setup).
- **SSO Management**: Enables Single Sign-On between FB and IG for seamless syncing.
- **Cookie-Based Auth**: No API keys needed—just paste your FB cookie.
- **Error Handling**: Checks cookie validity, account linking, and API responses with user-friendly messages.
- **Colorful CLI**: ANSI-colored output for better UX (works on terminals supporting colors).

## Requirements
- **Python**: 3.8 or higher.
- **Libraries**: `requests` (for HTTP calls). Install via:
  ```
  pip install requests
  ```
- **Accounts**: Instagram linked to Facebook via [Accounts Center](https://accountscenter.facebook.com).
- **Cookie**: Fresh Facebook session cookie (extract from browser dev tools).

## Installation
1. Clone or download this repo:
   ```
   git clone https://github.com/keekzz13/Facebook-Name-Emoji-changer-no-limit-for-u-twin.git
   cd Downloads (depends on ur path, Downloads is common if you're in pc)
   ```
   Or just save the `emoji.py` file to a folder.

2. Install dependencies:
   ```
   pip install requests
   ```

3. Make executable (optional, Unix-like systems):
   ```
   chmod +x emoji.py
   ```

## Usage
1. Run the script:
   ```
   python emoji.py
   ```

2. **Enter Cookie**: When prompted, paste your full Facebook cookie (e.g., from Chrome DevTools > Network tab > Copy as cURL > Extract `Cookie:` header).
   - How to get it: Log into FB > F12 > Network > Refresh > Select any request > Headers > Cookie.

3. **Follow Prompts**:
   - Script validates cookie and links.
   - Sets up SSO sync (FB ↔ IG).
   - Enter your new name (e.g., `nvz` or `🦄NvZ👑`).
   - It updates IG first, then syncs to FB.

4. **Output Example**:
   ```
   [+] Verifying your Facebook cookie...
   [✓] Your cookie is active...

   [+] Synchronizing your FB account to Insta...
   [+] Synchronizing your Insta account to FB...

   (+) Enter the name (emoji optional): nvz

   [+] Updating your name on Instagram...
   [+] Synchronizing your name on Facebook...

   Your Name has been changed successfully
   [✓] Your current name is: nvz
   ```

- **Refresh Profiles**: Check IG/FB apps/websites to see changes (may take a few minutes).

## Customization
- **Min Name Length**: Edit `main()` in `emoji.py` (line ~300): Change `if int(name_length) < 1:` to your preference.
- **Locale**: Change `"locale": "fr_FR"` in functions to `"en_US"` for English API responses.
- **Debugging**: Add `print(rp1)` in step functions to log full API responses.

## Warnings & Risks
- **TOS Violation**: Automating via cookies may breach Meta's Terms of Service. Accounts could be flagged, limited, or banned. Test on secondary accounts.
- **API Changes**: Facebook's GraphQL endpoints (e.g., `doc_id`) can update—script may break. Check Network tab in browser for new IDs if errors occur.
- **Cookie Security**: Never share cookies. They grant full session access—use incognito and revoke if compromised.
- **Rate Limits**: Frequent runs may trigger cooldowns ("try again later"). Wait 7-14 days between name changes.
- **No Guarantees**: Success depends on linked accounts and valid cookies. If IG not linked, visit Accounts Center first.
- **Legal/Ethical**: For personal use only. Not for spam, impersonation, or commercial tools.

## Troubleshooting
| Issue | Solution |
|-------|----------|
| `Cookie Invalid or Expired` | Refresh FB login; get fresh cookie. |
| `Instagram Account Not Linked` | Link via [Accounts Center > Profiles](https://accountscenter.facebook.com/profiles). |
| `Connection Error` | Check internet/VPN; retry. |
| `Name too short` | Edit script (min 1 char by default now). |
| `An unknown error occurred` | Run with `print(rp1)` debug; share output for help. |
| Colors not showing (Windows) | Use Git Bash/PowerShell or add `import colorama; colorama.init()`. |

- **Logs**: Script prints statuses; check terminal for details.
- **Updates**: As of Nov 2025, compatible with recent Meta APIs. Fork and PR fixes!

## Credits
- Original script inspired by community tools for FB/IG automation.
- Maintained by: [keekzz13](https://github.com/keekzz13)
- License: MIT—free to use/modify.
- Main: [Emoji](https://github.com/MrUser-404/Fb_emoji)
-# zvynx tuff
---

⭐ Star if useful! Questions? Open an issue. Remember: Use responsibly.
