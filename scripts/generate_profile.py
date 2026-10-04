from pathlib import Path
import json
import os
import urllib.request
import datetime
import html

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))

def github_stats(username):
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        return {"repos": "—", "followers": "—", "contributions": "—"}

    query = """
    query($login:String!) {
      user(login:$login) {
        repositories(privacy:PUBLIC, ownerAffiliations:OWNER) { totalCount }
        followers { totalCount }
        contributionsCollection {
          contributionCalendar { totalContributions }
        }
      }
    }
    """
    payload = json.dumps({"query": query, "variables": {"login": username}}).encode()
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "profile-svg-generator",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
        user = data["data"]["user"]
        return {
            "repos": user["repositories"]["totalCount"],
            "followers": user["followers"]["totalCount"],
            "contributions": user["contributionsCollection"]["contributionCalendar"]["totalContributions"],
        }
    except Exception:
        return {"repos": "—", "followers": "—", "contributions": "—"}

def esc(v):
    return html.escape(str(v))

stats = github_stats(CONFIG["github_username"])
today = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="520" viewBox="0 0 1000 520">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#07111f"/>
    <stop offset="100%" stop-color="#0b1628"/>
  </linearGradient>
  <filter id="glow">
    <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
    <feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <style>
    .mono {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace; }}
    .label {{ fill:#6f89a8; font-size:13px; }}
    .value {{ fill:#e8f3ff; font-size:14px; font-weight:700; }}
    .small {{ fill:#607b9b; font-size:11px; }}
    .title {{ fill:#22d3ee; font-size:12px; font-weight:700; letter-spacing:1.2px; }}
  </style>
</defs>

<rect width="1000" height="520" rx="18" fill="url(#bg)"/>
<rect x="1" y="1" width="998" height="518" rx="17" fill="none" stroke="#203554"/>

<circle cx="22" cy="22" r="5" fill="#fb7185"/>
<circle cx="39" cy="22" r="5" fill="#fbbf24"/>
<circle cx="56" cy="22" r="5" fill="#34d399"/>
<text x="500" y="27" text-anchor="middle" class="mono small">profile.sh --live</text>
<line x1="0" y1="46" x2="1000" y2="46" stroke="#203554"/>

<rect x="20" y="66" width="350" height="430" rx="8" fill="#0b1728" stroke="#1e3a5f"/>
<rect x="390" y="66" width="590" height="430" rx="8" fill="#0b1728" stroke="#1e3a5f"/>

<text x="36" y="90" class="mono title">SYSTEM_MAP</text>
<text x="348" y="90" text-anchor="end" class="mono small">FULLSTACK / CLOUD</text>
<line x1="32" y1="104" x2="358" y2="104" stroke="#17324f"/>

<g class="mono">
  <path d="M92 184 H165" stroke="#23577d" stroke-width="2" stroke-dasharray="4 6">
    <animate attributeName="stroke-dashoffset" from="0" to="-20" dur="1.6s" repeatCount="indefinite"/>
  </path>
  <path d="M215 184 H286" stroke="#23577d" stroke-width="2" stroke-dasharray="4 6">
    <animate attributeName="stroke-dashoffset" from="0" to="-20" dur="1.6s" repeatCount="indefinite"/>
  </path>
  <path d="M190 210 V272" stroke="#23577d" stroke-width="2" stroke-dasharray="4 6">
    <animate attributeName="stroke-dashoffset" from="0" to="-20" dur="1.6s" repeatCount="indefinite"/>
  </path>
  <path d="M190 322 V374" stroke="#23577d" stroke-width="2" stroke-dasharray="4 6">
    <animate attributeName="stroke-dashoffset" from="0" to="-20" dur="1.6s" repeatCount="indefinite"/>
  </path>

  <rect x="40" y="158" width="52" height="52" rx="9" fill="#0f2238" stroke="#22d3ee"/>
  <text x="66" y="180" text-anchor="middle" fill="#22d3ee" font-size="15">WEB</text>
  <text x="66" y="197" text-anchor="middle" class="small">UI</text>

  <rect x="165" y="158" width="52" height="52" rx="9" fill="#0f2238" stroke="#60a5fa"/>
  <text x="191" y="180" text-anchor="middle" fill="#60a5fa" font-size="15">API</text>
  <text x="191" y="197" text-anchor="middle" class="small">REST</text>

  <rect x="286" y="158" width="52" height="52" rx="9" fill="#0f2238" stroke="#34d399"/>
  <text x="312" y="180" text-anchor="middle" fill="#34d399" font-size="15">DB</text>
  <text x="312" y="197" text-anchor="middle" class="small">SQL</text>

  <rect x="144" y="272" width="94" height="50" rx="9" fill="#0f2238" stroke="#f59e0b"/>
  <text x="191" y="294" text-anchor="middle" fill="#fbbf24" font-size="14">DOCKER</text>
  <text x="191" y="309" text-anchor="middle" class="small">container</text>

  <rect x="130" y="374" width="122" height="56" rx="9" fill="#0f2238" stroke="#a78bfa"/>
  <text x="191" y="397" text-anchor="middle" fill="#c4b5fd" font-size="14">KUBERNETES</text>
  <text x="191" y="414" text-anchor="middle" class="small">helm · argo cd</text>

  <circle r="4" fill="#22d3ee" filter="url(#glow)">
    <animateMotion dur="3s" repeatCount="indefinite" path="M66 184 H191 H312"/>
  </circle>
  <circle r="4" fill="#a78bfa" filter="url(#glow)">
    <animateMotion dur="2.6s" repeatCount="indefinite" path="M191 210 V402"/>
  </circle>
</g>

<text x="36" y="462" class="mono small">STATUS</text>
<circle cx="90" cy="458" r="4" fill="#34d399">
  <animate attributeName="opacity" values="1;.35;1" dur="1.8s" repeatCount="indefinite"/>
</circle>
<text x="102" y="462" class="mono small" fill="#34d399">ALL SYSTEMS NOMINAL</text>

<text x="408" y="90" class="mono title">SYSTEM_INFO</text>
<circle cx="866" cy="87" r="4" fill="#fb7185"/>
<text x="878" y="91" class="mono small" fill="#fb7185">LIVE</text>
<rect x="910" y="76" width="54" height="20" rx="10" fill="#0f2942" stroke="#1f6f9b"/>
<text x="937" y="90" text-anchor="middle" class="mono small" fill="#67e8f9">@{esc(CONFIG["github_username"])}</text>
<line x1="404" y1="104" x2="966" y2="104" stroke="#17324f"/>

<g class="mono">
  <text x="410" y="132" class="label">Subject</text><text x="950" y="132" text-anchor="end" class="value">{esc(CONFIG["name"])}</text>
  <text x="410" y="157" class="label">Role</text><text x="950" y="157" text-anchor="end" class="value">{esc(CONFIG["role"])}</text>
  <text x="410" y="182" class="label">Origin</text><text x="950" y="182" text-anchor="end" class="value">{esc(CONFIG["origin"])}</text>
  <text x="410" y="207" class="label">Focus</text><text x="950" y="207" text-anchor="end" class="value">{esc(CONFIG["focus"])}</text>

  <text x="410" y="244" class="label">Core.Frontend</text><text x="950" y="244" text-anchor="end" class="value">{esc(CONFIG["frontend"])}</text>
  <text x="410" y="269" class="label">Core.Backend</text><text x="950" y="269" text-anchor="end" class="value">{esc(CONFIG["backend"])}</text>
  <text x="410" y="294" class="label">Core.Database</text><text x="950" y="294" text-anchor="end" class="value">{esc(CONFIG["data"])}</text>
  <text x="410" y="319" class="label">Core.DevOps</text><text x="950" y="319" text-anchor="end" class="value">{esc(CONFIG["devops"])}</text>
  <text x="410" y="344" class="label">Core.Cloud</text><text x="950" y="344" text-anchor="end" class="value">{esc(CONFIG["cloud"])}</text>
  <text x="410" y="369" class="label">Core.CI/CD</text><text x="950" y="369" text-anchor="end" class="value">{esc(CONFIG["cicd"])}</text>
  <text x="410" y="394" class="label">Core.Testing</text><text x="950" y="394" text-anchor="end" class="value">{esc(CONFIG["testing"])}</text>

  <text x="410" y="431" class="label">Grid.Web</text><text x="950" y="431" text-anchor="end" class="value">{esc(CONFIG["website"])}</text>
  <text x="410" y="456" class="label">Grid.LinkedIn</text><text x="950" y="456" text-anchor="end" class="value">{esc(CONFIG["linkedin"])}</text>
</g>

<line x1="404" y1="472" x2="966" y2="472" stroke="#17324f"/>
<text x="410" y="490" class="mono small" fill="#34d399">● {esc(CONFIG["status"])}</text>
<text x="950" y="490" text-anchor="end" class="mono small">repos {stats["repos"]} · followers {stats["followers"]} · contributions {stats["contributions"]}</text>

<rect x="20" y="66" width="960" height="2" fill="#22d3ee" opacity=".08">
  <animate attributeName="y" values="66;494;66" dur="8s" repeatCount="indefinite"/>
</rect>

<text x="500" y="512" text-anchor="middle" class="mono small">{today}</text>
</svg>"""

(ROOT / "assets" / "profile.svg").write_text(svg, encoding="utf-8")
print("Generated assets/profile.svg")
