# Demonstration Video — Recording Script (≈4 minutes)

**Candidate:** Subodh Shivmurti Bansode · OsdagBridge screening task
**Format:** 1080p MP4 · OBS Studio or Xbox Game Bar (`Win + Alt + R`) · headset microphone
**Rule for the whole video:** say only what is visible on screen or recorded in the evidence. If something behaves differently from this script, say what you see. That is a finding, not a failure.

## Before you press record (about 10 minutes)

1. Open **Anaconda Prompt** and type `conda activate osdagbridge-py312`.
2. Do a **dry run** of the helper without the GUI:
   ```
   python "F:\FOSSEE internship\submission\video\automated_video_demo_runner.py" --no-gui --no-pause
   ```
   Confirm that you see 17/17 OK, 15/15 OK and 27/27 OK.
3. Set the display to 1920×1080 and turn on Do Not Disturb. Make the terminal font larger (Ctrl + scroll).
4. Have the technical report PDF open in a second window.
5. Note the values you will type into the custom-material dialog, for example:
   - steel: f<sub>y</sub> 350 MPa, f<sub>u</sub> 490 MPa, E 200,000 MPa;
   - concrete: f<sub>ck</sub> 35 MPa.

The helper only **reads** the workspace evidence. It runs the tests from a fresh copy of the submission ZIP in a temporary folder, so recording cannot overwrite any evidence.

To start recording, run the helper (it pauses before each step):

```
python "F:\FOSSEE internship\submission\video\automated_video_demo_runner.py"
```

## Script

### 1. Introduction (0:00–0:20) — show the report's first page

> "Hi, I'm Subodh Bansode. This is my screening task for OsdagBridge's composite plate girder module. I tested the calculation pipeline, found defects against IRC:6 and IS 800, and fixed five of them. I'll show the software running, the evidence for the defects, and the tests that prove the fixes."

### 2. Live GUI (0:20–1:40) — helper Step 1 opens OsdagBridge

**On screen:**

1. Enter span 24 m and carriageway 7.5 m, and select a project location.
2. In the Girder material row, choose **Custom** or click the ⓘ button. Enter the steel values you noted, then do the same for the deck concrete.
3. Click **Design**. Pause the recording while it computes, if it takes long.
4. Show the output dock and rotate the 3D model.
5. Click the **padlock** to unlock. Change the span to 30 m and run Design again.
6. Unlock again, change the skew angle (for example to 15°) and run a third time.

**Say:**

> "I'm entering custom steel and concrete properties … running the design … here are the results and the 3D model. Now I unlock, change the span to 30 metres and run again … and a third run with a 15-degree skew."

**After each run, check:**

- the girder count;
- that the custom material values are still in the dialog;
- that the 3D view shows the new geometry.

**Say exactly what you observe**, for example:

> "The custom yield strength is still 350 after re-running."

or

> "The 3D view did not refresh. This matches upstream issue 85."

Close the window to continue.

### 3. The defects (1:40–2:30) — helper Steps 2 and 3

**On screen:** the baseline log lines, then the commit list.

> "These lines come from the sealed baseline logs of the unmodified code.
>
> First, the bearing-stiffener web buckling capacity came out at 214,533 kilonewtons. The IS 800 value for this geometry is 63.4, so the capacity was overstated about 3,400 times. That can make a needed stiffener look unnecessary.
>
> Second, the finite-element model applied the 314-kilonewton crash-barrier load 117.7 kilonewtons short, 37.5 percent lost.
>
> Third, a 1.35 load factor had no effect: the factored-to-unfactored force ratio is exactly 1.00.
>
> Each defect has a test with a hand-calculated expected value. I also checked that each test fails on a plausible but wrong fix.
>
> These six small commits fix five defects."

### 4. Proof from a clean copy (2:30–3:35) — helper Step 4

**On screen:** the ZIP is extracted to a temporary folder and the three suites run.

> "To show this is reproducible, the helper extracts the exact ZIP I'm submitting into an empty folder and runs the tests from there.
>
> Batch 2 checks force, centroid and reaction equilibrium for line and patch loads, including skewed lines and the full-bridge barrier: 17 out of 17.
>
> Batch 3 checks that load factors now reach the solver for every load type, against nine hand-calculated cases: 15 out of 15.
>
> The governance suite checks that the sealed evidence and the reference databases have not been altered."

### 5. After the fix, and close (3:35–4:05) — helper Step 5

**On screen:** the post-fix log lines, then the report's limitations section.

> "After the fix, the same stiffener test gives 63.4 kilonewtons and the load-factor ratio is 1.35. Both pass.
>
> To be clear about scope: 15 register entries are still open. For example, barrier dead load is still missing from the ULS combinations. Those are documented in the report with proposed fixes. Thank you for reviewing my submission."

## After recording

1. Watch the video once. Check the audio and that the terminal text is readable. Trim long waits.
2. Upload to YouTube as **Unlisted**, or to Google Drive with "Anyone with the link can view".
3. Open the link in a private/incognito window to confirm it plays.
4. Paste the link into the form's video field.
