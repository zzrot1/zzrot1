from pathlib import Path
import json
import os
import urllib.request
import datetime
import html
import base64

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

def embedded_image(path):
    p = Path(path)
    if not p.exists():
        return ""
    mime = "image/png" if p.suffix.lower() == ".png" else "image/jpeg"
    encoded = base64.b64encode(p.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"

mr_robot_image = embedded_image(ROOT / "assets" / "mr-robot.jpg")

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

<text x="36" y="90" class="mono title">IDENTITY_STREAM</text>
<text x="348" y="90" text-anchor="end" class="mono small">PHOTO / SOURCE</text>
<line x1="32" y1="104" x2="358" y2="104" stroke="#17324f"/>

<defs>
  <clipPath id="mediaClip">
    <rect x="34" y="120" width="322" height="300" rx="8"/>
  </clipPath>
</defs>

<!-- MR. ROBOT IMAGE PHASE -->
<g clip-path="url(#mediaClip)">
  <rect x="34" y="120" width="322" height="300" rx="8" fill="#06101d"/>

  {f'<image href="{mr_robot_image}" x="34" y="120" width="322" height="300" preserveAspectRatio="xMidYMid slice"/>' if mr_robot_image else '<text x="195" y="260" text-anchor="middle" class="mono small">add assets/mr-robot.jpg</text>'}

  <!-- dark cinematic tint -->
  <rect x="34" y="120" width="322" height="300" fill="#03111d" opacity=".38"/>

  <!-- photo fades out -->
  <rect x="34" y="120" width="322" height="300" fill="#07111f" opacity="0">
    <animate attributeName="opacity"
             values="0;0;1;1;0"
             keyTimes="0;0.38;0.48;0.88;1"
             dur="10s"
             repeatCount="indefinite"/>
  </rect>

  <!-- CODE PHASE -->
  <g class="mono" opacity="0">
    <animate attributeName="opacity"
             values="0;0;1;1;0"
             keyTimes="0;0.40;0.50;0.88;1"
             dur="10s"
             repeatCount="indefinite"/>

    <rect x="34" y="120" width="322" height="300" fill="#06101d"/>

    <text x="48" y="145" fill="#22d3ee" font-size="11">$ whoami</text>
    <text x="48" y="165" fill="#dbeafe" font-size="11">ioan@mihu: full-stack-engineer</text>

    <text x="48" y="195" fill="#34d399" font-size="11">const stack = &#123;</text>
    <text x="62" y="215" fill="#93c5fd" font-size="11">frontend: ["React", "Next.js"],</text>
    <text x="62" y="235" fill="#93c5fd" font-size="11">backend: ["Node.js", "C#"],</text>
    <text x="62" y="255" fill="#93c5fd" font-size="11">infra: ["Docker", "K8s"],</text>
    <text x="62" y="275" fill="#93c5fd" font-size="11">cloud: ["AWS", "Azure"],</text>
    <text x="48" y="295" fill="#34d399" font-size="11">&#125;;</text>

    <text x="48" y="328" fill="#fbbf24" font-size="11">deploy --env production</text>
    <text x="48" y="350" fill="#64748b" font-size="10">[build] compiling...</text>
    <text x="48" y="370" fill="#64748b" font-size="10">[test] all checks passed</text>
    <text x="48" y="390" fill="#34d399" font-size="10">[ship] production ready ✓</text>

    <rect x="48" y="400" width="7" height="13" fill="#22d3ee">
      <animate attributeName="opacity" values="1;0;1" dur=".8s" repeatCount="indefinite"/>
    </rect>
  </g>

  <!-- glitch strips during transition -->
  <g opacity="0">
    <animate attributeName="opacity"
             values="0;0;1;0;1;0;0"
             keyTimes="0;0.39;0.42;0.44;0.46;0.49;1"
             dur="10s"
             repeatCount="indefinite"/>
    <rect x="34" y="188" width="322" height="5" fill="#22d3ee" opacity=".7">
      <animate attributeName="x" values="20;52;34" dur=".18s" repeatCount="indefinite"/>
    </rect>
    <rect x="34" y="274" width="322" height="3" fill="#fb7185" opacity=".6">
      <animate attributeName="x" values="42;18;34" dur=".13s" repeatCount="indefinite"/>
    </rect>
    <rect x="34" y="337" width="322" height="4" fill="#60a5fa" opacity=".45">
      <animate attributeName="x" values="28;58;34" dur=".16s" repeatCount="indefinite"/>
    </rect>
  </g>
</g>

<text x="36" y="447" class="mono small">MODE</text>
<circle cx="77" cy="443" r="4" fill="#34d399">
  <animate attributeName="opacity" values="1;.3;1" dur="1.4s" repeatCount="indefinite"/>
</circle>
<text x="89" y="447" class="mono small" fill="#34d399">IDENTITY → SOURCE → REPEAT</text>
<text x="36" y="470" class="mono small">10s LOOP / SVG SMIL</text>

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
