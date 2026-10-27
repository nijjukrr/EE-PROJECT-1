# Brozer — Project Knowledge Base

**Brozer: a privacy boundary for browser agents.** A privacy-first browser agent with on-device visual perception.

---

## 1. One-Sentence Definition

Brozer is a browser agent that understands and operates websites while keeping sensitive information on the user's device whenever it isn't actually needed for the task.

## 2. Core Idea

A **browser agent** is software that looks at a webpage, decides what to do, and acts on it (clicking, filling fields, navigating) on behalf of a user who gave a plain-language instruction.

Most browser agents capture the screen and/or DOM and send the **entire context** to a large reasoning model, often hosted externally. A real page mixes task-relevant information (button locations, field purposes) with irrelevant private information (emails, passwords, balances, messages). Sending everything is an unnecessary privacy exposure — not because the AI is malicious, but because more data leaves the device than the task requires.

Brozer changes the order of operations: instead of "capture everything, then think," it does **"perceive locally, protect locally, then think with only what is needed."**

### The Six-Stage Pipeline

`PERCEIVE → DETECT → SANITIZE → REASON → POLICY CHECK → ACT`

| Stage | Meaning |
|---|---|
| Perceive | Read the page |
| Detect | Find sensitive data |
| Sanitize | Redact / mask |
| Reason | AI decides action |
| Policy check | Validate action |
| Act | Execute in browser |

Every request passes through all six stages, in order, every time.

### Brozer is NOT
- A chatbot that happens to control a browser — the privacy boundary is the actual product.
- Just an OCR or PII detector — detection is one stage of a larger pipeline.
- A system where every AI computation must run on a laptop — heavier reasoning can run on a server or shared machine, as long as it only receives sanitized context.
- A replacement for browser or OS security — it is an additional privacy layer built for agent-driven browsing.

### Brozer IS
- A browser-agent architecture with a local, testable privacy boundary.
- A combination of on-device perception, sensitive-data detection, sanitization, AI reasoning, and policy-gated execution.
- Aligned with an "on-device" and "lightweight" design direction.

## 3. Open-Source Foundation: WebBrain

Brozer is built on **WebBrain**, an existing open-source browser-agent project. WebBrain already provides browser integration, page observation, and agent-driven action execution. Brozer's own contribution is the privacy layer wrapped around WebBrain's agent loop:

- Local perception tuned for sensitive-data awareness
- Privacy/PII detection engine
- Sanitization
- Policy-gated execution boundary

## 4. Perception and Privacy Together

On-device perception means the part that looks at and understands the page runs on the user's machine rather than depending on a heavy remote model, using lightweight techniques a modest computer can run. The same local processing step that lets the agent understand the page without a heavy remote vision model also keeps sensitive information from leaving the device.

**Why visual perception matters:** a page is not only its HTML/DOM. Some information is only meaningful visually — form layout, icons without labels, photos, highlighted warning colours. A DOM-only agent can miss this.

## 5. Why Ordinary Browser Agents Create a Privacy Problem

Agents may operate on email inboxes, banking dashboards, college portals, HR tools, healthcare forms, or internal enterprise systems. The agent needs enough context to understand controls and page state, but the page may also display information it has no need to know.

| Page contains | Agent may need | Agent should NOT need |
|---|---|---|
| Email address | Where the email field is | The actual email value |
| Password field | That a password field exists | The password itself |
| Payment page | Which control confirms the task | CVV / full card details |
| Profile page | Where an "edit" control is | Unrelated personal details |
| Face / photo | Relevant visual layout | Identity of the person shown |

### Privacy Principle
Send the **minimum context required for reasoning**. Sensitive values not necessary for the requested action should be removed, masked, or replaced with a semantic placeholder before they leave the trusted local side.

### Raw vs. Protected Context

| Raw page context (never sent as-is) | Protected context (what gets sent) |
|---|---|
| `Email: user@example.com` | `Email: [EMAIL]` |
| `Password: hunter2` | `Password: [PASSWORD]` |
| `[ LOGIN ]` | `[ LOGIN ]` |

The model can still infer that a login form and a Login control exist. Actual values stay local and are only used there — e.g., for local, user-authorized autofill.

### Why This Matters
- Reduces unnecessary exposure of personal and sensitive information to external systems.
- Makes privacy part of the pipeline instead of an afterthought.
- Allows powerful server-side reasoning without exposing every raw detail on screen.
- Creates a privacy boundary that can be tested and measured, not just claimed.

## 6. System Overview and Trust Boundary

Brozer has two sides separated by a **privacy trust boundary**:

- **Trusted local side:** browser + extension, screen/DOM capture, local perception, sensitive-data detection, sanitization, policy engine, action validation, browser automation, local sensitive-value handling, final execution.
- **Network / reasoning side:** receives **sanitized context only** (e.g., server-side VLM reasoning) and returns a structured action.

Only sanitized context and structured actions cross the boundary.

### Request Walkthrough

| Step | What happens | Where |
|---|---|---|
| 1 | User gives a plain-language instruction | Browser |
| 2 | Webpage observed via screen and/or DOM context | Local |
| 3 | Sensitive regions and values identified | Local |
| 4 | Context masked, blurred, redacted, or tokenized | Local |
| 5 | Only protected context transmitted | Network |
| 6 | AI reasons over protected context, produces structured command | Server |
| 7 | Command checked against local policy rules | Local |
| 8 | Approved action executed in browser | Local |

### What Stays Strictly Local
- Raw screen and DOM content before sanitization
- Critical secrets: passwords, OTPs, CVV codes, authentication tokens, session identifiers
- The decision logic that determines what may cross the boundary
- Final execution of any browser action

### What May Cross the Boundary (after sanitization)
- Semantic, redacted, or tokenized context describing page structure and task-relevant controls
- The user's plain-language instruction
- The structured action returned by the reasoning model (re-validated locally before execution)

### Rule: No Module May Bypass the Boundary
Every network request must pass through sanitization and policy. Every AI-generated action must pass through the local policy gate before execution. This applies to all modules equally.

## 7. Full Workflow (10 Steps)

1. The browser extension observes the relevant webpage.
2. Local perception extracts page context using DOM information and, when required, lightweight visual information.
3. A local privacy engine detects sensitive information (PII, credentials, tokens, financial data).
4. Sensitive information is redacted, masked, blurred, tokenized, or blocked according to policy.
5. Only permitted, sanitized context is provided to the reasoning component.
6. The AI reasoning layer determines the next browser action.
7. The AI does not receive unrestricted ability to execute arbitrary code.
8. The proposed action is a structured action (click, type, scroll, navigate).
9. A policy / action-validation layer checks whether the action is allowed.
10. The extension executes the permitted action locally.

**Key principle:** the reasoning system receives the minimum useful information for the task, not raw private browser content by default.

## 8. Browser Extension Architecture

The extension is the user's local control point, connecting the webpage, privacy layer, AI reasoning service, and action executor.

| Module | Responsibility |
|---|---|
| Extension UI | Start/stop the agent, show privacy state, approvals, errors |
| Page observer | Collect relevant DOM information and/or screen context |
| Local perception | Understand visible UI elements and relevant visual regions |
| Privacy engine | Detect sensitive content and decide how to sanitize it |
| Policy engine | Decide what may be transmitted and which actions may run |
| Action executor | Perform approved click, scroll, select, type, or related actions |

**Browser-native information is valuable:** the browser exposes input types, labels, accessible names, buttons, and links. E.g., an input with `type="password"` can be classified high-risk before any visual analysis runs. Visual perception and DOM structure are complementary signals.

### The Five Architectural Layers
1. **Browser Extension** — integration, content scripts, background worker, agent UI, permissions
2. **Local Perception** — DOM extraction, lightweight visual perception, element/region detection
3. **Privacy Engine** — PII detection, rule/ML detection, sanitization, policy decisions
4. **Reasoning Engine** — receives sanitized context, returns structured actions only
5. **Policy + Execution Gate** — validates and executes only approved actions

## 9. Local Perception

Turns a raw webpage into a structured representation of "what is on this page and what can be done with it," without sending the raw page anywhere.

**Covers:**
- DOM extraction first — structured, fast, precise where the page has good semantics
- Lightweight visual perception when DOM alone is insufficient
- Screenshot / visual context when useful
- Element and region detection, with bounding boxes and confidence scores

**DOM alone is not enough:** icons without labels, layout cues, images, and pages with generic markup hide real structure. DOM = speed and precision; vision = everything else.

**Lightweight by design:** not every laptop has a GPU. Perception is built around a **CPU/WebAssembly baseline**, with **WebGPU only as optional acceleration**.

## 10. Local Privacy Engine

The component that makes Brozer privacy-focused. It decides what can safely leave the device while preserving enough context for the agent to keep working.

### Detection Signals

| Signal | Example | Why it helps |
|---|---|---|
| DOM | `type="password"` | Strong semantic indication of sensitive data |
| Pattern matching | Email / phone / card-like pattern | Fast detection of common structured PII |
| Text semantics | "name", "address", "OTP", "CVV" labels | Adds meaning beyond raw patterns |
| Visual detection | Face, document, sensitive region | Catches info not cleanly in the DOM |
| Context | Label positioned near an input | Distinguishes similar-looking fields |

### Sanitization Options
- **Redact** — replace with a placeholder such as `[REDACTED]`
- **Mask** — hide the value while preserving region and layout
- **Blur** — for visual info such as faces or photos
- **Semantic replacement** — `[EMAIL]`, `[PHONE]`, `[PASSWORD]`, etc., preserving structure
- **Block** — prevent critical information from crossing the boundary at all

### Risk Tiers

| Level | Examples | Default treatment |
|---|---|---|
| Critical | Password, OTP, CVV, auth token | Never send raw value; local-only handling |
| Sensitive | Email, phone, address, identity data | Redact / mask / tokenize unless required |
| Contextual | Ordinary page text or controls | May be sent when needed for reasoning |

## 11. AI Reasoning and Structured Actions

The privacy layer doesn't replace the agent — it makes it safer. The reasoning component interprets the instruction, understands the sanitized page, decides the next action, and returns it in a predictable structured form rather than free-form code.

### Worked Example: "Find Submit and click it"

| Stage | What happens |
|---|---|
| Raw webpage | Contains all visible content, including private info |
| Protected context | Relevant controls remain; sensitive content replaced or hidden |
| AI reasoning | Model determines 'Submit' is the target |
| Structured action | `click(target="submit_button")` |
| Local policy check | Browser verifies the action is allowed |
| Execution | Extension performs the approved click |

**Why structured actions, not free-form code:** the model returns a command like `{"action":"click","target":"submit_button"}` rather than getting unconditional browser control or the ability to run arbitrary generated code. The local side can inspect and validate it first.

**Sensitive form filling:** the AI can identify that an email or password field exists without receiving its value. If the user explicitly authorized local autofill, the extension inserts the real value locally.

> The AI decides *where and what* to act on. The local system decides *whether* the action is allowed, and with what (if any) sensitive data.

## 12. Policy Gate and Execution

Every structured action from the reasoning model passes through a local policy gate before execution. It is the last line of defence and runs entirely locally.

| Outcome | Meaning |
|---|---|
| ALLOW | Action and context are safe under current rules |
| REDACT | Transform sensitive information further before transmission |
| BLOCK | Do not transmit the context or execute the operation |
| ASK USER | Pause for explicit confirmation when risk is high or confidence is low |

The gate checks the action's type, target element, and parameters against policy rules. High-risk or low-confidence actions are escalated to the user rather than executed silently.

## 13. Tech Stack (Free / Open-Source)

No paid API is required for the MVP to work end-to-end.

| Layer | Technology / approach | Purpose |
|---|---|---|
| Browser agent base | WebBrain (open-source) | Agent loop: observation, action execution, extension scaffolding |
| Browser extension | TypeScript + React + Vite | Extension UI, orchestration, build tooling |
| Browser integration | WebExtension APIs (Manifest V3) | Page/DOM access and browser operations |
| Local ML runtime | ONNX Runtime Web | Run lightweight ML models in the browser |
| Acceleration (optional) | WebGPU | GPU acceleration for local inference when present |
| Baseline execution | WebAssembly / CPU | Guaranteed fallback without a GPU |
| Privacy detection | TypeScript rule/regex engine + lightweight NER/visual model | Combine multiple signals to find sensitive content |
| Backend | Node.js + Express (or lightweight HTTP API) | Receive sanitized context, coordinate reasoning |
| Reasoning | Open local model via Ollama, or shared machine on LAN | Interpret protected context, generate structured actions |
| Testing | Playwright, unit and integration tests | Verify detection, redaction, policy, end-to-end behaviour |
| Version control | Git + GitHub | Collaboration and history |
| Storage | Local storage / config / JSON files | Avoid a database for the MVP unless necessary |

### Feasibility Notes
- Browser-side perception runs on WASM/CPU by default; WebGPU is never required.
- Local reasoning can use an open model served through Ollama.
- If a model is too heavy for every laptop, one stronger machine can host it and serve others over LAN.
- A deterministic/mock reasoning layer can stand in during early development so other modules can be built in parallel.
- No expensive cloud infrastructure needed; a laptop-class machine can develop, test, and demo the full pipeline.

## 14. Team Roles (Team of Six)

### Member 1 — Browser Extension & WebBrain Integration
- Set up/maintain the WebBrain fork; identify hook points for perception, privacy, and policy.
- Own extension architecture: manifest, content scripts, service worker, message passing.
- Implement the **action executor** (performs approved click/type/scroll/select/navigate).
- Handle least-privilege permission scoping.
- Maintain compatibility with upstream WebBrain; document local modifications.
- **Deliverables:** extension shell loading WebBrain's loop; action-executor module with documented interface; reviewed permission manifest; integration notes.
- **Skills:** TypeScript, WebExtension APIs (MV3), Git (forks/rebasing), React/Vite.

### Member 2 — Local Perception
- DOM extraction: walk accessibility tree/DOM for elements, labels, input types, positions.
- Lightweight visual perception for icons without labels, layout cues, photos/documents.
- Integrate ONNX Runtime Web (CPU/WASM baseline, opportunistic WebGPU).
- Own the **PageContext** contract (fields, per-element confidence, versioning).
- Ensure perception output carries signals the privacy engine needs.
- Benchmark latency and memory/CPU use on a modest laptop.
- **Deliverables:** DOM extraction module producing PageContext; visual perception path with measured CPU latency; documented schema.
- **Skills:** JS/TS DOM APIs, ONNX Runtime Web, small vision/OCR model docs.

### Member 3 — Privacy / Security Engine
- Rule/regex detection for emails, phones, card-like patterns.
- Lightweight NER/ML or visual detector for names, addresses, faces, documents.
- Combine DOM, pattern, and semantic/visual signals into one confidence score using the Critical / Sensitive / Contextual tiers.
- Implement redact, mask, blur, semantic replacement, and block.
- Own the **SanitizedContext** contract.
- Design adversarial test cases with Member 6 (misleading labels, hidden fields, odd layouts).
- Maintain an honest list of known detection limitations backed by test results.
- **Deliverables:** rule-based detector; sanitization pipeline with all five operations; documented schema; precision/recall from real runs.
- **Skills:** regex/pattern design, basic NLP/NER, TypeScript, writing failure-mode tests.

### Member 4 — AI / Reasoning
- Design prompting that gives the model exactly the SanitizedContext and instruction, nothing more.
- Own the **AgentAction** schema and validate every model response against it.
- Integrate a local open model via Ollama; coordinate the shared LAN reasoning machine.
- Build a deterministic/mock reasoning layer so others aren't blocked.
- Tune confidence/uncertainty signalling so the policy gate knows when to escalate.
- Keep the Node.js/Express backend simple to run locally or on the shared machine.
- **Deliverables:** reasoning service (SanitizedContext in → validated AgentAction out); mock mode; documented schema; model-choice notes.
- **Skills:** prompt design, Ollama, Node.js/Express, JSON schema validation.

### Member 5 — UI / UX
- Build the agent panel (instruction input, live status).
- Privacy indicators showing in real time what was detected and sanitized.
- Permission and confirmation UI for ASK USER outcomes.
- Pipeline progress display (perceive → detect → sanitize → reason → policy check → act).
- Present detected categories without ever displaying the raw sensitive value.
- Keep the UI uncluttered on a modest laptop screen.
- **Deliverables:** agent panel; privacy indicator UI; confirmation flow; UI able to carry the live demo end to end.
- **Skills:** React, UI/UX design sense, translating pipeline state into visuals.

### Member 6 — QA / Integration
- Co-own policy engine rules with Member 3 (category → ALLOW / REDACT / BLOCK / ASK USER).
- Build the Playwright end-to-end harness on the controlled demo page.
- Write and run adversarial/security tests (bypassing detection or policy gate, extracting secrets from payloads or logs).
- Instrument the network boundary to show raw sensitive values are absent from outgoing payloads.
- Record performance/resource metrics on a realistic, modest machine.
- Browser-compatibility testing.
- Own demo-script integration; keep demo data safe (never real secrets).
- **Deliverables:** Playwright suite; adversarial results and failure modes; latency/resource measurements; rehearsed demo script.
- **Skills:** Playwright, security-testing mindset, reading network traffic/logs, reproducibility.

### Shared Data Contracts

| Contract | Produced by | Consumed by |
|---|---|---|
| PageContext | Perception (Member 2) | Privacy engine, Reasoning |
| SanitizedContext | Privacy engine (Member 3) | Reasoning engine |
| AgentAction | Reasoning engine (Member 4) | Policy gate |
| PolicyDecision | Policy gate (Member 6 / extension) | Action executor (Member 1) |

**Rule:** no module may bypass the privacy boundary.

## 15. MVP — What We Build First

The MVP proves the core concept end-to-end on one controlled scenario. It is deliberately *not* a universal autonomous browser.

1. Open a controlled webpage.
2. User gives Brozer an instruction.
3. Brozer perceives the page locally.
4. Brozer detects defined sensitive information.
5. Brozer sanitizes it.
6. The sanitized context is shown to the user.
7. Sanitized context is sent to reasoning.
8. A structured action is received.
9. The action is validated.
10. The action is executed in the browser.
11. The result and privacy decision are shown.

**Demo scenario:** a test webpage with ordinary task information mixed with clearly fake PII-like data. The user gives a simple task, and the demo shows: raw page → local detection → sanitized context → AI reasoning → policy decision → action.

**Never use real secrets** in the demo — only clearly fake names, emails, and passwords.

## 16. What Not to Build (First)
- Universal browser automation
- Perfect website understanding
- Giant local vision-language models
- Complex cloud infrastructure
- Dozens of PII categories at once
- Unrestricted generated-JS execution
- Multi-agent orchestration without need
- Production-grade security claims

The goal is a reliable proof of the architecture, not a feature-complete product.

## 17. Implementation Roadmap

| Phase | Focus |
|---|---|
| 1 | Repository setup, extension shell, basic browser interaction, shared types/interfaces |
| 2 | DOM perception, page-context extraction, rule-based PII detection, sanitization |
| 3 | Reasoning service, structured actions, policy validation, basic UI |
| 4 | Lightweight visual perception, optional ONNX Runtime Web, better sensitive-region detection |
| 5 | Playwright tests, security tests, performance tests, browser compatibility |
| 6 | End-to-end demo, metrics, documentation, failure handling |

## 18. Security Model

Browser/local processing is the trusted privacy boundary. Raw sensitive information stays local whenever it isn't necessary for reasoning.

### Defences
- Local sanitization before any network transmission
- Least-privilege browser permissions
- Structured AI actions instead of free-form generated code
- Independent, local action validation before execution
- No arbitrary code execution by the reasoning model
- Minimal logging, with no sensitive values ever written to logs
- Confidence thresholds for detection and action decisions
- User confirmation for uncertain or high-risk actions

### Limitations (stated honestly)
No PII detector is perfect. Brozer reduces unnecessary exposure of sensitive information; it does not claim perfect detection or absolute security.

### Potential Failure Modes
- False negatives (missed data) and false positives (over-redaction)
- OCR errors when visual text recognition is used
- Dynamic pages that change after initial perception
- Hidden or deliberately misleading page content
- Adversarial pages designed to confuse detection
- Layout changes and cross-browser differences

### Mitigations
- Combine DOM, regex, and ML/visual signals rather than one detector
- Confidence thresholds with escalation of uncertain cases to the user
- Controlled, well-tested MVP scope
- Automated tests including adversarial cases, evaluated continuously

## 19. Metrics and Testing

### Metrics

| # | Metric | What it tells us |
|---|---|---|
| 1 | Visual context accuracy | Are relevant visual/page elements understood correctly? |
| 2 | PII detection precision/recall | How reliably are sensitive regions detected? |
| 3 | Redaction precision | Is sensitive info protected while useful context remains? |
| 4 | Client resource utilization | Does local inference stay lightweight? |
| 5 | End-to-end latency | Does perceive → protect → reason → act stay responsive? |
| 6 | Task completion success | Does the agent still complete the task after sanitization? |

No final numerical results exist yet; all metrics must come from actual testing before being reported.

### Test Categories
- **Unit** — individual functions (a regex rule, a sanitizer)
- **Integration** — modules together (perception → privacy engine)
- **Browser** — behaviour across supported browsers
- **End-to-end** — full instruction-to-action pipeline
- **Adversarial / security** — attempts to bypass detection or policy
- **Performance** — latency and resource use under realistic conditions

### Representative Test Questions
- Does PII get detected on a controlled test page?
- Does the original sensitive value stay absent from the outgoing reasoning payload?
- Does the sanitized page retain enough context to complete the task?
- Can the AI reliably return a valid structured action?
- Can a malicious or malformed action bypass the policy gate?
- Are secrets ever written to logs?
- Does the system work without WebGPU?
- Can it run on an 8GB RAM, no-GPU machine with a lightweight configuration?

## 20. FAQ

**Is Brozer just another browser automation tool?**
No. Automation is only the last step. Brozer's contribution is the local perception and privacy boundary that decides what the automation layer may see and do.

**Why local perception at all?**
The page must be understood before it can be sanitized. If perception were remote, the raw page would leave the device before any protection.

**Why not run the entire AI stack locally?**
Heavy reasoning models are expensive on ordinary laptops. Privacy-critical steps (perception, detection, sanitization, policy) stay local; reasoning can run on a server or shared machine on sanitized data only.

**What if the detector misses something (false negative)?**
Critical categories (passwords, OTPs, tokens) use conservative, multi-signal rules. False negatives are measured through testing, not assumed away.

**What if the detector redacts too much (false positive)?**
Confidence thresholds, combined signals, and semantic placeholders (like `[EMAIL]`) preserve structure even when the value is hidden.

**Can the AI directly execute anything?**
No. It only proposes a structured action; a separate local policy gate must approve it.

**Does the user lose control?**
No. High-risk or low-confidence actions require explicit user confirmation.

**What about unfamiliar websites?**
DOM and visual signals are combined generically, not hard-coded per site. Confidence may be lower on unfamiliar layouts, which is why thresholds and user escalation exist.

**If sensitive data is already visible on screen, isn't privacy already lost?**
Being visible to the user on their own device differs from being transmitted externally. Brozer prevents unnecessary transmission; it doesn't hide data from its owner.

**Why use both regex and ML detection?**
Regex is fast, precise, and predictable for structured data (emails, card numbers). ML/visual detection catches unstructured or visual cases. Together they cover more.

**What exactly is the trust boundary?**
The line between the local trusted side (browser, extension, perception, privacy engine, policy gate, execution) and the network/reasoning side, which only receives sanitized context.

**What if the AI tries to override the policy?**
It can't. The AI has no execution capability; the policy gate and executor are separate local components.

**Why not blur the entire screenshot?**
It would destroy the context the agent needs. Brozer targets specific sensitive regions and values.

**What does "lightweight" mean?**
Perception and detection run on CPU/WebAssembly by default, with WebGPU as optional acceleration, so ordinary laptops work without a dedicated GPU.

**Can it work without WebGPU? On basic computers?**
Yes. The CPU/WASM baseline is the design target, and a heavier reasoning model can be hosted on one shared machine over LAN.

**Is Ollama mandatory?**
No. It's one way to serve a local open model. A mock/deterministic reasoning layer works during early development, and the reasoning component is swappable.

**Does it require a paid API?**
No. Every layer has a free or local option.

**What data is stored, and where?**
Minimal: local storage/config/JSON files; no database unless necessary.

**How are secrets kept out of logs?**
Logging is minimal by default, and sensitive values are explicitly excluded from log output as a policy rule.

**How are browser differences handled?**
WebExtension-compatible APIs plus browser-compatibility testing.

**What if a malicious webpage manipulates the agent?**
Adversarial testing targets this; confidence thresholds, conservative critical-field rules, and the policy gate are the main defences.

**How do we prove it's better?**
Instrument the network boundary and show, with real measurements, that sensitive values are absent from outgoing payloads while task completion still succeeds.

**Biggest engineering risk?**
Balancing detection accuracy against latency and resource use on ordinary hardware — a heavy model may be accurate but slow; a tiny one fast but leaky.

**What's innovative?**
The privacy boundary is a first-class, testable part of the agent pipeline, not a policy statement layered on top of an existing agent.

**Strongest technical claim?**
With an inspectable network payload, raw sensitive values did not leave the device while the agent still completed a real browser task.

**Minimum demo to prove the idea?**
One controlled webpage, one real instruction, and a visible chain: raw page → sanitized context → AI action → policy decision → executed result.

**What if a feature isn't implemented yet?**
Say so directly and describe it as planned; never claim a capability the system lacks.

## 21. Impact and Scalability

- **Impact:** safer browser automation, reduced unnecessary data exposure, better user control, potentially lower bandwidth/inference overhead.
- **Scalability:** add more perception models, browser support, policy rules, and task types over time.

## 22. Limitations and Future Scope

### MVP Scope
- One controlled demo webpage and one strong end-to-end scenario
- A small, defined set of sensitive-data categories
- A local policy gate with ALLOW / REDACT / BLOCK / ASK USER outcomes
- Manual or lightly automated measurement of the listed metrics

### Planned Near-Term Improvements
- Broader sensitive-data category coverage with tuned thresholds
- Improved visual detection using additional lightweight local models
- More extensive automated adversarial and cross-browser test suites
- A refined policy-rule authoring experience

### Long-Term Vision
- A general-purpose privacy boundary layer that any browser agent can sit behind
- Support for more browsers and task types
- Continuous evaluation against new adversarial patterns

### What Brozer Does NOT Claim
Perfect PII detection, guaranteed security, or 100% privacy. It claims a **measurable reduction in unnecessary exposure** of sensitive information, backed by testing.

## 23. Summary

**Four words:** PERCEIVE (understand page locally) → PROTECT (find + sanitize sensitive data) → REASON (decide next action) → ACT (validate + execute).

**Central engineering question:** Can we make an AI browser agent useful without making the user's private webpage information unnecessarily available to the reasoning model?

**What success looks like:**
- Anyone on the team can explain the architecture without implementation details.
- The privacy boundary is understandable within seconds of seeing the diagram.
- A demo visibly shows raw context becoming protected before transmission.
- The agent completes a useful browser task after sanitization.
- Measurements — not claims — support statements about detection, redaction, resource use, and latency.
