# Agent Dispatch

Use subagents only when the user explicitly allows delegation or asks to dispatch agents.

## Dispatch Principles

- Delegate bounded sidecar tasks.
- Keep immediate blocking work local.
- Avoid duplicate work.
- Give clear ownership.
- Ask workers not to revert or overwrite others' work.
- Integrate and QA in the main agent.

## Suggested Splits

### Strategy Agent

Owns market diagnosis, offer architecture, objections, mechanism, and positioning.

### Copy Agent

Owns sales copy, ad copy, email copy, and VSL narrative.

### Visual Agent

Owns design resolver, image prompts, asset sequencing, and visual QA notes.

### Build Agent

Owns HTML/CSS pages, scripts, dashboard implementation, and manifest wiring.

### QA Agent

Owns broken links, missing files, PDF/deck/dashboard checks, mobile overflow, and placeholder scans.

## When Not To Dispatch

Do not dispatch if:

- the task is tiny
- the next step is blocked on the answer
- the output requires tight single-threaded judgment
- the user has not allowed agents

