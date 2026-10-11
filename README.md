Related Issue: Closes #<README issue number>

WHAT CHANGED?
- Replaced the placeholder README.md with the full README
- Added: project goal, team table, setup, how to run, menu options, how to run tests, priority rules, status rules, work queue rules, where tickets are saved, known limitations, PR links section

HOW DOES IT WORK?
- Documentation only. No Python code or tests were changed.
- The priority, status and queue rules in the README were written from the project requirements and checked against the code in main.

HOW DID I TEST IT?
- Command: python3 -m unittest discover -s tests -v
- Actual result: Ran 63 tests in 0.009s, OK (run on a fresh clone of main)
- Checked: the test command in the README works from a fresh clone of main

WHAT DID I LEARN WITH AI?
- Concept: <what you learned, for example how branches, pushes and pull requests fit together>
- My verification: Cloned main into a separate folder and ran the full test suite to confirm what is really on GitHub
- Changed/rejected advice: <only if it really happened, otherwise write "None for this PR">

REVIEWER NOTES
- Please check that the priority and status rules in the README match what the code does
- Please confirm your name and role in the Team table are correct

KNOWN LIMITATIONS
- PR links in the README are added after both feature PRs are confirmed