---
name: spryx-get-started
description: Check the Spryx connection with read-only requests and introduce CRM, inbox and task workflows. Use after installation or when the user asks how to start using Spryx in chat.
---

# Get started with Spryx

Use only `objects_list` and `tasks_find` in this onboarding workflow.

1. Explain that Spryx connects this assistant to the one workspace selected
   during OAuth sign-in. Access follows the connected member's role and approved
   permissions. The connection can support writes; this setup check is read-only.
2. Call `objects_list` with `limit: 5` to discover accessible CRM objects. Use
   returned names and IDs; do not infer an organization name from an object name.
3. Call `tasks_find` with `assignee: "me"`, `status: "open"`, `limit: 5` to check
   task access. Report a small sample, without exposing unnecessary customer data.
4. State which checks succeeded. Empty successful results mean no matching data,
   not a failed connection. A successful object check does not prove inbox access.
5. Explain the available workflows: inbox triage, pipeline and List summaries,
   account briefs, and task follow-ups. Calendar reading and scheduling,
   permanent contact deletion, and payments are unavailable.
6. Suggest these three first prompts:
   - "Show my open conversations waiting for a reply and suggest next steps."
   - "Review my pipeline and highlight work that needs attention."
   - "Show my overdue tasks and draft a follow-up plan."

If authentication is missing or expired, ask the user to connect or reauthorize
Spryx through the host's connection UI. Never ask for a password, token or API key
in chat. If a tool is unavailable or returns a permission/feature error, identify
the affected check and explain that the workspace administrator or connection
permissions may need attention. Do not claim the entire connection is broken.
To use another workspace, reconnect and select an authorized workspace.

Do not create sample records or tasks to test access. Make no writes, including
batch writes, and do not retry an uncertain operation automatically. If the user
requests a mutation, finish this read-only check and use the appropriate workflow;
show the exact proposed change and obtain explicit confirmation before changing
existing state, regardless of tool annotations. Never silently replace deletion
with archival or promise that archiving a view can be reversed.
