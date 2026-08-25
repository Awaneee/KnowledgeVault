# KnowledgeVault Flutter — Frontend Architecture

**Version:** 1.0.0  
**Backend:** KnowledgeVault v1.0.0 (frozen)  
**Date:** 2026-08-06

---

## 1. Application Architecture Overview

KnowledgeVault Flutter follows a layered, feature-sliced architecture:

```
Presentation Layer  (Screens, Widgets)
        ↓
State Layer         (Riverpod Providers / Notifiers)
        ↓
Domain Layer        (Use Cases / Business Logic)
        ↓
Data Layer          (Repositories → API Services / Local Cache)
        ↓
Infrastructure      (HTTP Client, Secure Storage, SQLite)
```

Every feature (auth, notes, categories, ask, intents, topics, attachments) is a self-contained vertical slice under `lib/features/`. Cross-cutting concerns (HTTP, auth token injection, error handling, theming) live in `lib/core/`.

---

## 2. Folder Structure

```
lib/
├── main.dart
├── app.dart                          # MaterialApp + router + theme bootstrap
│
├── core/
│   ├── api/
│   │   ├── api_client.dart           # Dio instance, base URL, interceptors
│   │   ├── auth_interceptor.dart     # Injects Bearer token; handles 401 refresh cycle
│   │   └── api_exceptions.dart       # Typed exception hierarchy
│   ├── auth/
│   │   ├── token_storage.dart        # flutter_secure_storage wrapper
│   │   └── auth_state.dart           # Global auth status notifier
│   ├── cache/
│   │   └── local_cache.dart          # SQLite / drift tables for offline data
│   ├── error/
│   │   └── error_handler.dart        # Maps HTTP status → user-facing message
│   ├── router/
│   │   └── app_router.dart           # GoRouter configuration
│   └── theme/
│       ├── app_theme.dart
│       └── app_colors.dart
│
├── features/
│   ├── auth/
│   │   ├── data/
│   │   │   ├── auth_repository.dart
│   │   │   └── models/
│   │   │       ├── login_request.dart
│   │   │       ├── register_request.dart
│   │   │       ├── token_response.dart
│   │   │       └── user_response.dart
│   │   ├── providers/
│   │   │   └── auth_provider.dart
│   │   └── ui/
│   │       ├── login_screen.dart
│   │       └── register_screen.dart
│   │
│   ├── notes/
│   │   ├── data/
│   │   │   ├── notes_repository.dart
│   │   │   └── models/
│   │   │       ├── note_create_request.dart
│   │   │       ├── note_response.dart
│   │   │       ├── note_create_response.dart
│   │   │       └── note_search_response.dart
│   │   ├── providers/
│   │   │   ├── notes_provider.dart
│   │   │   └── note_detail_provider.dart
│   │   └── ui/
│   │       ├── notes_screen.dart
│   │       ├── note_detail_screen.dart
│   │       ├── create_note_screen.dart
│   │       └── widgets/
│   │           ├── note_card.dart
│   │           └── note_search_bar.dart
│   │
│   ├── categories/
│   │   ├── data/
│   │   │   ├── categories_repository.dart
│   │   │   └── models/
│   │   │       ├── category_create_request.dart
│   │   │       └── category_response.dart
│   │   ├── providers/
│   │   │   └── categories_provider.dart
│   │   └── ui/
│   │       ├── categories_screen.dart
│   │       └── widgets/
│   │           └── category_chip.dart
│   │
│   ├── ask/
│   │   ├── data/
│   │   │   ├── ask_repository.dart
│   │   │   └── models/
│   │   │       ├── ask_request.dart
│   │   │       ├── ask_response.dart
│   │   │       ├── citation.dart
│   │   │       └── chunk_preview.dart
│   │   ├── providers/
│   │   │   └── ask_provider.dart
│   │   └── ui/
│   │       ├── ask_screen.dart
│   │       └── widgets/
│   │           ├── answer_bubble.dart
│   │           ├── citation_card.dart
│   │           └── stream_answer_view.dart
│   │
│   ├── search/
│   │   ├── data/
│   │   │   ├── search_repository.dart
│   │   │   └── models/
│   │   │       └── search_result.dart
│   │   ├── providers/
│   │   │   └── search_provider.dart
│   │   └── ui/
│   │       ├── search_screen.dart
│   │       └── widgets/
│   │           └── search_result_tile.dart
│   │
│   ├── topics/
│   │   ├── data/
│   │   │   ├── topics_repository.dart
│   │   │   └── models/
│   │   │       └── topic_response.dart
│   │   ├── providers/
│   │   │   └── topics_provider.dart
│   │   └── ui/
│   │       └── topics_screen.dart
│   │
│   ├── intents/
│   │   ├── data/
│   │   │   ├── intents_repository.dart
│   │   │   └── models/
│   │   │       ├── intent_category_response.dart
│   │   │       ├── intent_note_response.dart
│   │   │       └── note_intent_response.dart
│   │   ├── providers/
│   │   │   └── intents_provider.dart
│   │   └── ui/
│   │       ├── intents_screen.dart
│   │       └── widgets/
│   │           └── intent_category_tile.dart
│   │
│   ├── attachments/
│   │   ├── data/
│   │   │   ├── attachments_repository.dart
│   │   │   └── models/
│   │   │       └── attachment_response.dart
│   │   ├── providers/
│   │   │   └── attachments_provider.dart
│   │   └── ui/
│   │       └── widgets/
│   │           ├── attachment_list.dart
│   │           └── upload_button.dart
│   │
│   ├── dashboard/
│   │   └── ui/
│   │       └── dashboard_screen.dart
│   │
│   ├── profile/
│   │   └── ui/
│   │       └── profile_screen.dart
│   │
│   └── settings/
│       └── ui/
│           └── settings_screen.dart
│
└── shared/
    ├── widgets/
    │   ├── loading_overlay.dart
    │   ├── error_view.dart
    │   ├── empty_state.dart
    │   └── kv_app_bar.dart
    └── extensions/
        └── datetime_ext.dart
```

---

## 3. State Management — Riverpod

**Recommendation: Riverpod (`flutter_riverpod` + `riverpod_annotation`)**

### Justification vs Bloc

| Criterion | Riverpod | Bloc |
|-----------|----------|------|
| Boilerplate | Minimal — `@riverpod` codegen, one file per feature | High — event, state, bloc classes per feature |
| Learning curve | Shallow — Dart developers familiar with providers adapt quickly | Steep — event-driven paradigm is non-obvious |
| Testing | `ProviderContainer` with `override` — straightforward | Requires `MockBloc` / `whenListen` setup |
| Async patterns | Native `AsyncValue<T>` covers loading/data/error in one type | Manual `BlocState` sealed classes needed |
| Streaming (SSE) | `StreamProvider` maps directly to `/ask/stream` SSE | Custom bloc event loop required |
| Side effects | `Notifier` / `AsyncNotifier` — actions return futures | `add(event)` — return values need separate states |
| Dependency injection | Riverpod IS the DI container — no `get_it` needed | Bloc needs a separate DI layer |

**This project has streaming AI answers (`POST /ask/stream`) — Riverpod's `StreamProvider` is the natural fit.**

### Provider Taxonomy

| Type | Use |
|------|-----|
| `Provider<T>` | Synchronous, pure values (API client, theme, config) |
| `FutureProvider<T>` | One-shot async data (current user, categories list) |
| `StreamProvider<T>` | SSE streaming answer from `/ask/stream` |
| `AsyncNotifierProvider<N, T>` | Pageable lists with mutation (notes CRUD) |
| `NotifierProvider<N, T>` | Local UI state (form inputs, selected tab) |

---

## 4. Navigation Structure

**Library: `go_router`**

```
/                       → SplashScreen
/login                  → LoginScreen
/register               → RegisterScreen
/dashboard              → DashboardScreen          [auth guard]
/notes                  → NotesScreen              [auth guard]
/notes/new              → CreateNoteScreen          [auth guard]
/notes/:id              → NoteDetailScreen          [auth guard]
/notes/search           → SearchScreen              [auth guard]
/categories             → CategoriesScreen          [auth guard]
/categories/:id         → CategoryNotesScreen        [auth guard]
/ask                    → AskScreen                 [auth guard]
/topics                 → TopicsScreen              [auth guard]
/intents                → IntentsScreen             [auth guard]
/intents/:id/notes      → IntentCategoryNotesScreen [auth guard]
/settings               → SettingsScreen            [auth guard]
/profile                → ProfileScreen             [auth guard]
```

**Auth Guard:** A `redirect` function on the router reads `authStateProvider`. If unauthenticated, any protected route redirects to `/login`. After login, redirect target is restored via `extra` parameter.

**Shell Route:** Dashboard, Notes, Search, Ask, and Settings share a `ShellRoute` with a bottom navigation bar. The shell persists navigation state across tabs.

---

## 5. Repository Pattern

Every feature has one repository class that is the single source of truth for data. Repositories are injected via Riverpod providers.

```dart
// Pattern
abstract class NotesRepository {
  Future<List<NoteResponse>> listNotes();
  Future<NoteCreateResponse> createNote(String content);
  Future<NoteResponse> getNote(int id);
  Future<void> deleteNote(int id);
  Future<List<NoteSearchResponse>> searchNotes(String query);
  Future<List<NoteSearchResponse>> getRelatedNotes(int noteId);
}

class NotesRepositoryImpl implements NotesRepository {
  final ApiClient _client;
  final LocalCache _cache;

  NotesRepositoryImpl(this._client, this._cache);
  // ...
}
```

Repositories:
- Call the API service (Dio)
- Write successful responses to the local SQLite cache
- Return cached data when offline
- Throw typed `ApiException` subclasses on error

---

## 6. API Layer

**HTTP client: `dio`**

```dart
// core/api/api_client.dart
final dio = Dio(BaseOptions(
  baseUrl: AppConfig.baseUrl,           // from env / build flavor
  connectTimeout: Duration(seconds: 10),
  receiveTimeout: Duration(seconds: 60), // long for /ask/ (LLM latency)
  headers: {'Content-Type': 'application/json'},
));

dio.interceptors.addAll([
  AuthInterceptor(tokenStorage),        // adds Authorization: Bearer <token>
  LogInterceptor(requestBody: kDebugMode),
  RetryInterceptor(retries: 2),
]);
```

**Auth Interceptor behavior:**
1. On every request, read token from secure storage and add `Authorization: Bearer <token>`.
2. On 401 response: clear token, navigate to `/login` via GoRouter, cancel the request.

**Streaming (SSE):**  
`POST /ask/stream` returns `text/event-stream`. Use Dio's `ResponseType.stream` and parse lines with `utf8.decoder` + `LineSplitter`.

---

## 7. Authentication Flow

```
App Start
    │
    ├─ Token in secure storage?
    │       YES → verify with GET /auth/me
    │               OK  → route to /dashboard
    │               401 → clear token, route to /login
    │       NO  → route to /login
    │
Login Screen
    │
    POST /auth/login  {email, password}
    │
    ├─ 200 → store access_token in flutter_secure_storage
    │         update authStateProvider → authenticated
    │         navigate to /dashboard
    │
    └─ 401 → show "Invalid email or password"
             (no account lockout — backend has no lockout mechanism)

Register Screen
    │
    POST /auth/register  {username, email, password (min 8 chars)}
    │
    ├─ 201 → navigate to /login with success banner
    │
    └─ 400 → show "Email already registered" / "Username already taken"

Token expiry (30 min — backend has NO refresh token endpoint):
    │
    ├─ Any 401 response → AuthInterceptor clears token
    │                     navigates to /login
    │                     shows "Session expired. Please log in again."
```

**Important constraints from backend:**
- No refresh token endpoint exists. The 30-minute access token is the only credential.
- No logout endpoint exists. Logout is client-side only: clear the token from secure storage.
- Token payload: `{"sub": "<user_id_string>", "exp": <timestamp>}`

---

## 8. Secure Token Storage

**Library: `flutter_secure_storage`**

```dart
class TokenStorage {
  static const _key = 'kv_access_token';
  final FlutterSecureStorage _storage;

  Future<void> save(String token) => _storage.write(key: _key, value: token);
  Future<String?> read()          => _storage.read(key: _key);
  Future<void> delete()           => _storage.delete(key: _key);
}
```

Platform storage:
- iOS: Keychain Services
- Android: Android Keystore / EncryptedSharedPreferences

Never store the token in `SharedPreferences` (plaintext on Android).

---

## 9. Offline Caching Strategy

**Library: `drift` (type-safe SQLite ORM)**

The backend has no pagination, so note lists can be large. The cache allows the app to display data immediately while a refresh happens in the background (stale-while-revalidate).

**Cached entities:**

| Entity | Cache policy | Staleness |
|--------|-------------|-----------|
| Notes list | Cache-first, background refresh on pull-to-refresh | 5 min |
| Note detail | Cache-first | 5 min |
| Categories | Cache-first, refresh on app foreground | 10 min |
| Intent categories | Cache-first | 10 min |
| Topics | Cache-first | 15 min |
| Ask answers | In-memory only (no offline re-ask) | — |
| Search results | No cache (always live) | — |

**Strategy: stale-while-revalidate**
1. Return cached data immediately (non-null if available).
2. Concurrently fire the API request.
3. On response, update cache and emit new data to the UI.

**Not cached:**
- Streaming answers — ephemeral by nature.
- Search results — intent is to find the freshest match.

---

## 10. Error Handling Strategy

**Typed exception hierarchy:**

```dart
sealed class ApiException implements Exception {
  const ApiException(this.message);
  final String message;
}

class UnauthorizedException extends ApiException { ... }  // 401
class ForbiddenException extends ApiException { ... }     // 403
class NotFoundException extends ApiException { ... }      // 404
class ValidationException extends ApiException {          // 422
  final List<FieldError> errors;
}
class ConflictException extends ApiException { ... }      // 400 duplicate
class ServerException extends ApiException { ... }        // 500
class NetworkException extends ApiException { ... }       // no connectivity
class RateLimitException extends ApiException { ... }     // 429
```

**UI rendering of errors:**

| Scope | Component |
|-------|-----------|
| Full screen error | `ErrorView` widget with retry button |
| Snackbar | Transient errors (delete failed, upload failed) |
| Inline form error | Field-level validation messages |
| Banner | Auth expiry session warning |

**`AsyncValue` pattern:**

```dart
ref.watch(notesProvider).when(
  data: (notes) => NotesList(notes: notes),
  loading: () => const LoadingOverlay(),
  error: (e, _) => ErrorView(message: e.toString(), onRetry: ...),
);
```

---

## 11. Loading State Strategy

| Scenario | Strategy |
|----------|----------|
| Initial data load | Full-screen skeleton loader |
| Pull-to-refresh | `RefreshIndicator` on top of existing data |
| Create/delete mutation | Optimistic update + spinner on action button |
| AI Ask (non-streaming) | Animated "thinking" indicator; disable submit |
| AI Ask (streaming) | Token-by-token text animation |
| File upload | Linear progress bar with percentage |
| Background refresh | No indicator (silent) |

**Skeleton screens** over empty loading spinners — show the shape of content before data arrives. Use `shimmer` package.

---

## 12. Theming

**Material 3 with dynamic color support.**

```dart
// core/theme/app_theme.dart
ThemeData get lightTheme => ThemeData(
  useMaterial3: true,
  colorScheme: ColorScheme.fromSeed(
    seedColor: const Color(0xFF6750A4),  // brand purple
    brightness: Brightness.light,
  ),
  // Typography, card theme, input decoration theme...
);

ThemeData get darkTheme => ThemeData(
  useMaterial3: true,
  colorScheme: ColorScheme.fromSeed(
    seedColor: const Color(0xFF6750A4),
    brightness: Brightness.dark,
  ),
);
```

**User preference:** Stored in `SharedPreferences` (not sensitive). Options: system / light / dark. Exposed via a `themeModeProvider`.

**AI Chat distinct styling:** The Ask screen uses a chat-bubble UI. Assistant answer bubbles use a distinct `surfaceVariant` background. Citation references `[N]` are rendered as tappable chips that navigate to the source note.

---

## 13. Responsive Layout

The app targets **mobile-first** (360dp–480dp width) as the primary form factor. Tablet and desktop are secondary.

| Breakpoint | Layout |
|-----------|--------|
| < 600dp (phone) | Single-column, bottom nav bar |
| 600–840dp (tablet portrait) | Two-panel (list + detail) where applicable; rail nav |
| > 840dp (tablet landscape / desktop) | Three-panel or master/detail; side rail nav |

**Adaptive widgets:**
- `LayoutBuilder` for per-widget breakpoints.
- `NavigationBar` on mobile → `NavigationRail` on tablet → `NavigationDrawer` on desktop.
- Note detail and search results use `Expanded`/`Flexible` so they fill available space.

No fixed pixel widths. Use `MediaQuery.of(context).size.width` for conditional layout decisions only at the screen level.
