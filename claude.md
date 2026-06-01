**RANDOMS**

Build Guide & Product Blueprint

_A permanent memory archive built by the people who love you_

Version 1.0 • For African Audiences • Flask + HTMX Stack

_Human memories are the hardest we keep - and they slip through time every time we forget. Randoms exists to stop that._

# 1\. What Is Randoms

Randoms is a permanent memory archive built for African audiences. It solves a problem every family has: the photos people take of you at your most important moments - your graduation, your wedding, your birthday - disappear. They vanish into WhatsApp statuses after 24 hours, sit unread in group chats, or stay buried in someone's camera roll forever.

Randoms gives those photos and the words people attach to them a permanent home - built around you, the person being celebrated, not around an event or a platform.

## The Core Problem

- WhatsApp statuses expire after 24 hours - the moment dies
- Family photos live in scattered camera rolls no one shares
- Old photos (CD-Rs, hard copies) have no digital home and no context
- Every other photo app is built for Western audiences with stable internet and tech-comfortable users
- There is no single place where the story of a person's life, told by the people who love them, lives permanently

## The Randoms Solution

- Create an occasion link for any event (graduation, birthday, wedding)
- Share it via WhatsApp - no app download needed for guests
- Guests upload photos and write one comment each
- Everything lives on your personal wall permanently
- The wall grows with you across every occasion of your life
- When you pass, your next of kin gets a living tribute built from everything people remembered about you

# 2\. The Three Wall Types

Randoms has three distinct event types. They all use the same core mechanic - a link, an upload, a comment, a wall - but serve different purposes.

## 2.1 Personal Wall

This is the core product. You are the subject. People add photos and comments to your wall.

- Created by: the person whose life it is
- Upload access: anyone with the occasion link
- View access: only the wall owner (private by default)
- Sharing: owner can share individual posts as cards to social media or WhatsApp
- Expiry: upload window can close; wall never expires

_Example: Kofi creates his graduation occasion. Shares the link in his family WhatsApp. His auntie uploads a photo of him wiping a tear and writes "We are so proud of you chale." That comment lives on Kofi's wall forever._

## 2.2 Group Throwback Wall

A shared memory space for a group - a class, a friend group, a team. Everyone is both contributor and subject.

- Created by: a group representative (e.g. class rep)
- Upload access: anyone with the link
- View access: anyone with the link - forever, no expiry
- Comments: anyone with the link can comment

_Example: The UGBS Class of 2025 class rep creates a graduation throwback wall. Shares the link in the class WhatsApp. Everyone uploads photos from year one to final year. The whole class can go back and watch, comment, and remember - anytime, years later._

## 2.3 Legacy Wall

Activated when the wall owner passes away. The next of kin gains access and can create a permanent tribute.

- Friends and family can continue adding memories
- AI reads the full life archive and builds a tribute video
- Next of kin reviews, edits, and shares the tribute
- The wall stays accessible forever as a living memorial

# 3\. The Legacy Feature (Long-Term Vision)

This is the soul of the product. Every photo, every comment, every occasion across a person's life - when they pass, AI weaves it into a living tribute told through the eyes of everyone who loved them.

## Why This Matters for African Audiences

We don't have the same culture of documenting. Your mother's wedding photos are on a CD-R nobody can read anymore. Your grandfather may have no digital record at all. The people who remembered him are getting older. Randoms becomes the tool that ensures the next generation does not lose their people the same way.

## How It Works

- User designates a next of kin when setting up their account
- User builds their wall over years through occasions - graduations, weddings, births
- When the person passes, the next of kin is notified and gets access to the full archive
- Next of kin unlocks legacy mode: create a tribute video, share the wall, or keep it private
- AI reads every photo, comment, and occasion in the archive
- AI identifies recurring people, emotional moments, and the arc of the person's life
- AI assembles a tribute video: photos sequenced chronologically, comments from loved ones as text or voiceover
- Next of kin reviews, edits if needed, approves the tribute
- A private link is shared with family and friends
- The wall stays accessible forever as a living memorial

## Hard Copy Bridge

People like your mother have physical photos with no digital record. Randoms lets you scan and upload old hard copies, add context and dates, and invite friends and family to comment on them. The CD-R generation and the smartphone generation belong on the same wall.

## Critical Design Note

_This feature touches grief. Every word in this flow must feel human, warm, and unhurried. The next of kin designation must be set while the person is alive and well. Legacy mode must never be triggerable by accident. The AI must never feel clinical._

# 4\. Authentication and Privacy Model

## Two Types of Users

### Event Creator (Account Required)

- Owns their wall permanently
- Creates and manages occasions
- Approves photos before they go live
- Controls privacy settings for each wall
- Login method: Google OAuth only - do not build email/password from scratch
- Implementation: Flask-Dance or Authlib - ~10 lines of code

### Guest / Contributor (Zero Login)

- Clicks a link someone shared
- Types their name - that is it
- Uploads a photo and writes a comment
- Can view the wall (if it is a group wall or if the owner shared it)

_Adding a login step for guests will kill your upload rate. Your auntie from Kumasi will close the app the moment she sees a signup form._

## Privacy Rules by Wall Type

| **Who**                    | **Upload**      | **View Wall**        | **Comment**          |
| -------------------------- | --------------- | -------------------- | -------------------- |
| Wall owner (personal)      | Yes             | Always               | Yes                  |
| Guest with link (personal) | Yes, while open | Only if owner shares | Only if owner shares |
| Anyone with link (group)   | Yes, while open | Forever              | Yes                  |
| Random public (no link)    | Never           | Never                | Never                |

## Sharing a Post from Your Personal Wall

- Owner taps share on any photo - generates a clean card with the photo and comment
- Card shared to WhatsApp as an image - no link back to the private wall
- Download option saves the card to camera roll
- The wall URL never becomes public - only the card image

# 5\. Technology Stack

| **Layer**     | **Choice**        | **Why**                                                                               |
| ------------- | ----------------- | ------------------------------------------------------------------------------------- |
| Backend       | Python Flask      | You know it. Move fast. Golang can come later for performance.                        |
| Frontend      | HTML + HTMX       | No JS framework needed. Forms, uploads, and feeds work natively.                      |
| Database      | PostgreSQL        | Free on Railway or Supabase. Handles all your data cleanly. Use SQLite for local dev. |
| Image Storage | Cloudflare R2     | Free 10GB + 1M requests/month. No egress fees. S3-compatible so code is portable.     |
| Hosting       | Railway or Render | Free tier. Deploys Flask from GitHub in minutes. No server config.                    |
| Auth          | Google OAuth      | Flask-Dance or Authlib. One button login. No passwords to manage.                     |
| Guest Access  | None              | Guests use a link and type a name. No signup ever.                                    |

_Never store images on your Flask server. The moment a photo uploads it goes straight to Cloudflare R2. Your database only ever stores the URL string. This is the single most important architectural decision in the whole project._

# 6\. Database Schema (MVP - 4 Tables Only)

Start with these four tables. Do not add more until you have real users.

## users

| **Field**         | **Type**  | **Notes**                          |
| ----------------- | --------- | ---------------------------------- |
| id                | UUID      | Primary key                        |
| name              | VARCHAR   | From Google profile                |
| email             | VARCHAR   | From Google OAuth                  |
| google_id         | VARCHAR   | Google's unique user ID            |
| avatar_url        | VARCHAR   | Google profile picture             |
| next_of_kin_email | VARCHAR   | For the legacy feature (add later) |
| created_at        | TIMESTAMP |                                    |

## events

| **Field**   | **Type**  | **Notes**                                        |
| ----------- | --------- | ------------------------------------------------ |
| id          | UUID      | Primary key - also used as the share slug        |
| title       | VARCHAR   | e.g. "Kofi's Graduation 2025"                    |
| event_type  | ENUM      | 'personal' or 'group' - drives all privacy logic |
| created_by  | UUID FK   | References users.id                              |
| upload_open | BOOLEAN   | Creator can close uploads without closing view   |
| created_at  | TIMESTAMP |                                                  |

## photos

| **Field**     | **Type**  | **Notes**                                       |
| ------------- | --------- | ----------------------------------------------- |
| id            | UUID      | Primary key                                     |
| event_id      | UUID FK   | References events.id                            |
| uploader_name | VARCHAR   | Guest types this - no account needed            |
| image_url     | VARCHAR   | Cloudflare R2 URL - never store the file itself |
| caption       | TEXT      | The comment the guest writes on upload          |
| is_approved   | BOOLEAN   | Creator approves before it appears on wall      |
| uploaded_at   | TIMESTAMP |                                                 |

## comments

| **Field**      | **Type**  | **Notes**            |
| -------------- | --------- | -------------------- |
| id             | UUID      | Primary key          |
| photo_id       | UUID FK   | References photos.id |
| commenter_name | VARCHAR   | Guest types this     |
| body           | TEXT      | The comment text     |
| created_at     | TIMESTAMP |                      |

# 7\. What Can Break - Risk Register

| **Risk Level** | **Problem**                                                                                           | **Fix**                                                                                                                  |
| -------------- | ----------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| HIGH           | Storing images on Flask server - files wiped on redeploy, disk fills fast, no CDN delivery            | Use Cloudflare R2 from day one. Store only the URL in your DB, never the file.                                           |
| HIGH           | Large photo uploads timing out - a 15MB phone photo over 3G will fail on Flask's default sync request | Compress images client-side before upload using the browser Canvas API. Set max upload size to 8MB. Show a progress bar. |
| MEDIUM         | Someone spams the upload link with 500 photos or offensive content                                    | Rate limit uploads per IP. Creator must approve photos before they appear on the wall.                                   |
| MEDIUM         | Upload link gets shared publicly beyond intended audience                                             | Links are UUIDs (unguessable). Creator can close the upload window anytime.                                              |
| LOW            | Database going down - losing event and comment data                                                   | Supabase and Railway both auto-backup daily on free tier.                                                                |

# 8\. Build Phases - Step by Step

Build in this exact order. Do not skip ahead. Do not build the legacy or AI features until Phase 3 is working with real people.

## Phase 1: The Core Loop (Weeks 1-2)

Goal: A guest can click a link, upload a photo with a comment, and it appears on a wall.

- Set up Flask project structure - app.py, templates/, static/
- Set up PostgreSQL locally with SQLite for dev (or Supabase free tier immediately)
- Create the four tables from Section 6
- Build the event creation page - title, type (personal/group), submit
- On creation, generate a UUID and save as the event ID and share slug
- Build the guest upload page - name field, photo upload, caption field
- Wire the upload to Cloudflare R2: photo goes to R2, URL saved to photos table
- Build the wall page - shows all approved photos with uploader name and caption
- Test the full loop: create event → share link → upload → see on wall

_At this point you have the entire product. Everything else is polish and features on top of this loop._

## Phase 2: Creator Controls (Week 3)

Goal: The event creator can manage their wall properly.

- Add Google OAuth login using Flask-Dance or Authlib
- Lock event creation behind login - guests still need nothing
- Build creator dashboard: list of their events, photo counts
- Add photo approval flow: creator sees pending photos, approves or rejects
- Add upload close/open toggle on each event
- Add comments on individual photos (name + comment, no login needed)
- Add the privacy check: personal walls redirect non-owners to a "This is private" page

## Phase 3: Ship It to Your Class (Week 4)

Goal: Real users, real photos, real feedback.

- Deploy to Railway or Render - connect your GitHub repo, done
- Set up Cloudflare R2 in production with your real bucket
- Talk to your class rep - create the graduation throwback event together
- Share the link in your class WhatsApp group
- Watch what breaks. Watch what people love. Write it all down.
- Fix the top 3 things that broke before telling anyone else about the app

_This is your proof of concept. If the class uploads photos and comments and comes back to look at the wall, the idea works. That's all you need to know before building more._

## Phase 4: Personal Walls and Sharing (After Phase 3)

Goal: The personal wall experience is polished and shareable.

- Build the shareable post card: Flask route that renders photo + comment as a styled image using Pillow
- Add share button on each photo: generates card image, offers WhatsApp share and download
- Add the scan and upload flow for old hard copy photos
- Allow guests to upload photos to an existing personal wall at any time (not just during the event window) if the creator keeps it open
- Notifications: email the wall owner when a new photo is uploaded

## Phase 5: The Legacy Feature (Future)

Goal: When a person passes, their life archive becomes a permanent tribute.

- Add next of kin designation in user settings
- Add legacy mode unlock - requires confirmation, cannot be triggered by accident
- Build the AI summary: feed all photos, captions, and comments to a language model, ask it to identify the emotional arc and key moments
- Build the tribute video assembly: sequence photos chronologically, overlay comments as text
- Add next of kin review and edit interface
- Add private tribute share link for family and friends

_Do not build any of Phase 5 until you have at least 50 real users actively using Phases 1-4. The legacy feature is the soul of the product but it is not the MVP._

# 9\. Cloudflare R2 Image Upload - How to Wire It

This is the most critical technical piece. Get this right in Week 1.

- Create a free Cloudflare account at cloudflare.com
- Go to R2 Object Storage and create a bucket called 'randoms-photos'
- Create an API token with R2 read and write permissions
- Install boto3 in your Flask project: pip install boto3
- In your Flask upload route, use boto3 with the R2 endpoint to push the file
- Save only the returned URL to your photos table - never the file bytes
- In your wall template, use the URL directly in an img tag - R2 serves it as a CDN

_The R2 free tier gives you 10GB storage and 1 million read requests per month. For your early users this is more than enough and costs nothing. When you outgrow it, the cost is genuinely cheap._

## Environment Variables to Set

| **Variable**         | **What It Is**                                      |
| -------------------- | --------------------------------------------------- |
| R2_ENDPOINT_URL      | Your Cloudflare R2 endpoint (found in R2 dashboard) |
| R2_ACCESS_KEY_ID     | Your R2 API token access key                        |
| R2_SECRET_ACCESS_KEY | Your R2 API token secret                            |
| R2_BUCKET_NAME       | randoms-photos (or whatever you named it)           |
| GOOGLE_CLIENT_ID     | From Google Cloud Console OAuth credentials         |
| GOOGLE_CLIENT_SECRET | From Google Cloud Console OAuth credentials         |
| SECRET_KEY           | A long random string for Flask session security     |
| DATABASE_URL         | Your PostgreSQL connection string                   |

# 10\. The Full Product Vision

This is what you are building toward. Keep it visible when the small problems feel big.

## Randoms is three things at once

### The Daily App

Occasion links. Photo walls. Candid moments from people who love you. The unfiltered, unposed, unplanned photos your cousin took when you weren't looking - the ones that tell the truth about who you are.

### The Archive

Your life wall. Every occasion stacked up over years. Your WASSCE results party. Your first day at university. Your graduation. Your wedding. Your children's naming ceremonies. A record of who you were, built by the people who were there.

### The Legacy

What remains. When you are gone, the people you loved most get to keep you. Not a slideshow someone rushed together the night before the funeral. A real, living memory of who you were - in the words and photos of everyone who loved you.

_Every other app treats the event as the product. Randoms treats you as the product. That is the difference. That is what you are building._

**Start with Phase 1. Ship to your class in Week 4. Build from there.**