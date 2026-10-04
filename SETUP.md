# Setup

1. Create a **public GitHub repository named exactly like your GitHub username**.
2. Copy everything from this project into that repository.
3. Update `config.json` with your real GitHub username if needed.
4. Commit and push.
5. GitHub will automatically render `README.md` on your profile.

## Dynamic dashboard

The dashboard is generated from:

`scripts/generate_profile.py`

The generated file is:

`assets/profile.svg`

The image used by the animated identity panel is:

`assets/mr-robot.jpg`

To regenerate locally:

```bash
python scripts/generate_profile.py
```

The GitHub Action in `.github/workflows/update-profile.yml` also regenerates the SVG automatically.
