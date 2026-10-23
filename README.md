# Spryx

## What it is

Official Spryx plugin for Claude and ChatGPT. Connects your AI assistant to your
Spryx workspace (CRM, inbox, pipelines and tasks) via MCP, plus skills for sales
and customer service workflows.

The plugin contains a remote MCP connection and five shared skills. A Spryx
account, appropriate workspace permissions and the relevant product features are
required. Each connection is bound to the member and workspace chosen at sign-in.

## What you can do

- "Check my Spryx connection and show my open tasks."
- "Show conversations waiting for a reply and draft an internal handoff note."
- "Review my pipeline and Lists without changing any stages."
- "Prepare an account brief using CRM records, conversations and linked tasks."
- "Show my overdue tasks and propose a follow-up plan."

Skills require a concrete preview and explicit confirmation before changing
existing state, sending a customer message or enabling a conversation's AI agent.
New tasks are created only when requested. Summaries do not authorize changes.
The plugin cannot permanently delete contacts, process payments, read or schedule
calendars, or access another workspace through the same connection.

## Install

Version 0.1.0 is prepared for review; directory publication is pending. The
directory instructions below apply after the listings are published.

**Claude directory:** find **Spryx** in the Claude plugin directory, add it, then
connect Spryx from the plugin's Connectors tab. Sign in and select your workspace.

**ChatGPT directory:** find **Spryx** in the ChatGPT plugin directory, install it,
and connect your Spryx account. Run setup to invoke `spryx-get-started`.

**Claude Code from this repository:** once this version is on the repository's
default branch, run in Claude Code 2.1.275 or later:

```text
/plugin install spryx --marketplace Spryx-AI/spryx-plugin
```

For older versions that support marketplaces, add and install separately:

```text
/plugin marketplace add Spryx-AI/spryx-plugin
/plugin install spryx@spryx-plugins
```

Then run `/mcp` and authenticate Spryx. For local development, start Claude Code
with `claude --plugin-dir /path/to/spryx-plugin`.

**Manual MCP connection:** use `https://api.spryx.ai/mcp` with OAuth in a compatible
client. In Claude Code:

```sh
claude mcp add --transport http spryx https://api.spryx.ai/mcp
```

A manual MCP connection exposes tools; install the plugin to get these skills.

### Package layout and build

`skills/` and `assets/icon.png` are shared. Claude reads
`.claude-plugin/plugin.json` and `.mcp.json`. OpenAI reads the portable root
`plugin.json` and `mcp.json`. There is no separate Codex compatibility manifest.

Only the MCP configuration is duplicated: Claude requires `type: "http"`, while
the portable schema linked by OpenAI requires `type: "streamable-http"` and its
schema declaration. Claude's validator rejects the URL-only configuration shown
in the Codex compatibility example. Both files point to the same endpoint and
contain no credentials or custom headers. See the
[OpenAI migration guide](https://developers.openai.com/plugins/guides/submit-claude-plugin)
and [package reference](https://developers.openai.com/plugins/build/plugins).

Build the OpenAI ZIP with Bash and Python 3, from any working directory:

```sh
./scripts/build-openai-zip.sh
unzip -l dist/spryx-openai-0.1.0.zip
```

An optional first argument selects the output `.zip` path. The archive contains
the portable manifests, five skills, icon, README and license. It excludes Claude
configuration, the build/validation scripts, Git data and local research files.

Validate before releasing:

```sh
claude plugin validate .
claude plugin validate .claude-plugin/plugin.json
claude plugin validate .claude-plugin/marketplace.json
python3 -m venv .context/validation-env
.context/validation-env/bin/pip install jsonschema pyyaml
.context/validation-env/bin/python scripts/validate.py
```

The Python check downloads the versioned Agent Plugins schemas linked by OpenAI
and checks package metadata, skill frontmatter and paths. These checks do not
replace either directory's review, authenticated testing or tool scans.

The icon is copied from Spryx's MCP server (512×512 PNG). `brandColor` is
`#165DFC`, converted from the app's `--primary: oklch(54.6% 0.245 262.9)` using
OKLab-to-linear-sRGB conversion, sRGB encoding and 8-bit rounding. No dark variants
are supplied.

### Submission status

The manifest targets **Productivity**, availability in **BR**, and includes a
`pt-BR` translation. Its five positive and three negative review cases are
procedures to run with synthetic reviewer data, not claims of completed tests.
The only placeholder is `extensions.com.openai.review.demo_recording_url`.

Before submission, the separate MCP work must resolve the phase-1 findings:
missing tool titles (B1), destructive annotations (B2), Origin validation (B3),
the OpenAI domain challenge (B4), issuer identification on OAuth error redirects
(B5), and misleading reversible-archive instructions (B6). The skills enforce
confirmation independently of annotations and never promise view restoration.

Recommended server follow-ups include OIDC/UserInfo for Enterprise domain
restrictions, clearer tool descriptions, retention-policy consistency and
authenticated isolation/partial-failure coverage. This repository changes no
server behavior.

Maintainers must supply the demo recording, a populated test account with verified
email and no MFA/email-code prompts, and a verified OpenAI publishing identity.
Enter reviewer access only in the secure dashboard. Claude requires both the
GitHub plugin submission and a separate remote MCP connector submission; see its
[submission guide](https://claude.com/docs/plugins/submit). No store submission is
performed by this repository or its scripts.

## Authentication

Spryx uses OAuth authorization-code sign-in with PKCE S256. The remote server
supports dynamic client registration and Client ID Metadata Documents, and
publishes OAuth discovery metadata. Do not put passwords, API keys or bearer
tokens in plugin files or chat.

Choose the intended workspace and grant only the capabilities needed. The
`records` scope includes both read and write tools; onboarding itself is read-only.
Inbox reading, organization and messaging may need additional approved scopes.
Your current Spryx role still controls each operation, and some features require
the corresponding workspace entitlement. Reauthorize through the host's connection
UI if needed. Reconnect and select another authorized workspace to change scope.
Connections can be reviewed and revoked in Spryx's connected-app settings.

## Skills

| Skill | Purpose |
| --- | --- |
| `spryx-get-started` | Read-only connection checks and three first prompts. |
| `spryx-inbox-triage` | Inbox summaries, drafts and explicitly confirmed changes. |
| `spryx-pipeline-review` | Read-only pipeline/List summaries and relevant history. |
| `spryx-account-brief` | CRM, inbox and task context for account discussions. |
| `spryx-task-follow-ups` | Requested task creation and confirmed edits/completion. |

## Privacy Policy

Read the [Spryx Privacy Policy](https://www.spryx.ai/legal/privacidade).
The server processes requests as the connected member in the selected workspace.
Records, conversations and tasks returned by tools become available to the
assistant host for the requested workflow. Review that host's data settings too.
The plugin package contains instructions and public configuration, not customer
data or credentials. Revoking a connection stops future access; it does not erase
content already returned to the assistant.

## Support

See [Spryx Help](https://www.spryx.ai/help) or email
[suporte@spryx.ai](mailto:suporte@spryx.ai). The service is governed by the
[Spryx Terms of Service](https://www.spryx.ai/legal/contrato-de-servico).

## License

Copyright 2026 Spryx. Licensed under [Apache-2.0](LICENSE).
