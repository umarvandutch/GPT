from pathlib import Path
import re

current_path = Path('index.html')
backup_path = Path('/tmp/index-before-secondary.html')
s = current_path.read_text(encoding='utf-8')
old = backup_path.read_text(encoding='utf-8')

# Pull the exact original Salaam artwork/content block from the backup.
m = re.search(r'(\n\s*<div class="salaam-wrap">.*?</div>)\n\s*<button class="salaam-enter"', old, re.S)
if not m:
    raise SystemExit('Could not find original Salaam block in backup')
greeting = m.group(1).strip('\n')

# Restore the exact original Salaam block on the gateway page.
gateway_pattern = re.compile(r'\n\s*<div class="salaam-ornament salaam-page-ornament"[^>]*>.*?</div>\n\s*<button class="salaam-enter"', re.S)
if not gateway_pattern.search(s):
    raise SystemExit('Current gateway placeholder not found')
s = gateway_pattern.sub('\n' + greeting + '\n      <button class="salaam-enter"', s, count=1)

# Replace the middle transition contents with that same exact artwork/content block.
stage_pattern = re.compile(r'(\s*<div class="intro-stage two" id="introStageTwo">).*?(\n\s*</div>\n\s*</div>\n\n\s*<section class="salaam-section")', re.S)
stage_match = stage_pattern.search(s)
if not stage_match:
    raise SystemExit('Secondary intro stage not found')
new_stage = '''    <div class="intro-stage two" id="introStageTwo">
      <div class="secondary-salaam">
%s
      </div>
    </div>

  <section class="salaam-section"''' % greeting
s = stage_pattern.sub('\n' + new_stage, s, count=1)

# Replace the prior text-rendered transition styling. Child artwork keeps the exact
# same styles used by the original gateway; this only animates the whole block.
style_pattern = re.compile(r'\n\s*<style id="secondary-salaam-transition-style">.*?</style>', re.S)
new_style = r'''
  <style id="secondary-salaam-transition-style">
    .secondary-salaam{position:relative;z-index:2;display:grid;place-items:center;width:min(96vw,680px);padding:24px;text-align:center}
    .secondary-salaam::before{content:"";position:absolute;z-index:-1;width:min(72vw,620px);aspect-ratio:1;border-radius:50%;background:radial-gradient(circle,rgba(213,173,102,.08),transparent 68%);filter:blur(6px);pointer-events:none}
    .intro-stage.two .secondary-salaam .salaam-wrap{opacity:0;transform:translateY(12px) scale(.96);filter:blur(7px);transition:opacity 1s cubic-bezier(.22,.8,.2,1),transform 1s cubic-bezier(.22,.8,.2,1),filter 1s ease}
    .intro-stage.two.show .secondary-salaam .salaam-wrap{opacity:1;transform:none;filter:blur(0)}
    @media(max-width:600px){.secondary-salaam{width:96vw;padding:16px}}
    @media(prefers-reduced-motion:reduce){.intro-stage.two .secondary-salaam .salaam-wrap{opacity:1;transform:none;filter:none;transition:none}}
  </style>'''
if not style_pattern.search(s):
    raise SystemExit('Secondary transition style block not found')
s = style_pattern.sub('\n' + new_style, s, count=1)

current_path.write_text(s, encoding='utf-8')
