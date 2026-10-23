---
name: spryx-task-follow-ups
description: Review Spryx follow-up tasks, create requested reminders and apply confirmed edits or completion changes. Use for overdue-work reviews, task planning and managing CRM-linked to-dos.
---

# Manage task follow-ups

1. Call `tasks_find` for the requested scope. Default to `assignee: "me"` and
   `status: "open"`; use `overdue: true` for overdue work or `due_from` and
   `due_before` for a requested period. Dates need an explicit timezone offset;
   clarify ambiguous dates/timezones rather than inventing a deadline.
2. Follow returned cursors within the agreed scope. Summarize actual titles,
   owners, deadlines and linked records. Call `task_read` for a selected task
   before proposing edits or completion, to obtain its current state and version.
3. Draft a prioritized plan. A plan alone authorizes no writes. Tasks are to-dos,
   not calendar events, and this skill does not send customer follow-up messages.

## Create a requested task

For an explicit creation request, call `task_save` without `task_id`, with a
concrete `title` and a fresh `idempotency_key`. Reuse that key only for the same
creation attempt and unchanged payload. New tasks default to the connected
member unless the user names other assignees. Include `due_at` or `record_ids`
only when requested and known; never fabricate a record link.

If creation is only a suggestion, ask whether the user wants it created first.
Read back the returned task with `task_read` and report its actual saved fields.

## Confirm changes to existing tasks

Before **every** edit, completion or reopening, show the task's title and ID,
current relevant fields, and exact proposed changes. Wait for explicit
confirmation of that preview, independently of the server's annotations.

- Edit with `task_save`, providing `task_id` and the latest `version` as
  `expected_version`. Send only intended changes. `assignees` and `record_ids`
  replace their lists; show the entire proposed replacement before confirmation.
- `due_at: null` clears a deadline; omitting it preserves it. Make that distinction
  clear in the preview. Do not turn "next week" into a specific date silently.
- Complete with `task_complete` and `done: true`; reopen with `done: false`.
- After approval, check the task again if it may have changed. If the material
  state differs, revise the preview and obtain confirmation again. A version
  conflict requires a fresh read and decision, not an automatic overwrite.
- For multiple tasks, preview the full set and exact changes, then ask for
  confirmation before applying them. There is no assumed atomic batch operation.

After each write, call `task_read` and verify the saved state. Report successful,
failed and uncertain items separately; never claim total success without checking
all results. Keep proposed, approved and verified actions distinct.

## Recovery and boundaries

After an uncertain write, call `task_read` before considering a retry. If creation
failed without returning an ID, use `tasks_find` with the title/search and
assignee to check for an already created task; do not create a duplicate blindly.
If the result remains unclear, stop and ask how the user wants to proceed.
Never automatically resend a customer message.

For no matches, report the applied filters and offer to broaden them. For missing
task permissions, a missing feature or an unavailable scope, explain the blocked
operation and direct the user to the workspace administrator or host connection
UI. Do not bypass the connected workspace. No task deletion tool is available;
never substitute completion or archival for deletion, and never promise that
archiving a view is reversible.
