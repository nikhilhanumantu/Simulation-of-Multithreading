---
name: ThreadLab Simulation Engine
colors:
  surface: '#f9f9ff'
  surface-dim: '#cfdaf2'
  surface-bright: '#f9f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f0f3ff'
  surface-container: '#e7eeff'
  surface-container-high: '#dee8ff'
  surface-container-highest: '#d8e3fb'
  on-surface: '#111c2d'
  on-surface-variant: '#434655'
  inverse-surface: '#263143'
  inverse-on-surface: '#ecf1ff'
  outline: '#737686'
  outline-variant: '#c3c6d7'
  surface-tint: '#0053db'
  primary: '#004ac6'
  on-primary: '#ffffff'
  primary-container: '#2563eb'
  on-primary-container: '#eeefff'
  inverse-primary: '#b4c5ff'
  secondary: '#6b38d4'
  on-secondary: '#ffffff'
  secondary-container: '#8455ef'
  on-secondary-container: '#fffbff'
  tertiary: '#5d41ab'
  on-tertiary: '#ffffff'
  tertiary-container: '#765ac5'
  on-tertiary-container: '#f5edff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dbe1ff'
  primary-fixed-dim: '#b4c5ff'
  on-primary-fixed: '#00174b'
  on-primary-fixed-variant: '#003ea8'
  secondary-fixed: '#e9ddff'
  secondary-fixed-dim: '#d0bcff'
  on-secondary-fixed: '#23005c'
  on-secondary-fixed-variant: '#5516be'
  tertiary-fixed: '#e8ddff'
  tertiary-fixed-dim: '#cebdff'
  on-tertiary-fixed: '#21005e'
  on-tertiary-fixed-variant: '#4f319c'
  background: '#f9f9ff'
  on-background: '#111c2d'
  surface-variant: '#d8e3fb'
typography:
  display:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.02em
  display-mobile:
    fontFamily: Inter
    fontSize: 26px
    fontWeight: '700'
    lineHeight: 34px
    letterSpacing: -0.01em
  headline-lg:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.015em
  headline-md:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
    letterSpacing: -0.01em
  headline-sm:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '600'
    lineHeight: 24px
    letterSpacing: -0.005em
  body-lg:
    fontFamily: Inter
    fontSize: 15px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 20px
  body-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 18px
  label-mono:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
  counter-mono:
    fontFamily: JetBrains Mono
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 24px
  status-badge:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: '600'
    lineHeight: 14px
    letterSpacing: 0.02em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 1rem
  gutter-desktop: 1.5rem
  margin: 1rem
  margin-desktop: 2rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 0.75rem
  space-lg: 1.25rem
  space-xl: 1.75rem
  space-2xl: 2.5rem
---

## Brand & Style

This design system establishes a high-precision, technical educational interface engineered specifically for computer science students, educators, and systems engineers simulating concurrent processing, scheduling algorithms, and synchronization primitives. 

The aesthetic marries high-tech developer tooling with approachable pedagogical clarity. The emotional atmosphere is calm, cerebral, and rigorously structured: visual noise is eliminated in favor of clean information grouping, translucent lavender/blue boundaries, vibrant chromatic state representations, and tactile control interfaces.

### Core Visual Principles
- **Atmospheric Clarity (Strict Light Mode):** Built entirely around high-luminance, ultra-low-strain surfaces (#F7F9FF backdrop paired with pure #FFFFFF container surfaces). Dark mode is strictly excluded to maintain consistent educational readability, presentation fidelity, and diagrammatic contrast.
- **Structural Luminance:** Containers use delicate lavender-blue borders (`#E0E7FF` / `#EEF2F6`) paired with diffused, indigo-tinted elevation shadows, creating soft separation without harsh contrast.
- **Semantic State Vibrancy:** Operating system states (Running, Ready, Blocked, Terminated, Critical/Deadlock) are communicated via hyper-legible, vivid chromatic badges, glowing telemetry pills, and dynamic timeline bars.
- **Instrument Precision:** Data readouts, Gantt segments, resource graphs, and memory register displays use monospaced numerals, crisp geometric icons, and fluid responsive tracks.

## Colors

The palette balances authoritative brand blues with pedagogical violet accents and definitive OS telemetry states.

### Palette Architecture
- **Canvas & Surfaces:**
  - `canvas-base`: `#F7F9FF` — Subtly tinted cool-blue canvas, preventing screen glare while framing white panels.
  - `surface-card`: `#FFFFFF` — Pure white for interactive containers, panels, and data surfaces.
  - `surface-subtle`: `#F1F5FD` — Elevated inner tiles, inactive tabs, and table header rows.
  - `surface-hover`: `#EDF2FE` — Interactive row and button secondary hover target.

- **Borders & Dividers:**
  - `border-subtle`: `#EEF2F6` — Faint baseline separators and interior card partitions.
  - `border-card`: `#E0E7FF` — Soft lavender-blue defining bounding boxes for primary cards and widgets.
  - `border-active`: `#C7D2FE` — Focused inputs, active tabs, and highlighted Gantt intervals.

- **Primary & Secondary Spectrum:**
  - `primary`: `#2563EB` — Core interactions, selected navigation items, primary call-to-action buttons.
  - `primary-hover`: `#1D4ED8` — Active/pressed states for primary actions.
  - `primary-subtle`: `#EFF6FF` — Primary badge backdrops, highlighted execution lanes.
  - `secondary`: `#8B5CF6` — Accent modules, secondary action buttons, synchronization triggers.
  - `accent-violet`: `#A78BFA` — Supporting data visualizations, execution timelines, secondary thread nodes.

- **System & Thread Telemetry States:**
  - **Running / Safe:** `#16A34A` (Background: `#DCFCE7`, Border: `#86EFAC`)
  - **Ready / Queued:** `#2563EB` (Background: `#EFF6FF`, Border: `#BFDBFE`)
  - **Blocked / Waiting:** `#F59E0B` (Background: `#FEF3C7`, Border: `#FDE68A`)
  - **Deadlock / Danger:** `#EF4444` (Background: `#FEE2E2`, Border: `#FCA5A5`)
  - **Terminated / Idle:** `#64748B` (Background: `#F1F5F9`, Border: `#CBD5E1`)

- **Typography & Neutrals:**
  - `text-primary`: `#1E293B` — Dominant titles, critical numbers, table text.
  - `text-secondary`: `#475569` — Section labels, descriptions, and passive metadata.
  - `text-tertiary`: `#94A3B8` — Placeholders, inactive icons, auxiliary timestamps.

## Typography

The typography leverages **Inter** for clean, legible interface text and **JetBrains Mono** for machine-level execution metrics, timeline counters, and memory registers.

### Type Hierarchy Usage
- **Display & Section Titles:** Rendered in `Inter` Bold (`display`, `headline-lg`) with tight tracking to anchor major dashboards (e.g., "Thread Manager", "CPU Scheduling").
- **Card & Module Headers:** Handled by `headline-md` and `headline-sm` with semi-bold weights for rapid contextual scanning.
- **Metrics & Machine Values:** All process counts, iteration IDs, CPU quantum values, burst metrics, and cycle timestamps utilize `JetBrains Mono` (`label-mono`, `counter-mono`). This ensures numerical columns and Gantt tick intervals align precisely across tabular rows.
- **Pills & Status Indicators:** Rendered in `status-badge` using uppercase or title-case text with slight positive tracking (+0.02em) to ensure immediate decipherability at small scale.

## Layout & Spacing

The layout is arranged around a persistent high-density application shell consisting of an interactive lateral navigation bar and a responsive 12-column grid.

### Grid & Breakpoints
- **Desktop (>= 1280px):** 
  - Fixed 240px lateral navigation rail.
  - Fluid multi-column workspace with `margin-desktop` (2rem) and `gutter-desktop` (1.5rem).
  - Main simulation layouts support 2-column or 3-column data-pane splits (e.g., Configuration Panel: 4 cols; Live Visualization: 8 cols).
- **Tablet (768px – 1279px):**
  - Collapsed 72px icon-only navigation bar.
  - 8-column layout with 1.25rem gutters.
  - Multi-pane simulators stack into 2-tier stacked views (Controls top, Visualization bottom).
- **Mobile (< 768px):**
  - Off-canvas drawer navigation.
  - 4-column single-column flow with 1rem margins.
  - Simulation boards expose horizontally scrollable Gantt timelines and state diagrams with pinned telemetry summaries.

### Spacing Principles
Internal component padding enforces systematic density: cards employ `space-lg` (1.25rem) to preserve expansive breathing room around dense telemetry data, while interactive pill buttons, inputs, and list rows maintain tight, click-target-efficient rhythms using `space-sm` (0.5rem) and `space-md` (0.75rem).

## Elevation & Depth

Visual hierarchy relies on soft, chromatic elevation rather than stark heavy dropshadows. Surfaces simulate subtle levitation over the `#F7F9FF` background.

### Elevation Architecture
- **Layer 0 (Canvas):** `#F7F9FF` base plane.
- **Layer 1 (Card Standard):** Pure `#FFFFFF` fill with border `1px solid #E0E7FF` and an ambient glow shadow:
  - `box-shadow: 0 4px 16px -2px rgba(37, 99, 235, 0.05), 0 2px 6px -1px rgba(139, 92, 246, 0.04);`
- **Layer 2 (Interactive Floating Modules / Hovered Cards):**
  - `box-shadow: 0 10px 25px -4px rgba(37, 99, 235, 0.08), 0 4px 12px -2px rgba(139, 92, 246, 0.06);`
  - Subtle upward translateY (-1.5px) transition.
- **Layer 3 (Modals, Overlays, and Tooltips):**
  - `box-shadow: 0 20px 35px -5px rgba(30, 41, 59, 0.12), 0 10px 15px -3px rgba(37, 99, 235, 0.06);`
  - Paired with soft lavender backdrop blur: `backdrop-filter: blur(8px); background: rgba(247, 249, 255, 0.7);`

### Glow Highlights
Active simulation elements (e.g., executing threads, semaphore unlocks, active deadlock warnings) utilize soft directional outer glows:
- Running Thread Glow: `box-shadow: 0 0 12px 2px rgba(22, 163, 74, 0.2);`
- Deadlock Warning Alert Glow: `box-shadow: 0 0 14px 3px rgba(239, 68, 68, 0.22);`
- Active Quantum Gantt Bar: `box-shadow: 0 2px 8px 0 rgba(37, 99, 235, 0.3);`

## Shapes

The design system employs a refined radius scale of 12px to 18px (`roundedness: 2`), balancing software utility with modern visual warmth.

### Geometry Hierarchy
- **Cards & Data Modules:** `14px` to `16px` border radius (`rounded-lg`). Provides balanced separation while accommodating internal charts and lists.
- **Buttons & Control Inputs:** `10px` to `12px` border radius (`rounded-md`). Consistent, tactile form factors for form fields, run buttons, and numeric inputs.
- **Badges, Status Indicators, and Timeline Pills:** Full pill radius (`9999px`). High-contrast capsule shape distinguishes state indicators (Running, Ready, Blocked) from square-format card modules.
- **Gantt Chart Blocks:** `8px` corner radius. Softens raw horizontal timeline bars while retaining clear segment cutoffs.

## Components

### 1. Navigation Sidebar
- **Container:** Pure `#FFFFFF` sidebar with `border-right: 1px solid #E0E7FF`.
- **Navigation Items:** Height `40px`, border radius `10px`, typography `13px / 500`.
- **Inactive State:** Text `#475569`, transparent background. On hover: text `#2563EB`, background `#EFF6FF`.
- **Active State:** Solid gradient `linear-gradient(135deg, #2563EB, #1D4ED8)` with text `#FFFFFF` and soft blue shadow `0 4px 10px rgba(37, 99, 235, 0.25)`. Includes an active right-edge indicator or inset icon glow.

### 2. Buttons & Simulation Controls
- **Primary Action (Run / Execute / Create):**
  - Background: Gradient `linear-gradient(135deg, #2563EB, #1D4ED8)`.
  - Radius: `10px` to `12px`. Padding: `0.5rem 1.25rem`. Text: White `#FFFFFF`, `Inter 600`.
  - Box Shadow: `0 4px 12px rgba(37, 99, 235, 0.25)`.
- **Secondary / Action Tooling (Step, Reset, Pause):**
  - Background: `#FFFFFF`. Border: `1px solid #E0E7FF`. Text: `#1E293B`.
  - Hover: Background `#F1F5FD`, border `#C7D2FE`, text `#2563EB`.
- **Accent Action (Secondary Lab Features / Mutex Locks):**
  - Background: Gradient `linear-gradient(135deg, #8B5CF6, #7C3AED)`.
  - Box Shadow: `0 4px 12px rgba(139, 92, 246, 0.25)`.

### 3. Status Badges & Glow Pills
- **Badge Anatomy:** Capsule border radius (`9999px`), padding `3px 10px`, typography `11px / 600` uppercase/title.
- **Running:** Text `#15803D`, background `#DCFCE7`, border `1px solid #86EFAC`. Features a `6px` pulsing emerald circle marker.
- **Ready:** Text `#1D4ED8`, background `#EFF6FF`, border `1px solid #BFDBFE`.
- **Blocked:** Text `#B45309`, background `#FEF3C7`, border `1px solid #FDE68A`.
- **Terminated:** Text `#475569`, background `#F1F5F9`, border `1px solid #CBD5E1`.
- **Deadlock Alert:** Text `#B91C1C`, background `#FEE2E2`, border `1px solid #FCA5A5`, outer glow animation.

### 4. Interactive Simulation Cards
- **Base Style:** Background `#FFFFFF`, border `1px solid #E0E7FF`, border radius `16px`, padding `1.25rem`.
- **Header:** Features an icon badge (40x40px, rounded-10px, background `#EFF6FF` or `#F3E8FF`), title in `headline-sm`, and secondary action buttons or pill stats.
- **Divider:** Light `#EEF2F6` hairline rule between configuration inputs and simulation canvas.

### 5. Inputs & Form Selectors
- **Fields:** Height `38px`, background `#FFFFFF`, border `1px solid #E0E7FF`, border radius `10px`, typography `JetBrains Mono 13px`.
- **Focus:** Border color `#2563EB`, outer ring `3px rgba(37, 99, 235, 0.15)`, smooth 150ms transition.
- **Toggles / Segmented Controls:** Pill container with `#F1F5FD` background, active segment slides with white card surface and `0 2px 6px rgba(0,0,0,0.06)` shadow.

### 6. Gantt Charts & Execution Timelines
- **Timeline Canvas:** Background `#F8FAFC`, border `1px solid #E2E8F0`, rounded `12px`, padding `12px`.
- **Gantt Blocks:** Height `32px`, border-radius `6px`, text `#FFFFFF`, font `JetBrains Mono 11px / 600`.
- **Color by Thread:**
  - Thread 1 (T1): `#2563EB`
  - Thread 2 (T2): `#10B981`
  - Thread 3 (T3): `#F59E0B`
  - Thread 4 (T4): `#8B5CF6`
- **Time Mark Ticks:** Monospaced label (`label-mono`) at each quantum interval with vertical faint guides `#E2E8F0`.

### 7. Resource Allocation Graphs (RAG) & Process Nodes
- **Process Node (Circles):** 48px circle, `#EFF6FF` fill, `2px solid #2563EB` border, typography `JetBrains Mono 14px / 700`.
- **Resource Node (Squares):** 44px square with `10px` rounded corners, `#F0FDF4` fill, `2px solid #16A34A` border.
- **Vectors / Arrows:** Directed bezier arrows; allocated arrows in solid `#2563EB`, request arrows in animated dashed `#8B5CF6`, deadlock loop highlights in pulsating `#EF4444`.