import os

BOT_TOKEN = os.getenv("BOT_TOKEN") or "YOUR_TELEGRAM_BOT_TOKEN"
SUPABASE_URL = os.getenv("SUPABASE_URL") or "https://your-project.supabase.co"
SUPABASE_KEY = os.getenv("SUPABASE_KEY") or "your-supabase-anon-key"
CHANNEL_ID = int(os.getenv("CHANNEL_ID") or "-1001234567890")
