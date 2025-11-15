# WiFi Security Education - Beta Testing Checklist

**Complete testing guide for beta testers**

Author: Juan-Dev + AI Architect - Soli Deo Gloria ✝️
Date: 2025-11-15

---

## 📋 How to Use This Checklist

1. Work through each section systematically
2. Check ✅ items that work correctly
3. Mark ❌ items that have issues
4. Report all ❌ items using F1 (bug report)
5. Add notes for anything unusual

---

## 🎯 Testing Phases

Complete these in order:

- [ ] **Phase 1:** Installation & First Launch (15 min)
- [ ] **Phase 2:** Basic Functionality (30 min)
- [ ] **Phase 3:** Educational Scenarios (60 min)
- [ ] **Phase 4:** Advanced Features (30 min)
- [ ] **Phase 5:** Performance & Stability (30 min)
- [ ] **Phase 6:** Final Feedback (15 min)

**Total Time:** ~3 hours

---

## Phase 1: Installation & First Launch (15 min)

### Installation

**Platform-Specific:**

#### Linux
- [ ] AppImage runs without installation
- [ ] AppImage has execute permissions
- [ ] .deb package installs successfully
- [ ] Desktop shortcut created
- [ ] Menu entry created
- [ ] Application icon displays

#### Windows
- [ ] Installer runs without errors
- [ ] Installation path is correct
- [ ] Desktop shortcut created
- [ ] Start menu entry created
- [ ] Application icon displays
- [ ] Uninstaller works

#### macOS
- [ ] .dmg opens correctly
- [ ] Drag-and-drop installation works
- [ ] App appears in Applications folder
- [ ] Launchpad icon displays
- [ ] No Gatekeeper issues (or bypassed correctly)

### First Launch

- [ ] Application launches successfully
- [ ] Window size is correct (1280x720)
- [ ] Title displays: "WiFi Security Dashboard - Project Lighthouse"
- [ ] No immediate crashes
- [ ] Console shows no critical errors

### Telemetry Consent

- [ ] Consent dialog appears on first launch
- [ ] Dialog explains what data is collected
- [ ] Privacy policy is clear
- [ ] "Yes" option works
- [ ] "No" option works
- [ ] Choice is saved (doesn't ask again)

**Notes:**
```
[Write any installation issues here]
```

---

## Phase 2: Basic Functionality (30 min)

### UI Elements

- [ ] Title renders correctly
- [ ] Subtitle displays version
- [ ] Guardian emoji (🛡️) displays
- [ ] Health bar renders
- [ ] Network information shows
- [ ] Signal strength updates
- [ ] Encryption type displays
- [ ] FPS counter visible

### Controls

- [ ] ESC key quits game
- [ ] P key pauses/unpauses
- [ ] F11 toggles fullscreen
- [ ] F1 opens bug report
- [ ] F2 toggles telemetry
- [ ] F12 opens feedback dialog
- [ ] Mouse input works (if applicable)

### Characters

**Guardian (🛡️):**
- [ ] Guardian emoji renders
- [ ] Health bar syncs with signal strength
- [ ] Guardian speaks (dialog bubbles)
- [ ] Armor changes with encryption level

**Professor Packet (👨‍🏫):**
- [ ] Professor emoji renders
- [ ] Welcome message appears
- [ ] Dialog bubbles work
- [ ] Educational tips display

### Network State

- [ ] SSID displays correctly
- [ ] Signal strength (-dBm) updates
- [ ] Signal percentage calculates correctly
- [ ] Encryption type shows
- [ ] Network changes detected (if testing with real WiFi)

**Notes:**
```
[Write any basic functionality issues here]
```

---

## Phase 3: Educational Scenarios (60 min)

### Scenario 1: First Day Online

**Loading:**
- [ ] Press "1" key to load scenario
- [ ] Scenario loads without errors
- [ ] Intro dialog displays
- [ ] Professor Packet introduces scenario

**Objectives:**
- [ ] Objective 1 displays
- [ ] Objective tracking works
- [ ] Press "C" to complete objectives (testing)
- [ ] Progress bar updates
- [ ] Completion triggers next objective

**Content:**
- [ ] Educational content is clear
- [ ] Difficulty is appropriate for age 9-12
- [ ] Terminology explained
- [ ] No technical jargon without explanation

**Completion:**
- [ ] All objectives completable
- [ ] Outro dialog displays
- [ ] XP award shows
- [ ] Success message appears

**Educational Value:**
Did you learn something about WiFi security?
- [ ] Yes, learned new concepts
- [ ] Yes, reinforced existing knowledge
- [ ] No, too easy
- [ ] No, too difficult

**Notes:**
```
[Scenario 1 feedback]
```

---

### Scenario 2: The Impostor

**Loading:**
- [ ] Press "2" key to load scenario
- [ ] Scenario loads correctly
- [ ] Impostor introduced

**The Impostor Threat (👻):**
- [ ] Press "I" to activate Impostor
- [ ] Impostor emoji appears
- [ ] Threat warning displays (red)
- [ ] Dialog explains rogue AP threat
- [ ] Press "D" to detect threat
- [ ] Detection mechanic works
- [ ] Educational content about Evil Twin attacks

**Objectives:**
- [ ] Identify rogue AP objective
- [ ] Learn about SSID spoofing
- [ ] Mitigation steps explained
- [ ] Completion works

**Educational Value:**
Did you understand rogue AP/Evil Twin attacks?
- [ ] Yes, concept is clear
- [ ] Partially understood
- [ ] No, too confusing

**Notes:**
```
[Scenario 2 feedback]
```

---

### Scenario 3: The Invisible Listener

**Loading:**
- [ ] Press "3" key to load scenario
- [ ] Scenario loads correctly
- [ ] Eavesdropper introduced

**The Eavesdropper Threat (👁️):**
- [ ] Press "E" to activate Eavesdropper
- [ ] Eavesdropper emoji appears
- [ ] Threat warning displays (orange)
- [ ] Dialog explains packet sniffing
- [ ] Press "D" to detect threat
- [ ] Detection mechanic works
- [ ] Educational content about HTTP vs HTTPS

**Objectives:**
- [ ] Identify packet sniffing threat
- [ ] Learn about encryption importance
- [ ] Understand HTTP vs HTTPS
- [ ] Mitigation steps clear
- [ ] Completion works

**Educational Value:**
Did you understand packet sniffing and encryption?
- [ ] Yes, concept is clear
- [ ] Partially understood
- [ ] No, too confusing

**Notes:**
```
[Scenario 3 feedback]
```

---

## Phase 4: Advanced Features (30 min)

### Threat System

**Multiple Threats:**
- [ ] Activate both threats (I + E)
- [ ] Both threats visible simultaneously
- [ ] No performance degradation
- [ ] Detection works for both
- [ ] Dialog doesn't overlap

**Threat Lifecycle:**
- [ ] Activate → threat appears
- [ ] Detect → threat acknowledged
- [ ] Defeat → threat disappears (if implemented)
- [ ] Deactivate → threat fades out

### Feedback System

**Bug Report (F1):**
- [ ] F1 opens bug report dialog
- [ ] All fields work
- [ ] Steps to reproduce field functional
- [ ] Severity selection works
- [ ] Category selection works
- [ ] "Cancel" aborts report
- [ ] "Submit" saves report
- [ ] Confirmation message displays

**General Feedback (F12):**
- [ ] F12 opens feedback dialog
- [ ] Rating (1-5 stars) works
- [ ] Comment field functional
- [ ] Like/Dislike fields work
- [ ] Suggestions field works
- [ ] Age group selection works
- [ ] "Cancel" aborts
- [ ] "Submit" saves feedback

**Telemetry Toggle (F2):**
- [ ] F2 toggles telemetry
- [ ] Status message shows ON/OFF
- [ ] Setting persists between sessions

### Data Files

Check if feedback files created in `~/.wifi_security_game/`:
- [ ] `feedback.json` (if feedback submitted)
- [ ] `bugs.json` (if bugs reported)
- [ ] `events.json` (if telemetry enabled)
- [ ] `consent.json` (telemetry preference)

**Notes:**
```
[Advanced features feedback]
```

---

## Phase 5: Performance & Stability (30 min)

### Performance

**FPS Testing:**
- [ ] FPS counter displays
- [ ] Target FPS: 60
- [ ] Actual FPS: _______ (write value)
- [ ] Performance: _______% (FPS/60 * 100)
- [ ] No frame drops during normal play
- [ ] Smooth animations

**Resource Usage:**

Check with Task Manager / Activity Monitor:
- [ ] CPU usage: _______% (write value)
- [ ] RAM usage: _______ MB (write value)
- [ ] No memory leaks (RAM stable over 10 min)

### Stability

**Long Session Test:**

Run the game for 30 minutes:
- [ ] No crashes
- [ ] No freezes
- [ ] No visual glitches
- [ ] Performance stays consistent
- [ ] Dialog system works after extended use

**Stress Test:**

Try to break the game:
- [ ] Rapid key presses (spam keys)
- [ ] Activate/deactivate threats rapidly
- [ ] Switch scenarios quickly
- [ ] Pause/unpause repeatedly
- [ ] Toggle fullscreen multiple times

Did anything break?
- [ ] No, game is stable
- [ ] Yes, found issues (report with F1)

**Notes:**
```
[Performance and stability feedback]
```

---

## Phase 6: Final Feedback (15 min)

### Overall Experience

**Rating (1-5 stars):**
- Overall quality: ⭐⭐⭐⭐⭐ (circle rating)
- Educational value: ⭐⭐⭐⭐⭐
- Fun factor: ⭐⭐⭐⭐⭐
- Difficulty: ⭐⭐⭐⭐⭐
- Visual design: ⭐⭐⭐⭐⭐

### What Worked Well ✅

```
[Write 3-5 things you liked]

1.

2.

3.

```

### What Needs Improvement ❌

```
[Write 3-5 things that could be better]

1.

2.

3.

```

### Suggestions 💡

```
[Write any suggestions for new features or improvements]




```

### For Teachers/Parents

If you're a teacher or parent:

**Would you use this in a classroom/at home?**
- [ ] Yes, definitely
- [ ] Yes, with modifications
- [ ] Maybe
- [ ] Probably not
- [ ] No

**Why or why not?**
```




```

**Age appropriateness:**
- [ ] Perfect for 9-12 years
- [ ] Too easy for 9-12 years
- [ ] Too difficult for 9-12 years
- [ ] Better for older students (13-16)
- [ ] Better for younger students (6-8)

**Educational alignment:**
- [ ] Aligns with curriculum
- [ ] Good supplemental material
- [ ] Needs alignment adjustments

### Final Thoughts

**One sentence summary:**
```
[In one sentence, describe your overall experience]
```

**Would you recommend this game to others?**
- [ ] Yes, highly recommend
- [ ] Yes, recommend
- [ ] Neutral
- [ ] Probably not
- [ ] No, would not recommend

---

## 📤 Submitting Your Testing Results

### Option 1: In-Game Feedback (Preferred)
1. Press **F12** to open feedback dialog
2. Fill in your responses from this checklist
3. Submit

### Option 2: Email
Send this completed checklist to:
**beta@wifisecurity.education**

### Option 3: Discord
Share your findings in the beta channel

---

## 🏆 Testing Complete!

**Thank you for your thorough testing!** 🎉

Your feedback helps make WiFi Security Education better for students worldwide.

---

**Platform Tested:** ________________ (Windows / macOS / Linux)
**Date Tested:** ________________
**Tester Name (optional):** ________________
**Tester Age Group:** ________________

---

**Soli Deo Gloria** ✝️
