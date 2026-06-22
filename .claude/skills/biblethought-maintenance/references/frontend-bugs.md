# Frontend JS Known Bugs & Workarounds

Non-obvious runtime behavior in `_layouts/default.html`. Read before touching the TTS or font-size code.

---

## Chrome: SpeechSynthesis stops after ~15 seconds

**Symptom:** TTS plays normally for ~15s then goes silent. Button still shows "暂停" (playing state) but no audio.

**Root cause:** Chrome/Chromium has a bug where `SpeechSynthesisUtterance` objects are silently garbage-collected mid-speech on long texts. Affects Chrome on all platforms.

**Fix (already in code):** Text is split into ~500-char chunks via `splitIntoChunks()`. Each chunk is a separate utterance; when one ends (`onend`), `speakChunk(idx + 1)` starts the next immediately. Chunk boundaries land at sentence endings (`。！？`) so transitions are natural reading pauses.

```js
// splitIntoChunks() splits at sentence boundaries, MAX 500 chars per chunk
// speakChunk(idx) speaks one chunk and chains to the next via onend
utt.onend = function() { speakChunk(idx + 1); };
```

Do NOT merge these back into one long utterance — the Chrome bug returns immediately.

**Not affected:** Safari/iOS (different TTS engine, but `pause()` doesn't work there — see below).

---

## iOS/Safari: `speechSynthesis.pause()` has no effect

**Symptom:** Clicking "暂停" on iOS changes the button label to "继续" but audio keeps playing.

**Root cause:** iOS Safari does not implement `SpeechSynthesis.pause()`. It's a no-op.

**Current behavior:** Graceful degradation — the state machine gets out of sync but the user can still click "继续" (which calls `resume()`, also a no-op) or click again to cancel and restart.

**No fix needed** unless we want to implement a full cancel-and-restart approach for iOS.

---

## Pause/resume: two separate bugs

### Silent dead-end when chunk ends while paused

**Symptom:** User pauses, clicks "继续" — button changes to "暂停" but no audio.

**Root cause:** If the current chunk finishes naturally while `ttsState === 'paused'`, `utt.onend` calls `speakChunk(idx + 1)` which returns early (state not 'playing'). `resume()` finds nothing queued — silent.

**Fix:** Pause = `cancel()` + save position. Resume = `doSpeak(savedPos)`. Never use `pause()`/`resume()`.

### Resume restarts from beginning of article

**Symptom:** After pausing, clicking "继续" always restarts from the top.

**Root cause (two layers):**
1. `onboundary` often doesn't fire for Chinese text → `ttsCharIdx` stays at `chunk.offset`. For chunk 0 that offset is 0 = beginning of article.
2. `onerror` with an unexpected error code (not `'interrupted'`/`'canceled'`) resets `ttsState = 'idle'` → next click triggers the idle branch (`ttsText = ''; ttsCharIdx = 0; doSpeak(0)`).

**Fix (already in code):**
- `speakChunk(idx, fromChar)` accepts a start-within-chunk offset and slices the text: `chunk.text.slice(fromChar - chunk.offset)`. `doSpeak` passes `fromChar` through so resume starts mid-chunk, not at chunk head.
- `onerror` checks `if (ttsState !== 'playing') return` before resetting — stale error events from a cancelled utterance can't corrupt paused state.
- Resume uses `nearestSentenceStart(ttsCharIdx)` (same as speed-change) for a clean sentence boundary.

```js
// Pause: cancel and save position
window.speechSynthesis.cancel();
ttsState = 'paused';

// Resume: find nearest sentence boundary, restart there
var pos = nearestSentenceStart(ttsCharIdx);
window.speechSynthesis.cancel();
setTimeout(function() { doSpeak(pos); }, 100);

// speakChunk: skip already-read portion of the chunk
var skip = (fromChar && fromChar > chunk.offset) ? fromChar - chunk.offset : 0;
var text = skip > 0 ? chunk.text.slice(skip) : chunk.text;
```

**Residual:** If `onboundary` never fires and the user pauses within chunk 0, `ttsCharIdx` is 0 → restarts from the beginning of chunk 0 (= article start). No fix without time-based estimation — acceptable.

---

## Speed change: position rollback up to 1 sentence

**Symptom:** After clicking 慢/快, speech resumes slightly before the pause point (up to ~1 sentence back).

**Root cause:** `onboundary` events are unreliable; `ttsCharIdx` is an approximation. Without `onboundary`, it equals the chunk start, which could be ~500 chars back.

**Fix (already in code):** `changeSpeed()` calls `nearestSentenceStart(ttsCharIdx)` before restarting. This scans backward up to 300 chars for a sentence terminator (`。！？\n`) and restarts from just after it — at most ~1 sentence of rollback, not a full chunk.

```js
var pos = nearestSentenceStart(ttsCharIdx); // ≤300 chars back, not chunk start
window.speechSynthesis.cancel();
setTimeout(function() { doSpeak(pos); }, 150);
```

**Residual:** If `onboundary` never fired for the current chunk, rollback can be up to 300 chars. Acceptable.

---

## 朗读高亮不随内容滚动

**Symptom:** TTS 朗读时当前段落有黄色高亮，但页面不滚动，高亮段落移出屏幕后用户看不到。

**Fix (already in code):** `highlightPara()` 在切换 class 后调用 `scrollIntoView`：

```js
if (active) active.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
```

`block: 'nearest'` — 只在元素不可见时才滚动，避免页面频繁跳动。不要用 `block: 'center'`（每次都跳到中间，体验差）。

---

## 不要强制预选语音

**Symptom (past bug):** 代码曾加入 `initTTSVoice()` 预选本地 zh-CN 语音，结果覆盖了用户在系统/浏览器中设置的默认语音，用户听到了不认识的声音。

**Rule:** 只设 `utt.lang = 'zh-CN'`，**不设 `utt.voice`**，让浏览器用用户的默认语音。

```js
// 正确
utt.lang = 'zh-CN';
utt.rate = speedPresets[speedIndex];

// 错误 — 不要这样做
if (ttsVoice) utt.voice = ttsVoice;
```

Do NOT add voice pre-selection back — it breaks the user's preferred voice setting.
