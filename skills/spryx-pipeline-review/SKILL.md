---
name: spryx-pipeline-review
description: Summarize Spryx pipeline and List entries, stage counts and relevant history without changing data. Use for pipeline health reviews, stalled-work checks and sales-process summaries.
---

# Review pipelines and Lists

This workflow is read-only. Use `pipelines_list`, `pipeline_entries_query`,
`lists_list`, `list_entries_query` and `history_get`.

1. Establish the object and process to review. Call `lists_list` to discover Lists
   and their `parent_object_id` values. If the object ID is already available
   from the conversation, use it; otherwise use a matching returned List's parent
   object or ask the user for the object ID. Do not invent an ID or assume every
   object has a List. Call `pipelines_list` with that `object_id` and disambiguate
   similarly named processes. CRM pipelines and inbox funnels are different.
2. For a pipeline, call `pipeline_entries_query` with the returned `object_id`
   and `pipeline_id`. Use `group_by: "stage"` for stage counts, and a separate
   paginated entry query for details. Use returned cursors and label any summary
   based on a partial page. Do not infer monetary totals from counts.
3. For a List, call `list_entries_query` with its returned `list_id`. Read entry
   labels, record labels and returned values. Group with `group_by_attribute_id`
   only when a real status attribute ID is already available. If it is not,
   summarize the entries you can read and explain that grouped counts need it.
   Multiple entries for the same record are valid; do not silently deduplicate.
4. Use `history_get` selectively to investigate an entry that appears stalled.
   For pipeline history, use `target: "entry"` with the actual object, pipeline
   and entry IDs. For a List's parent record, use `target: "record"` with its
   `parent_object_id` as `object_id` and its returned `record_id`. Parent-record
   history is not a complete history of List entry values. Do not pass `list_id`
   to `history_get`, which does not accept it.
5. Report scope, stage counts where available, entries needing attention,
   supporting history and suggested next actions. Separate observed inactivity
   from inferred risk; do not invent a last-contact date, SLA or lost deal.

Do not move entries while producing the review. If the user separately requests
a move, preview the exact entry, process, current stage and target stage, then
obtain explicit confirmation before any state-changing tool call, regardless of
annotations. Verify real target IDs and current versions from the relevant tools;
the review alone does not authorize a move or a bulk cleanup.

If a requested follow-on write affects several entries, verify each returned
result and report actual successes, failures and partial completion. Re-read the
affected entries after an uncertain error before considering a retry. Never
silently substitute archival for deletion, promise that archiving a view is
reversible, or send a customer message as part of a review.

For no matches, report what was queried and ask whether the user meant another
object/process. For permission or feature errors, explain which results are
unavailable; do not treat inaccessible entries as empty stages or attempt another
workspace. Request reauthorization through the host UI for missing scopes.
