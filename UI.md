# Randoms — UI Design & Implementation Guide

> This document defines every screen, component, layout rule, and interaction pattern for the Randoms webapp. Use it as the single source of truth when building UI with any AI agent or frontend tool.

---

## 1. Product Overview

**Randoms** is a memory-collection webapp. People create occasions (graduations, birthdays, group throwbacks), share a link, and guests upload photos with comments. Photos live permanently on the person's wall. The app is a **Progressive Web App (PWA)** — one codebase that works in the browser and installs as a native-feeling app on Android and iPhone.

**Stack:** Python Flask + HTMX + plain HTML/CSS. No JavaScript framework.

**Hosting:** Railway (not Vercel). Vercel runs Flask as serverless functions — sessions break across invocations, no persistent filesystem, cold starts kill upload UX. Railway runs Flask as a proper always-on server. Deploy from GitHub, free tier is sufficient for MVP. Add a `Procfile` with `web: gunicorn app:app` and Railway detects it automatically.

---

## 2. Design System

### 2.1 Color Palette

| Name | Hex | Usage |
|------|-----|-------|
| Brand Blue | `#1D9BF0` | Buttons, active states, links, brand accents |
| Brand Blue Dark | `#1A8CD8` | Hover states on blue elements |
| Brand Blue Tint | `#1D9BF01A` | Selected backgrounds, tinted fills |
| Background | `#000000` | Page background |
| Surface | `#16181C` | Card/panel background |
| Surface Raised | `#1E2328` | Elevated cards, sidebar |
| Border Default | `rgba(255,255,255,0.12)` | Default borders — 0.5px |
| Border Emphasis | `rgba(255,255,255,0.25)` | Hover borders |
| Text Primary | `#E7E9EA` | Headings, important text |
| Text Secondary | `#71767B` | Body, descriptions |
| Text Tertiary | `#536471` | Timestamps, hints, labels |
| Amber Light | `#3D2E00` | Warning badge backgrounds |
| Amber Text | `#FFB800` | Warning badge text |
| Red Light | `#3D0000` | Reject/danger backgrounds |
| Red Text | `#F4212E` | Danger text and icons |

### 2.2 Typography

```
Font: Sora (Google Fonts) — weights 400 and 500 only. Never use 600 or 700.
Import: @import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;500&display=swap');

Heading large:  20–22px / weight 500 / color Text Primary
Heading medium: 16px   / weight 500 / color Text Primary
Heading small:  13–14px / weight 500 / color Text Primary
Body:           13px   / weight 400 / line-height 1.6 / color Text Secondary
Label:          11px   / weight 400 / color Text Tertiary
Badge/tag:      10px   / weight 500 / uppercase / letter-spacing 0.06em
Mono (links):   font-family: 'JetBrains Mono', monospace / 11px
```

**Rules:**
- Sentence case always. Never Title Case or ALL CAPS in body content.
- No mid-sentence bold. Bold (weight 500) is for headings and labels only.
- Two font weights only: 400 regular, 500 medium.

### 2.3 Spacing & Radius

```
Page padding desktop:   24px horizontal
Page padding mobile:    16px horizontal
Section gap:            20px
Card padding:           14px–16px
Component gap:          8px–12px
Input height:           36px
Button height:          36px
Border radius card:     10px
Border radius input:    6px
Border radius badge:    99px (pill)
Border radius button:   6px
Border width:           0.5px (all borders)
```

### 2.4 Shadows & Effects

- **No drop shadows.** No gradients. No blur. No glow.
- Cards use `border: 0.5px solid` only — no elevation.
- Accent cards (selected/active) use `border: 0.5px solid #9FE1CB` with `background: #E1F5EE`.
- Featured/recommended items use `border: 2px solid #1D9E75` — the only 2px exception.

### 2.5 Icons

Use **Tabler Icons** (outline only, webfont). Include via CDN:
```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css">
```
Usage: `<i class="ti ti-home" aria-hidden="true"></i>`

All decorative icons get `aria-hidden="true"`. Icon-only buttons get `aria-label`.

Common icons used in Randoms:
- `ti-aperture` — app logo
- `ti-calendar-event` — occasions
- `ti-camera` / `ti-photo` — photos
- `ti-wall` — memory wall
- `ti-link` — share link
- `ti-brand-whatsapp` — WhatsApp share
- `ti-check` / `ti-x` — approve/reject
- `ti-bell` — notifications
- `ti-graduation-cap` — graduation
- `ti-cake` — birthday
- `ti-users` — group event
- `ti-lock` — personal/private
- `ti-share` — share action
- `ti-download` — install/save
- `ti-dots` — more options menu

### 2.6 Brand Color Application

The brand blue (`#1D9BF0`) appears on:
- Primary buttons (filled)
- Active nav links (bottom border line — 2px blue underline, Twitter-style)
- Active sidebar items (left border + text)
- The letter "d" in the "randoms" logotype
- Upload progress indicators
- The PWA install pill in browser bar

---

## 3. Layout Architecture

### 3.1 Desktop Layout (≥768px)

```
┌─────────────────────────────────────────────┐
│  NAVBAR  (48px height, full width)          │
├──────────┬──────────────────────────────────┤
│          │                                  │
│ SIDEBAR  │     MAIN CONTENT AREA            │
│ (200px)  │     (flex: 1)                    │
│          │                                  │
│          │                                  │
├──────────┴──────────────────────────────────┤
│  (no bottom nav on desktop)                 │
└─────────────────────────────────────────────┘
```

**Navbar (desktop):**
- Height: 48px
- Left: logo + nav links
- Right: notification bell + avatar
- Border bottom: 0.5px

**Sidebar (desktop):**
- Width: 200px fixed
- Sections separated by small uppercase labels
- Active item: green left border (2px) + green text + green tint background
- Border right: 0.5px

**Main content:**
- Padding: 20px 24px
- Uses CSS Grid for cards: `repeat(auto-fit, minmax(160px, 1fr))`
- Max content width: none — fills available space

### 3.2 Mobile Layout (< 768px)

```
┌──────────────┐
│  TOP NAV     │  (logo + icons only, 48px)
├──────────────┤
│              │
│    MAIN      │
│   CONTENT    │
│              │
│              │
├──────────────┤
│  BOTTOM NAV  │  (4 tabs, 56px)
└──────────────┘
```

**Top nav (mobile):**
- Logo left, bell + avatar right
- No nav links (moved to bottom nav)

**Bottom nav (mobile):**
- 4 items: Home · My Wall · Occasions · Settings
- Active item: green icon + green label
- Height: 56px + safe area inset
- Border top: 0.5px
- Never show sidebar on mobile

**Cards on mobile:**
- Single column always
- Full-width cards
- Reduced padding: 12px

### 3.3 Responsive Breakpoints

```css
/* Mobile first */
@media (min-width: 768px) { /* Tablet/Desktop — show sidebar, hide bottom nav */ }
@media (min-width: 1024px) { /* Desktop — 3-column grids unlock */ }
```

---

## 4. Screens — Implementation Spec

### Screen 1: Landing / Login Page

**Route:** `/`
**Auth:** Logged-out users only. Redirect logged-in users to `/dashboard`.

**Desktop layout:**
- Full-height two-column split (50/50)
- Left column: logo, tagline, sign-in button, "got a link?" note
- Right column: grey background surface showing 2 sample post cards in a 2-column grid as a preview

**Mobile layout:**
- Single column
- Logo + app icon at top
- Tagline text
- Google sign-in button
- "No account? Just use a link someone shared." note below button

**Elements:**
```
App icon: 40x40px, green (#1D9E75) background, border-radius 10px, ti-aperture icon white
Logotype: "randoms" — 18px/500. The letter "d" is #1D9E75, rest is Text Primary
Tagline: "Human memories are the hardest to keep. They slip through time every time we forget."
         — 22px/500 on desktop, 18px on mobile
Body copy: "Collect photos and words from everyone who was there. Build a wall that never disappears."
           — 13px/400, Text Secondary

Google button:
  - Border: 0.5px solid Border Default
  - Background: white
  - Left icon: 14x14px circle, #4285F4 background, white "G" at 8px/700
  - Label: "Continue with Google" — 12–13px/400
  - Full width on mobile, auto width on desktop

PWA install banner (shown by browser automatically):
  - Do not build manually — handled by browser via manifest.json
```

**HTMX:** None needed — static page.

---

### Screen 2: Creator Dashboard

**Route:** `/dashboard`
**Auth:** Requires login. Redirect to `/` if not logged in.

**Desktop layout:**
- Navbar + Sidebar (active: Dashboard) + Main content

**Main content structure:**
1. Greeting: "Good morning, [First name]" — 16px/500
2. Subtitle: any pending approvals count — 12px/400 Text Secondary
3. Stats row: 4 metric cards in a row
4. Two-column section below stats: occasions list (left) + recent activity feed (right)
5. "New occasion" button — green filled, bottom of occasions list

**Stats cards (4):**
- Occasions count
- Photos collected
- Total comments
- Contributors (unique uploaders)
- Each: grey surface background, 22px number, 11px label below

**Occasions list:**
- Most recent active occasion appears as accent card (green tint)
- Shows: title, type badge, photo count, pending approval count if any
- Older/closed occasions: standard white card, grey "closed" badge
- "+ New occasion" button below list, full width, green filled

**Recent activity feed:**
- Simple list of events: "[Name] added a photo to [Occasion]"
- Timestamp right-aligned — "2h ago", "1d ago"
- Green dot (6px circle) left of each row
- Border bottom between rows

**Mobile layout:**
- Stats: 2x2 grid
- Occasions list: full width stacked cards
- Recent activity: below occasions
- Bottom nav active: Home

---

### Screen 3: Create New Occasion

**Route:** `/occasions/new`
**Auth:** Requires login.

**Desktop layout:**
- Two-column: form left, explainer panel right
- Right panel: numbered steps explaining what happens after creation (static, no interaction)

**Mobile layout:**
- Single column form
- Explainer panel collapses to an accordion or is hidden

**Form fields:**

```
1. Occasion name
   Input text, placeholder: "e.g. Graduation 2025, Birthday bash, Class of 2025"
   Required

2. Date
   Date input
   Optional but recommended

3. Occasion type (radio, styled as tile picker)
   Option A — Personal
     Icon: ti-lock, green when selected
     Label: "Personal"
     Sub: "Only you can view"
     Selected state: green tint background, green border
   Option B — Group
     Icon: ti-users, grey when unselected
     Label: "Group"
     Sub: "Anyone with the link"
     Unselected state: grey surface, default border

4. Upload window (how long guests can add photos)
   Styled segmented control — 3 options:
   "7 days" | "30 days" | "Always open"
   Selected: green tint background, green text
   Unselected: grey surface, grey text

5. Submit button
   Label: "Create occasion"
   Style: green filled, full width on mobile, auto width on desktop
```

**After submit:**
- HTMX posts form data
- On success: redirect to share link screen (Screen 4)
- On error: show inline error messages below fields

---

### Screen 4: Share Link

**Route:** `/occasions/<slug>/share`
**Auth:** Requires login (creator only).

**Desktop layout:**
- Centered card, max-width 480px, centered on page
- No sidebar needed — use full-width centered layout

**Mobile layout:**
- Full-width card, page padding

**Elements:**
```
Success illustration area:
  - Green tint background box
  - ti-link icon, 28px, green
  - Heading: "Your occasion is live"
  - Sub: "Share this link so people can add their photos"

Link display row:
  - Grey surface background
  - Monospace font, URL truncated if too long
  - ti-copy icon right — copies to clipboard on click (HTMX or JS)
  - Show "Copied!" feedback for 2 seconds after copy

Primary CTA:
  - "Share to WhatsApp" — green filled button, ti-brand-whatsapp icon left
  - Opens: https://wa.me/?text=encoded_message_with_link

Secondary CTA:
  - "Copy link" — outline button

Footer note (11px, Text Tertiary, centered):
  "Guests don't need an account — just tap the link"
```

---

### Screen 5: Guest Upload Page

**Route:** `/e/<event-slug>`
**Auth:** None — fully public. This is the page guests land on.

**This is the most critical screen. Maximum simplicity.**

**Desktop layout:**
- Two-column: upload form left, wall preview right
- Right panel shows already-approved photos (teaser, not full wall)

**Mobile layout:**
- Single column
- Upload form only — no wall preview panel
- Wall preview is hidden on mobile to reduce distraction

**Top banner (full width, green tint):**
```
"You're adding to [Owner name]'s [Occasion name]"
Sub: "Your photo will be reviewed before it appears · No account needed"
Background: #E1F5EE, border-bottom: 0.5px solid #9FE1CB
```

**Upload form fields:**

```
1. Your name
   Input text, placeholder: "What should Kofi call you?"
   Required
   No login, no email — just a display name

2. Photo upload
   Large dashed upload zone:
     - ti-camera icon, 26px, grey
     - "Tap to choose from camera roll" (mobile)
     - "Click to upload or drag and drop" (desktop)
     - "JPG, PNG up to 8MB · compresses automatically"
   On file selected: show thumbnail preview in the zone
   File is compressed client-side before upload:
     - Max dimension: 1920px
     - Max size after compression: 1MB
     - Use browser Canvas API for compression

3. Comment / message
   Textarea, min-height 64px
   Placeholder: "Leave a message for [Owner name]..."
   Required — a photo must have a comment

4. Submit button
   Label: "Add to [Owner name]'s wall"
   Style: green filled, full width
   Disabled until name + photo + comment are all filled
   On submit: show loading spinner in button, disable form
   On success: replace form with success message
   On error: show error inline
```

**Success state (replaces form):**
```
ti-circle-check icon, green, 32px
"Your photo has been added — [Owner name] will review it shortly"
"Come back to see if it's on the wall"
No redirect. No prompt to sign up.
```

**Wall preview panel (desktop only, right column):**
- Grey surface background
- "Already on the wall" — 12px/500 label
- Show max 2 approved posts as small cards
- Footer: "X more photos · visible to [Owner] only" (for personal) or "X more photos" (for group)

**HTMX implementation:**
- Form submits via `hx-post`, response swaps the form with success state
- No full page reload
- Upload progress shown via `hx-indicator`

---

### Screen 6: My Wall — Social Feed View

**Route:** `/wall`
**Auth:** Requires login. This is the owner's personal feed — their full memory archive across all occasions.
**Accessed from:** Dashboard sidebar "My wall" link, bottom nav "Wall" tab on mobile.

This is NOT a grid. It is a vertical social media feed — like Instagram or Twitter but private and permanent. All approved photos across all of the owner's occasions appear here in reverse chronological order (newest first). Each post takes up meaningful vertical space, like a real social post. The owner scrolls down through their entire life archive in one continuous feed.

---

**Desktop layout:**

```
┌─────────────────────────────────────────────────┐
│  NAVBAR                                         │
├──────────┬──────────────────────────────────────┤
│          │   ┌──────────────────────────────┐   │
│ SIDEBAR  │   │  FEED (max-width 560px,      │   │
│          │   │  centered in main area)      │   │
│ Occasions│   │                              │   │
│ list     │   │  [post]                      │   │
│          │   │  [post]                      │   │
│ Filter   │   │  [post]                      │   │
│ by       │   │  ...                         │   │
│ occasion │   └──────────────────────────────┘   │
└──────────┴──────────────────────────────────────┘
```

The feed column is centred with `max-width: 560px; margin: 0 auto`. Wide screens show whitespace on both sides of the feed — like Twitter's timeline. This is intentional. It keeps the feed readable and intimate.

**Sidebar content (wall view):**
```
Owner name + initials avatar — top of sidebar
"X photos · Y moments" — 11px Text Tertiary

Filter section label: "OCCASIONS"
  - "All moments" (default active)
  - Each occasion listed as sidebar item with icon + name + photo count
  - Clicking an occasion filters the feed to that occasion only (HTMX, no reload)
  Icons by type: ti-graduation-cap, ti-cake, ti-users, ti-calendar-event

Active filter: blue left border (#1D9BF0) + blue tint background
```

---

**Mobile layout:**

```
┌──────────────┐
│  TOP NAV     │
├──────────────┤
│ Occasion     │  ← horizontal scrollable pill filter bar
│ filter pills │     "All · Graduation · Birthday · Class..."
├──────────────┤
│              │
│  FEED        │
│  (full width)│
│              │
├──────────────┤
│  BOTTOM NAV  │
└──────────────┘
```

On mobile the sidebar disappears. Occasion filters become a horizontal scrollable pill row pinned below the top nav. Pills: "All", then one per occasion. Active pill: blue fill (#1D9BF0), white text. Inactive: surface raised background, secondary text.

---

**Feed header (above first post):**
```
Left:  "My wall" — 16px/500
Right: dropdown to sort — "Newest first" | "Oldest first" | "By occasion"
```

---

**Each post in the feed:**

A post is tall and generous — not a compact card. Think of it like a Facebook post from someone who loves you.

```
┌─────────────────────────────────────┐
│  OCCASION CHIP  ← small pill at top │
│  e.g. "🎓 Graduation 2025"          │
│                                     │
│  [PHOTO — full width, max 480px,    │
│   aspect-ratio 4/3, object-fit      │
│   cover, border-radius 8px top]     │
│                                     │
│  ┌─ UPLOADER ROW ────────────────┐  │
│  │ [avatar] Name · timestamp     │  │
│  └───────────────────────────────┘  │
│                                     │
│  COMMENT TEXT                       │
│  Full comment, not truncated.       │
│  14px / 400 / Text Primary          │
│  line-height 1.6                    │
│                                     │
│  ─────────────────────────────────  │
│  ♥ 4   💬 2 replies      [Share →] │
└─────────────────────────────────────┘
```

Post element details:

```
Occasion chip (top of post):
  Inline pill — tiny icon + occasion name
  Background: #E1F5EE, color: #085041, border-radius: 99px
  Font: 10px/500
  Only shown in "All moments" view — hidden when filtered to one occasion

Photo:
  Full width of the feed column (max 480px on desktop, 100% on mobile)
  aspect-ratio: 4 / 3
  object-fit: cover
  border-radius: 8px 8px 0 0 (rounded top only — body attaches below)
  Background: #F0F0EE while loading (grey placeholder)
  Lazy loaded: loading="lazy"

Post body (below photo, same card):
  padding: 14px 16px
  border: 0.5px solid Border Default
  border-top: none (connects flush to photo)
  border-radius: 0 0 10px 10px
  background: white

Uploader row:
  Initials avatar: 32px circle, green tint background, 11px/500 initials
  Name: 13px/500 Text Primary
  Timestamp: 11px Text Tertiary — "May 30 at 2:34pm" (full date, not relative — these are permanent memories)
  Row: display flex, align-items center, gap 8px, margin-bottom 8px

Comment text:
  14px / 400 / Text Primary / line-height 1.6
  Full text — NEVER truncated. This is the soul of the post.
  No italic. Plain text, readable.

Actions row:
  border-top: 0.5px solid Border Default
  padding-top: 8px, margin-top: 10px
  display: flex, align-items: center

  Left side:
    ♥ [count]  — heart/like toggle button
      Liked state: filled heart, blue color (#1D9BF0)
      Unliked: outline heart, Text Tertiary
    💬 [count] replies — opens inline reply thread (see below)

  Right side (margin-left: auto):
    ti-share button — opens share modal (Screen 8)
    text: "Share" — 11px Text Tertiary
```

---

**Inline reply thread (below a post):**

When owner taps "replies", a thread expands inline below the post actions — no modal, no page reload. HTMX fetches and inserts the thread.

```
[thread container — hx-get triggered on click]
  Each reply:
    Small avatar (24px) + name + reply text + timestamp
    Indented 8px from left edge
    Border-left: 2px solid #E1F5EE

  Reply input (owner can reply to their own wall):
    Small text input + "Send" button
    hx-post → appends new reply to thread
```

---

**Empty state (no photos yet):**
```
Centred in feed area:
  ti-aperture icon, 40px, green
  "Your wall is empty"
  "Share an occasion link with someone and ask them to add a photo."
  Link: "Create an occasion →" (green, goes to Screen 3)
```

---

**HTMX — wall feed specific patterns:**

Filter by occasion (sidebar click or pill tap):
```html
<!-- Sidebar occasion item -->
<a hx-get="/wall?occasion={{ occasion.slug }}"
   hx-target="#feed"
   hx-swap="innerHTML"
   hx-push-url="true"
   hx-indicator="#feed-spinner">
  {{ occasion.title }}
</a>

<!-- Feed container -->
<div id="feed">
  {% for photo in photos %}
    {% include 'fragments/feed_post.html' %}
  {% endfor %}
</div>
```

Load more posts (infinite scroll using intersection observer):
```html
<!-- Last post in the feed has this sentinel div -->
<div hx-get="/wall/more?page={{ next_page }}&occasion={{ current_filter }}"
     hx-trigger="intersect once"
     hx-target="#feed"
     hx-swap="beforeend"
     hx-indicator="#load-more-spinner">
</div>
<div id="load-more-spinner" class="htmx-indicator" style="text-align:center;padding:16px;">
  Loading more memories...
</div>
```

Expand reply thread:
```html
<button hx-get="/photos/{{ photo.id }}/replies"
        hx-target="#replies-{{ photo.id }}"
        hx-swap="innerHTML"
        hx-trigger="click once">
  <i class="ti ti-message-circle" aria-hidden="true"></i>
  {{ photo.reply_count }} replies
</button>
<div id="replies-{{ photo.id }}"></div>
```

Like toggle:
```html
<button hx-post="/photos/{{ photo.id }}/like"
        hx-target="#like-{{ photo.id }}"
        hx-swap="outerHTML">
  <span id="like-{{ photo.id }}">
    <i class="ti ti-heart{% if liked %}-filled{% endif %}"
       style="color: {% if liked %}#1D9E75{% else %}var(--text-tertiary){% endif %}"
       aria-hidden="true"></i>
    {{ photo.like_count }}
  </span>
</button>
```

---

### Screen 7: Approval Queue

**Route:** `/occasions/<slug>/approvals`
**Auth:** Requires login as occasion creator.

**Desktop layout:**
- Navbar + Sidebar (active: Approvals with badge) + Main content list

**Mobile layout:**
- Single column list
- Bottom nav active: Occasions

**Header:**
```
Title: "X photos pending — [Occasion name]"
Right: "Approve all X" — green filled button
```

**Each pending row:**
```
Left: 44x44px photo thumbnail (grey placeholder)
Middle:
  - Uploader name — 12px/500
  - Comment preview — 11px italic, Text Secondary, truncated to 1 line
Right:
  - Timestamp — "2h ago", 11px Text Tertiary
  - Approve button: 26px circle, green tint, ti-check green
  - Reject button: 26px circle, red tint, ti-x red
Border bottom between rows
```

**HTMX:**
- Approve/reject each row: `hx-post` → row fades out and removes from list
- "Approve all": `hx-post` → entire list clears
- Counter in sidebar badge updates via `hx-swap-oob`

---

### Screen 8: Share a Post (Modal/Sheet)

**Desktop:** Modal overlay (centered, max-width 400px)
**Mobile:** Bottom sheet (slides up from bottom)

**Content:**

```
Header row: "Share this moment" + close icon (ti-x)

Preview card:
  - Photo (full-width, fixed height 100px, object-fit cover)
  - Below photo:
      "[Uploader name] on [Owner name]'s [Occasion]" — 12px/500
      Comment text — 11px italic
      "randoms.app" — 10px Text Tertiary (branding)
  - Border: 0.5px, border-radius 10px

Note: "Share as a card — your wall stays private" — 11px Text Secondary

Buttons:
  1. "Share to WhatsApp" — green filled, ti-brand-whatsapp icon, full width
  2. "Save to camera roll" — outline, ti-download icon, full width
     (uses Canvas API to render card as image, triggers download)

Desktop modal:
  - Backdrop: rgba(0,0,0,0.3), click backdrop to close
  - Do NOT use position:fixed — use a wrapper div with min-height

Mobile sheet:
  - Slides up from bottom using CSS transform animation
  - Drag handle at top (4x32px grey pill, border-radius 99px)
  - Closes on drag down or tap outside
```

---

### Screen 9: Settings / Profile

**Route:** `/settings`
**Auth:** Requires login.

**Sections:**

```
1. Profile
   - Display name (editable)
   - Profile photo from Google (not editable here)

2. Next of kin (Legacy feature — important)
   - Input: Name of next of kin
   - Input: Their contact (phone or email)
   - Note: "This person will be notified in the event you pass away.
             They will have access to your memory wall."
   - Save button

3. Account
   - "Sign out" — outline button, full width on mobile

4. PWA / App install
   - "Install Randoms as an app" section
   - Show only if app is not already installed (check via JS beforeinstallprompt)
   - Button triggers PWA install prompt
```

---

## 5. PWA Implementation

### 5.1 Required Files

**`/static/manifest.json`:**
```json
{
  "name": "Randoms",
  "short_name": "Randoms",
  "description": "Collect photos and words from everyone who was there.",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#F5F5F3",
  "theme_color": "#1D9E75",
  "icons": [
    { "src": "/static/icons/icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/static/icons/icon-512.png", "sizes": "512x512", "type": "image/png" },
    { "src": "/static/icons/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable" }
  ]
}
```

**`/static/sw.js` (service worker — basic shell caching):**
```javascript
const CACHE = 'randoms-v1';
const SHELL = ['/', '/static/style.css', '/static/icons/icon-192.png'];

self.addEventListener('install', e => e.waitUntil(
  caches.open(CACHE).then(c => c.addAll(SHELL))
));

self.addEventListener('fetch', e => e.respondWith(
  caches.match(e.request).then(r => r || fetch(e.request))
));
```

**In base HTML template `<head>`:**
```html
<link rel="manifest" href="/static/manifest.json">
<meta name="theme-color" content="#1D9E75">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<link rel="apple-touch-icon" href="/static/icons/icon-192.png">
<script>
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/static/sw.js');
  }
</script>
```

### 5.2 Icon Requirements

Create two PNG icons:
- `icon-192.png` — 192x192px — green background (#1D9E75), white aperture icon centered
- `icon-512.png` — 512x512px — same design, larger

### 5.3 Install Prompt (Settings page)

```javascript
let installPrompt;
window.addEventListener('beforeinstallprompt', e => {
  e.preventDefault();
  installPrompt = e;
  document.getElementById('install-btn').style.display = 'block';
});

document.getElementById('install-btn').addEventListener('click', async () => {
  if (installPrompt) {
    await installPrompt.prompt();
    installPrompt = null;
  }
});
```

---

## 6. HTMX — Full Implementation Guide

HTMX is the only dynamic interaction layer. No React, no Vue, no JavaScript framework. Flask returns HTML fragments. HTMX swaps them into the page. The page never does a full reload for user actions.

### 6.0 Setup

Include HTMX in `base.html` `<head>`:
```html
<script src="https://unpkg.com/htmx.org@1.9.12" integrity="sha384-ujb1lZYygJmzgSwoxRggbCHcjc0rB2uPlA23ad5r3IkjPQz2CxoF2cjNpp8jl0Y" crossorigin="anonymous"></script>
```

Global HTMX config — place after the script tag:
```html
<meta name="htmx-config" content='{"defaultSwapStyle":"outerHTML", "indicatorClass":"htmx-loading"}'>
```

Base loading indicator CSS in `style.css`:
```css
.htmx-loading { opacity: 0.5; pointer-events: none; transition: opacity 200ms; }
.htmx-indicator { display: none; }
.htmx-request .htmx-indicator { display: inline-block; }
.htmx-request.htmx-indicator { display: inline-block; }
```

---

### 6.1 How Flask must respond to HTMX requests

Every route that HTMX calls must detect whether it is an HTMX request and return only an HTML fragment — not the full page. Use the `HX-Request` header to detect this.

```python
from flask import request, render_template

def is_htmx():
    return request.headers.get('HX-Request') == 'true'

@app.route('/photos/<int:photo_id>/approve', methods=['POST'])
def approve_photo(photo_id):
    # ... approve logic ...
    if is_htmx():
        return ''  # return empty string — HTMX will remove the row
    return redirect(url_for('approvals'))
```

For fragments that replace UI, return `render_template('fragments/success_upload.html')` instead of the full page template.

Create a `templates/fragments/` folder for all partial HTML responses:
```
templates/
├── fragments/
│   ├── upload_success.html      ← replaces upload form on success
│   ├── upload_error.html        ← replaces form on error
│   ├── photo_card.html          ← single photo card (wall)
│   ├── approval_row.html        ← single approval row
│   ├── occasion_card.html       ← single occasion card (dashboard)
│   └── comment_item.html        ← single comment
```

---

### 6.2 Screen-by-screen HTMX interactions

#### Screen 1 — Landing / Login
No HTMX needed. Google OAuth is a full redirect flow handled by Authlib. Static page.

---

#### Screen 2 — Dashboard

**No HTMX on initial load** — Flask renders the full dashboard server-side.

**Notification badge update** — when user navigates to dashboard, badge updates:
```html
<!-- In base.html navbar -->
<div hx-get="/notifications/count"
     hx-trigger="load"
     hx-swap="innerHTML"
     id="notif-badge">
</div>
```

Flask route returns a fragment:
```python
@app.route('/notifications/count')
def notification_count():
    count = get_pending_count(current_user.id)
    if count == 0:
        return ''
    return f'<span class="badge badge-amb">{count}</span>'
```

---

#### Screen 3 — Create New Occasion

**Form submission — no page reload:**
```html
<form id="new-occasion-form"
      hx-post="/occasions/new"
      hx-target="#new-occasion-form"
      hx-swap="outerHTML"
      hx-indicator="#form-spinner">

  <input type="text" name="title" required>

  <!-- Type picker — radio inputs styled as tiles -->
  <input type="radio" name="event_type" value="personal" checked>
  <input type="radio" name="event_type" value="group">

  <!-- Upload window picker -->
  <input type="radio" name="upload_window" value="7" >
  <input type="radio" name="upload_window" value="30" checked>
  <input type="radio" name="upload_window" value="0">  <!-- 0 = always open -->

  <button type="submit">
    Create occasion
    <span id="form-spinner" class="htmx-indicator">Creating...</span>
  </button>
</form>
```

Flask route on success returns the share link fragment (Screen 4 content), which replaces the form entirely:
```python
@app.route('/occasions/new', methods=['POST'])
def new_occasion():
    # create event, generate slug
    if is_htmx():
        return render_template('fragments/share_link.html', event=event)
    return redirect(url_for('share_link', slug=event.slug))
```

**Inline validation errors** — Flask returns the form fragment with errors marked:
```python
# On validation error:
return render_template('fragments/new_occasion_form.html', errors=errors, form_data=request.form), 422
```

HTMX respects non-2xx status codes — it will still swap on 422 if you add `hx-swap="outerHTML"` and the response contains the form with errors shown.

---

#### Screen 4 — Share Link

**Copy link button — plain JS (clipboard API, no server needed):**
```html
<span id="share-url" class="link-text">randoms.app/e/{{ event.slug }}</span>
<button onclick="copyLink()" id="copy-btn">
  <i class="ti ti-copy" aria-hidden="true"></i> Copy
</button>

<script>
function copyLink() {
  navigator.clipboard.writeText(document.getElementById('share-url').textContent.trim());
  const btn = document.getElementById('copy-btn');
  btn.textContent = 'Copied!';
  setTimeout(() => btn.innerHTML = '<i class="ti ti-copy" aria-hidden="true"></i> Copy', 2000);
}
</script>
```

**WhatsApp share — plain anchor, no HTMX:**
```html
<a href="https://wa.me/?text={{ 'Join my Randoms wall: randoms.app/e/' + event.slug | urlencode }}"
   target="_blank"
   class="btn-primary">
  <i class="ti ti-brand-whatsapp" aria-hidden="true"></i> Share to WhatsApp
</a>
```

---

#### Screen 5 — Guest Upload (most important screen)

**Image compression before upload — plain JS, runs before HTMX sends the request:**
```html
<input type="file" id="photo-input" accept="image/*" onchange="compressImage(this)">
<input type="hidden" id="photo-data" name="photo_data">
<div id="photo-preview"></div>

<script>
async function compressImage(input) {
  const file = input.files[0];
  if (!file) return;
  const bitmap = await createImageBitmap(file);
  const canvas = document.createElement('canvas');
  const MAX = 1920;
  const scale = Math.min(1, MAX / Math.max(bitmap.width, bitmap.height));
  canvas.width = bitmap.width * scale;
  canvas.height = bitmap.height * scale;
  canvas.getContext('2d').drawImage(bitmap, 0, 0, canvas.width, canvas.height);
  const compressed = canvas.toDataURL('image/jpeg', 0.82);
  document.getElementById('photo-data').value = compressed;
  document.getElementById('photo-preview').innerHTML =
    `<img src="${compressed}" style="width:100%;border-radius:6px;">`;
}
</script>
```

**Upload form with HTMX:**
```html
<form id="upload-form"
      hx-post="/e/{{ event.slug }}/upload"
      hx-target="#upload-form"
      hx-swap="outerHTML"
      hx-indicator="#upload-spinner"
      hx-on::before-request="validateUploadForm(event)">

  <input type="text" name="uploader_name" placeholder="Your name" required>
  <input type="file" id="photo-input" accept="image/*" onchange="compressImage(this)">
  <input type="hidden" id="photo-data" name="photo_data">
  <textarea name="caption" placeholder="Leave a message..." required></textarea>

  <button type="submit" id="upload-btn" disabled>
    Add to {{ event.owner.name }}'s wall
    <span id="upload-spinner" class="htmx-indicator">Uploading...</span>
  </button>
</form>

<script>
function validateUploadForm(evt) {
  const name = document.querySelector('[name=uploader_name]').value.trim();
  const photo = document.getElementById('photo-data').value;
  const caption = document.querySelector('[name=caption]').value.trim();
  if (!name || !photo || !caption) {
    evt.preventDefault();  // stop HTMX from sending
    document.getElementById('form-error').textContent = 'Please fill in all fields and add a photo.';
  }
}

// Enable submit button only when all fields filled
document.querySelectorAll('input, textarea').forEach(el => {
  el.addEventListener('input', () => {
    const name = document.querySelector('[name=uploader_name]').value.trim();
    const photo = document.getElementById('photo-data').value;
    const caption = document.querySelector('[name=caption]').value.trim();
    document.getElementById('upload-btn').disabled = !(name && photo && caption);
  });
});
</script>
```

Flask route returns the success fragment on upload, which replaces the entire form:
```python
@app.route('/e/<slug>/upload', methods=['POST'])
def guest_upload(slug):
    # save photo to R2, create DB record
    if is_htmx():
        return render_template('fragments/upload_success.html', owner_name=event.owner.name)
    return redirect(url_for('upload_page', slug=slug))
```

`upload_success.html` fragment:
```html
<div id="upload-form" style="text-align:center; padding: 32px 16px;">
  <i class="ti ti-circle-check" style="font-size:40px; color:#1D9E75;" aria-hidden="true"></i>
  <p style="font-size:14px; font-weight:500; margin-top:12px;">
    Your photo has been added — {{ owner_name }} will review it shortly.
  </p>
  <p style="font-size:12px; color:#6B6B66; margin-top:6px;">
    Come back to see if it's on the wall.
  </p>
</div>
```

---

#### Screen 6 — Memory Wall

**Load more photos (infinite scroll or button):**
```html
<!-- Button approach — simpler, more reliable on mobile -->
<div id="photo-grid">
  {% for photo in photos %}
    {% include 'fragments/photo_card.html' %}
  {% endfor %}
</div>

<button hx-get="/wall/{{ event.slug }}/photos?page={{ next_page }}"
        hx-target="#photo-grid"
        hx-swap="beforeend"
        hx-indicator="#load-more-spinner">
  Load more
  <span id="load-more-spinner" class="htmx-indicator">Loading...</span>
</button>
```

**Heart / like a photo:**
```html
<!-- In photo_card.html fragment -->
<button hx-post="/photos/{{ photo.id }}/like"
        hx-target="#like-count-{{ photo.id }}"
        hx-swap="innerHTML"
        aria-label="Like this photo">
  <i class="ti ti-heart" aria-hidden="true"></i>
  <span id="like-count-{{ photo.id }}">{{ photo.like_count }}</span>
</button>
```

Flask returns just the updated count:
```python
@app.route('/photos/<int:photo_id>/like', methods=['POST'])
def like_photo(photo_id):
    new_count = toggle_like(photo_id, session.get('guest_name'))
    if is_htmx():
        return str(new_count)
    return redirect(request.referrer)
```

**Out-of-band sidebar update** — when viewing a wall, keep sidebar occasion count current:
```html
<!-- Flask can return this alongside the main fragment -->
<div id="sidebar-photo-count" hx-swap-oob="true">{{ total_count }} photos</div>
```

---

#### Screen 7 — Approval Queue

**Approve a single photo — row disappears:**
```html
<!-- In approval_row.html fragment -->
<div class="approve-row" id="approval-{{ photo.id }}">
  <div class="thumb">...</div>
  <div class="approve-meta">
    <div class="approve-name">{{ photo.uploader_name }}</div>
    <div class="approve-caption">{{ photo.caption }}</div>
  </div>
  <button hx-post="/photos/{{ photo.id }}/approve"
          hx-target="#approval-{{ photo.id }}"
          hx-swap="outerHTML swap:300ms"
          aria-label="Approve photo from {{ photo.uploader_name }}">
    <i class="ti ti-check" aria-hidden="true"></i>
  </button>
  <button hx-post="/photos/{{ photo.id }}/reject"
          hx-target="#approval-{{ photo.id }}"
          hx-swap="outerHTML swap:300ms"
          aria-label="Reject photo from {{ photo.uploader_name }}">
    <i class="ti ti-x" aria-hidden="true"></i>
  </button>
</div>
```

Flask returns empty string to remove the row, plus OOB badge update:
```python
@app.route('/photos/<int:photo_id>/approve', methods=['POST'])
def approve_photo(photo_id):
    approve(photo_id)
    remaining = get_pending_count(current_user.id)
    if is_htmx():
        # empty string removes the row, OOB updates the badge
        badge = f'<span id="pending-badge" hx-swap-oob="true" class="badge badge-amb">{remaining}</span>' if remaining else '<span id="pending-badge" hx-swap-oob="true"></span>'
        return badge
    return redirect(url_for('approvals'))
```

**Approve all — full list clears:**
```html
<button hx-post="/occasions/{{ event.slug }}/approve-all"
        hx-target="#approval-list"
        hx-swap="innerHTML"
        hx-confirm="Approve all {{ pending_count }} photos?">
  Approve all {{ pending_count }}
</button>
```

Flask returns empty `<div id="approval-list"></div>` with a success message inside.

---

#### Screen 8 — Share Post Modal

**Open modal without page reload:**
```html
<!-- On the wall, each post's share button -->
<button hx-get="/photos/{{ photo.id }}/share-card"
        hx-target="#modal-container"
        hx-swap="innerHTML">
  <i class="ti ti-share" aria-hidden="true"></i> Share
</button>

<!-- Modal container always present in base.html, empty by default -->
<div id="modal-container"></div>
```

Flask returns the modal HTML fragment which renders inside `#modal-container`:
```python
@app.route('/photos/<int:photo_id>/share-card')
def share_card(photo_id):
    if is_htmx():
        return render_template('fragments/share_modal.html', photo=photo)
    return redirect(url_for('wall'))
```

**Close modal:**
```html
<!-- In share_modal.html -->
<div class="modal-backdrop"
     hx-get="/empty"
     hx-target="#modal-container"
     hx-swap="innerHTML">
  <div class="modal-card" onclick="event.stopPropagation()">
    ...
    <button hx-get="/empty"
            hx-target="#modal-container"
            hx-swap="innerHTML">
      <i class="ti ti-x" aria-hidden="true"></i>
    </button>
  </div>
</div>
```

Flask `/empty` route returns an empty string — clears the modal container.

---

#### Screen 9 — Settings

**Save profile name inline:**
```html
<form hx-post="/settings/profile"
      hx-target="#profile-section"
      hx-swap="outerHTML">
  <input type="text" name="display_name" value="{{ current_user.name }}">
  <button type="submit">Save</button>
</form>
```

Flask returns the updated profile section fragment with a success flash message included.

**Save next of kin:**
```html
<form hx-post="/settings/next-of-kin"
      hx-target="#kin-section"
      hx-swap="outerHTML">
  <input type="text" name="kin_name" value="{{ current_user.kin_name or '' }}">
  <input type="text" name="kin_contact" value="{{ current_user.kin_contact or '' }}">
  <button type="submit">Save</button>
</form>
```

---

### 6.3 HTMX — Global Rules for the Agent

These rules apply to every screen. Never break them.

1. **Every hx-post and hx-get must have a matching Flask route** that checks `is_htmx()` and returns a fragment, not a full page.

2. **Always set hx-target and hx-swap explicitly.** Never rely on defaults for anything beyond trivial cases.

3. **Use hx-indicator on every form submit and every button that triggers a server request.** Users must always see that something is happening.

4. **Never use hx-boost on the whole page.** Apply HTMX only to specific elements that need it.

5. **Flash messages / toasts** — return them as OOB swaps alongside the main fragment:
```html
<!-- In any Flask fragment response, append this for user feedback -->
<div id="toast" hx-swap-oob="true" class="toast toast-success">
  Photo approved
</div>
```

6. **HTMX and file uploads** — HTMX can submit forms with `enctype="multipart/form-data"` but for this app, image data is sent as a base64 string in a hidden field (after client-side compression). This avoids multipart complexity.

7. **hx-confirm for destructive actions** — use on reject, close event, delete:
```html
hx-confirm="Are you sure you want to reject this photo?"
```

8. **Transitions** — add `hx-swap="outerHTML transition:true"` for smooth element removal. Pair with CSS:
```css
.htmx-swapping { opacity: 0; transition: opacity 200ms ease-out; }
```

9. **Browser history** — use `hx-push-url="true"` on major navigation actions (switching between occasions on the wall) so the back button works correctly.

10. **Error handling** — HTMX triggers `htmx:responseError` on 4xx/5xx. Add a global error handler in `base.html`:
```html
<script>
document.body.addEventListener('htmx:responseError', function(evt) {
  document.getElementById('toast').innerHTML =
    '<div class="toast toast-error">Something went wrong. Try again.</div>';
});
</script>
```

---

## 7. Accessibility Rules

- Every image uploaded by users gets `alt=""` (decorative) or the uploader's comment as alt text
- All icon-only buttons have `aria-label`
- All decorative icons have `aria-hidden="true"`
- All interactive elements are keyboard-accessible (tab order follows visual order)
- Colour is never the only indicator of state — use text or icon alongside colour
- Forms have visible labels — no placeholder-only labels
- Error messages are associated with fields via `aria-describedby`

---

## 8. Build Order

Build screens in this sequence. Each depends on the previous.

```
Phase 1 — Core loop (Week 1–2)
  1. base.html template (navbar, sidebar, bottom nav, CSS variables)
  2. Landing / login page (Screen 1)
  3. Guest upload page (Screen 5) ← most critical, build early
  4. Share link page (Screen 4)

Phase 2 — Creator controls (Week 3)
  5. Dashboard (Screen 2)
  6. Create occasion (Screen 3)
  7. Memory wall (Screen 6)
  8. Approval queue (Screen 7)

Phase 3 — Polish (Week 4)
  9. Share post modal (Screen 8)
  10. Settings / profile (Screen 9)
  11. PWA manifest + service worker
  12. Mobile responsiveness pass — test every screen at 390px width
```

---

## 9. File Structure

```
randoms/
├── app.py
├── models.py
├── routes/
│   ├── auth.py
│   ├── events.py
│   └── uploads.py
├── storage.py
├── templates/
│   ├── base.html          ← navbar, sidebar, bottom nav, head
│   ├── landing.html       ← Screen 1
│   ├── dashboard.html     ← Screen 2
│   ├── new_occasion.html  ← Screen 3
│   ├── share_link.html    ← Screen 4
│   ├── upload.html        ← Screen 5 (guest, no login)
│   ├── wall.html          ← Screen 6
│   ├── approvals.html     ← Screen 7
│   └── settings.html      ← Screen 9
├── static/
│   ├── style.css
│   ├── sw.js
│   ├── manifest.json
│   └── icons/
│       ├── icon-192.png
│       └── icon-512.png
├── .env
└── requirements.txt
```

---

## 10. Key Design Decisions (Do Not Change)

1. **Guests never sign up.** The upload page asks for a name only. No email, no password, no Google. Ever.
2. **Owners approve before photos go live.** Every photo sits in a pending queue until the creator taps approve.
3. **Personal walls are private.** Only the owner sees them unless they explicitly share a single post as a card.
4. **Group walls are viewable by anyone with the link.** The link does not expire for viewing. Upload window can close.
5. **Photos are stored in Cloudflare R2.** Never on the Flask server. Only the URL string goes in the database.
6. **Comments are mandatory.** A guest cannot upload a photo without writing something. This is the soul of the product.
7. **The wall never deletes.** There is no auto-expiry. Photos and comments are permanent unless the owner manually removes them.