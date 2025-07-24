# QuickShare Telegram Bot

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Fill in environment variables (or edit config.py):
   - `BOT_TOKEN`, `SUPABASE_URL`, `SUPABASE_KEY`, `CHANNEL_ID`

3. Create a Supabase table named `files` with columns:
   - `id` (text, primary key)
   - `file_type` (text)
   - `channel_msg_id` (integer)
   - `uploaded_by` (text)
   - `timestamp` (timestamp default now())

4. Give your bot admin access to a private Telegram channel.

5. Run locally:
   ```
   python bot.py
   ```

Or deploy on Render / Railway with env vars and Procfile.
