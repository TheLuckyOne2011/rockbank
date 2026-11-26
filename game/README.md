# Rockbank game — base mode

A 1–6 player Rocks & Minerals quiz using `../questions.json` and the specimen photos in `../../rockid/images`.

```
npm install
npm start          # http://localhost:3100  (LAN address is printed and shown in the lobby)
npm test
```

One person hosts on a big screen. Everyone else opens the LAN address on their phone and enters the 4-digit room code.
To play solo, tick **I'm playing too, on this screen** and start right away.

## Rules (lib/scoring.js)

- Answers unlock 3 s after a question appears; you can type during the lock (prefire) but can't submit.
- Correct within 0.5 s of unlock: 1000. After that the value slides down one point at a time to 500 at the time cap.
- Every wrong answer costs 200 from your eventual correct score. Repeating the same wrong answer is free, and so is
  unreadable input (an empty box, a letter that isn't an option, a non-number for a number question).
- Your 3rd wrong answer locks you out of that question (shown as X's next to "Worth now"). If every player is correct or locked
  out, the question ends right away.
- 2nd correct player: -100. 3rd: -300. A correct answer always earns at least 100. No partial credit.
- The question ends as soon as half the room (rounded up) is correct, or when the time cap (default 45 s) runs out.

## Answering (lib/check.js)

Everything is typed. Multiple-choice questions are played without their options (ones that only make sense with options,
like "Which of these..." or "...NOT...", are left out). True/false takes T or F; select-all and ordering still show lettered
options. Free-response questions whose answer is about a sentence are included.

- Names, terms and formulas: typo-tolerant exact match. Where several answers are valid (a mineral's other lusters,
  environments or uses), all of them are accepted.
- Numbers in short answers: anything inside a stated range counts ("6" for hardness 5.5-6).
- Sentences: graded laxly by key words (with plurals/typos handled): roughly a third of the answer's key words, or one key
  point, is enough. Saying the opposite ("slow cooling" for "rapid cooling"), using a different number, or dumping a long
  list of words does not count.

Below the answer box is a feed of your attempts, shaded by how close each was (no highlight, then yellow, then green),
plus a line whenever another player gets it right (their answer isn't shown). A correct answer turns your box green.
The timer bar is grey during the 3 s lock, then fades from dark green to dark red as time runs out.

## Host settings

10–50 questions; regional list only or include State/Nationals (★) specimens; question mix (everything,
identification, mineral properties, concepts); time cap 30/45/60/90 s.

## Race mode (lib/race.js)

Pick **Race** under Mode in the lobby. Everyone gets the same questions in the same order but goes at their own pace;
there are no points.

- After every graded answer, right or wrong, you wait 3 s before you can submit again (you can type meanwhile).
  Unreadable input and repeating an answer you already tried don't trigger the wait.
- A correct answer brings up your next question immediately (with the 3 s wait on it).
- Up to 3 hints per question (lib/hints.js), each adding 10 s to your wait. You can't take another hint until the
  previous hint's 10 s has run out. If you've been on a question for 30 s, the next hint appears for free. Hints get
  stronger: letter patterns for names (`A_______` -> `A_e_h_s_` -> `Amethys_`), narrowing ranges for numbers, key words
  revealed one at a time for sentence answers, and options/order revealed for select-all and ranking questions.
  Hint 3 nearly gives the answer away, so nobody gets stuck. A "Hints used" count is shown under the answer box and
  on the track.
- **Race (first hint shown)** mode: hint 1 is up on every question for free (the 30 s rule then frees hint 2).
- No 3-strike lockout in Race: wrong answers already cost time.
- A track at the top shows everyone's progress; the feed says when others answer or skip.
- The race ends the moment someone finishes the last question. Everyone else is ranked by questions completed,
  then by who got there first. The final screen shows how many hints each player used.

## Hosting on Render

`render.yaml` (repo root) is a Render blueprint: in Render, **New + -> Blueprint**, pick this repo, **Apply**.
It runs `game/` on the free plan. The free plan sleeps after ~15 minutes with no visitors; the first visit after
that takes ~30-60 s while it wakes. Rooms live in memory, so a restart or redeploy ends any game in progress.

Photos: the server uses `ROCKID_IMAGES` if set, else the full library at `../../rockid/images` if present, else the
small set bundled in `game/images` (8 per specimen, resized; made by `python tools/bundle_images.py`).
Photo credits and licenses are in `game/images/CREDITS.md`.

The lobby shows `PUBLIC_URL` or Render's `RENDER_EXTERNAL_URL` as the join address when set, otherwise LAN addresses.
