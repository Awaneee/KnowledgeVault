# KnowledgeVault Flutter — Implementation Plan

**Version:** 1.0.0  
**Backend:** KnowledgeVault v1.0.0 (frozen, stable API)  
**Date:** 2026-08-06

This plan breaks the Flutter application into five sequential phases. Each phase is a shippable increment. The backend API is treated as an immutable contract — no backend changes are proposed.

---

## Dependencies (pubspec.yaml)

```yaml
dependencies:
  flutter:
    sdk: flutter

  # Navigation
  go_router: ^14.0.0

  # State management
  flutter_riverpod: ^2.5.0
  riverpod_annotation: ^2.3.0

  # HTTP client
  dio: ^5.4.0

  # Secure token storage
  flutter_secure_storage: ^9.0.0

  # Local cache (offline support)
  drift: ^2.18.0
  sqlite3_flutter_libs: ^0.5.0

  # File picking
  file_picker: ^8.0.0

  # Shimmer loading skeletons
  shimmer: ^3.0.0

  # Date formatting
  intl: ^0.19.0

dev_dependencies:
  flutter_test:
    sdk: flutter
  build_runner: ^2.4.0
  riverpod_generator: ^2.3.0
  drift_dev: ^2.18.0
  mocktail: ^1.0.0
  flutter_lints: ^4.0.0
```

---

## Phase 1 — Foundation

**Goal:** Working app scaffold. No real API calls. Everything compiles and navigates.  
**Estimated effort:** 3–4 days  
**Prerequisite:** Flutter SDK, target device/simulator confirmed.

### Files to Create

```
lib/main.dart
lib/app.dart
lib/core/router/app_router.dart
lib/core/theme/app_theme.dart
lib/core/theme/app_colors.dart
lib/core/api/api_client.dart
lib/core/api/api_exceptions.dart
lib/core/api/auth_interceptor.dart
lib/core/auth/token_storage.dart
lib/core/auth/auth_state.dart
lib/core/cache/local_cache.dart          (drift database skeleton)
lib/core/error/error_handler.dart
lib/shared/widgets/loading_overlay.dart
lib/shared/widgets/error_view.dart
lib/shared/widgets/empty_state.dart
lib/shared/widgets/kv_app_bar.dart
lib/shared/extensions/datetime_ext.dart

# Screen stubs (no data, just layout scaffold)
lib/features/auth/ui/login_screen.dart
lib/features/auth/ui/register_screen.dart
lib/features/dashboard/ui/dashboard_screen.dart
lib/features/notes/ui/notes_screen.dart
lib/features/notes/ui/note_detail_screen.dart
lib/features/notes/ui/create_note_screen.dart
lib/features/search/ui/search_screen.dart
lib/features/ask/ui/ask_screen.dart
lib/features/categories/ui/categories_screen.dart
lib/features/topics/ui/topics_screen.dart
lib/features/intents/ui/intents_screen.dart
lib/features/settings/ui/settings_screen.dart
lib/features/profile/ui/profile_screen.dart
```

### Key Tasks

1. **App scaffold** — `MaterialApp.router` with GoRouter, Material 3 theme (light + dark), `ProviderScope` at root.
2. **Router** — All routes defined in `app_router.dart`. Auth guard redirect configured. Shell route with bottom nav bar for the 5 primary tabs.
3. **API client** — Dio instance with base URL, timeouts (connect: 10s, receive: 60s), `LogInterceptor` in debug mode. `AuthInterceptor` stub (reads token, adds header, handles 401).
4. **Token storage** — `flutter_secure_storage` wrapper. Read/write/delete methods.
5. **Theme** — Light and dark `ThemeData` from `ColorScheme.fromSeed`. `themeModeProvider` reading from `SharedPreferences`.
6. **Shared widgets** — `LoadingOverlay`, `ErrorView` (with retry callback), `EmptyState`, `KvAppBar`.
7. **Screen stubs** — Each screen compiles and shows its route path as placeholder text. No real data.
8. **Drift database** — Empty database class with no tables yet. Confirms SQLite links on both platforms.

### Completion Criteria

- [ ] App launches on iOS and Android without crash.
- [ ] All 13 routes navigate correctly.
- [ ] Bottom nav persists state across tab switches.
- [ ] Auth guard redirects unauthenticated users to `/login`.
- [ ] Light/dark theme toggle works.
- [ ] No compile errors or lint warnings.

---

## Phase 2 — Authentication

**Goal:** Real login, register, logout. Token stored securely. Auth guard enforced.  
**Estimated effort:** 2–3 days  
**Prerequisite:** Phase 1 complete. Backend reachable at `AppConfig.baseUrl`.

### Files to Create

```
lib/features/auth/data/models/login_request.dart
lib/features/auth/data/models/register_request.dart
lib/features/auth/data/models/token_response.dart
lib/features/auth/data/models/user_response.dart
lib/features/auth/data/auth_repository.dart
lib/features/auth/providers/auth_provider.dart
```

### Files to Update

```
lib/features/auth/ui/login_screen.dart      (wire to real AuthRepository)
lib/features/auth/ui/register_screen.dart   (wire to real AuthRepository)
lib/features/profile/ui/profile_screen.dart (show UserResponse)
lib/features/settings/ui/settings_screen.dart (logout action)
lib/core/router/app_router.dart             (token validation on startup)
```

### Key Tasks

1. **Dart models** — `LoginRequest`, `RegisterRequest`, `TokenResponse`, `UserResponse`. All fields matched to JSON keys from backend. Use `fromJson` factory constructors.
2. **AuthRepository** — `login()`, `register()`, `getMe()`. Each method calls Dio, parses response, throws typed `ApiException` on error status codes.
3. **`authProvider`** — `AsyncNotifier<UserResponse?>`. On init, reads token → calls `GET /auth/me`. Exposes `login()`, `logout()`, `register()` actions.
4. **`currentUserProvider`** — Derived from `authProvider.value`. Used throughout the app to access user ID.
5. **Splash screen** — Watches `authProvider` state to determine initial route. Handles timeout.
6. **Login screen** — Form validation → `authProvider.login()` → store token → navigate.
7. **Register screen** — Form validation (password ≥ 8 chars client-side) → `authProvider.register()` → navigate to login.
8. **Auth interceptor** — Fully wired. On 401 response: call `authProvider.logout()`, navigate to `/login` using `GoRouter` from context or a global navigator key.
9. **Logout** — Clear token from storage, set `authProvider` to null, GoRouter redirects to `/login`.

### Dependencies

- `flutter_secure_storage` configured for Android (backup rules) and iOS (keychain sharing disabled).
- Backend base URL configured via a `AppConfig` class (hardcode for now; build flavors in Phase 5).

### Completion Criteria

- [ ] User can register a new account.
- [ ] User can log in with email + password.
- [ ] JWT token stored in secure storage.
- [ ] App restores session on restart (token → `/auth/me` → dashboard).
- [ ] Expired/invalid token → redirect to login with "Session expired" banner.
- [ ] Logout clears token and redirects to login.
- [ ] Rate limit (429) shows user-friendly snackbar.
- [ ] Form validation errors shown inline.

---

## Phase 3 — Notes (Core CRUD)

**Goal:** Users can create, read, delete notes. Categories shown. File upload works.  
**Estimated effort:** 5–6 days  
**Prerequisite:** Phase 2 complete (auth token available for all API calls).

### Files to Create

```
# Notes
lib/features/notes/data/models/note_create_request.dart
lib/features/notes/data/models/note_response.dart
lib/features/notes/data/models/note_create_response.dart
lib/features/notes/data/models/note_search_response.dart
lib/features/notes/data/notes_repository.dart
lib/features/notes/providers/notes_provider.dart
lib/features/notes/providers/note_detail_provider.dart
lib/features/notes/ui/widgets/note_card.dart
lib/features/notes/ui/widgets/note_search_bar.dart

# Categories
lib/features/categories/data/models/category_create_request.dart
lib/features/categories/data/models/category_response.dart
lib/features/categories/data/categories_repository.dart
lib/features/categories/providers/categories_provider.dart
lib/features/categories/ui/widgets/category_chip.dart

# Attachments
lib/features/attachments/data/models/attachment_response.dart
lib/features/attachments/data/attachments_repository.dart
lib/features/attachments/providers/attachments_provider.dart
lib/features/attachments/ui/widgets/attachment_list.dart
lib/features/attachments/ui/widgets/upload_button.dart

# Topics
lib/features/topics/data/models/topic_response.dart
lib/features/topics/data/topics_repository.dart
lib/features/topics/providers/topics_provider.dart

# Intents
lib/features/intents/data/models/intent_category_response.dart
lib/features/intents/data/models/intent_note_response.dart
lib/features/intents/data/models/note_intent_response.dart
lib/features/intents/data/intents_repository.dart
lib/features/intents/providers/intents_provider.dart
lib/features/intents/ui/widgets/intent_category_tile.dart

# Drift tables
lib/core/cache/tables/notes_table.dart
lib/core/cache/tables/categories_table.dart
```

### Files to Update

```
lib/features/notes/ui/notes_screen.dart         (real data + skeleton + pull-to-refresh)
lib/features/notes/ui/note_detail_screen.dart   (full detail, intent, related, attachments)
lib/features/notes/ui/create_note_screen.dart   (form + file picker)
lib/features/categories/ui/categories_screen.dart
lib/features/topics/ui/topics_screen.dart
lib/features/intents/ui/intents_screen.dart
lib/features/dashboard/ui/dashboard_screen.dart (recent notes + topics widget)
lib/core/cache/local_cache.dart                 (add drift tables)
```

### Key Tasks

1. **`notesProvider`** — `AsyncNotifierProvider<NotesNotifier, List<NoteResponse>>`. Loads from cache first, fetches in background. Exposes `createNote()`, `deleteNote()`, `refresh()`.
2. **Optimistic delete** — Remove note from state immediately. On API failure, re-insert and show error snackbar.
3. **Note creation** — `CreateNoteScreen` submits content → `POST /notes/` → navigate to detail. File import uses `POST /uploads/file`.
4. **Note detail** — `noteDetailProvider(id)` fires `GET /notes/:id`. Related notes, intent, and attachments loaded lazily in parallel with `Future.wait`.
5. **Categories** — `categoriesProvider` loads `GET /categories/`. Filter chips on `NotesScreen` filter `notesProvider` client-side by `categoryId`.
6. **Note card** — Shows title, first 100 chars of content, `created_at` (formatted "2 hours ago"), category chip if present.
7. **Intent panel** — In `NoteDetailScreen`, watch `intentProvider(noteId)`. `AsyncValue.when` — hide on error/null, show collapsible card on data.
8. **Attachments** — Upload via `POST /attachments/?note_id=:id`. Show progress with `Dio.onSendProgress`. List existing attachments from `GET /notes/:id/attachments`.
9. **Topics screen** — `topicsProvider` loads `GET /topics/`. Renders `ExpansionTile` list.
10. **Intents screen** — `intentsProvider` loads `GET /intents/categories`. Icon mapped from `intentType`.
11. **Drift cache** — Write notes and categories to SQLite on fetch. Read from SQLite on startup for instant display.
12. **Shimmer loading** — `NoteCard` skeleton on first load. 3-item skeleton on topic/intent lists.

### Completion Criteria

- [ ] `GET /notes/` loads and displays all notes.
- [ ] Pull-to-refresh works on notes list.
- [ ] Note detail shows content, intent, related notes, attachments.
- [ ] Create note via text input works.
- [ ] Create note via PDF/TXT/DOCX file import works.
- [ ] Delete note (optimistic) works with undo snackbar.
- [ ] Category filter chips work (client-side filter).
- [ ] Create new category works.
- [ ] Topics screen shows AI clusters.
- [ ] Intents screen shows intent categories.
- [ ] Offline: notes show from cache when offline.
- [ ] Attachment upload with progress bar works.

---

## Phase 4 — AI Search and Ask

**Goal:** Semantic search, chunk retrieval, AI Ask with streaming, citations.  
**Estimated effort:** 4–5 days  
**Prerequisite:** Phase 3 complete.

### Files to Create

```
# Search
lib/features/search/data/models/chunk_result.dart
lib/features/search/data/search_repository.dart
lib/features/search/providers/search_provider.dart
lib/features/search/ui/widgets/search_result_tile.dart

# Ask
lib/features/ask/data/models/ask_request.dart
lib/features/ask/data/models/ask_response.dart
lib/features/ask/data/models/citation.dart
lib/features/ask/data/models/chunk_preview.dart
lib/features/ask/data/ask_repository.dart
lib/features/ask/providers/ask_provider.dart
lib/features/ask/ui/widgets/answer_bubble.dart
lib/features/ask/ui/widgets/citation_card.dart
lib/features/ask/ui/widgets/stream_answer_view.dart
```

### Files to Update

```
lib/features/search/ui/search_screen.dart   (real search, 3 tabs, debounce)
lib/features/ask/ui/ask_screen.dart         (streaming + full response modes)
```

### Key Tasks

1. **Search debounce** — 400ms debounce using `ref.debounce` or a manual `Timer`. Cancel previous Dio request on each new query via `CancelToken`.
2. **Search tabs** — `DefaultTabController` with 3 tabs: Smart (`GET /notes/search`), Semantic (`POST /retrieve`), Chunks (`POST /retrieve/hybrid`). Each tab has its own `AsyncNotifierProvider` keyed by query string.
3. **`askProvider`** — `AsyncNotifier<AskResponse?>`. Exposes `ask(question)` (calls `POST /ask/`) and `streamAsk(question)` (calls `POST /ask/stream`).
4. **SSE streaming** — `AskRepository.streamAsk()` returns `Stream<String>`. Use Dio `ResponseType.stream` + `utf8.decoder` + `LineSplitter`. Filter lines starting with `data:`. Emit token strings.
5. **`StreamProvider`** — `streamAnswerProvider(question)` wraps `askRepository.streamAsk()`. `StreamAnswerView` widget watches this and appends tokens to a `StringBuffer`.
6. **Citation rendering** — `RegExp(r'\[(\d+)\]')` on answer text. Split into `TextSpan` list. Citation refs render as tappable `WidgetSpan` chips. Tap → `showModalBottomSheet` with `Citation.snippet` and "Go to note →" `ElevatedButton`.
7. **Degraded mode** — Watch `askResponse.retrievalOnly`. If `true`, show `ChunkPreview` cards instead of answer text.
8. **Mode toggle** — `NotifierProvider<AskModeNotifier, AskMode>` where `AskMode` is `streaming | full`. Persisted to `SharedPreferences`.
9. **Input constraints** — Enforce `maxLength: 2000` on the question `TextField` (matches backend `Field(max_length=2000)`).
10. **Ask loading state** — Disable send button during request. Streaming: show typing dots until first token arrives. Full: show thinking animation.

### Completion Criteria

- [ ] Note-level semantic search (`GET /notes/search`) returns and displays results.
- [ ] Chunk-level semantic retrieval (`POST /retrieve`) tab works.
- [ ] Hybrid retrieval (`POST /retrieve/hybrid`) tab works.
- [ ] Search debounces correctly (no redundant API calls).
- [ ] AI Ask (full response) returns answer with citations.
- [ ] AI Ask (streaming) renders tokens progressively.
- [ ] Citation `[N]` references are tappable and navigate to source note.
- [ ] Degraded mode (no LLM) shows chunk list with banner.
- [ ] Question field enforces 2000 char limit.
- [ ] Streaming mode toggle persists across sessions.

---

## Phase 5 — Polish

**Goal:** Production-ready app. Performance, accessibility, error states, theming, responsive layout, build configuration.  
**Estimated effort:** 4–5 days  
**Prerequisite:** Phases 1–4 complete.

### Files to Create

```
lib/core/config/app_config.dart            # Build-flavor URL + env config
lib/core/config/app_flavor.dart            # dev | staging | prod enum
lib/features/settings/ui/settings_screen.dart (fully wired: theme, backfill, health)

# Build configurations
android/app/src/dev/                       # dev flavor assets
android/app/src/prod/                      # prod flavor assets
ios/Flutter/dev.xcconfig
ios/Flutter/prod.xcconfig
```

### Key Tasks

#### Error States and Resilience
1. **Offline banner** — `ConnectivityPlus` package. Show persistent `MaterialBanner` when offline. Auto-dismiss when reconnected.
2. **Global error handler** — `ProviderObserver` that catches unhandled `AsyncError` states. Log to console in debug; surface snackbar in release.
3. **Empty states** — All screens have illustrated empty state with actionable CTA (e.g., "Add your first note").
4. **Retry everywhere** — Every `ErrorView` has a retry button that calls `ref.invalidate(provider)`.
5. **Session expiry** — `AuthInterceptor` navigates to `/login` using a `GlobalKey<NavigatorState>` or GoRouter's `refresh` listenable. Show `MaterialBanner` "Session expired. Please log in again."

#### Performance
6. **`ListView.builder`** — All note lists use `ListView.builder` (lazy). Never `Column` with dynamic children.
7. **Image caching** — Attachments with image types (`.png`, `.jpg`, `.jpeg`) displayed with `Image.network` + `cacheWidth`/`cacheHeight`.
8. **Provider auto-dispose** — Use `@riverpod` with `keepAlive: false` on detail providers (note detail, intent detail) so they are freed when screen is popped.
9. **Debounce and cancel** — Confirm all search paths debounce + cancel. No memory leaks from dangling `StreamSubscription`.

#### Accessibility
10. **Semantic labels** — All icon buttons have `Semantics(label: ...)` or `Tooltip`.
11. **Minimum tap target** — 48×48 dp for all interactive elements.
12. **Contrast ratio** — Verify all text against background meets WCAG AA (4.5:1) in both themes.
13. **Dynamic text size** — All `Text` widgets use `overflow: TextOverflow.ellipsis` where appropriate. No hard-coded font sizes without `TextScaler` consideration.

#### Responsive Layout
14. **Navigation rail** — On screens ≥600dp, replace `NavigationBar` with `NavigationRail` using a `LayoutBuilder`.
15. **Two-panel notes** — On tablet landscape (≥840dp), `NotesScreen` shows note list + note detail side by side.
16. **Bottom sheet → dialog** — On tablets, replace `showModalBottomSheet` with `showDialog` for better ergonomics.

#### Settings Screen
17. **Theme toggle** — `SegmentedButton` for system/light/dark. `themeModeProvider` updates `MaterialApp` theme in real time.
18. **Backfill action** — "Organise my notes" → loading modal → `POST /intents/backfill?limit=50` → result summary ("12 organised, 0 failed, 5 remaining").
19. **Server status** — `GET /health` on screen open. Green dot / amber dot / red dot.

#### Build Configuration
20. **Build flavors** — `dev` (local backend), `staging`, `prod`. `AppConfig.baseUrl` set per flavor. Use `--dart-define` flags.
21. **App icon** — `flutter_launcher_icons` configured for all platforms.
22. **Splash screen** — `flutter_native_splash` for native platform splash before Flutter renders.
23. **ProGuard rules** — Android release build: ensure `flutter_secure_storage` and `drift` classes are not obfuscated.

#### Testing
24. **Widget tests** — `LoginScreen`, `NoteCard`, `AnswerBubble` (citation rendering), `StreamAnswerView`.
25. **Repository tests** — Mock Dio with `mocktail`. Test `AuthRepository`, `NotesRepository`, `AskRepository` for success and error paths.
26. **Provider tests** — `ProviderContainer` tests for `notesProvider` optimistic delete.
27. **Integration test** — Happy path: register → login → create note → search → ask question.

### Completion Criteria

- [ ] App works offline (shows cached notes, graceful error on actions requiring network).
- [ ] All empty states display with actionable CTAs.
- [ ] All error states have retry buttons.
- [ ] Session expiry handled gracefully without crash.
- [ ] Responsive layout correct on 360dp phone and 768dp tablet.
- [ ] All routes accessible via keyboard (desktop/tablet).
- [ ] Build flavors configured: `dev`, `prod`.
- [ ] Release build (APK + IPA) compiles without errors.
- [ ] Core widget and repository tests pass.
- [ ] App icon and splash screen display correctly on both platforms.

---

## Phase Summary

| Phase | Focus | Effort | Shippable? |
|-------|-------|--------|-----------|
| 1 — Foundation | Scaffold, routing, theming | 3–4 days | No (stubs only) |
| 2 — Authentication | Login, register, token, session | 2–3 days | No (no content) |
| 3 — Notes | CRUD, categories, topics, intents, attachments | 5–6 days | Yes (core app) |
| 4 — AI Search & Ask | Semantic search, streaming AI chat, citations | 4–5 days | Yes (full feature) |
| 5 — Polish | Error states, a11y, responsive, testing, build | 4–5 days | Yes (production-ready) |
| **Total** | | **18–23 days** | |

---

## Backend Constraints to Keep in Mind

These are not bugs to fix — they are facts the Flutter code must accommodate:

| Constraint | Flutter implication |
|-----------|---------------------|
| No refresh token (30-min expiry) | `AuthInterceptor` must handle 401 gracefully and re-prompt login. Consider warning user at 25-min mark with a countdown. |
| No logout endpoint | Client-side token deletion only. No server-side session invalidation. |
| No note update (PUT/PATCH) | Do not show an "Edit" button. Notes are read-only after creation. |
| No pagination on `GET /notes/` | Use `ListView.builder` always. Consider client-side virtual scrolling for 500+ notes. |
| No delete for individual attachments (SEC-3, post-freeze) | Don't show a delete button for attachments. |
| `POST /ask/` cached 1 hour by backend | Identical questions return instantly — this is a feature, not a bug. |
| Bulk note create: partial success | Compare response length to request length; show partial-success warning. |
| Backfill is synchronous, capped at 50 | Show loading modal, warn user it may take up to 60 seconds. |
| No search pagination | All search results returned at once — render with `ListView.builder`. |
| `POST /ask/stream` has no citations | Show "View full answer with citations" chip to fire `POST /ask/` after streaming. |
