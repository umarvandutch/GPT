from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

if '<body class="intro-sequence-active">' not in s:
    s = s.replace('<body>', '<body class="intro-sequence-active">', 1)

style = r'''
  <style id="transition-order-fix">
    body.intro-sequence-active{overflow:hidden}
    body.intro-sequence-active > .salaam-section,
    body.intro-sequence-active > .ambient,
    body.intro-sequence-active > .shell,
    body.intro-sequence-active > .toast{visibility:hidden!important}
    .intro{z-index:2147483000!important;isolation:isolate;background:radial-gradient(circle at 50% 45%,rgba(213,173,102,.075),transparent 28%),#0b0907!important}
    .intro::before,.intro::after{z-index:0}
    .intro-stage{z-index:2}
    .intro-stage.one{z-index:3}
    .intro-stage.one.exit{z-index:1}
    .intro-stage.two{z-index:2}
    .intro-stage.two.show{z-index:4}
    .intro.sequence-gone{display:none!important}
    @media(prefers-reduced-motion:reduce){
      body.intro-sequence-active{overflow:auto}
      body.intro-sequence-active > .salaam-section,
      body.intro-sequence-active > .ambient,
      body.intro-sequence-active > .shell,
      body.intro-sequence-active > .toast{visibility:visible!important}
    }
  </style>
'''
if 'id="transition-order-fix"' not in s:
    s = s.replace('</head>', style + '</head>', 1)

old = "let introPlayed=false;function playIntro(){if(introPlayed)return;introPlayed=true;const intro=$('intro'),one=$('introStageOne'),two=$('introStageTwo');setTimeout(()=>one.classList.add('exit'),2800);setTimeout(()=>two.classList.add('show'),3400);setTimeout(()=>two.classList.add('exit'),6900);setTimeout(()=>intro.classList.add('hidden'),7750)}"
new = "let introPlayed=false;function playIntro(){if(introPlayed)return;introPlayed=true;const intro=$('intro'),one=$('introStageOne'),two=$('introStageTwo');if(window.matchMedia('(prefers-reduced-motion: reduce)').matches){document.body.classList.remove('intro-sequence-active');intro.classList.add('hidden','sequence-gone');return}document.body.classList.add('intro-sequence-active');window.scrollTo(0,0);one.classList.remove('exit');two.classList.remove('show','exit');intro.classList.remove('hidden','sequence-gone');setTimeout(()=>one.classList.add('exit'),2800);setTimeout(()=>two.classList.add('show'),3400);setTimeout(()=>two.classList.add('exit'),6900);setTimeout(()=>intro.classList.add('hidden'),7750);setTimeout(()=>{intro.classList.add('sequence-gone');document.body.classList.remove('intro-sequence-active');window.scrollTo(0,0)},8900)}"
if old not in s:
    raise SystemExit('Expected intro timing block not found; no changes made')
s = s.replace(old, new, 1)

p.write_text(s, encoding='utf-8')
