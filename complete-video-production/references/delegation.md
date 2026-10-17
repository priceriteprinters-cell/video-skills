# Specialized Production Delegation

## Prepare a complete but faithful handoff

Load the specialized animation tool before invoking it. Follow the currently loaded video-creator skill; it owns the production surface. Provide requirements and known facts, not an invented storyboard or a rendering recipe.

For motion graphics, invoke `acp_subagent--animate_video`, not an ordinary read-only research agent, a generative-footage tool, or an independently implemented replacement. Its completed result supplies the MP4 and summary. In plan mode, describe the invocation and its inputs in the plan; run it only after approval.

Use this adaptable handoff structure:

```text
User ask verbatim: <exact request>
Requested result: <motion-graphics video, or specific revision>
Master source: <confirmed narration path or supplied script>
Measured input duration: <exact seconds, only if measured>
Transcript: <supplied/parsed words, with uncertainty noted>
Timing precision: precisely align captions and relevant subject visuals to narration; return evidence and disclose unresolved approximation
Language/captions: English for all authored text unless explicitly overridden; preserve original spoken narration
Aspect ratio: <user-confirmed ratio; required before this handoff>
Typography: <user choice/delegation, resolved family per role, weights, existing local font and CSS paths, license evidence, language/glyph checks>
Palette/theme: <user choice/delegation, variant, exact background/text/accent/secondary colors, contrast results>
Resource manifest: <existing downloaded asset paths, SHA-256, source, license evidence, trademark caveats, attribution, scene purpose>
Brief validation: <result and remaining blockers; helper validation is not visual QA>
Duration/output specifications: <known requirements; omit unknowns>
Sound requirements: <music, SFX, narration preservation, exclusions>
Assets: <every relevant confirmed existing path, its purpose, official/authentic provenance, and discussion interval>
Visual standard: authentic assets first, honest generated fallback only after searching; polished purposeful premium motion with safe readable text
Brand facts: <only supplied or read from actual project assets>
Existing video/revision: <path and authorized changes, if applicable>
Local preview: <running URL only when relevant, with what it shows>
Output directory: <requested destination or appropriate Files directory>
Return: MP4 path, actual metadata, audio inclusion, QA evidence, limitations.
Keep original narration unless explicitly authorized otherwise.
Choose storyboard, soundtrack and implementation within these requirements.
```

Use `/mnt/documents/videos/` for ordinary standalone animated videos, and `/mnt/documents/ads/videos/` in an ad flow. Follow explicit user destinations. Never send a repository directory as the MP4 export destination; large committed videos can block the project.

Supply the running app's local development URL when one exists, describing accurately whether it is meaningful subject material or an empty template. The animation specialist cannot discover the project asset inventory: enumerate every relevant screenshot, store image, logo, and brand file collected during intake. Only pass visual asset paths that currently exist in the repository or Files; uploads needing another location must be staged through an allowed handoff. Unknown duration may be omitted, but the user's mandatory aspect-ratio answer may not.

Do not pass a temporary asset from a previous turn assuming it still exists. Verify asset paths now. The original upload is source narration, not an app asset to be committed. If the specialist needs a supported staging location, use a permitted handoff rather than embedding binary media into the repository.

## What not to add

Do not supplement the user's brand with invented offers, product descriptions, contact information, prices, hours, or claims. A transcript is evidence of what was said, not evidence that it is true.

Require precise phrase-caption and relevant subject synchronization. For word-reveal effects, obtain word-level alignment; translated English captions follow source phrase meaning rather than matching different-language word order. Timing requirements need measured/manual correction and exported evidence, not a confident prompt adjective. Disclose a remaining approximation as a draft limitation.

Never leave aspect ratio unspecified: obtain the user's answer before delegation. Unknown duration may remain unspecified when there is no narration clock. Keep authored text English unless explicitly overridden; never replace the original narration language or requested style silently.

## Background execution

Store the returned agent handle. Continue only independent work: reviewing input transcription, checking brief completeness, preparing QA criteria, or unrelated requested tasks.

Wait for the completion notification before fetching the final result. Do not repeatedly call the result tool, run long file-existence polling loops, or tell the user a final video exists merely because an encoder has opened an output file.

Read the whole final result, including qualifiers. Record the returned actual path, length, format, soundtrack status, and review status. Compare them against the brief.

## Repair path

If the specialist returns a usable clip with a requested correction needed, delegate a focused revision using its confirmed outputs and preserved requirements. Ask it to use a new versioned filename and return refreshed QA evidence.

If it fails or returns only intermediate assets, explain the failure and next step. Do not render or encode a rescue video in the parent agent. Tool unavailability is a blocker, not permission to bypass the designated production workflow.

Provider refusals, access denials, account issues, and credit restrictions follow the platform's current semantics. Do not retry, rephrase, change providers/models, or rotate credentials to evade terminal failures.