# Terminal Layout Refinement Plan
**Date:** 2025-11-12  
**Author:** Juan-Dev - Soli Deo Gloria ✝️  
**Goal:** Make dashboard feel like native terminal app, not flashy GUI

---

## 🎯 Problem Statement

**Current:** Dashboard looks like GUI app that happens to run in terminal
- Multiple bright border colors (green, yellow, cyan, magenta)
- Unicode box-drawing characters
- High color contrast
- "Flashy" modern app aesthetic

**Target:** Terminal-native feel like htop, btop, nvim
- Muted, consistent colors
- Simple ASCII borders (or minimal unicode)
- Cohesive terminal aesthetic
- Professional, not flashy

---

## 📋 Analysis: What Makes Terminal Apps Feel Native?

### ✅ Good Examples (htop, btop, nvim, ranger):
1. **Limited color palette** (3-4 colors max)
2. **Muted tones** (no bright neon)
3. **Consistent borders** (same style everywhere)
4. **ASCII-first** (or minimal unicode)
5. **Dark background** (terminal default)
6. **Information density** (compact, efficient)

### ❌ Current Issues:
1. **6 different border colors** per dashboard
   - Green (CPU, RAM)
   - Cyan (Disk, Network)
   - Yellow (WiFi)
   - Magenta (Packets)
   
2. **Box-drawing unicode** (●, █, ░, ▂, ▄, ▆)
   - Looks modern, but not terminal-native

3. **High contrast colors**
   - bright_white, bright_cyan, bright_yellow
   - Too "GUI-like"

---

## 🔧 Refinement Strategy

### Phase 1: Unified Border Style
**Current:**
```css
CPUWidget { border: solid green; }
RAMWidget { border: solid green; }
DiskWidget { border: solid cyan; }
WiFiWidget { border: solid yellow; }
```

**Option A: Single color (minimal)**
```css
CPUWidget, RAMWidget, DiskWidget, WiFiWidget {
    border: solid $primary;  /* or dim white */
}
```

**Option B: ASCII borders (more terminal)**
```css
Widget {
    border: ascii $primary;
}
```

**Recommendation:** Option A - single muted color

---

### Phase 2: Muted Color Palette

**Current palette:**
```
bright_white, bright_cyan, bright_yellow, bright_green
green, yellow, red, cyan, magenta
```

**Target palette (terminal-native):**
```
PRIMARY:   dim white / gray     (text, borders)
SUCCESS:   muted green          (normal status)
WARNING:   muted yellow/orange  (high status)
CRITICAL:  muted red            (critical status)
ACCENT:    subtle blue/cyan     (highlights only)
```

**Implementation:**
```css
/* In main CSS or theme */
$terminal-text: #c0c0c0;      /* Muted white */
$terminal-border: #808080;    /* Gray */
$terminal-success: #5faf5f;   /* Muted green */
$terminal-warning: #d78700;   /* Muted orange */
$terminal-critical: #d75f5f;  /* Muted red */
$terminal-accent: #5f87af;    /* Muted blue */
```

---

### Phase 3: Simplify Visual Elements

**Status dots - Keep but mute:**
```python
# Before
"[bright_green]●[/bright_green]"

# After
"[green]●[/green]"  # Let terminal theme control brightness
```

**Progress bars - ASCII alternative:**
```python
# Current (Unicode)
bar = "█" * filled + "░" * (bar_length - filled)

# Option A: Keep unicode but mute colors
bar = "█" * filled + "░" * (bar_length - filled)  # No color wrapping

# Option B: Pure ASCII
bar = "#" * filled + "-" * (bar_length - filled)

# Recommendation: Option A (unicode is fine if colors are muted)
```

**Headers - Reduce emoji intensity:**
```python
# Before
"[bold bright_white]💻 CPU[/bold bright_white]"

# After
"[bold]💻 CPU[/bold]"  # Remove bright_white
# Or even: "CPU" (no emoji if too flashy)
```

---

### Phase 4: Layout Density

**Goal:** More information, less whitespace (like htop)

**Current:** Generous padding (1-2 units)
```css
padding: 1 2;
margin: 0 1 0 1;
```

**Target:** Compact terminal density
```css
padding: 0 1;  /* Tighter */
margin: 0;     /* Minimal */
```

**Grid gutter:**
```css
/* Current */
grid-gutter: 1 2;

/* Target */
grid-gutter: 1 1;  /* More compact */
```

---

## 🎨 Proposed CSS Theme: "Terminal Native"

```css
/* Terminal-native theme for dashboard */

:root {
    /* Base colors - muted terminal palette */
    $terminal-bg: #1e1e1e;
    $terminal-panel: #2d2d2d;
    $terminal-text: #c0c0c0;
    $terminal-text-dim: #808080;
    $terminal-border: #4a4a4a;
    
    /* Status colors - muted */
    $terminal-success: #5faf5f;
    $terminal-warning: #d78700;
    $terminal-critical: #d75f5f;
    $terminal-info: #5f87af;
}

Screen {
    background: $terminal-bg;
}

/* Unified border style - no color coding */
CPUWidget, RAMWidget, DiskWidget, WiFiWidget, 
NetworkStatsWidget, PacketStatsWidget {
    border: solid $terminal-border;
    background: $terminal-panel;
    padding: 0 1;
}

/* Only use color for status indicators */
.status-normal { color: $terminal-success; }
.status-warning { color: $terminal-warning; }
.status-critical { color: $terminal-critical; }

/* Mute all text */
Static {
    color: $terminal-text;
}

Header, Footer {
    background: $terminal-panel;
    color: $terminal-text;
}
```

---

## 📝 Implementation Checklist

### Step 1: Consolidate Colors
- [ ] Replace all border colors with single gray/dim
- [ ] Remove `bright_*` color modifiers
- [ ] Use color only for status dots (●)

### Step 2: Simplify Headers
- [ ] Remove or reduce emoji usage
- [ ] Change `[bold bright_white]` to `[bold]`
- [ ] Let terminal theme control brightness

### Step 3: Unify Borders
- [ ] All widgets use same border color
- [ ] Consider `border: solid $primary` globally
- [ ] Test with ASCII borders (`border: ascii`)

### Step 4: Compact Layout
- [ ] Reduce padding: `padding: 1 2` → `0 1`
- [ ] Reduce grid gutter: `grid-gutter: 1 2` → `1 1`
- [ ] Increase information density

### Step 5: Test in Real Terminal
- [ ] Test in GNOME Terminal
- [ ] Test in iTerm2
- [ ] Test in Alacritty (pure terminal emulator)
- [ ] Verify it looks "native" not "app-like"

---

## 🎯 Success Criteria

**Visual test:** If user sees dashboard, they should think:
- ✅ "This is a terminal monitoring tool like htop"
- ❌ "This is a GUI app running in terminal"

**Technical criteria:**
- Single consistent border style across all widgets
- Max 3-4 colors (background, text, status)
- Muted tones (no bright neon)
- Compact, information-dense layout
- Emoji optional (can be disabled)

---

## 🚀 Quick Win Strategy (Boris approach)

**30-minute implementation:**

1. **Create terminal theme CSS** (5 min)
   - Single border color
   - Muted palette
   
2. **Update consolidated_dashboard.py** (10 min)
   - Remove color-coded borders
   - Mute headers
   
3. **Apply to all dashboards** (10 min)
   - Batch find/replace bright_white → bold
   - Unified borders
   
4. **Test** (5 min)
   - Quick visual check
   - Compare to htop aesthetic

---

**Soli Deo Gloria** ✝️

"Clean, minimal, terminal-native - not flashy GUI"
