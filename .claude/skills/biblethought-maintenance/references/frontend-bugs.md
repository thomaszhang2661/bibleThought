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

## Pause/resume: silent dead-end when chunk ends while paused

**Symptom:** User pauses TTS, then clicks "继续" — button changes back to "暂停" but no audio plays.

**Root cause:** With chunked TTS, if the current chunk finishes naturally while `ttsState === 'paused'`, `utt.onend` fires and calls `speakChunk(idx + 1)`, which returns early (state isn't 'playing'). When the user clicks "继续", `speechSynthesis.resume()` is called but there's nothing queued — TTS is silently dead.

**Fix (already in code):** Pause is implemented as `cancel()` + save position, not `pause()`. Resume calls `doSpeak(savedPosition)` to restart from the saved char index. `pause()`/`resume()` are not used.

```js
// Pause: cancel and remember position
window.speechSynthesis.cancel();
ttsState = 'paused';

// Resume: restart from remembered position
var pos = ttsCharIdx;
window.speechSynthesis.cancel();
setTimeout(function() { doSpeak(pos); }, 100);
```

Do NOT switch back to `speechSynthesis.pause()`/`resume()` — the bug returns.

---

## Speed change: position drift of ~1–2 sentences

**Symptom:** After clicking 慢/快, speech resumes a few sentences before/after the actual pause point.

**Root cause:** `onboundary` fires at word boundaries, not character boundaries, and not every browser fires it reliably. `ttsCharIdx` is an approximation.

**Acceptable:** Not worth fixing. The drift is small and the alternative (exact byte offset tracking) is fragile across browsers.
