# Lenses: how to test each one

Each lens has a question, a way to test it on a running product, what survives if you only have stills, the direction a fix usually takes, and cases from the source crits. The cases described frame by frame, with links to the videos, are in `cases.md`.

The cases come from three of Brian Lovin's five crits (Placemark, Outline, Less Annoying CRM). The other two, Buttondown and Sizzy, were kept out on purpose as a test set.

## 1. Scope

**Question.** Every control changes something: the app, the account, the workspace or document, the current view, or the selected object. Does its position and container say which?

**Test.** From the survey screenshots, list every control in the chrome: top bars, sidebars, menus, panel headers. Tag each with what it changes. Then read the tags region by region.
- A region whose controls carry different tags is a finding.
- So is a control sitting in a region of another scope.
- So is a parent that looks like a sibling of its children (the workspace switcher as one icon among tools).
- Panels too: a panel belongs to the thing it inspects, and its edges should start where that thing's controls end.

**From stills.** Works fully, as long as the menus are open in at least one screenshot.

**Fix direction.** One band or region per scope, broad to narrow from the outside in. Move the control to the region of the thing it changes. Put frequent actions next to the work they affect. Name the parent with a label, not an icon.

**Cases.**
- Placemark: one top strip held the map menu, the account avatar, feedback, the panel tabs and the drawing tools, and the properties panel ran to the top of the window. The mock makes two bands (document and account on top, editor tools below) and starts the panel under the tool band.
- Placemark: a "Visual" tab sat beside "Feature" and "Table", but it held map-wide appearance settings while the other two were about the selection. Moved to the document menu.
- Placemark: undo and redo lived in the app menu beside open and export. Moved to the editor toolbar.
- Less Annoying CRM: edit, assign, merge, print and delete for the open contact sat in a second dark column right beside global navigation, so they read as navigation. Moved under the contact's own header.
- Outline: the entry labelled with the team name opened the personal profile. Organization at the top of the sidebar, personal menu at the bottom.

## 2. Context

**Question.** While I decide or act, can I still see what I am acting on, and where I am?

**Test.** Take each step's screenshot on its own. Shown cold to a colleague, could they say which object this step is about, which workspace or account it is in, and what the parent task is? A step that fails that test at a moment of decision (confirming, granting access, sending) is a finding.

**From stills.** Works for the steps you have.

**Fix direction.** Keep the parent visible while the sub-task runs: the sub-task opens over or beside the object instead of replacing the page. If product-design is in use, its depth rules choose between peek, page and modal; this lens only requires that the object stays identifiable. Show the active workspace or account where consequential work happens. In mixed lists, put the owner on every item.

**Cases.**
- Outline: deleting a document replaced the whole window with a confirmation page. The name was there in bold, but the document was gone from view.
- Outline: collection permissions, then "create a group", then "add people" were three stacked full-window pages with only "Back" to orient. The designer lost track of what Back would do.
- Less Annoying CRM: the workspace activity feed mixed events from several contacts. The redesign reuses the event card from the contact page and adds the contact's avatar, name and role above it.

## 3. Consequence

**Question.** After I act, is the result visible where I acted?

**Test.** Put the before and after screenshots of each action side by side. The thing you created or changed should be in the after shot, in its new state. A toast alone does not count: it disappears, and it does not show where the thing now lives. Also count clicks: more than one to reach something done many times a day is worth writing down.

**From stills.** Only if you were given a before and after of the same action. Otherwise list it under Not checked.

**Fix direction.** Show the result in place. Added items stay in the list, marked as added. After a create, land on the created object or keep it visible in the list.

**Cases.**
- Outline: after adding the only available person to a group, the screen said "No people left to add" with a toast. The person only appeared after going Back to the "Group members" screen.

## 4. Signifier

**Question.** Does each thing look like what it does, before I click?

**Test.**
- For every row or bar with several targets, hover each one and screenshot. The highlighted region should match the click region, and targets with different actions should highlight separately.
- On a resting screenshot, mark everything you believe is clickable, then check. A mismatch in either direction is a finding.
- For selected and active states: could you find the selected tab or active tool in a blurred greyscale copy of the screenshot? If not, it relies on a slight color shift.
- For forms: can you tell typing from choosing, and enabled from disabled, without hovering?

**From stills.** The resting-state checks work. Hover behavior does not.

**Fix direction.** Give each sub-action its own hover target. Give clickable objects a boundary or other cue at rest. Mark selection with two signals (contrast plus shape, weight or background).

**Cases.**
- Outline: a sidebar row highlighted as one strip, yet the triangle expanded children and the label navigated.
- Outline: hovering a history entry lit its "…" button; clicking the "…" of another entry both switched version and opened a menu.
- Placemark: the selected panel tab differed from the others only by black versus grey text. The mock adds a tab shape. The active drawing tool was also easy to lose; the mock gives it a filled purple state.
- Less Annoying CRM: in the first redesign pass, leads and issues became plain text rows, so users would have to hover to learn they open. The final pass puts them back in bounded cards. Grey "add another" links read as disabled and became blue.

## 5. Prominence

**Question.** Does the size and position of each thing match how often its job is done?

**Test.** Rank the visible chrome by area and position. Rank the jobs by frequency, from the brief, analytics, or by asking. Where the two rankings disagree you have a finding if the frequency is known, and a question if it is not.

**From stills.** Works, but frequency is usually a guess, so expect questions.

**Fix direction.** Give space to the frequent job and let the rare one take only what it needs, on demand. If product-design is installed, its frequency × consequence grid is the rule; don't restate it.

**Cases.**
- Placemark: the properties list scrolled inside a short box while Export and GeoJSON held fixed space under it and the rest of the panel stayed blank. In the mock the properties fill the height and the two export sections collapse to a line each at the bottom.
- Less Annoying CRM: the search dialog led with a paragraph of explanation and a dark strip of shortcut help, and showed recent contacts as narrow pills that cut names off. The redesign leads with full rows of recent contacts.

## 6. One treatment, one meaning

**Question.** Does the same color, shape or component always mean the same thing?

**Test.** Take each strong treatment in the product (the accent color, the filled button, the pill, the bordered box) and list every place it appears across the survey. If the list holds different kinds of thing, the treatment tells the user nothing. Do the same for components: are the dialogs all built on one frame, or was each one designed alone?

**From stills.** Works across the screenshots you have.

**Fix direction.** Give each treatment one job. Build one frame for a component family and let it scale (a dialog header, footer and button position that serve both a two-line confirmation and a long form).

**Cases.**
- Less Annoying CRM: the same blue covered the dialog title, the fields, a section bar and the footer. Green marked both "Save" and a dropdown opener.
- Less Annoying CRM: every dialog had its own layout. Proposed: one dialog system reused from the small delete confirmation to the large new-contact form.

## 7. Scan lines

**Question.** In repeated rows, does each field keep its position, so the eye can run down a column?

**Test.** On any list, draw a vertical line at the start of each field across five rows. Fields that drift are a finding. Look for status markers placed inside titles, and for section headings that look like the entries below them.

**From stills.** Works fully.

**Fix direction.** One column per repeated field. Status markers get their own fixed column. Section headings get a quieter, different text style from entries.

**Cases.**
- Outline Home: titles lined up, but stars followed each title at a different x and the metadata line ran to a different length on every row. The mock puts the star in its own column left of the document icon.
- Outline sidebar: "Starred" and "Collections" were set almost like the entries under them. The mock makes them small grey labels.
- Placemark: the property table was inset from the panel edges for no reason. Made full width, with faint alternating rows.

## 8. Simplification loss

**Question.** What did the cleanup remove that people needed?

**When.** Any time you look at a redesign, a "cleaner" new version, or a screen that was generated recently. Always on your own after from step 5.

**Test.** Compare old and new (or the brief and the build) and list what disappeared: text size and contrast, click cues, the metadata that explains an event, color people used to find things, familiar positions, character. For each item ask whether it was noise or was doing a job. Then check the audience: who uses this, and do they want it denser, larger, plainer?

**From stills.** Works if you have both versions.

**Fix direction.** Restore the job, not the old styling.

**Cases.**
- Less Annoying CRM: the original had a dark two-column sidebar, blue contact names and striped rows. The designer's first pass was near-white with small dark names. He and the client both found it too plain and "enterprise" for a product sold on being approachable, and its customers prefer larger text. The same pass turned leads into plain rows and dropped the metadata from the history. The final pass kept the new structure and brought back larger, darker text, colored navigation icons, bounded cards, and the event verbs and timestamps.
- Less Annoying CRM: the first pass also moved the contact's actions under a full-width header. Cleaner, but existing users find those actions by position, so it was walked back toward the old placement.
