from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# Lock the gateway directly in its own class from first paint.
s = s.replace('<section class="salaam-section" id="salaamSection"', '<section class="salaam-section gateway-locked" id="salaamSection"', 1)

style = r'''
  <style id="hard-gateway-lock-fix">
    #salaamSection.gateway-locked{
      visibility:hidden!important;
      opacity:0!important;
      pointer-events:none!important;
    }
    #salaamSection.gateway-ready{
      visibility:visible!important;
      opacity:1!important;
      pointer-events:auto!important;
      transition:opacity .55s cubic-bezier(.22,.8,.2,1);
    }
    html.intro-lock,html.intro-lock body{overflow:hidden!important;overscroll-behavior:none}
    #intro{background:#0b0907!important}
    #intro::marker{display:none}
    @media(prefers-reduced-motion:reduce){
      #salaamSection.gateway-locked{visibility:hidden!important;opacity:0!important;pointer-events:none!important}
    }
  </style>
'''
if 'id="hard-gateway-lock-fix"' not in s:
    s = s.replace('</head>', style + '</head>', 1)

old = "let introPlayed=false;function playIntro(){if(introPlayed)return;introPlayed=true;const intro=$('intro'),one=$('introStageOne'),two=$('introStageTwo');if(window.matchMedia('(prefers-reduced-motion: reduce)').matches){document.body.classList.remove('intro-sequence-active');intro.classList.add('hidden','sequence-gone');return}document.body.classList.add('intro-sequence-active');window.scrollTo(0,0);one.classList.remove('exit');two.classList.remove('show','exit');intro.classList.remove('hidden','sequence-gone');setTimeout(()=>one.classList.add('exit'),2800);setTimeout(()=>two.classList.add('show'),3400);setTimeout(()=>two.classList.add('exit'),6900);setTimeout(()=>intro.classList.add('hidden'),7750);setTimeout(()=>{intro.classList.add('sequence-gone');document.body.classList.remove('intro-sequence-active');window.scrollTo(0,0)},8900)}"
new = "let introPlayed=false;function playIntro(){if(introPlayed)return;introPlayed=true;const intro=$('intro'),one=$('introStageOne'),two=$('introStageTwo'),gateway=$('salaamSection');const reduced=window.matchMedia('(prefers-reduced-motion: reduce)').matches;document.documentElement.classList.add('intro-lock');document.body.classList.add('intro-sequence-active');if(gateway){gateway.classList.add('gateway-locked');gateway.classList.remove('gateway-ready')}window.scrollTo(0,0);one.classList.remove('exit');two.classList.remove('show','exit');intro.classList.remove('hidden','sequence-gone');if(reduced){setTimeout(()=>{intro.classList.add('hidden','sequence-gone');if(gateway){gateway.classList.remove('gateway-locked');gateway.classList.add('gateway-ready')}document.body.classList.remove('intro-sequence-active');document.documentElement.classList.remove('intro-lock');window.scrollTo(0,0)},250);return}setTimeout(()=>one.classList.add('exit'),2800);setTimeout(()=>two.classList.add('show'),3400);setTimeout(()=>two.classList.add('exit'),6900);setTimeout(()=>intro.classList.add('hidden'),7750);setTimeout(()=>{intro.classList.add('sequence-gone');if(gateway){gateway.classList.remove('gateway-locked');gateway.classList.add('gateway-ready')}document.body.classList.remove('intro-sequence-active');document.documentElement.classList.remove('intro-lock');window.scrollTo(0,0);window.dispatchEvent(new Event('resize'))},8900)}"
if old not in s:
    raise SystemExit('Expected current intro block not found; refusing to patch')
s = s.replace(old, new, 1)

# Make BFCache/pageshow reset deterministic instead of leaving prior end-state visible.
old2 = "window.addEventListener('load',playIntro);window.addEventListener('pageshow',playIntro);"
new2 = "window.addEventListener('load',playIntro);window.addEventListener('pageshow',e=>{if(e.persisted){introPlayed=false;playIntro()}else{playIntro()}});"
s = s.replace(old2, new2, 1)

p.write_text(s, encoding='utf-8')
