# Beta Testing Documentation

**Complete beta testing resources for WiFi Security Education**

Author: Juan-Dev + AI Architect - Soli Deo Gloria ✝️
Date: 2025-11-15

---

## 📚 Documentation Index

### For Beta Testers

1. **[BETA_PROGRAM.md](BETA_PROGRAM.md)** - Complete beta program overview
   - Who can join
   - What we're testing
   - How to participate
   - Timeline and rewards

2. **[TESTING_CHECKLIST.md](TESTING_CHECKLIST.md)** - Systematic testing guide
   - Installation testing
   - Feature testing
   - Performance testing
   - Complete workflow

3. **[BUG_REPORT_TEMPLATE.md](BUG_REPORT_TEMPLATE.md)** - Bug reporting template
   - How to report bugs
   - What information to include
   - Email template

4. **[FEEDBACK_TEMPLATE.md](FEEDBACK_TEMPLATE.md)** - General feedback template
   - Feature feedback
   - User experience
   - Suggestions

---

## 🚀 Quick Start for Beta Testers

### Step 1: Read the Program Overview
Start with **[BETA_PROGRAM.md](BETA_PROGRAM.md)** to understand:
- Beta program goals
- Your role as a beta tester
- Timeline and expectations

### Step 2: Install the Game
Follow the installation instructions for your platform:
- **Windows:** Run the installer (.exe)
- **macOS:** Open .dmg and drag to Applications
- **Linux:** Use AppImage or install .deb package

See **[../BUILD_GUIDE.md](../BUILD_GUIDE.md)** for detailed instructions.

### Step 3: Complete the Testing Checklist
Use **[TESTING_CHECKLIST.md](TESTING_CHECKLIST.md)** to:
- Test all features systematically
- Track your progress
- Identify issues

**Estimated time:** 3 hours

### Step 4: Submit Feedback

**In-Game (Preferred):**
- **F1** - Report bugs
- **F12** - Submit feedback
- **F2** - Enable/disable telemetry

**External:**
- Email: beta@wifisecurity.education
- Discord: [Beta Testing Channel](#)
- Use templates for consistency

---

## 📋 Testing Workflow

### Week 1-2: Initial Testing
**Focus:** Installation and basic functionality

1. Install the game
2. Complete Phase 1-2 of testing checklist
3. Report installation issues
4. Test basic controls and UI

**Deliverables:**
- Installation success/failure report
- Basic functionality bugs
- First impressions feedback

### Week 3-4: Deep Dive
**Focus:** Educational scenarios and gameplay

1. Complete all 3 scenarios
2. Complete Phase 3 of testing checklist
3. Evaluate educational effectiveness
4. Test character interactions

**Deliverables:**
- Scenario completion reports
- Educational value feedback
- Character/threat system bugs

### Week 5-6: Polish and Performance
**Focus:** Performance, stability, and final feedback

1. Long-session stability testing
2. Complete Phase 5 of testing checklist
3. Performance metrics
4. Final feedback survey

**Deliverables:**
- Performance report (FPS, stability)
- Final feedback (F12)
- Suggestions for v1.1

---

## 🐛 How to Report Bugs

### Method 1: In-Game (F1) ⭐ RECOMMENDED

1. Press **F1** during gameplay
2. Fill in the bug report form:
   - Title (short summary)
   - Description (what happened)
   - Steps to reproduce
   - Expected vs actual behavior
   - Severity (low/medium/high/critical)
   - Category (gameplay/performance/ui/etc.)
3. Press ENTER to submit
4. Bug saved to `~/.wifi_security_game/bugs.json`

**Advantages:**
- Quick and easy
- Includes system info automatically
- Works offline

### Method 2: Email

1. Use **[BUG_REPORT_TEMPLATE.md](BUG_REPORT_TEMPLATE.md)**
2. Fill in all sections
3. Attach screenshots/logs if possible
4. Send to: beta@wifisecurity.education

**Use when:**
- Bug prevents game from running
- Need to attach files (screenshots, logs)
- Prefer detailed written reports

### Method 3: Discord

1. Post in #beta-bugs channel
2. Include:
   - Platform (Windows/macOS/Linux)
   - Steps to reproduce
   - Screenshots if possible
3. Tag @developers for urgent issues

**Use when:**
- Need real-time discussion
- Want to check if others have same issue
- Quick questions

---

## 💬 How to Submit Feedback

### Method 1: In-Game (F12) ⭐ RECOMMENDED

1. Press **F12** during gameplay
2. Fill in the feedback form:
   - Rating (1-5 stars)
   - What you liked
   - What you disliked
   - Suggestions
   - Age group (optional)
3. Press ENTER to submit
4. Feedback saved to `~/.wifi_security_game/feedback.json`

### Method 2: Weekly Survey

- Sent every Friday via email
- 5-minute quick survey
- Covers week's testing progress

### Method 3: Email

1. Use **[FEEDBACK_TEMPLATE.md](FEEDBACK_TEMPLATE.md)**
2. Fill in relevant sections
3. Send to: beta@wifisecurity.education

### Method 4: Discord

- Share in #beta-feedback channel
- Discuss with other testers
- Real-time conversations

---

## 📊 Telemetry System

### What is Telemetry?

Anonymous usage data that helps us understand:
- Which scenarios players complete
- How long they play
- What features they use
- Performance metrics (FPS)

### Your Choice

**Telemetry is OPT-IN:**
- Disabled by default
- You choose on first launch
- Toggle anytime with **F2**

### What We Collect (IF YOU SAY YES)

✅ **Collected:**
- Scenario completions
- Session duration
- Performance metrics
- Feature usage

❌ **NOT Collected:**
- Your name
- Your WiFi password
- Personal information
- Location data

### Privacy Promise

- 100% anonymous
- Stored locally first
- You can delete anytime
- Not sold to third parties

### How to Manage

- **F2** - Toggle telemetry ON/OFF
- Check status on quit screen
- Delete data: `~/.wifi_security_game/`

---

## 🎯 Testing Priorities

### Critical (MUST TEST)
1. **Installation** - Does the game install correctly?
2. **First Launch** - Does it run without crashing?
3. **Core Gameplay** - Can you complete scenarios?
4. **Educational Value** - Do you actually learn?

### High Priority
1. **Character System** - Do characters work correctly?
2. **Threat System** - Do threats activate/detect properly?
3. **Dialog System** - Can you read and understand dialogs?
4. **Performance** - Does the game run at 60 FPS?

### Medium Priority
1. **Feedback System** - Does F1/F12 work?
2. **Telemetry** - Does F2 toggle work?
3. **UI/UX** - Is everything clear and readable?
4. **Cross-platform** - Works on your OS?

### Nice to Have
1. **Long Sessions** - Stable after 30+ minutes?
2. **Edge Cases** - What happens if you spam keys?
3. **Accessibility** - Any issues for specific needs?

---

## 📈 What Makes Good Feedback?

### ✅ Good Bug Report

```
Title: "Impostor doesn't deactivate after defeating"

Description:
After I detected and defeated the Impostor threat,
the threat warning stayed on screen and wouldn't disappear.

Steps to Reproduce:
1. Load Scenario 2
2. Press 'I' to activate Impostor
3. Press 'D' to detect Impostor
4. Complete the scenario
5. Impostor warning still shows

Expected: Impostor warning disappears after defeat
Actual: Warning stays on screen

Severity: Medium
Platform: Windows 11
```

**Why it's good:**
- Clear, specific title
- Detailed description
- Reproducible steps
- Expected vs actual behavior
- Includes platform

### ❌ Bad Bug Report

```
Title: "Game broken"

Description:
The game doesn't work right.

Steps: I don't know, it just happens.

Severity: Critical
```

**Why it's bad:**
- Vague title
- No details
- Can't reproduce
- No platform info
- Not helpful

### ✅ Good Feedback

```
I really enjoyed Scenario 2! The Impostor character was engaging
and I learned a lot about rogue APs. The emoji visuals work
surprisingly well!

Suggestions:
- Add more scenarios about other WiFi threats
- Make the dialog bubbles stay on screen a bit longer
- Add keyboard shortcuts reference (F1/F2/etc.)

Overall: 4/5 stars. Great educational game!
```

**Why it's good:**
- Specific about what worked
- Constructive suggestions
- Positive tone
- Actionable feedback

---

## 🏆 Beta Tester Recognition

### Top Contributors

We track contributions through:
- Number of bugs reported
- Quality of feedback
- Testing thoroughness
- Community participation

### Rewards

**All testers receive:**
- Name in game credits (optional)
- Beta tester badge
- Certificate of participation

**Top contributors receive:**
- Special recognition in release announcement
- Elite tester badge
- Priority access to future betas
- Physical stickers (mailed)

---

## 📞 Support & Contact

### General Questions
**Email:** beta@wifisecurity.education
**Response Time:** 1-2 business days

### Technical Issues
**Email:** support@wifisecurity.education
**Discord:** #beta-support channel
**Response Time:** Same day (weekdays)

### Security Issues
**Email:** security@wifisecurity.education
**Priority:** Immediate

### Feedback Submission
**In-Game:** F1 (bugs), F12 (feedback)
**Email:** beta@wifisecurity.education
**Discord:** #beta-bugs, #beta-feedback

---

## 📅 Important Dates

- **Nov 15, 2025:** Beta program opens
- **Nov 22, 2025:** Applications close
- **Nov 23, 2025:** Beta testing begins
- **Dec 20, 2025:** Beta testing ends
- **Dec 27, 2025:** Final testing phase
- **Jan 15, 2026:** Public release (planned)

---

## 🔗 Additional Resources

### Documentation
- [Main README](../../README.md) - Project overview
- [Build Guide](../BUILD_GUIDE.md) - Installation instructions
- [Implementation Status](../IMPLEMENTATION_STATUS.md) - Development progress

### External Links
- **Discord:** [discord.gg/wifi-security-beta](#)
- **GitHub:** [github.com/JuanCS-Dev/wifi-security-dashboard](#)
- **Website:** [wifisecurity.education](#) (coming soon)

---

## 🙏 Thank You!

Your participation in this beta program is **invaluable**. You're helping create an educational experience that will benefit students worldwide.

**Happy Testing!** 🚀

---

**Soli Deo Gloria** ✝️

---

## Change Log

- **2025-11-15:** Beta program launched
- **2025-11-15:** Documentation created
- **2025-11-15:** Feedback system integrated
