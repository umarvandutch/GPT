from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

css = '''
  <style id="secondary-salaam-transition-style">
    .secondary-salaam{position:relative;z-index:2;display:grid;justify-items:center;text-align:center;width:min(92vw,900px);padding:24px}
    .secondary-salaam::before{content:"";position:absolute;z-index:-1;width:min(72vw,620px);aspect-ratio:1;border-radius:50%;background:radial-gradient(circle,rgba(213,173,102,.1),transparent 68%);filter:blur(8px);opacity:.9}
    .secondary-salaam-ornament{display:flex;align-items:center;gap:18px;margin-bottom:clamp(18px,3vh,30px);color:rgba(240,212,155,.72);font-size:12px;opacity:0;transform:translateY(10px);transition:opacity .8s ease .05s,transform .8s ease .05s}
    .secondary-salaam-ornament::before,.secondary-salaam-ornament::after{content:"";width:clamp(46px,9vw,84px);height:1px;background:linear-gradient(90deg,transparent,rgba(240,212,155,.52))}.secondary-salaam-ornament::after{transform:scaleX(-1)}
    .secondary-arabic{direction:rtl;font-family:"Rakkas","Noto Nastaliq Urdu","Aref Ruqaa",serif;font-weight:400;font-size:clamp(76px,13vw,156px);line-height:1.2;padding:.05em .08em .18em;background:linear-gradient(120deg,#fff6df 0%,#f0d49b 23%,#c9984c 51%,#f0d49b 76%,#fff6df 100%);-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 12px 36px rgba(213,173,102,.3)) drop-shadow(0 0 70px rgba(240,212,155,.18));opacity:0;transform:translateY(14px) scale(.96);transition:opacity 1s cubic-bezier(.22,.8,.2,1) .12s,transform 1s cubic-bezier(.22,.8,.2,1) .12s}
    .secondary-latin{margin-top:clamp(6px,1.4vh,14px);font-family:"Italiana",serif;font-size:clamp(27px,4.6vw,46px);letter-spacing:.04em;color:var(--paper-soft);opacity:0;transform:translateY(12px);transition:opacity .9s ease .3s,transform .9s ease .3s}
    .secondary-peace{margin-top:clamp(10px,1.6vh,16px);font-size:clamp(9px,1.4vw,12px);letter-spacing:.3em;text-transform:uppercase;color:rgba(246,239,227,.46);opacity:0;transform:translateY(9px);transition:opacity .9s ease .45s,transform .9s ease .45s}
    .intro-stage.two.show .secondary-salaam-ornament,.intro-stage.two.show .secondary-arabic,.intro-stage.two.show .secondary-latin,.intro-stage.two.show .secondary-peace{opacity:1;transform:none}
    .salaam-page-ornament{margin:clamp(18px,3dvh,30px) 0 0}
    .salaam-section .salaam-enter{margin-top:clamp(30px,4dvh,44px)}
    @media(max-width:600px){.secondary-arabic{font-size:clamp(68px,20vw,104px)}.secondary-latin{font-size:clamp(25px,7.5vw,34px)}.secondary-peace{font-size:9px;letter-spacing:.27em}.secondary-salaam{padding:18px}}
    @media(prefers-reduced-motion:reduce){.secondary-salaam-ornament,.secondary-arabic,.secondary-latin,.secondary-peace{opacity:1;transform:none;transition:none}}
  </style>
'''
if 'secondary-salaam-transition-style' not in s:
    s = s.replace('</head>', css + '</head>', 1)

old_intro = '''  <div class="intro" id="intro" aria-hidden="true">
    <div class="intro-stage one" id="introStageOne">
      <div class="intro-inner">
        <div class="intro-line"></div>
        <div class="intro-monogram">U+A</div>
        <div class="intro-small">A wedding invitation</div>
        <div class="intro-title">Umar & Ansa</div>
      </div>
    </div>
  </div>'''
new_intro = '''  <div class="intro" id="intro" aria-hidden="true">
    <div class="intro-stage one" id="introStageOne">
      <div class="intro-inner">
        <div class="intro-line"></div>
        <div class="intro-monogram">U+A</div>
        <div class="intro-small">A wedding invitation</div>
        <div class="intro-title">Umar & Ansa</div>
      </div>
    </div>
    <div class="intro-stage two" id="introStageTwo">
      <div class="secondary-salaam">
        <div class="secondary-salaam-ornament" aria-hidden="true">✦</div>
        <div class="secondary-arabic" lang="ar" dir="rtl">السلام عليكم</div>
        <div class="secondary-latin">As-salāmu ʿalaykum</div>
        <div class="secondary-peace">Peace be upon you</div>
      </div>
    </div>
  </div>'''
if old_intro not in s:
    raise SystemExit('intro block not found')
s = s.replace(old_intro, new_intro, 1)

gateway_pattern = re.compile(r'\n\s*<div class="salaam-wrap">.*?<button class="salaam-enter"', re.S)
if not gateway_pattern.search(s):
    raise SystemExit('gateway greeting block not found')
s = gateway_pattern.sub('\n      <div class="salaam-ornament salaam-page-ornament" aria-hidden="true">✦</div>\n      <button class="salaam-enter"', s, count=1)

old_js = "let introPlayed=false;function playIntro(){if(introPlayed)return;introPlayed=true;const intro=$('intro'),one=$('introStageOne');setTimeout(()=>one.classList.add('exit'),1500);setTimeout(()=>intro.classList.add('hidden'),2350)}"
new_js = "let introPlayed=false;function playIntro(){if(introPlayed)return;introPlayed=true;const intro=$('intro'),one=$('introStageOne'),two=$('introStageTwo');setTimeout(()=>one.classList.add('exit'),2800);setTimeout(()=>two.classList.add('show'),3400);setTimeout(()=>two.classList.add('exit'),6900);setTimeout(()=>intro.classList.add('hidden'),7750)}"
if old_js not in s:
    raise SystemExit('intro timing script not found')
s = s.replace(old_js, new_js, 1)

p.write_text(s, encoding='utf-8')
