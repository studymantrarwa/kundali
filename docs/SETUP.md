# Setup checklist

## Supabase
Run `supabase/schema.sql` in SQL Editor. Enable Email/Password authentication.

Create one account for yourself. Then run:
`update public.profiles set role='admin' where email='YOUR_EMAIL';`

Astrologers register as normal users; an admin can change their profile role to `astrologer`, then the astrologer fills the profile. For a production launch, use a controlled onboarding/RPC instead of allowing arbitrary role changes.

## Google
Enable Places API (New) and Time Zone API.
Restrict browser key by HTTP referrer.
Keep the Time Zone server key only in Vercel environment variables.

## Vercel
Set:
- GOOGLE_TIMEZONE_SERVER_KEY

Edit `public/js/config.js` with Supabase URL, anon key and browser Google key.

## Live Chat
Supabase Realtime must be enabled for `chat_messages` and `chat_rooms`. The schema attempts to add both tables to `supabase_realtime`.
