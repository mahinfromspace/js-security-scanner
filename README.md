# Project 7: HTML and JavaScript Security Scanner

This project uses Python and GitHub Actions to scan `.html` and `.js` files for risky JavaScript patterns. Every push starts the scan automatically. The workflow passes when no risky pattern is found and fails when the scanner reports a finding.

## Patterns detected

- `document.write(...)`
- `eval(...)`
- `.innerHTML = ...`
- `Function(...)` or `new Function(...)`
- A string or direct variable passed to `setTimeout(...)` (final challenge)

## Repository files

- `index.html` — small webpage used for the demonstration
- `app.js` — safe JavaScript demo
- `js_scan.py` — Python security scanner
- `.github/workflows/js-scan.yml` — GitHub Actions workflow
- `README.md` — setup, demonstration, and project explanation

## How the scanner works

1. Python searches the repository for `.html` and `.js` files.
2. It ignores `.git` and `node_modules` directories.
3. It reads each file line by line.
4. Regular expressions compare each line with the risky-pattern rules.
5. If a match is found, the scanner prints the file, line number, rule, and code.
6. It exits with status `1`, so GitHub Actions marks the workflow as failed.
7. If there are no findings, it exits with status `0`, so the workflow passes.

## Run locally

Python 3 is the only requirement.

```bash
python js_scan.py
```

Expected clean result:

```text
Scanning 2 HTML/JavaScript file(s)...
SECURITY SCAN PASSED: no risky patterns were found.
```

## Basic demonstration

### 1. Show a passed scan

Keep this safe line inside `showMessage()` in `app.js`:

```javascript
output.textContent = userInput;
```

Commit and push the files. GitHub Actions should pass.

### 2. Introduce a safe demo problem

Replace the safe line with:

```javascript
output.innerHTML = userInput;
```

Commit and push again. The scan should fail and report `innerHTML assignment`.

This pattern is risky because browser input could be interpreted as HTML instead of harmless text. In a real vulnerable application, this can contribute to cross-site scripting (XSS).

### 3. Fix the problem

Change the line back to:

```javascript
output.textContent = userInput;
```

Commit and push. The scan should pass again.

## Final challenge

I added a new rule named `unsafe setTimeout()` to `js_scan.py`. It detects a string or direct variable used as the first argument of `setTimeout`.

The safe code is:

```javascript
setTimeout(() => showMessage(userInput), 1000);
```

For the challenge demonstration, replace it temporarily with:

```javascript
setTimeout(userInput, 1000);
```

Commit and push. The workflow should fail and display `unsafe setTimeout()`.

Fix it by restoring the callback function:

```javascript
setTimeout(() => showMessage(userInput), 1000);
```

Commit and push once more. The final scan should pass.

## My Work

### 1. What did you build?

I built a lightweight static security scanner that automatically checks HTML and JavaScript files whenever code is pushed to GitHub.

### 2. What files did you create or modify?

I created `index.html`, `app.js`, `js_scan.py`, `.github/workflows/js-scan.yml`, and `README.md`. I modified `app.js` during the pass-fail-fix demonstrations and added a new detection rule to `js_scan.py` for the final challenge.

### 3. What made the GitHub Actions workflow fail?

The first failure happened when I changed `textContent` to an `innerHTML` assignment. The final-challenge failure happened when a direct variable was passed to `setTimeout`.

### 4. How did you fix it?

I replaced `innerHTML` with `textContent` so input was displayed only as text. I also replaced the direct `setTimeout` argument with an arrow-function callback.

### 5. What final challenge did you complete?

I added an `unsafe setTimeout()` rule to the Python scanner and demonstrated that it detects `setTimeout(userInput, 1000)`.

### 6. What did the final scan show?

The final scan passed and reported that no risky patterns were found after both unsafe examples were fixed.

## Important limitation

This is an educational pattern scanner, not a complete professional security tool. It can find selected text patterns, but it does not fully understand JavaScript syntax or prove that an application is secure. Professional projects combine tools like this with code review, dependency scanning, testing, and dynamic security testing.
