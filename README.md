# Study Mantra — Kundli + User/Astrologer/Admin + Live Chat

This package is a deployable starter production project for Vercel + Supabase.

## Includes
- Real server-side Swiss Ephemeris Kundli calculation (Lahiri sidereal)
- D1/Rashi/Lagna and D9/Navamsa
- Nakshatra/Pada
- Vimshottari Mahadasha / Antardasha / Pratyantardasha
- Google Places birth-place lookup + Google Time Zone API endpoint
- Supabase authentication
- User, Astrologer and Admin dashboards
- Realtime chat using Supabase Realtime
- Astrologer approval/suspension workflow
- Pricing + discount fields
- Reviews
- RLS policies for user/astrologer/chat/Kundli access
- Hindi/English UI toggle

## Important
The astronomical calculation is based on Swiss Ephemeris. Validate your expected charts against trusted reference software before commercial launch. Swiss Ephemeris licensing must be reviewed for your intended distribution.

## Setup
1. Create a Supabase project.
2. Run `supabase/schema.sql` in Supabase SQL Editor.
3. In Supabase Authentication enable Email/Password.
4. Create your first admin account, then run:
   update public.profiles set role='admin' where email='YOUR_EMAIL';
5. Copy Supabase URL and anon key into `public/js/config.js`.
6. Create a Google Maps browser key restricted to your website and enable Places API (New).
7. Create a separate Google server key and enable Time Zone API. Put it in Vercel as GOOGLE_TIMEZONE_SERVER_KEY.
8. Deploy this folder to Vercel. The Python API requires a Vercel Python-compatible runtime.

## Never put a Supabase service-role key in browser code.
