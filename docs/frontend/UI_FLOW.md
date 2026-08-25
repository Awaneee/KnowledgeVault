# KnowledgeVault Flutter — UI Flow

**Version:** 1.0.0  
**Date:** 2026-08-06

This document describes the complete user journey across every screen and the navigation transitions between them.

---

## Navigation Map (High Level)

```
                    ┌──────────────────────────────────────┐
                    │             Splash Screen             │
                    └──────────────┬───────────────────────┘
                                   │
              ┌────────────────────┼────────────────────┐
              │                   │                     │
         Token valid         No token stored       Token invalid
              │                   │                    (401)
              ▼                   ▼                     │
         Dashboard           Login Screen  ◄────────────┘
                                  │
                    ┌─────────────┴──────────────┐
                    │                            │
               "Register"                   Login success
                    │                            │
              Register Screen              Dashboard
                    │
               Register success
                    │
               Login Screen (banner)
```

---

## Shell Navigation (Bottom Navigation Bar)

After login, all primary screens share a persistent shell with a bottom nav bar (mobile) or navigation rail (tablet).

```
Bottom Nav Items:
  🏠 Dashboard    /dashboard
  📝 Notes        /notes
  🔍 Search       /notes/search
  🤖 Ask AI       /ask
  ⚙️  Settings     /settings
```

Tapping a bottom nav item preserves its scroll state. The back button inside a shell tab navigates within the tab stack, not to the previous tab.

---

## Screen: Splash

**Route:** `/`  
**Purpose:** Token validation on startup.

```
┌────────────────────────────────────┐
│                                    │
│                                    │
│           KnowledgeVault           │
│              [Logo]                │
│                                    │
│          ●  ●  ●  (pulsing)        │
│                                    │
└────────────────────────────────────┘
```

**Flow:**
1. App opens → show logo + loading indicator.
2. Read token from `flutter_secure_storage`.
   - No token → navigate to `/login`.
   - Token found → call `GET /auth/me`.
     - 200 → hydrate `currentUserProvider` → navigate to `/dashboard`.
     - 401 → clear token → navigate to `/login`.
3. Max wait: 5 seconds. If request times out → navigate to `/login` with error snackbar.

---

## Screen: Login

**Route:** `/login`

```
┌────────────────────────────────────┐
│         KnowledgeVault             │
│                                    │
│  ┌──────────────────────────────┐  │
│  │  Email                       │  │
│  └──────────────────────────────┘  │
│  ┌──────────────────────────────┐  │
│  │  Password             👁      │  │
│  └──────────────────────────────┘  │
│                                    │
│  ┌──────────────────────────────┐  │
│  │         Log In               │  │
│  └──────────────────────────────┘  │
│                                    │
│  Don't have an account? Register   │
└────────────────────────────────────┘
```

**Flow:**
- Tap "Log In" → `POST /auth/login`.
  - 200 → save token → navigate to `/dashboard`.
  - 401 → inline error "Incorrect email or password".
  - 429 → snackbar "Too many attempts. Try again in a minute."
- Tap "Register" → navigate to `/register`.
- Session expired redirect: pre-fill email if known from `currentUserProvider`.

**Validation (client-side, before API call):**
- Email: valid format.
- Password: non-empty.

---

## Screen: Register

**Route:** `/register`

```
┌────────────────────────────────────┐
│  ← Back                            │
│         Create Account             │
│                                    │
│  ┌──────────────────────────────┐  │
│  │  Username                    │  │
│  └──────────────────────────────┘  │
│  ┌──────────────────────────────┐  │
│  │  Email                       │  │
│  └──────────────────────────────┘  │
│  ┌──────────────────────────────┐  │
│  │  Password             👁      │  │
│  └──────────────────────────────┘  │
│  Password must be at least 8 chars │
│                                    │
│  ┌──────────────────────────────┐  │
│  │       Create Account         │  │
│  └──────────────────────────────┘  │
│                                    │
│  Already have an account? Log In   │
└────────────────────────────────────┘
```

**Flow:**
- Tap "Create Account" → `POST /auth/register`.
  - 201 → navigate to `/login` with success banner "Account created — please log in."
  - 400 email/username conflict → inline field error.
  - 422 → show field-level validation messages from Pydantic response.
- Tap "Log In" → navigate to `/login`.

**Validation (client-side):**
- Username: non-empty.
- Email: valid format.
- Password: min 8 characters (mirrors backend `Field(min_length=8)`).

---

## Screen: Dashboard

**Route:** `/dashboard`

```
┌────────────────────────────────────┐
│  KnowledgeVault          [Profile] │
│                                    │
│  Good morning, Awane               │
│                                    │
│  ┌──────────┐ ┌──────────────────┐ │
│  │  12      │ │  Ask AI          │ │
│  │  Notes   │ │  "What should    │ │
│  └──────────┘ │  I work on?"     │ │
│               └──────────────────┘ │
│                                    │
│  Recent Notes                      │
│  ┌──────────────────────────────┐  │
│  │ 📝 Meeting with Sid          │  │
│  │    2 hours ago               │  │
│  └──────────────────────────────┘  │
│  ┌──────────────────────────────┐  │
│  │ 📝 System design notes       │  │
│  │    Yesterday                 │  │
│  └──────────────────────────────┘  │
│                                    │
│  Topics at a Glance                │
│  ┌──────┐ ┌──────┐ ┌──────┐       │
│  │ Work │ │Study │ │ Life │       │
│  └──────┘ └──────┘ └──────┘       │
│                                    │
│  🏠      📝      🔍      🤖      ⚙ │
└────────────────────────────────────┘
```

**Data sources:**
- Recent notes: from `notesProvider` (take last 5 by `created_at`).
- Note count: `notesProvider.length`.
- Topics at a Glance: from `topicsProvider` (take first 5 topics).

**Navigation from Dashboard:**
- Tap note card → `/notes/:id`
- Tap "Ask AI" shortcut → `/ask`
- Tap topic chip → `/topics` (scrolled to that cluster)
- Tap profile icon → `/profile`
- Bottom nav items

---

## Screen: Notes

**Route:** `/notes`

```
┌────────────────────────────────────┐
│  My Notes              [+] [🔍]   │
│                                    │
│  Filter: All ▾   [Sort: Newest ▾] │
│                                    │
│  ┌──────────────────────────────┐  │
│  │ Meeting with Sid             │  │
│  │ We discussed the Q3 roadmap… │  │
│  │ 2h ago  · Work               │  │
│  └──────────────────────────────┘  │
│  ┌──────────────────────────────┐  │
│  │ System design notes          │  │
│  │ CAP theorem: you can only… … │  │
│  │ Yesterday  · Study           │  │
│  └──────────────────────────────┘  │
│  ┌──────────────────────────────┐  │
│  │ + Add note                   │  │
│  └──────────────────────────────┘  │
│                                    │
│  🏠      📝      🔍      🤖      ⚙ │
└────────────────────────────────────┘
```

**Flow:**
- Lists all notes (`GET /notes/`). Client-side sort by `created_at`.
- Category filter: chips row from `categoriesProvider`. Tap chip → filter list client-side.
- Tap note card → `/notes/:id`
- Tap [+] or "Add note" → `/notes/new`
- Tap [🔍] → `/notes/search`
- Swipe left on note card → reveal delete action (confirm dialog → `DELETE /notes/:id`).
- Pull to refresh → re-fetch `GET /notes/`.

---

## Screen: Create Note

**Route:** `/notes/new`

```
┌────────────────────────────────────┐
│  ← Back             [Save]         │
│  New Note                          │
│                                    │
│  ┌──────────────────────────────┐  │
│  │  Start writing...            │  │
│  │                              │  │
│  │                              │  │
│  │                              │  │
│  └──────────────────────────────┘  │
│                                    │
│  ─── or ───                        │
│  📎 Import from file (PDF/TXT/DOCX)│
│                                    │
│  Character count: 0 / 50,000       │
└────────────────────────────────────┘
```

**Flow:**
- Tap [Save] → `POST /notes/` with content.
  - 201 → navigate to `NoteDetailScreen` for the new note.
- Tap "Import from file" → platform file picker → `POST /uploads/file`.
  - 200 → navigate to `NoteDetailScreen` for `note_id` in response.
- Character count shown live. Warn at 45,000. Block at 50,000 (`max_length`).

---

## Screen: Note Detail

**Route:** `/notes/:id`

```
┌────────────────────────────────────┐
│  ←           Meeting with Sid  [⋮]│
│                                    │
│  We discussed the Q3 roadmap…      │
│                                    │
│  [Content body — scrollable]       │
│                                    │
│  ─── Intent ───────────────────── │
│  Type: Communication               │
│  Actor: Sid   Action: Discuss      │
│  Urgency: medium                   │
│                                    │
│  ─── Related Notes ─────────────  │
│  📝 Q3 planning notes              │
│  📝 Sid's feedback                 │
│                                    │
│  ─── Attachments ───────────────  │
│  📄 roadmap.pdf      [📎 Add]      │
│                                    │
│  [Delete note]                     │
└────────────────────────────────────┘
```

**Data loaded in parallel:**
1. `GET /notes/:id` — main content.
2. `GET /notes/:id/related` — related notes section (lazy).
3. `GET /intents/notes/:id` — intent panel (lazy, hide if 404).
4. `GET /notes/:id/attachments` — attachments section (lazy).

**[⋮] menu actions:**
- Delete → confirmation dialog → `DELETE /notes/:id` → navigate back.
- Share (future — not backed by API).

**Navigation from Note Detail:**
- Tap related note → `/notes/:related_id`
- Tap attachment → platform file viewer (file:// path from `file_path` field)
- Tap [📎 Add] → file picker → `POST /attachments/?note_id=:id`

---

## Screen: Search

**Route:** `/notes/search`

```
┌────────────────────────────────────┐
│  ← Search notes                    │
│  ┌──────────────────────────────┐  │
│  │ 🔍  Type to search…          │  │
│  └──────────────────────────────┘  │
│                                    │
│  Smart  │  Semantic  │  Chunks     │
│  ─────────────────────────────     │
│                                    │
│  [Results appear here]             │
│  ┌──────────────────────────────┐  │
│  │ Note title                   │  │
│  │ …matched content snippet…    │  │
│  └──────────────────────────────┘  │
│                                    │
│  🏠      📝      🔍      🤖      ⚙ │
└────────────────────────────────────┘
```

**Tabs:**
- **Smart** (default): `GET /notes/search?q=` — note-level semantic search.
- **Semantic**: `POST /retrieve` — chunk-level semantic retrieval.
- **Chunks**: `POST /retrieve/hybrid` — intent-aware hybrid retrieval.

**Flow:**
- Debounce 400ms after user stops typing.
- Cancel previous in-flight request on each new keystroke (Dio cancel token).
- Empty query → show "Start typing to search" placeholder.
- No results → show "No notes found for this query."
- Tap result → `/notes/:id`

---

## Screen: AI Ask

**Route:** `/ask`

```
┌────────────────────────────────────┐
│  Ask KnowledgeVault         [Mode] │
│                                    │
│  ╔════════════════════════════╗    │
│  ║  Based on your notes, here ║    │
│  ║  is what I found…          ║    │
│  ║                            ║    │
│  ║  [1] See Meeting with Sid  ║    │
│  ║  [2] See Q3 planning notes ║    │
│  ╚════════════════════════════╝    │
│                                    │
│  Sources:                          │
│  ┌──────────┐ ┌──────────────┐    │
│  │[1] Note  │ │[2] Note      │    │
│  │title     │ │title         │    │
│  └──────────┘ └──────────────┘    │
│                                    │
│  ┌──────────────────────────────┐  │
│  │  Ask a question…          ➤  │  │
│  └──────────────────────────────┘  │
│                                    │
│  🏠      📝      🔍      🤖      ⚙ │
└────────────────────────────────────┘
```

**Mode toggle:** [Mode] button switches between streaming (default) and full response.

**Streaming flow (default):**
1. User submits question.
2. Disable input field + send button.
3. Show typing indicator (three pulsing dots in assistant bubble).
4. Call `POST /ask/stream`.
5. Parse SSE tokens → append to answer text progressively.
6. On stream end → re-enable input.
7. Show "See full answer with citations →" chip to trigger `POST /ask/`.

**Full response flow:**
1. User submits question.
2. Show thinking animation.
3. Call `POST /ask/`.
4. On response:
   - `status: "ok"` → render `answer` with inline citation chips.
   - `retrievalOnly: true` → show degraded banner + `chunks` as note cards.
5. Citation `[N]` in answer text → tappable; opens `BottomSheet` with snippet and "Go to note →" navigation.

**Degraded state:**
```
┌──────────────────────────────────────┐
│  ⚠️  AI answer unavailable right now  │
│  Here are the most relevant notes:   │
│  ┌──────────────────────────────┐    │
│  │ Chunk title           0.92   │    │
│  │ …preview text…               │    │
│  └──────────────────────────────┘    │
└──────────────────────────────────────┘
```

---

## Screen: Categories

**Route:** `/categories`

```
┌────────────────────────────────────┐
│  Categories                  [+]   │
│                                    │
│  ┌──────────────────────────────┐  │
│  │ Work              12 notes   │  │
│  └──────────────────────────────┘  │
│  ┌──────────────────────────────┐  │
│  │ Study             8 notes    │  │
│  └──────────────────────────────┘  │
│  ┌──────────────────────────────┐  │
│  │ Personal          5 notes    │  │
│  └──────────────────────────────┘  │
│                                    │
│  [+ Add category]                  │
└────────────────────────────────────┘
```

**Note counts:** Client-side from `notesProvider` (`notes.where(n => n.categoryId == category.id).length`).

**Flow:**
- Tap [+] or "Add category" → bottom sheet with text input → `POST /categories/`.
- Tap category row → `CategoryNotesScreen` (filters `notesProvider` client-side by `categoryId`).

**`CategoryNotesScreen`** (`/categories/:id`):
- Same layout as `NotesScreen` but pre-filtered to that category.
- Title: category name.
- No separate API call needed — filter from cached `notesProvider`.

---

## Screen: Topics

**Route:** `/topics`  
*(Accessible via Dashboard chips or nav drawer — not in bottom nav)*

```
┌────────────────────────────────────┐
│  ← Topics                          │
│                                    │
│  ▸ Work                  8 notes   │
│  ▸ System Design         5 notes   │
│  ▸ Personal              4 notes   │
│  ▸ Projects              3 notes   │
│                                    │
└────────────────────────────────────┘
```

**Expand a topic:**
```
  ▼ Work                  8 notes
    📝 Meeting with Sid
    📝 Q3 roadmap notes
    📝 Standup notes
    …
```

**Flow:**
- Data: `GET /topics/` — returns AI-clustered topic groups.
- Each note item → tap → `/notes/:id`.
- If topics list is empty: "Add more notes to see AI-generated topics."

---

## Screen: Intents

**Route:** `/intents`  
*(Accessible via nav drawer or Dashboard section)*

```
┌────────────────────────────────────┐
│  ← Smart Organisation              │
│                                    │
│  📬 Communication       5 notes    │
│  ✅ Todo                3 notes    │
│  📚 Study               8 notes    │
│  💡 Idea                2 notes    │
│  📅 Event               1 note     │
│                                    │
└────────────────────────────────────┘
```

**Flow:**
- Data: `GET /intents/categories`.
- `intentType` mapped to icon and colour.
- Tap intent category row → `/intents/:id/notes`.

**`IntentCategoryNotesScreen`** (`/intents/:id/notes`):
```
┌────────────────────────────────────┐
│  ← Communication  (5 notes)        │
│  Actor: Sid                        │
│                                    │
│  📝 Meeting with Sid               │
│     We discussed the Q3 roadmap…   │
│                                    │
│  📝 Email to the team              │
│     Reminder to send the update…   │
│                                    │
└────────────────────────────────────┘
```

Data: `GET /intents/categories/:id/notes`.

---

## Screen: Settings

**Route:** `/settings`

```
┌────────────────────────────────────┐
│  Settings                          │
│                                    │
│  ── Appearance ──────────────────  │
│  Theme              System ▾       │
│                                    │
│  ── Account ─────────────────────  │
│  Email         user@example.com    │
│  Change password        →          │
│                                    │
│  ── AI Features ─────────────────  │
│  Organise my notes      [Run]      │
│  (Runs AI intent detection on      │
│   notes without a category)        │
│                                    │
│  ── Connection ──────────────────  │
│  Server status         ● Online    │
│                                    │
│  ── ─────────────────────────────  │
│  Log out                           │
└────────────────────────────────────┘
```

**Flows:**
- **Theme:** toggle light/dark/system — persisted to `SharedPreferences`. No API call.
- **Organise my notes:** confirm dialog → `POST /intents/backfill` → show progress → "Done: 12 notes organised."
- **Server status:** `GET /health` on page open. Green dot = ok, amber = degraded.
- **Log out:** clear token from `flutter_secure_storage`. Clear `currentUserProvider`. Navigate to `/login`.

---

## Screen: Profile

**Route:** `/profile`

```
┌────────────────────────────────────┐
│  ← Profile                         │
│                                    │
│       [Avatar initials circle]     │
│                                    │
│  Username         awane            │
│  Email            user@thapar.edu  │
│  User ID          #42              │
│                                    │
│  Member since     August 2026      │
│                                    │
│  ── Stats ───────────────────────  │
│  Total notes      12               │
│  Categories        3               │
│  Intent categories 5               │
│                                    │
│  Log out                           │
└────────────────────────────────────┘
```

**Data:**
- User info: from `currentUserProvider` (cached `GET /auth/me` response).
- Stats: derived client-side from `notesProvider`, `categoriesProvider`, `intentsProvider`.

---

## Navigation Summary Table

| From | Action | To |
|------|--------|----|
| Splash | No token | Login |
| Splash | Token valid | Dashboard |
| Splash | Token invalid (401) | Login |
| Login | Login success | Dashboard |
| Login | Tap "Register" | Register |
| Register | Register success | Login (with banner) |
| Register | Tap "Log In" | Login |
| Dashboard | Tap note card | Note Detail |
| Dashboard | Tap "Ask AI" | Ask AI |
| Dashboard | Tap profile icon | Profile |
| Dashboard | Tap topic chip | Topics |
| Notes | Tap note | Note Detail |
| Notes | Tap [+] | Create Note |
| Notes | Tap [🔍] | Search |
| Notes | Swipe delete | (in place, confirm dialog) |
| Note Detail | Tap related note | Note Detail |
| Note Detail | Tap [Delete] | Notes (pop) |
| Note Detail | Tap intent category | Intent Category Notes |
| Create Note | Save success | Note Detail |
| Create Note | Import file success | Note Detail |
| Search | Tap result | Note Detail |
| Ask AI | Tap citation [N] | Bottom Sheet → Note Detail |
| Categories | Tap category | Category Notes |
| Topics | Tap note | Note Detail |
| Intents | Tap intent category | Intent Category Notes |
| Intent Category Notes | Tap note | Note Detail |
| Settings | Tap Log Out | Login |
| Profile | Tap Log Out | Login |
| Any protected screen | 401 response | Login (session expired banner) |

---

## Empty States

| Screen | Empty condition | Message |
|--------|----------------|---------|
| Notes | No notes | "You haven't added any notes yet. Tap + to start." |
| Search | No results | "No notes found for this query." |
| Categories | No categories | "No categories yet. Notes are auto-organised by AI." |
| Topics | No topics | "Add more notes to see AI-generated topics." |
| Intents | No intent categories | "Notes are still being organised. Try adding more notes." |
| Ask AI | First use | "Ask a question about your notes." |

---

## Error States

| Scenario | UI |
|----------|----|
| Network offline | Full-screen error view "No internet connection" + retry button |
| Server error (500) | Snackbar "Something went wrong. Please try again." |
| Session expired (401) | Banner "Session expired" → navigate to Login |
| Rate limited (429) | Snackbar "Too many requests. Try again in a moment." |
| Note not found (404) | Pop back to Notes with snackbar "Note not found." |
