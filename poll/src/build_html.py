import json, html
opts = json.load(open('options.json'))

cards = []
for i, o in enumerate(opts, 1):
    tag = '<span class="chip">salon pick</span>' if o['top'] else ''
    cards.append(f'''      <button class="cand" type="button" role="radio" aria-checked="false" data-n="{i}" data-name="{html.escape(o['name'])}">
        <span class="portrait"><img src="{o['img']}" alt="{html.escape(o['name'])}"><span class="num">{i}</span>{tag}</span>
        <span class="row"><span class="oval" aria-hidden="true"></span><span class="cname">{html.escape(o['name'])}</span></span>
      </button>''')
cards = "\n".join(cards)

page = f'''<title>Leo's Hair — Official Family Ballot</title>
<style>
  :root {{
    --paper: #F1EEE6;
    --card: #FBFAF6;
    --ink: #1B1E24;
    --ink-soft: #5C6068;
    --rule: #CBC5B5;
    --stamp: #6B3FA0;
    --stamp-soft: rgba(107,63,160,.12);
    --shadow: 0 1px 0 rgba(27,30,36,.06), 0 10px 24px -18px rgba(27,30,36,.5);
  }}
  @media (prefers-color-scheme: dark) {{
    :root:not([data-theme="light"]) {{
      --paper: #14161A;
      --card: #1D2027;
      --ink: #ECEAE3;
      --ink-soft: #9AA0AA;
      --rule: #3A3F49;
      --stamp: #B891E8;
      --stamp-soft: rgba(184,145,232,.16);
      --shadow: 0 1px 0 rgba(0,0,0,.4), 0 10px 24px -18px #000;
    }}
  }}
  :root[data-theme="dark"] {{
    --paper: #14161A;
    --card: #1D2027;
    --ink: #ECEAE3;
    --ink-soft: #9AA0AA;
    --rule: #3A3F49;
    --stamp: #B891E8;
    --stamp-soft: rgba(184,145,232,.16);
    --shadow: 0 1px 0 rgba(0,0,0,.4), 0 10px 24px -18px #000;
  }}

  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    background: var(--paper);
    color: var(--ink);
    font-family: "Avenir Next", Avenir, "Segoe UI", system-ui, sans-serif;
    -webkit-text-size-adjust: 100%;
  }}
  .display {{
    font-family: Futura, "Futura PT", "Century Gothic", "Avenir Next", system-ui, sans-serif;
    font-weight: 700;
    letter-spacing: .06em;
    text-transform: uppercase;
  }}
  .mono {{ font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace; }}

  .sheet {{
    max-width: 680px;
    margin: 0 auto;
    padding: 0 14px 64px;
  }}

  header {{
    position: relative;
    margin: 0 -14px 22px;
    padding: 30px 24px 22px;
    background: var(--card);
    border-bottom: 1px solid var(--rule);
    box-shadow: var(--shadow);
  }}
  header::after {{
    content: "";
    position: absolute; left: 0; right: 0; bottom: -7px; height: 7px;
    background: radial-gradient(circle at 7px 0, transparent 0 4.5px, var(--card) 5px) repeat-x;
    background-size: 14px 7px;
  }}
  .seal {{
    display: inline-flex; align-items: center; gap: 8px;
    font-size: 11px; letter-spacing: .18em;
    color: var(--stamp);
    border: 1px solid var(--stamp);
    border-radius: 999px;
    padding: 5px 11px 4px;
    margin-bottom: 16px;
  }}
  .seal svg {{ width: 12px; height: 12px; }}
  h1 {{
    margin: 0;
    font-size: clamp(30px, 8.5vw, 46px);
    line-height: .96;
    text-wrap: balance;
  }}
  h1 em {{ display: block; font-style: normal; color: var(--stamp); }}
  .dek {{
    margin: 14px 0 0;
    max-width: 46ch;
    font-size: 15px;
    line-height: 1.5;
    color: var(--ink-soft);
  }}

  .steps {{
    display: flex; flex-wrap: wrap; gap: 6px 18px;
    margin: 18px 0 0; padding: 14px 0 0;
    border-top: 1px solid var(--rule);
    list-style: none;
    font-size: 12.5px; letter-spacing: .04em;
    color: var(--ink-soft);
  }}
  .steps li {{ display: flex; align-items: baseline; gap: 7px; }}
  .steps b {{ color: var(--stamp); font-size: 11px; letter-spacing: .1em; }}

  .instruction {{
    display: flex; align-items: baseline; justify-content: space-between; gap: 12px;
    padding-bottom: 8px; margin-bottom: 14px;
    border-bottom: 2px solid var(--ink);
    font-size: 12px; letter-spacing: .14em;
  }}
  .instruction span:last-child {{ color: var(--ink-soft); letter-spacing: .06em; }}

  .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }}

  .cand {{
    display: block; width: 100%; text-align: left;
    padding: 8px 8px 4px;
    background: var(--card);
    border: 1px solid var(--rule);
    border-radius: 3px;
    box-shadow: var(--shadow);
    cursor: pointer;
    font: inherit; color: inherit;
    transition: border-color .18s, transform .18s, box-shadow .18s;
  }}
  .cand:hover {{ border-color: var(--stamp); }}
  .cand:focus-visible {{ outline: 3px solid var(--stamp); outline-offset: 2px; }}
  .cand[aria-checked="true"] {{
    border-color: var(--stamp);
    box-shadow: inset 0 0 0 2px var(--stamp), var(--shadow);
    transform: translateY(-2px);
  }}

  .portrait {{ position: relative; display: block; }}
  .portrait img {{
    display: block; width: 100%; max-width: 100%; aspect-ratio: 44/46;
    object-fit: cover; border-radius: 2px;
    filter: saturate(.96);
  }}
  .cand[aria-checked="true"] .portrait img {{ filter: none; }}
  .num {{
    position: absolute; top: 7px; left: 7px;
    width: 27px; height: 27px; border-radius: 50%;
    display: grid; place-items: center;
    background: var(--card); color: var(--ink);
    font-family: ui-monospace, "SF Mono", Menlo, monospace;
    font-size: 13px; font-weight: 700;
    border: 1px solid var(--rule);
  }}
  .chip {{
    position: absolute; top: 8px; right: 7px;
    background: var(--stamp); color: #fff;
    font-size: 9px; letter-spacing: .12em; text-transform: uppercase;
    padding: 3px 7px; border-radius: 999px;
  }}
  .row {{ display: flex; align-items: center; gap: 8px; padding: 9px 3px 8px; }}
  .oval {{
    flex: none; width: 20px; height: 13px; border-radius: 999px;
    border: 1.5px solid var(--ink-soft);
    position: relative;
  }}
  .cand[aria-checked="true"] .oval {{ border-color: var(--stamp); background: var(--stamp); }}
  .cname {{
    font-size: 13px; line-height: 1.2; letter-spacing: .01em; font-weight: 600;
  }}

  .ballot-foot {{
    margin-top: 26px; padding-top: 16px;
    border-top: 1px solid var(--rule);
    font-size: 12px; color: var(--ink-soft); line-height: 1.6;
  }}

  .cast {{
    position: fixed; z-index: 15;
    left: 50%; transform: translateX(-50%);
    bottom: max(10px, env(safe-area-inset-bottom));
    width: min(652px, calc(100vw - 20px));
    padding: 16px;
    background: var(--card);
    border: 1px solid var(--stamp);
    border-radius: 4px;
    box-shadow: 0 14px 34px -20px rgba(0,0,0,.6);
  }}
  .cast[hidden] {{ display: none; }}
  .cast-head {{
    display: flex; align-items: center; gap: 10px;
    font-size: 11px; letter-spacing: .16em; color: var(--ink-soft);
  }}
  .cast-pick {{ margin: 8px 0 14px; font-size: 19px; line-height: 1.15; }}
  .cast-pick b {{ color: var(--stamp); }}
  .actions {{ display: flex; gap: 9px; flex-wrap: wrap; }}
  button.act {{
    font: inherit; font-size: 14px; font-weight: 600;
    padding: 12px 18px; border-radius: 999px; cursor: pointer;
    border: 1px solid var(--stamp);
    transition: opacity .15s, background .15s;
  }}
  button.act:focus-visible {{ outline: 3px solid var(--stamp); outline-offset: 2px; }}
  .primary {{ background: var(--stamp); color: #fff; flex: 1 1 auto; }}
  .ghost {{ background: transparent; color: var(--stamp); }}
  button.act:active {{ opacity: .8; }}

  .stamp {{
    position: fixed; inset: 0; display: grid; place-items: center;
    pointer-events: none; z-index: 20;
  }}
  .stamp[hidden] {{ display: none; }}
  .stamp b {{
    font-family: Futura, "Futura PT", "Century Gothic", system-ui, sans-serif;
    text-transform: uppercase; letter-spacing: .12em;
    font-size: clamp(30px, 11vw, 62px);
    color: var(--stamp);
    border: 5px solid var(--stamp);
    border-radius: 8px;
    padding: 12px 26px;
    background: var(--stamp-soft);
    transform: rotate(-11deg);
    animation: thud .5s cubic-bezier(.2,1.5,.4,1);
  }}
  @keyframes thud {{
    from {{ transform: rotate(-30deg) scale(2.4); opacity: 0; }}
    to   {{ transform: rotate(-11deg) scale(1); opacity: 1; }}
  }}
  @media (prefers-reduced-motion: reduce) {{
    .stamp b {{ animation: none; }}
    .cand {{ transition: none; }}
  }}
  body.voted {{ padding-bottom: 190px; }}
  @media (min-width: 560px) {{
    .grid {{ grid-template-columns: repeat(4, 1fr); }}
    .cname {{ font-size: 12.5px; }}
  }}
</style>

<div class="sheet">
  <header>
    <div class="seal display">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="M4 20h16M6 16l6-12 6 12"/></svg>
      Household Ballot No. 1
    </div>
    <h1 class="display">Leo's hair<em>the family vote</em></h1>
    <p class="dek">Eight cuts made the shortlist. Pick the one Leo should walk out of the barber with. One vote each — then send it back to the group chat so it counts.</p>
    <ol class="steps display">
      <li><b>01</b> Tap a cut</li>
      <li><b>02</b> Copy your vote</li>
      <li><b>03</b> Paste it in the chat</li>
    </ol>
  </header>

  <div class="instruction display">
    <span>Vote for one</span>
    <span class="mono" id="status">no selection</span>
  </div>

  <div class="grid" role="radiogroup" aria-label="Hairstyle options">
{cards}
  </div>

  <p class="ballot-foot">Options 1–3 were flagged as most flattering by the salon analysis; 4–8 were rated solid alternatives. The bowl cut, the buzz and the gelled spikes did not make the ballot, and that is final.</p>

  <div class="cast" id="cast" hidden>
    <div class="cast-head display"><span>Your ballot</span></div>
    <p class="cast-pick">You picked <b id="pick">—</b></p>
    <div class="actions">
      <button class="act primary" type="button" id="copy">Copy my vote</button>
      <button class="act ghost" type="button" id="clear">Change it</button>
    </div>
  </div>
</div>

<div class="stamp" id="stampEl" hidden><b>Voted</b></div>

<script>
  var cands = Array.prototype.slice.call(document.querySelectorAll('.cand'));
  var cast = document.getElementById('cast');
  var pickEl = document.getElementById('pick');
  var statusEl = document.getElementById('status');
  var copyBtn = document.getElementById('copy');
  var stampEl = document.getElementById('stampEl');
  var KEY = 'leo-hair-ballot';
  var current = null;

  function render(stamp) {{
    cands.forEach(function (c) {{
      var on = c.dataset.n === current;
      c.setAttribute('aria-checked', on ? 'true' : 'false');
    }});
    document.body.classList.toggle('voted', !!current);
    if (!current) {{
      cast.hidden = true;
      statusEl.textContent = 'no selection';
      return;
    }}
    var el = cands.filter(function (c) {{ return c.dataset.n === current; }})[0];
    pickEl.textContent = '#' + current + ' ' + el.dataset.name;
    statusEl.textContent = 'no. ' + current + ' selected';
    cast.hidden = false;
    copyBtn.textContent = 'Copy my vote';
    if (stamp) {{
      stampEl.hidden = false;
      clearTimeout(render._t);
      render._t = setTimeout(function () {{ stampEl.hidden = true; }}, 850);
    }}
  }}

  cands.forEach(function (c) {{
    c.addEventListener('click', function () {{
      var changed = current !== c.dataset.n;
      current = c.dataset.n;
      try {{ localStorage.setItem(KEY, current); }} catch (e) {{}}
      render(changed);
    }});
  }});

  document.getElementById('clear').addEventListener('click', function () {{
    current = null;
    try {{ localStorage.removeItem(KEY); }} catch (e) {{}}
    render(false);
    window.scrollTo({{ top: 0, behavior: 'smooth' }});
  }});

  copyBtn.addEventListener('click', function () {{
    var el = cands.filter(function (c) {{ return c.dataset.n === current; }})[0];
    if (!el) return;
    var text = 'My vote for Leo\\u2019s hair: #' + current + ' \\u2014 ' + el.dataset.name;
    var done = function () {{
      copyBtn.textContent = 'Copied \\u2014 now paste it in the chat';
      setTimeout(function () {{ copyBtn.textContent = 'Copy my vote'; }}, 2600);
    }};
    if (navigator.clipboard && navigator.clipboard.writeText) {{
      navigator.clipboard.writeText(text).then(done, fallback);
    }} else {{ fallback(); }}
    function fallback() {{
      var ta = document.createElement('textarea');
      ta.value = text; ta.setAttribute('readonly', '');
      ta.style.position = 'fixed'; ta.style.top = '-1000px';
      document.body.appendChild(ta); ta.select();
      try {{ document.execCommand('copy'); done(); }}
      catch (e) {{ copyBtn.textContent = 'Copy this: ' + text; }}
      document.body.removeChild(ta);
    }}
  }});

  try {{
    var saved = localStorage.getItem(KEY);
    if (saved && cands.some(function (c) {{ return c.dataset.n === saved; }})) {{
      current = saved;
    }}
  }} catch (e) {{}}
  render(false);
</script>'''

open('leo-hair-poll.html','w').write(page)
print(len(page)/1024, 'KB')
