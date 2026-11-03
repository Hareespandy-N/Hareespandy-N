# Engineering case studies

These are **public-safe, general descriptions** of engineering approaches, not employer source releases or certified performance reports. They describe relevant work and technical interests without exposing customer identity or site details.

## 01 · AMR task execution and station coordination

**The problem:** A factory AMR mission is more than point-to-point navigation. It must coordinate approach points, equipment readiness, load handling, sensors, charging and recovery without losing track of state.

**Engineering approach:** Model actions as explicit stages with prerequisites and feedback. Separate navigation completion from equipment handshakes. Make abnormal states visible to the orchestration and operator layers.

**Engineering themes:** Python/C++, SEER API integration, multi-step mission logic, hardware I/O, commissioning, diagnostics.

**What to verify:** Station position tolerances, feedback timing, blocked transitions, safe recoveries and reproducibility across payloads.

## 02 · Fleet operations and diagnostic tooling

**The problem:** Multi-AMR operations become hard to debug when an API timeout, rejected state transition and truly offline robot all look the same.

**Engineering approach:** Distinguish HTTP reachability, robot/controller status, preview outcomes and apply results. Preserve backend rejection details rather than silently bypassing them.

**Engineering themes:** Networked services, REST/TCP, Python, PowerShell, structured reporting, operational observability.

**What to verify:** Correctness of each state classification, race conditions, per-robot error details and rollback readiness.

## 03 · Localization, sensing and precision docking

**The problem:** Real-world reflective surfaces, sensor ambiguity, payload variation and caster behavior can make robot alignment less repeatable than expected.

**Engineering approach:** Use LiDAR, RGB-D and coded position feedback appropriately, track error sources separately, and evaluate tuning changes against measured results rather than target numbers alone.

**Engineering themes:** Localization, differential-drive motion, docking, vision assistance, repeatability tests.

**What to verify:** Independent position measurement, angle error, payload sensitivity and performance near obstacles. No specific accuracy guarantee is claimed.

## 04 · Industrial robotics and connected production

**The problem:** Material movement involves storage, transport, robot manipulation and control systems that must agree on equipment state.

**Engineering approach:** Define clear request / ready / busy / complete / fault handshakes across ASRS concepts, AMRs, cobots and PLC/SCADA interfaces. Test unknown and fault states explicitly.

**Engineering themes:** Industrial robotics integration, ASRS, cobot workflows, PLC/SCADA, machine I/O and operator feedback.

**Scope note:** This section illustrates engineering focus across these domains, not a claim that a specific customer ASRS or cobot project was delivered.

---

### Evidence policy

Project metrics, customer names, screenshots, runtime logs and source are published only when verified and approved for public disclosure. No proprietary artifacts are included.
