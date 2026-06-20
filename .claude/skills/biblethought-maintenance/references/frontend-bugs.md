# Frontend JS Known Bugs & Workarounds

Non-obvious runtime behavior in `_layouts/default.html`. Read before touching the TTS or font-size code.

---

## Chrome: SpeechSynthesis stops after ~15 seconds

**Symptom:** TTS plays normally for ~15s then goes silent. Button still shows "暂停" (playing state) but no audio.

**Root cause:** Chrome/Chromium has a bug where `SpeechSynthesisUtterance` objects are silently garbage-collected mid-speech on long texts. Affects Chrome on all platforms.

**Fix (already in code):** A `setInterval` keepalive calls `pause()` + `resume()` every 14 seconds to reset Chrome's internal timer. Do NOT remove this — the bug returns immediately.

```js
// in doSpeak():
startKeepAlive();  // starts the 14s interval

// keepalive function:
ttsKeepAlive = setInterval(function() {
  if (ttsState === 'playing' && window.speechSynthesis.speaking) {
    window.speechSynthesis.pause();
    window.speechSynthesis.resume();
  }
}, 14000);
```

`stopKeepAlive()` is called in `utt.onend`, `utt.onerror`, and when speed changes trigger a restart.

**Not affected:** Safari/iOS (different TTS engine, but `pause()` doesn't work there — see below).

---

## iOS/Safari: `speechSynthesis.pause()` has no effect

**Symptom:** Clicking "暂停" on iOS changes the button label to "继续" but audio keeps playing.

**Root cause:** iOS Safari does not implement `SpeechSynthesis.pause()`. It's a no-op.

**Current behavior:** Graceful degradation — the state machine gets out of sync but the user can still click "继续" (which calls `resume()`, also a no-op) or click again to cancel and restart.

**No fix needed** unless we want to implement a full cancel-and-restart approach for iOS.

---

## Speed change: position drift of ~1–2 sentences

**Symptom:** After clicking 慢/快, speech resumes a few sentences before/after the actual pause point.

**Root cause:** `onboundary` fires at word boundaries, not character boundaries, and not every browser fires it reliably. `ttsCharIdx` is an approximation.

**Acceptable:** Not worth fixing. The drift is small and the alternative (exact byte offset tracking) is fragile across browsers.
