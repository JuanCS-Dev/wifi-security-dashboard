# WiFi Security Education - Teacher Guide

**Classroom Integration Guide for Educators**

This guide helps teachers integrate WiFi Security Education into their classroom curriculum. Perfect for computer science, technology, and digital citizenship courses.

**Author:** Juan-Dev + AI Architect - Soli Deo Gloria ✝️
**Version:** v1.0.0
**Target Audience:** K-12 Teachers, IT Instructors
**Date:** 2025-11-15

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Learning Objectives](#learning-objectives)
3. [Curriculum Alignment](#curriculum-alignment)
4. [Classroom Setup](#classroom-setup)
5. [Lesson Plans](#lesson-plans)
6. [Assessment & Evaluation](#assessment--evaluation)
7. [Student Management](#student-management)
8. [Troubleshooting](#troubleshooting)
9. [Additional Resources](#additional-resources)

---

## 🎯 Overview

### What is WiFi Security Education?

WiFi Security Education is an **educational game** that teaches students (ages 9-16) about WiFi security through:
- Interactive gameplay
- Character-driven storytelling
- Hands-on scenarios
- Real-world security concepts

### Why Use This in Your Classroom?

**Educational Benefits:**
✅ Engaging alternative to traditional lectures
✅ Self-paced learning
✅ Immediate feedback
✅ Gamified motivation
✅ Real-world relevance

**Teacher Benefits:**
✅ Ready-to-use lesson plans
✅ No preparation required
✅ Works offline (no internet needed)
✅ Free and open-source
✅ Assessment tools included

**Technical Benefits:**
✅ Cross-platform (Windows, macOS, Linux)
✅ Low system requirements
✅ Easy installation
✅ No accounts or login required
✅ COPPA compliant (safe for kids)

### Course Integration

**Best fit for:**
- Computer Science (middle/high school)
- Technology Education
- Digital Citizenship
- Internet Safety courses
- STEM electives
- Cybersecurity introduction

**Time Requirement:**
- **Minimum:** 2-3 class periods (90-120 minutes)
- **Recommended:** 4-5 class periods (180-240 minutes)
- **Extended:** 1-2 weeks (project-based learning)

---

## 📚 Learning Objectives

### Scenario 1: First Day Online

**Duration:** 30-40 minutes
**Age Group:** 9-12 years
**Difficulty:** Beginner

**Learning Objectives:**

**Knowledge (Remember & Understand):**
- Define WiFi and wireless networking
- Identify signal strength indicators
- List types of WiFi encryption (WEP, WPA, WPA2, WPA3)
- Explain why WiFi security matters

**Skills (Apply & Analyze):**
- Interpret signal strength measurements (dBm, percentage)
- Compare different encryption types
- Recognize secure vs. insecure networks

**Attitudes (Evaluate & Create):**
- Value the importance of network security
- Develop awareness of WiFi vulnerabilities

**Standards Alignment:**
- ISTE 2a: Digital Citizen - Students recognize rights/responsibilities
- CSP Framework: Network & Internet
- Common Core: CCSS.ELA-LITERACY.RST.6-8.4 (technical vocabulary)

---

### Scenario 2: The Impostor

**Duration:** 40-50 minutes
**Age Group:** 10-14 years
**Difficulty:** Intermediate

**Learning Objectives:**

**Knowledge:**
- Define Rogue Access Point (AP)
- Explain Evil Twin attacks
- Understand SSID spoofing
- Identify network impersonation tactics

**Skills:**
- Analyze network names for authenticity
- Detect suspicious WiFi networks
- Apply security best practices
- Evaluate network trustworthiness

**Attitudes:**
- Develop skepticism toward unfamiliar networks
- Appreciate the importance of verification

**Standards Alignment:**
- ISTE 2b: Engage in positive, safe behavior
- CSTA 3A-NI-04: Network security
- NIST NICE Framework: Cybersecurity concepts

---

### Scenario 3: The Invisible Listener

**Duration:** 40-50 minutes
**Age Group:** 12-16 years
**Difficulty:** Advanced

**Learning Objectives:**

**Knowledge:**
- Define packet sniffing and eavesdropping
- Explain HTTP vs. HTTPS
- Understand encryption in transit
- Recognize man-in-the-middle attacks

**Skills:**
- Identify HTTPS indicators in browsers
- Assess risk of public WiFi networks
- Apply encryption best practices
- Evaluate website security

**Attitudes:**
- Value encryption and privacy
- Develop security-conscious online habits

**Standards Alignment:**
- ISTE 2d: Manage personal data
- CSTA 3B-NI-05: Encryption and security
- AP Computer Science Principles: Internet concepts

---

## 🎓 Curriculum Alignment

### ISTE Standards for Students

**2. Digital Citizen**
- 2a: Rights, responsibilities, opportunities
- 2b: Positive, safe, legal, ethical behavior
- 2c: Respect for rights and intellectual property
- 2d: Manage personal data privacy and security

**5. Computational Thinker**
- 5c: Breaking problems into component parts
- 5d: Understanding how systems work

### CSTA K-12 Standards

**Level 2 (Grades 6-8):**
- 2-NI-04: Model network protocols
- 2-NI-05: Explain physical and digital security
- 2-CS-01: Recommend improvements to computing devices

**Level 3A (Grades 9-10):**
- 3A-NI-04: Evaluate security measures
- 3A-NI-06: Encryption to ensure confidentiality
- 3A-IC-24: Evaluate impacts of computing on society

### Common Core State Standards

**ELA/Literacy:**
- CCSS.ELA-LITERACY.RST.6-8.4: Technical vocabulary
- CCSS.ELA-LITERACY.RST.6-8.7: Integrate technical information

**Math:**
- CCSS.MATH.CONTENT.6.RP.A.3: Ratios and percentages (signal strength)

### NGSS (Science)

**Engineering Design:**
- MS-ETS1-1: Define criteria and constraints
- MS-ETS1-2: Evaluate solutions

---

## 🖥️ Classroom Setup

### Computer Lab Setup

**Hardware Requirements (Per Computer):**
- CPU: Modern processor (2015+)
- RAM: 4GB minimum, 8GB recommended
- OS: Windows 10/11, macOS 10.14+, or Linux
- Display: 1280x720 minimum resolution

**Software Installation:**

**Option 1: Lab-Wide Installation (Recommended)**
```bash
# Windows: Use MSI installer
WiFiSecurityGame-1.0.0-Windows-Setup.exe

# macOS: IT admin deployment
# Deploy .app to /Applications

# Linux: Package manager
sudo dpkg -i wifi-security-game_1.0.0_amd64.deb
```

**Option 2: Portable (No Install Required)**
- Use AppImage (Linux) or standalone .exe (Windows)
- Students can run from USB drives
- No admin rights required

**Network Configuration:**
- **No internet required** (game works offline)
- Optional: Disable internet to prevent distractions
- Mock mode: Safe for classroom use

### Student Computer Setup

**Individual Installation:**
1. Provide download link or USB with installer
2. Students follow [INSTALLATION.md](INSTALLATION.md)
3. First-run telemetry consent: Recommend "No" for privacy
4. Game ready to play!

**Shared Computer Setup:**
- Create separate user profiles
- Install once, available to all users
- Telemetry data stored per-user (~/.wifi_security_game/)

### Chromebook Compatibility

**Current Status:** ❌ Not supported (requires native install)

**Alternatives:**
- Use computer lab with Windows/macOS/Linux
- Run on teacher's computer, project to screen
- Future: Web-based version (planned)

---

## 📖 Lesson Plans

### Lesson Plan 1: Introduction to WiFi Security

**Scenario:** First Day Online
**Duration:** 45-60 minutes (1 class period)
**Grade Level:** 6-8

**Objectives:**
Students will be able to:
1. Define WiFi and wireless networking
2. Explain signal strength and its measurement
3. Identify different WiFi encryption types
4. Recognize the importance of network security

**Materials:**
- Computer lab with WiFi Security Education installed
- Optional: Projector for demo
- Student worksheet (see below)

**Lesson Procedure:**

**Introduction (10 min):**
1. Hook: "Who uses WiFi at home? What do you know about how it works?"
2. Show WiFi logo, discuss wireless connectivity
3. Preview: "Today we'll learn how WiFi works and why security matters"

**Direct Instruction (10 min):**
1. Demonstrate game launch
2. Introduce Guardian character and health bar
3. Explain signal strength (dBm, percentage)
4. Show encryption types (WEP → WPA → WPA2 → WPA3)

**Guided Practice (20 min):**
1. Students launch game
2. Complete Scenario 1: First Day Online
3. Teacher circulates, assists as needed
4. Students take notes on key concepts

**Independent Practice (10 min):**
1. Students complete worksheet
2. Reflect on real-world WiFi networks (home, school)

**Closure (5 min):**
1. Review key terms: WiFi, signal strength, encryption
2. Exit ticket: "What's the strongest WiFi encryption?"
3. Preview next lesson: Rogue APs

**Assessment:**
- Observation during gameplay
- Worksheet completion
- Exit ticket

**Student Worksheet:**

```
Name: ________________________  Date: __________

WiFi Security Basics

1. What does WiFi stand for?
   _____________________________________________

2. Signal strength measures how __________ or __________
   your WiFi connection is.

3. List the WiFi encryption types from weakest to strongest:
   Weakest: __________
            __________
            __________
   Strongest: __________

4. Why is WiFi security important?
   _____________________________________________
   _____________________________________________

5. Check your home WiFi:
   - Network name (SSID): __________________
   - Encryption type: ______________________
   - Is it secure? (circle)   YES  /  NO

6. What did you learn from the Guardian character?
   _____________________________________________
   _____________________________________________
```

---

### Lesson Plan 2: Spotting Fake Networks

**Scenario:** The Impostor
**Duration:** 45-60 minutes (1 class period)
**Grade Level:** 7-9

**Objectives:**
Students will be able to:
1. Define Rogue AP and Evil Twin attack
2. Identify characteristics of fake networks
3. Apply critical thinking to network authentication
4. Evaluate network trustworthiness

**Materials:**
- Computer lab
- Projector
- Student detective worksheet

**Lesson Procedure:**

**Hook (5 min):**
1. Scenario: "You're at a coffee shop. You see two WiFi networks: 'CoffeeShop' and 'CofeeShop'. Which do you choose?"
2. Discuss potential dangers

**Introduction (10 min):**
1. Define: Rogue AP, Evil Twin, SSID spoofing
2. Real-world examples of WiFi impersonation
3. Introduce The Impostor character

**Gameplay (25 min):**
1. Students play Scenario 2
2. Take notes on Impostor's tactics
3. Complete in-game objectives

**Discussion (10 min):**
1. What tricks did The Impostor use?
2. How can you identify fake networks?
3. Real-world applications

**Assessment (10 min):**
1. Quiz: Spot the fake network (visual examples)
2. Written response: Protection strategies

**Extension:**
- Research famous WiFi hacking incidents
- Create PSA about public WiFi safety

---

### Lesson Plan 3: Understanding Encryption

**Scenario:** The Invisible Listener
**Duration:** 45-60 minutes (1 class period)
**Grade Level:** 8-10

**Objectives:**
Students will be able to:
1. Explain packet sniffing and eavesdropping
2. Distinguish between HTTP and HTTPS
3. Evaluate encryption strength
4. Apply secure browsing practices

**Materials:**
- Computer lab
- Browser for HTTPS demo
- Student lab worksheet

**Lesson Procedure:**

**Hook (5 min):**
1. Question: "Can someone read your text messages while you're using WiFi?"
2. Discussion: Privacy expectations

**Demo (10 min):**
1. Show HTTP vs HTTPS in browser
2. Point out padlock icon 🔒
3. Explain encryption in transit

**Gameplay (25 min):**
1. Students play Scenario 3
2. Focus on encryption concepts
3. Meet The Eavesdropper

**Lab Activity (15 min):**
1. Students visit 5 websites
2. Check if HTTP or HTTPS
3. Classify as "safe" or "unsafe" for sensitive data

**Closure (5 min):**
1. Review: What is packet sniffing?
2. Exit ticket: "When should you use HTTPS?"

**Assessment:**
- Lab worksheet completion
- Exit ticket
- Optional: Create diagram of encrypted vs unencrypted traffic

---

### Multi-Day Project: WiFi Security Audit

**Duration:** 3-5 class periods
**Grade Level:** 9-12
**Type:** Project-based learning

**Project Overview:**
Students conduct a WiFi security audit of their home network and create a report with recommendations.

**Day 1: Game-Based Learning**
- Complete all 3 scenarios
- Take comprehensive notes
- Identify key security concepts

**Day 2: Research**
- Research home router settings
- Investigate router vulnerabilities
- Learn about router firmware updates

**Day 3-4: Audit**
- Survey home WiFi setup
- Check encryption type
- Test signal strength in different rooms
- Identify potential vulnerabilities

**Day 5: Presentation**
- Create presentation or report
- Present findings to class
- Share recommendations

**Rubric:**
| Criteria | Points |
|----------|--------|
| Game completion (all scenarios) | 20 |
| Research depth and sources | 20 |
| Audit thoroughness | 25 |
| Recommendations quality | 25 |
| Presentation/report quality | 10 |
| **Total** | **100** |

---

## 📊 Assessment & Evaluation

### Formative Assessment

**During Gameplay:**
- Observation checklist
- Scenario completion tracking
- Objective achievement

**Observation Checklist:**
```
Student: ________________  Date: __________

□ Engaged with game content
□ Read dialog carefully
□ Completed objectives
□ Demonstrated understanding
□ Asked relevant questions
□ Helped peers (if applicable)
□ Applied concepts to real-world

Notes:
_________________________________________
```

### Summative Assessment

**Option 1: Written Test**

Sample questions:

1. **Multiple Choice:** Which WiFi encryption is strongest?
   - A) WEP
   - B) WPA
   - C) WPA2
   - D) WPA3 ✓

2. **Short Answer:** Explain what a Rogue AP is and how to identify one.

3. **Scenario:** You're at a library and see three WiFi networks:
   - "LibraryGuest"
   - "LibraryGueest"
   - "Library_Public"

   Which would you choose and why?

4. **Essay:** Describe three ways to protect yourself when using public WiFi.

**Option 2: Performance Task**

Students demonstrate:
- Checking home WiFi encryption
- Identifying HTTPS websites
- Explaining security concepts to family

**Option 3: Project (See above)**

### Self-Assessment

**Student Reflection:**
```
After completing WiFi Security Education, I can:

□ Explain what WiFi is
□ Identify signal strength
□ Name encryption types
□ Spot fake networks
□ Understand packet sniffing
□ Recognize HTTP vs HTTPS
□ Apply security best practices

The most important thing I learned:
_________________________________________

One question I still have:
_________________________________________
```

---

## 👨‍🎓 Student Management

### Pacing

**Self-Paced (Recommended):**
- Students progress at own speed
- Advanced students finish early, can help others
- Struggling students get extra time

**Teacher-Paced:**
- All students on same scenario
- Pause for discussion between scenarios
- More control over timing

### Differentiation

**For Struggling Students:**
- Pair with peer mentor
- Extended time
- Simplified worksheet
- Focus on Scenario 1 only

**For Advanced Students:**
- Complete all scenarios quickly
- Extension project (home network audit)
- Create security presentation for class
- Research advanced topics (VPN, MAC filtering)

**For English Language Learners:**
- Visual game elements help comprehension
- Emoji characters are universal
- Pre-teach vocabulary
- Allow translation tools

**For Students with Disabilities:**
- Keyboard-only controls (accessible)
- Text-based UI (screen reader friendly)
- Adjustable pacing (pause anytime)
- Zoom support (F11 fullscreen)

### Classroom Management

**Headphones:** Recommended for focus (no audio currently, but reduces distractions)

**Screen Monitoring:** Use classroom management software to ensure on-task behavior

**Collaboration:** Allow pair programming/gaming for peer learning

**Breaks:** Recommend 5-minute break after each scenario

---

## 🔧 Troubleshooting

### Common Student Issues

**"I can't see the characters!"**
- Solution: Install emoji fonts (Linux: `fonts-noto-color-emoji`)

**"The game is laggy"**
- Solution: Close other programs, check FPS (should be ~60)

**"I don't understand the objectives"**
- Solution: Read Professor Packet's messages carefully, ask teacher

**"I completed the scenario but nothing happened"**
- Solution: Check all objectives marked ✅, may need to wait for outro dialog

### Common Teacher Issues

**"Game won't install on lab computers"**
- Solution: Request IT admin help, use portable .exe/.AppImage

**"Students finishing at different times"**
- Solution: Prepare extension activities or allow peer mentoring

**"How do I see student progress?"**
- Solution: Walk around, use observation checklist, check local data files

**"Is there a teacher dashboard?"**
- Solution: Not yet (future feature), currently manual tracking

---

## 📚 Additional Resources

### For Teachers

**Lesson Planning:**
- Common Sense Media: Digital Citizenship curriculum
- Code.org: Computer Science courses
- CyberPatriot: Cybersecurity competition

**Professional Development:**
- ISTE membership and certifications
- Google for Education: Be Internet Awesome
- CSTA workshops

### For Students

**Extensions:**
- Khan Academy: Computer Science
- Codecademy: Cybersecurity course
- TryHackMe: Hands-on security labs (ages 13+)

**Reading:**
- "Cybersecurity for Kids" by Anna Huddleston
- "Hacker" by Malorie Blackman (fiction)

**Videos:**
- Crash Course Computer Science (YouTube)
- How WiFi Works (TED-Ed)

### Parent Resources

Send home:
```
Dear Parents/Guardians,

Your student is learning about WiFi security through
an educational game called "WiFi Security Education."

This teaches important digital citizenship skills:
- Understanding WiFi networks
- Identifying security threats
- Protecting personal data online

No personal data is collected. The game is 100% safe
and educational.

Optional: Install at home for extended learning!
Download: [link]

Questions? Email: [your email]
```

---

## 📞 Support

**Technical Issues:** support@wifisecurity.education
**Curriculum Questions:** teachers@wifisecurity.education
**Bug Reports:** Use in-game F1 or GitHub issues

**Teacher Community:**
- Discord: #teachers channel
- Email list: teachers@wifisecurity.education

---

## 📝 Feedback

**We want to hear from you!**

Help us improve by sharing:
- What worked well in your classroom
- What could be better
- Lesson plans you created
- Student feedback

**Submit feedback:**
- Email: teachers@wifisecurity.education
- GitHub: Open an issue
- Survey: [link]

---

**Thank you for teaching the next generation of cybersecurity-aware citizens!** 🎓

**Soli Deo Gloria** ✝️

---

## Appendix: Standards Crosswalk

| WiFi Security Education | ISTE | CSTA | Common Core |
|-------------------------|------|------|-------------|
| Scenario 1: WiFi basics | 2a, 5d | 2-NI-04 | RST.6-8.4 |
| Scenario 2: Rogue APs | 2b, 5c | 3A-NI-04 | RST.6-8.7 |
| Scenario 3: Encryption | 2d, 5d | 3A-NI-06 | MATH.6.RP.A.3 |

---

## Version History

- **v1.0.0** (2025-11-15): Initial teacher guide
  - 3 lesson plans
  - Assessment tools
  - Curriculum alignment
  - Classroom setup guide
