# KnowledgeVault Flutter — API Mapping

**Backend version:** v1.0.0 (frozen)  
**Base URL:** configured via build flavor / `AppConfig.baseUrl`  
**All protected endpoints require:** `Authorization: Bearer <access_token>`

---

## Authentication

### POST /auth/register

| Field | Value |
|-------|-------|
| **Endpoint** | `POST /auth/register` |
| **Auth required** | No |
| **Rate limit** | 5 req/min (backend enforced) |

**Request model — `RegisterRequest`**
```dart
class RegisterRequest {
  final String username;   // required
  final String email;      // required, valid email format
  final String password;   // required, min 8 chars, max 128 chars
}
```

**Response model — `UserResponse`**
```dart
class UserResponse {
  final int id;
  final String username;
  final String email;
}
```

**Error responses**
| Status | Body | UI message |
|--------|------|-----------|
| 400 | `{"detail": "Email already registered"}` | "This email is already in use" |
| 400 | `{"detail": "Username already taken"}` | "This username is taken" |
| 422 | Pydantic validation errors | Field-level validation hints |
| 429 | Rate limit exceeded | "Too many attempts. Try again in a minute." |

**Flutter service class:** `AuthRepository`  
**UI screen:** `RegisterScreen`  
**Loading behaviour:** Disable submit button + show `CircularProgressIndicator` inside button while awaiting.  
**On success:** Navigate to `/login` with a `SnackBar` "Account created — please log in."

---

### POST /auth/login

| Field | Value |
|-------|-------|
| **Endpoint** | `POST /auth/login` |
| **Auth required** | No |
| **Rate limit** | 10 req/min (backend enforced) |

**Request model — `LoginRequest`**
```dart
class LoginRequest {
  final String email;
  final String password;
}
```

**Response model — `TokenResponse`**
```dart
class TokenResponse {
  final String accessToken;   // JWT, 30-minute lifetime
  final String tokenType;     // "bearer"
}
```

**Error responses**
| Status | Body | UI message |
|--------|------|-----------|
| 401 | `{"detail": "Invalid email or password"}` | "Incorrect email or password" |
| 429 | Rate limit exceeded | "Too many attempts. Try again in a minute." |

**Flutter service class:** `AuthRepository`  
**UI screen:** `LoginScreen`  
**Loading behaviour:** Disable form + button while awaiting.  
**On success:** Persist `accessToken` to `flutter_secure_storage`. Navigate to `/dashboard`.  
**Optimistic update:** N/A — login must succeed before proceeding.

---

### GET /auth/me

| Field | Value |
|-------|-------|
| **Endpoint** | `GET /auth/me` |
| **Auth required** | Yes |

**Request model:** None (token in header)

**Response model — `UserResponse`**
```dart
class UserResponse {
  final int id;
  final String username;
  final String email;
}
```

**Flutter service class:** `AuthRepository`  
**UI screen:** `ProfileScreen`, app startup token validation  
**Loading behaviour:** Splash screen spinner while verifying token on startup.  
**Use:** Called once at startup to validate a stored token and hydrate the current user. Also used to display profile info.

---

## Notes

### POST /notes/

| Field | Value |
|-------|-------|
| **Endpoint** | `POST /notes/` |
| **Auth required** | Yes |

**Request model — `NoteCreateRequest`**
```dart
class NoteCreateRequest {
  final String content;   // min 1, max 50,000 chars
}
```

**Response model — `NoteCreateResponse`**
```dart
class NoteCreateResponse {
  final int id;
  final String title;           // auto-generated from first ~120 chars
  final String? content;
  final int userId;
  final int? categoryId;
  final String? autoTitleSource;
  final String? organizationStatus;
  final DateTime createdAt;
  final NoteIntentResponse? intent;
  final IntentCategoryResponse? intentCategory;
}
```

**Flutter service class:** `NotesRepository`  
**UI screen:** `CreateNoteScreen`  
**Loading behaviour:** Show inline spinner; keep form editable (do not lock).  
**Optimistic update:** Prepend a placeholder note card immediately; replace with real note on response.  
**On success:** Navigate to `NoteDetailScreen` for the new note. Invalidate `notesProvider` to refresh list.

---

### POST /notes/bulk

| Field | Value |
|-------|-------|
| **Endpoint** | `POST /notes/bulk` |
| **Auth required** | Yes |

**Request model — `BulkNoteCreateRequest`**
```dart
class BulkNoteCreateRequest {
  final List<String> notes;
}
```

**Response model:** `List<NoteCreateResponse>`

**Notes:**  
The backend silently skips failed notes and returns a partial list. The client should compare `response.length` with `request.notes.length` and surface a warning if they differ: "X of Y notes were created."

**Flutter service class:** `NotesRepository`  
**UI screen:** File import flow (from `UploadScreen` after multi-file selection; not a direct user form)  
**Loading behaviour:** Progress indicator with "Creating notes…" label.

---

### GET /notes/

| Field | Value |
|-------|-------|
| **Endpoint** | `GET /notes/` |
| **Auth required** | Yes |

**Request model:** None

**Response model:** `List<NoteResponse>`
```dart
class NoteResponse {
  final int id;
  final String title;
  final String? content;
  final int userId;
  final int? categoryId;
  final String? autoTitleSource;
  final String? organizationStatus;
  final DateTime createdAt;
}
```

**Flutter service class:** `NotesRepository`  
**UI screen:** `NotesScreen`  
**Loading behaviour:** Skeleton list of 6 note cards on first load. Pull-to-refresh shows `RefreshIndicator`.  
**Caching:** Stale-while-revalidate from local SQLite. Show cached immediately, refresh in background.  
**Warning:** Backend returns ALL notes with no pagination. For users with many notes, the response can be large. Render with `ListView.builder` — never `Column`.

---

### GET /notes/search

| Field | Value |
|-------|-------|
| **Endpoint** | `GET /notes/search?q=<query>` |
| **Auth required** | Yes |

**Query param:** `q: String` (required)

**Response model:** `List<NoteSearchResponse>`
```dart
class NoteSearchResponse {
  final int id;
  final String title;
  final String? content;
}
```

**Flutter service class:** `SearchRepository`  
**UI screen:** `SearchScreen`  
**Loading behaviour:** Show spinner below search bar while waiting. Cancel previous request if user types again before response (debounce 400ms + Dio cancel token).  
**Caching:** No cache — always live.  
**Note:** This endpoint uses **note-level semantic search** (not chunk-level). Results are note titles + first portion of content — not exact passage matches.

---

### GET /notes/{note_id}

| Field | Value |
|-------|-------|
| **Endpoint** | `GET /notes/{note_id}` |
| **Auth required** | Yes |

**Response model:** `NoteResponse`

**Error responses**
| Status | Detail |
|--------|--------|
| 404 | "Note not found" |
| 403 | "Access forbidden" |

**Flutter service class:** `NotesRepository`  
**UI screen:** `NoteDetailScreen`  
**Loading behaviour:** Skeleton of note title + content area.  
**Caching:** Serve from cache instantly; refresh in background.

---

### GET /notes/{note_id}/related

| Field | Value |
|-------|-------|
| **Endpoint** | `GET /notes/{note_id}/related` |
| **Auth required** | Yes |

**Response model:** `List<NoteSearchResponse>`

**Flutter service class:** `NotesRepository`  
**UI screen:** `NoteDetailScreen` — "Related notes" section at the bottom  
**Loading behaviour:** Lazy-load this section after the main note content has rendered. Show 3-skeleton placeholder.  
**Note:** Backend returns `[]` silently if note is not owned. Empty list → hide the section.

---

### DELETE /notes/{note_id}

| Field | Value |
|-------|-------|
| **Endpoint** | `DELETE /notes/{note_id}` |
| **Auth required** | Yes |

**Response:** HTTP 204 No Content

**Flutter service class:** `NotesRepository`  
**UI screen:** `NoteDetailScreen` (swipe-to-delete or action menu)  
**Loading behaviour:** Show confirmation dialog. On confirm, optimistically remove from list and show `SnackBar` with "Undo" action. If API returns error, re-insert the note and show error snackbar.  
**Optimistic update:** Yes — remove from local cache immediately; roll back on failure.

---

### GET /notes/{note_id}/attachments

| Field | Value |
|-------|-------|
| **Endpoint** | `GET /notes/{note_id}/attachments` |
| **Auth required** | Yes |

**Response model:** `List<AttachmentResponse>`

**Flutter service class:** `AttachmentsRepository`  
**UI screen:** `NoteDetailScreen` — attachments section  
**Loading behaviour:** Inline spinner in the attachments section.

---

## Categories

### POST /categories/

| Field | Value |
|-------|-------|
| **Endpoint** | `POST /categories/` |
| **Auth required** | Yes |

**Request model — `CategoryCreateRequest`**
```dart
class CategoryCreateRequest {
  final String name;
}
```

**Response model — `CategoryResponse`**
```dart
class CategoryResponse {
  final int id;
  final String name;
}
```

**Flutter service class:** `CategoriesRepository`  
**UI screen:** `CategoriesScreen` — inline form or bottom sheet  
**Loading behaviour:** Spinner on submit button.  
**Optimistic update:** Add placeholder chip immediately; replace on response.

---

### GET /categories/

| Field | Value |
|-------|-------|
| **Endpoint** | `GET /categories/` |
| **Auth required** | Yes |

**Response model:** `List<CategoryResponse>`

**Flutter service class:** `CategoriesRepository`  
**UI screen:** `CategoriesScreen`, `NotesScreen` filter bar  
**Loading behaviour:** Skeleton chips row.  
**Caching:** 10-minute stale-while-revalidate.

---

### GET /categories/{category_id}

| Field | Value |
|-------|-------|
| **Endpoint** | `GET /categories/{category_id}` |
| **Auth required** | Yes |

**Response model:** `CategoryResponse`

**Flutter service class:** `CategoriesRepository`  
**UI screen:** `CategoryNotesScreen` (notes filtered by category — client-side filter from notes list)

---

## Attachments

### POST /attachments/

| Field | Value |
|-------|-------|
| **Endpoint** | `POST /attachments/?note_id={id}` |
| **Auth required** | Yes |
| **Content-Type** | `multipart/form-data` |

**Request:** Multipart file upload. `note_id` passed as query parameter.  
**Allowed types:** `.pdf`, `.txt`, `.docx`, `.png`, `.jpg`, `.jpeg`  
**Max size:** 10 MB (backend enforces; 413 on exceed)

**Response model — `AttachmentResponse`**
```dart
class AttachmentResponse {
  final int id;
  final String filename;
  final String filePath;
  final String fileType;
  final int noteId;
  final DateTime createdAt;
}
```

**Error responses**
| Status | Detail |
|--------|--------|
| 400 | Unsupported file type |
| 413 | File too large |
| 404 | Note not found |
| 403 | Access forbidden |

**Flutter service class:** `AttachmentsRepository`  
**UI screen:** `NoteDetailScreen` — attachment upload widget  
**Loading behaviour:** Linear progress bar during upload (`Dio.onSendProgress`).  
**Dart model names:** `AttachmentResponse`

---

### GET /attachments/

| Field | Value |
|-------|-------|
| **Endpoint** | `GET /attachments/` |
| **Auth required** | Yes |

**Response model:** `List<AttachmentResponse>`

**Flutter service class:** `AttachmentsRepository`  
**UI screen:** Not a standalone screen — used internally to populate attachment lists.

---

### GET /attachments/{attachment_id}

| Field | Value |
|-------|-------|
| **Endpoint** | `GET /attachments/{attachment_id}` |
| **Auth required** | Yes |

**Response model:** `AttachmentResponse`

**Flutter service class:** `AttachmentsRepository`  
**UI screen:** Attachment detail / viewer (tap on attachment in `NoteDetailScreen`)

---

## File Upload

### POST /uploads/file

| Field | Value |
|-------|-------|
| **Endpoint** | `POST /uploads/file` |
| **Auth required** | Yes |
| **Content-Type** | `multipart/form-data` |

**Request:** Single file upload. Accepted: `.pdf`, `.txt`, `.docx`  
**Behavior:** Backend extracts text content, creates a note automatically.

**Response model — `PDFUploadResponse`**
```dart
class PDFUploadResponse {
  final String message;   // "File processed successfully"
  final int noteId;       // ID of the created note
}
```

**Error responses**
| Status | Detail |
|--------|--------|
| 400 | "Unsupported file type" |
| 400 | "Could not read file — it may be corrupted or not a valid file of its declared type" |

**Flutter service class:** `NotesRepository` (delegates upload to Dio multipart)  
**UI screen:** `CreateNoteScreen` — "Import from file" action  
**Loading behaviour:** Upload progress bar + "Extracting text…" label.  
**On success:** Navigate to `NoteDetailScreen` for `noteId`. Invalidate notes list.

---

## Retrieval (Direct — Power Feature)

### POST /retrieve

| Field | Value |
|-------|-------|
| **Endpoint** | `POST /retrieve` |
| **Auth required** | Yes |

**Request model — `RetrieveRequest`**
```dart
class RetrieveRequest {
  final String query;   // min 1, max 2000 chars
}
```

**Response model:** `List<ChunkResult>`
```dart
class ChunkResult {
  final String chunkText;
  final String noteTitle;
  final String? source;
  final String? intentCategory;
}
```

**Flutter service class:** `SearchRepository`  
**UI screen:** `SearchScreen` — "Deep search" tab (semantic chunk results)  
**Loading behaviour:** Spinner; results replace on each new query.

---

### POST /retrieve/hybrid

| Field | Value |
|-------|-------|
| **Endpoint** | `POST /retrieve/hybrid` |
| **Auth required** | Yes |

**Request/Response:** Same as `POST /retrieve`

**Flutter service class:** `SearchRepository`  
**UI screen:** `SearchScreen` — "Smart search" tab (default tab; intent-aware)  
**Note:** This is the better retrieval path. `/retrieve` (pure semantic) is available as a secondary tab for power users.

---

## AI Ask

### POST /ask/

| Field | Value |
|-------|-------|
| **Endpoint** | `POST /ask/` |
| **Auth required** | Yes |

**Request model — `AskRequest`**
```dart
class AskRequest {
  final String question;   // min 1, max 2000 chars
}
```

**Response model — `AskResponse`**
```dart
class AskResponse {
  final String question;
  final String answer;
  final List<String> sources;          // legacy — note titles
  final List<Citation> citations;      // inline [N] references
  final bool retrievalOnly;            // true if LLM failed — show degraded UI
  final String status;                 // "ok" or "degraded"
  final String? provider;              // "gemini" or "groq"
  final bool reranked;
  final List<ChunkPreview> chunks;     // populated only when retrievalOnly=true
}

class Citation {
  final int ref;            // [N] number in answer text
  final int noteId;         // for navigation to the source note
  final String noteTitle;
  final int? chunkId;
  final String snippet;     // 200-char preview for hover/tap
}

class ChunkPreview {
  final String title;
  final String preview;
  final double score;
  final String? category;
}
```

**Flutter service class:** `AskRepository`  
**UI screen:** `AskScreen`  
**Loading behaviour:** Animated "thinking" indicator (pulsing dots). Disable question input while awaiting.  
**Degraded mode:** When `retrievalOnly: true` or `status: "degraded"`, show a notice "AI answer unavailable — showing relevant notes instead" and render `chunks` as a card list.  
**Citations:** Parse `[N]` in `answer` text using a regex. Render each as a tappable `InlineSpan` that opens a `BottomSheet` with `Citation.snippet` and a "Go to note →" action.  
**Caching note:** The backend caches Ask responses in Redis for 1 hour keyed by `(user_id, question)`. Identical questions within an hour return instantly.

---

### POST /ask/stream

| Field | Value |
|-------|-------|
| **Endpoint** | `POST /ask/stream` |
| **Auth required** | Yes |
| **Response type** | `text/event-stream` (SSE) |

**Request model:** `AskRequest` (same as above)

**Stream format:** Plain text tokens, one per SSE line. No structured JSON — no citations included.

**Flutter service class:** `AskRepository`  
**Dart model:** `Stream<String>` — each event is a token chunk  
**UI screen:** `AskScreen` — streaming mode (default)  
**Loading behaviour:** Tokens appear progressively in the answer bubble as they stream.  
**When to use vs POST /ask/:** Use streaming as the default for immediate feedback. If the user taps a citation source, fire `POST /ask/` in the background to get citations for that question (or cache the last non-streaming response).  
**Implementation note:** Use `dio` with `ResponseType.stream`. Parse `data:` prefix from SSE lines. Accumulate tokens in a `StringBuffer` and emit via a `StreamController<String>`.

---

## Topics

### GET /topics/

| Field | Value |
|-------|-------|
| **Endpoint** | `GET /topics/` |
| **Auth required** | Yes |

**Response model:** `List<TopicResponse>`
```dart
class TopicResponse {
  final int clusterId;
  final String topicName;
  final List<TopicNoteItem> notes;
}

class TopicNoteItem {
  final int id;
  final String title;
}
```

**Flutter service class:** `TopicsRepository`  
**UI screen:** `TopicsScreen` (accessible from dashboard or nav drawer)  
**Loading behaviour:** Skeleton list of expandable topic groups.  
**Caching:** 15-minute stale-while-revalidate (topic generation is compute-heavy).

---

## Intents

### GET /intents/categories

| Field | Value |
|-------|-------|
| **Endpoint** | `GET /intents/categories` |
| **Auth required** | Yes |

**Response model:** `List<IntentCategoryResponse>`
```dart
class IntentCategoryResponse {
  final int id;
  final String name;
  final String? description;
  final String intentType;   // "communication" | "todo" | "study" | "reminder" | "idea" | "reference" | "question" | "event" | "general"
  final String? actor;
  final String? action;
  final String? timeScope;
  final double confidence;
  final int noteCount;
  final DateTime? lastUsedAt;
}
```

**Flutter service class:** `IntentsRepository`  
**UI screen:** `IntentsScreen`  
**Loading behaviour:** Skeleton list of intent category tiles.  
**Caching:** 10-minute stale-while-revalidate.

---

### GET /intents/categories/{intent_category_id}/notes

| Field | Value |
|-------|-------|
| **Endpoint** | `GET /intents/categories/{id}/notes` |
| **Auth required** | Yes |

**Response model:** `List<IntentNoteResponse>`
```dart
class IntentNoteResponse {
  final int id;
  final String title;
  final String? content;
  final DateTime createdAt;
}
```

**Flutter service class:** `IntentsRepository`  
**UI screen:** `IntentCategoryNotesScreen`  
**Loading behaviour:** Skeleton note list.

---

### GET /intents/notes/{note_id}

| Field | Value |
|-------|-------|
| **Endpoint** | `GET /intents/notes/{note_id}` |
| **Auth required** | Yes |

**Response model:** `NoteIntentResponse`
```dart
class NoteIntentResponse {
  final int id;
  final int noteId;
  final String intentType;
  final String? action;
  final String? actor;
  final String? topic;
  final String? subtopic;
  final String? object;
  final DateTime? dueDate;
  final String? temporalText;
  final String? urgency;
  final double confidence;
  final String modelName;
}
```

**Flutter service class:** `IntentsRepository`  
**UI screen:** `NoteDetailScreen` — intent metadata panel (collapsible)  
**Error:** 404 → hide the intent panel silently (not all notes have intents).

---

### POST /intents/backfill

| Field | Value |
|-------|-------|
| **Endpoint** | `POST /intents/backfill?limit={n}` |
| **Auth required** | Yes |

**Query param:** `limit: int` (default 100; backend clamps to 1–50)

**Response model — `IntentBackfillResponse`**
```dart
class IntentBackfillResponse {
  final int processed;
  final int failed;
  final int remainingHint;
}
```

**Flutter service class:** `IntentsRepository`  
**UI screen:** `SettingsScreen` — "Organise notes" action (admin-level, not surfaced prominently)  
**Loading behaviour:** Full-screen modal with "Organising your notes… this may take a moment."  
**Warning:** Each call runs up to 50 synchronous LLM round-trips on the server. Do not call this repeatedly.

---

## Health

### GET /health

| Field | Value |
|-------|-------|
| **Endpoint** | `GET /health` |
| **Auth required** | No |

**Response:**
```dart
class HealthResponse {
  final String status;   // "ok" | "degraded"
  final String db;       // "ok" | "error"
  final String redis;    // "ok" | "error"
}
```

**Flutter service class:** `ApiClient` utility — not a full repository  
**UI screen:** `SettingsScreen` — "Connection status" indicator  
**Use:** Check on app foreground to surface a degraded-service banner.
