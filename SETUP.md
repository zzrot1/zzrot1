# Setup

1. Create a public GitHub repository named exactly like your GitHub username.
   The included config currently uses `imihu`.

2. Copy everything from this folder into that repository.

3. Commit and push.

4. The README will automatically appear on your GitHub profile.

## Dynamic dashboard

`.github/workflows/update-profile.yml` runs daily and regenerates
`assets/profile.svg`.

It uses GitHub's built-in `GITHUB_TOKEN`; you do not need to create a PAT.

The dashboard can display:
- public repository count
- follower count
- contribution count

You can also manually run:
**Actions → Update profile dashboard → Run workflow**

## Customize

Edit `config.json` and commit. The workflow regenerates the SVG.

Preview locally:

```bash
python scripts/generate_profile.py
```

Then open `assets/profile.svg` in a browser.

If your actual GitHub username is not `imihu`, change
`github_username` inside `config.json` and use the correct profile repository name.
