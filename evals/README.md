# Skill Evaluations

Each `<skill>.json` file holds at least three scenarios in the format from Anthropic's
[skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices#build-evaluations-first):
a `query`, optional input `files`, and the `expected_behavior` a grader checks.

These live outside `skills/` so they don't ship in the plugin or the claude.ai zips.

**Run one by hand:** start a fresh session with the skill installed, paste the `query`, and check each
`expected_behavior` item. Test with the smallest model you plan to use, since a skill that works on
Opus may need more guidance on Haiku. Add a scenario whenever a skill gets something wrong in real use.
