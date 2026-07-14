# Medium publishing playbook (Playwright MCP, draft only)

How to stage an article on Medium through the Playwright MCP with the human in
the loop. The editor is fragile and Medium resists automation, so the whole
playbook is built around one rule: **create a draft, never publish.**

## Why it works this way

- **The Medium API is dead.** New integration tokens stopped being issued on
  Jan 1, 2025 and the API repo is archived. There is no supported programmatic
  posting path, so browser automation is the only option.
- **Login is passwordless and human-only.** Sign-in is Google, Apple, X,
  Facebook, or an emailed code / magic link. You cannot and must not script it;
  automated auth trips bot detection.
- **The editor is a contenteditable surface** with floating toolbars whose
  positions are computed at runtime. Headings, code blocks, links, and especially
  images each require driving those toolbars, so direct automation needs manual
  cleanup and should always land a draft, not a published post.

## Preflight

- Confirm the Playwright MCP is available (`browser_*` tools). If not, tell the
  user to install it (`claude mcp add playwright npx @playwright/mcp@latest`) and
  stop.
- Confirm the diagram PNGs exist on disk (from the `mermaid-to-images` step) if
  the article has figures; images upload from local files.

## Step 1: Login (hand control to the human)

1. `browser_navigate` to `https://medium.com/m/signin`.
2. Tell the user to complete login in the browser window (choose their provider,
   or paste the emailed 5-digit code). Do not click through the auth yourself.
3. Poll for a logged-in signal instead of scripting auth: `browser_wait_for` a
   post-login marker (the "Write" button, the account avatar, or navigate to
   `https://medium.com/new-story` and wait until it does not redirect back to
   signin). Use a long timeout and retry. Reuse the session for the rest of the
   run so login happens once.

## Step 2: Create the draft

1. `browser_navigate` to `https://medium.com/new-story` (creates a fresh draft
   and drops you into the editor).
2. **Title**: the first line (placeholder "Title"). Click it, then type the
   title.
3. **Subtitle**: press Enter / arrow to the second line and type the subtitle.
4. **Body**: continue into the body. Type paragraphs as plain text first.
5. **Re-locate toolbars before each rich action.** Take a `browser_snapshot` to
   find the current toolbar / "+" menu position before clicking, because it moves
   with the cursor and layout.
   - **Headings**: select the line, then use the inline toolbar's heading button
     (Medium has two heading levels only). Map your `##` to large headings and
     `###` to the smaller one.
   - **Code blocks**: on an empty line, open the "+" menu and choose code block,
     then type or paste the code into it. Do not paste multi-line code into a
     normal paragraph; newlines collapse. Medium code blocks have no per-language
     highlighting (a GitHub Gist embed is the usual workaround for highlighted
     code, if the user wants it).
   - **Links**: select text, open the toolbar, click the link button, type the
     URL.
   - **Images**: on an empty line, open the "+" menu, choose image, and provide
     the local PNG via `browser_file_upload`. Add the caption. Place each figure
     near its section. This is the most fragile part; verify each upload with a
     `browser_snapshot` before moving on.

## Step 3: Stop at the draft

- **Never click Publish.** Medium autosaves drafts. Leave it staged.
- Report the draft URL and a short list of what likely needs manual touch-up:
  code block formatting, image placement and captions, and any heading that did
  not convert cleanly.
- Suggest the user review in Medium's preview, then publish manually when happy.

## Fallback: Import a story (least fragile)

If the article is (or can be) hosted at a **public URL** (for example a GitHub
Pages / repo render, a gist page, or a personal blog):

1. `browser_navigate` to the "Import a story" entry (`https://medium.com/p/import`
   or the top-right menu item).
2. Paste the public URL and click Import.
3. Land on the generated draft (Medium sets a canonical URL back to the source,
   which is SEO-safe). Formatting is best-effort; titles and images sometimes
   need a fix.

This sidesteps the contenteditable editor, headings, code blocks, and image
uploads entirely, so prefer it whenever a public URL is available. It still ends
at a draft for the user to publish.
