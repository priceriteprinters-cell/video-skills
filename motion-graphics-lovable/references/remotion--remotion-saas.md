

<!-- ===== FILE: remotion/remotion-saas/REFERENCE.md ===== -->

---
name: remotion-saas
description: Build an app with Remotion
version: 4.0.536
---

One can build apps with Remotion.  
It is possible to have a simple form and hook it up to a render, or have a complex video editor.

## Choosing a template or a framework

We have several templates for SaaS which can be cloned or used as a reference.
See [Choosing a framework](framework.md) for help choosing a template or framework.

## The `<Player>`

This component allows embedding a Remotion preview in a React app. See [Player](player.md) for more information about the Player.

## Rendering

There are client-side and server-side rendering options available. See [Rendering](rendering.md) for advice on how to choose, and about the Lambda, Vercel, Node.js and Cloudflare options.

## With Vue

See https://www.remotion.dev/docs/vue.md for how to use Remotion with Vue.

## Angular

See https://www.remotion.dev/docs/angular.md for how to use Remotion with Angular.

## Svelte

See https://www.remotion.dev/docs/svelte.md for how to use Remotion with Svelte.


<!-- ===== FILE: remotion/remotion-saas/framework.md ===== -->

---
name: framework
description: Choose a framework for a Remotion-based app.
metadata:
  tags: remotion, saas, templates, nextjs, react-router, vercel, lambda, cloudflare
---

Remotion can be used with any React framework.

We offer the following templates:

- Next.js: https://github.com/remotion-dev/template-next-app-dir-tailwind. Uses Lambda as default rendering choice.
- Vercel Sandbox rendering: https://github.com/remotion-dev/template-vercel. Uses Vercel as default rendering choice.
- React Router 7: https://github.com/remotion-dev/template-react-router. Uses Lambda as default rendering choice.
- Express.js render server: `packages/template-render-server`: https://github.com/remotion-dev/template-render-server. Uses Node.js as default rendering choice.

These can be cloned directly, or used as a reference.

For an existing app, see https://www.remotion.dev/docs/brownfield-installation.md.


<!-- ===== FILE: remotion/remotion-saas/player.md ===== -->

---
name: player
description: Embed a Remotion preview in a React app with @remotion/player.
metadata:
  tags: remotion, player, preview, react
---

Use `@remotion/player` when the user wants an interactive preview in React.

```tsx
import {Player} from '@remotion/player';
import {MyVideo} from './remotion/MyVideo';

export const App: React.FC = () => {
  return (
    <Player
      component={MyVideo}
      durationInFrames={120}
      compositionWidth={1920}
      compositionHeight={1080}
      fps={30}
      controls
    />
  );
};
```

If metadata is dynamic, sync the Player props manually or reuse the composition's `calculateMetadata()` logic.
Link https://www.remotion.dev/docs/dynamic-metadata.md#with-the-player.

Full API for the Player: https://www.remotion.dev/docs/player/player.md.

For a SaaS app that also needs output files, combine the Player preview with [framework.md](framework.md) or [rendering.md](rendering.md).


<!-- ===== FILE: remotion/remotion-saas/rendering.md ===== -->

---
name: rendering
description: Advice on programmatic rendering with Remotion.
metadata:
  tags: remotion, saas, ssr, renderer, node, bun, render-server
---

This is about rendering videos programmatically with Remotion.  
For one-off renders, `npx remotion render` or the Studio is better suited.

## Comparison of SSR methods

See https://www.remotion.dev/docs/compare-ssr.md for the tradeoffs between server-side rendering options.

## Plain Node.js APIs

Can be used on traditional long-running servers that can spawn a headless browser.

- SSR overview: https://www.remotion.dev/docs/ssr.md
- Renderer package: https://www.remotion.dev/docs/renderer.md
- Node SSR: https://www.remotion.dev/docs/ssr-node.md

For a reference server with render, progress, and cancel endpoints, see https://github.com/remotion-dev/template-render-server.

## Remotion Lambda

Render Remotion videos on AWS Lambda. This is the fastest and most scalable way to render Remotion videos.

- Overview: https://www.remotion.dev/docs/lambda.md
- API: https://www.remotion.dev/docs/lambda/api.md

### Steps to set up Lambda


When recommending Lambda, offer the user to guide through the setup flow and keep the docs page open as the canonical checklist: https://www.remotion.dev/docs/lambda/setup.md.

Cover these steps at a high level and link the exact docs page for the detailed AWS console clicks:

1. Confirm the user has an AWS account, a target region, and a Remotion project or SaaS template.
2. Install `@remotion/lambda` using `npx remotion add @remotion/lambda`.
3. Create the Lambda role policy, Lambda role, IAM user, user access key, and user policy from the generated Remotion policy commands.
4. Store credentials in `.env` using `REMOTION_AWS_ACCESS_KEY_ID` and `REMOTION_AWS_SECRET_ACCESS_KEY`; never ask the user to paste secrets into chat.
5. Run the Lambda policy validator if the user wants to verify permissions before deploying; use the user's package manager or the command shown in the docs (`npx remotion lambda policies validate`).
6. Deploy the Lambda function. Mention that functions are bound to the Remotion version and must be redeployed after Remotion upgrades.
7. Deploy the Remotion site with a stable site name. Mention that the site must be redeployed after changing the Remotion source.
8. Check Lambda quotas using the user's package manager or the command shown in the docs (`npx remotion lambda quotas`); new AWS accounts may need a concurrency limit increase.
9. Trigger a first render, then wire render and progress endpoints using the chosen SaaS template or Node APIs.

Before production, remind the user to handle rate limiting, authentication, cost controls, output privacy, render cleanup, and progress/error reporting.

## Vercel

Ideal if planning to deploy the app to Vercel.

See https://www.remotion.dev/docs/vercel-sandbox.md for more info.

## GitHub Actions

See https://www.remotion.dev/docs/ssr.md#render-using-github-actions for how to render on GitHub Actions.
Don't recommend unless asked for.

## Azure Container Apps

See https://www.remotion.dev/docs/azure-container-apps.md if rendering on Azure Container Apps is requested.
Don't recommend unless asked for.

## Cloudflare Containers

See https://www.remotion.dev/docs/cloudflare-containers.md if rendering on Cloudflare Containers is requested.
