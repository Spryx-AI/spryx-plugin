#!/usr/bin/env python3
"""Validate the package against published schemas and documented listing limits.

Requires jsonschema and PyYAML. Downloads versioned schemas; never authenticates
to Spryx or runs a tool. This is package validation, not a directory tool scan.
"""

import json
import re
import struct
from pathlib import Path
from urllib.request import urlopen

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_BASE = "https://agent-plugins.org/schemas/1.0.0/"
SKILLS = {
    "spryx-get-started", "spryx-inbox-triage", "spryx-pipeline-review",
    "spryx-account-brief", "spryx-task-follow-ups",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_json(name):
    return json.loads((ROOT / name).read_text())


def package_path(value):
    require(value.startswith("./"), f"Expected a package-relative path: {value}")
    path = (ROOT / value).resolve()
    require(path.is_relative_to(ROOT) and path.is_file(), f"Missing package file: {value}")
    return path


def main():
    for name, schema_file in (("plugin.json", "plugin.schema.json"),
                              ("mcp.json", "mcp.schema.json")):
        with urlopen(SCHEMA_BASE + schema_file, timeout=20) as response:
            schema = json.load(response)
        jsonschema.Draft202012Validator.check_schema(schema)
        jsonschema.Draft202012Validator(schema).validate(read_json(name))
        print(f"Published schema passed: {name}")

    plugin = read_json("plugin.json")
    claude = read_json(".claude-plugin/plugin.json")
    for field in ("name", "version", "description", "author", "homepage", "repository", "license"):
        require(plugin[field] == claude[field], f"Platform identity differs: {field}")
    require(plugin["name"] == "spryx" and plugin["license"] == "Apache-2.0", "Wrong package identity")
    require(claude["displayName"] == "Spryx", "Wrong Claude display name")

    portable = read_json("mcp.json")["mcpServers"]
    legacy = read_json(".mcp.json")["mcpServers"]
    require(set(portable) == set(legacy) == {"spryx"}, "Expected exactly one Spryx MCP server")
    require(portable["spryx"]["type"] == "streamable-http", "Wrong portable transport")
    require(legacy["spryx"]["type"] == "http", "Wrong Claude transport")
    require(portable["spryx"]["url"] == legacy["spryx"]["url"] == "https://api.spryx.ai/mcp",
            "MCP endpoints differ")
    for server in (portable["spryx"], legacy["spryx"]):
        require(set(server) == {"type", "url"}, "Unexpected MCP fields or credentials")

    extension = plugin["extensions"]["com.openai"]
    require(set(extension) == {"interface", "onboardingSkill", "review", "publication"},
            "Unexpected OpenAI components")
    interface = extension["interface"]
    # The portable schema leaves extension contents open; these additional checks
    # apply OpenAI's documented submission-field constraints, not a portal schema.
    for field, maximum in (("displayName", 30), ("shortDescription", 30),
                           ("longDescription", 4000), ("developerName", 80)):
        require(isinstance(interface[field], str) and 0 < len(interface[field]) <= maximum,
                f"Invalid listing text: {field}")
    require(interface["displayName"] == interface["developerName"] == "Spryx", "Wrong publisher label")
    require(interface["shortDescription"] == "Your CRM and inbox in chat", "Wrong short description")
    require(interface["category"] == "Productivity", "Wrong category")
    require(len(interface["capabilities"]) <= 20 and all(
        isinstance(value, str) and 0 < len(value) <= 120 for value in interface["capabilities"]
    ), "Invalid capabilities")
    prompts = interface["defaultPrompt"]
    require(len(prompts) == 3 and all(isinstance(p, str) and 0 < len(p) <= 128 for p in prompts),
            "Expected three prompts of at most 128 characters")
    for field, url in {
        "websiteURL": "https://www.spryx.ai/",
        "supportURL": "https://www.spryx.ai/help",
        "privacyPolicyURL": "https://www.spryx.ai/legal/privacidade",
        "termsOfServiceURL": "https://www.spryx.ai/legal/contrato-de-servico",
    }.items():
        require(interface[field] == url, f"Unexpected URL: {field}")
    require(interface["brandColor"] == "#165DFC", "Wrong converted primary color")
    require(not any("dark" in key.lower() for key in interface), "Dark variants were not requested")
    for field in ("logo", "composerIcon"):
        data = package_path(interface[field]).read_bytes()
        require(data[:8] == b"\x89PNG\r\n\x1a\n", "Expected a PNG icon")
        width, height = struct.unpack(">II", data[16:24])
        require(width == height and width >= 48, "Icon must be square and at least 48px")
    require(extension["onboardingSkill"] == "./skills/spryx-get-started/SKILL.md", "Wrong onboarding skill")
    package_path(extension["onboardingSkill"])

    review = extension["review"]
    require(review["commerce"] is False, "Commerce must be disabled")
    cases = review["test_cases"]
    for kind, count in (("positive", 5), ("negative", 3)):
        require(len(cases[kind]) == count, f"Wrong number of {kind} cases")
        for case in cases[kind]:
            fields = ("description", "prompt", "expected_behavior")
            if kind == "positive":
                fields += ("tools_triggered",)
            require(all(isinstance(case.get(f), str) and case[f].strip() for f in fields),
                    f"Incomplete {kind} review case")
    publication = extension["publication"]
    require(publication["countries"] == ["BR"], "Wrong countries")
    translation = publication["translations"]["pt-BR"]
    require(0 < len(translation["subtitle"]) <= 30 and 0 < len(translation["description"]) <= 4000,
            "Invalid pt-BR listing")

    require({p.name for p in (ROOT / "skills").iterdir()} == SKILLS, "Expected exactly five skills")
    for name in sorted(SKILLS):
        path = ROOT / "skills" / name / "SKILL.md"
        content = path.read_text()
        match = re.match(r"\A---\n(.*?)\n---\n", content, re.DOTALL)
        require(match is not None, f"Missing YAML frontmatter: {name}")
        metadata = yaml.safe_load(match.group(1))
        require(metadata["name"] == name and metadata["description"].strip(), f"Invalid skill: {name}")
        require(len(content.splitlines()) <= 150, f"Skill is too long: {name}")

    serialized = json.dumps(plugin)
    require(not re.search(r'"(?:apps|hooks|commands|agents|test_credentials|reviewer_instructions)"\s*:',
                          serialized), "Forbidden package components or reviewer credentials")
    draft = dict(review)
    draft.pop("demo_recording_url")
    require("TODO" not in json.dumps(draft), "Unexpected review placeholder")
    print("Listing, shared configuration, paths and five skill headers passed")
    if review["demo_recording_url"] == "TODO":
        print("Draft only: replace review.demo_recording_url before directory submission")


if __name__ == "__main__":
    main()
