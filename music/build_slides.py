import json,html
from pathlib import Path
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parent
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
 page=b.new_page(viewport={'width':1440,'height':1100},device_scale_factor=1)
 page.goto((root/'index.html').as_uri())
 page.locator('.editor').screenshot(path=str(root/'illustrations/png/editor-detail.png'))
 page.locator('.compare').screenshot(path=str(root/'illustrations/png/chords-detail.png'))
 b.close()
slides=[]
def slide(num,title,lead,body,shot,note):
 body='<br>'.join('<span>'+part+'</span>' for part in body.split('<br>'))
 d=f'''<div style="position:absolute;inset:0;background:#f6f7f2;color:#163b39;font-family:Arial,sans-serif;padding:34px 40px;box-sizing:border-box">
 <div style="display:flex;align-items:center;justify-content:space-between"><img src="/assets/bala.svg" style="width:42px;height:38px;object-fit:contain"><div style="font-size:12px;font-weight:700;letter-spacing:2px">BALA CITY · МУЗЫКАЛЬНАЯ ЛАБОРАТОРИЯ</div><div style="font-size:14px;font-weight:700">shuvaev.com</div></div>
 <div style="font-size:32px;font-weight:700;line-height:1.15;margin-top:24px">{title}</div>
 <div style="display:flex;gap:26px;margin-top:22px;height:326px"><div style="width:330px;flex-shrink:0"><div style="font-size:12px;font-weight:700;letter-spacing:1px;background:#fcc900;padding:9px 12px;border-radius:8px;margin-bottom:16px">{lead}</div><div style="font-size:19px;line-height:1.5">{body}</div></div><div style="flex:1;background:#fff;border:1px solid #dce3dc;border-radius:14px;padding:12px;display:flex;align-items:center;justify-content:center"><img src="/illustrations/png/{shot}" style="width:100%;max-height:298px;object-fit:contain" alt="Скриншот музыкального интерактивного тренажёра"></div></div><div style="position:absolute;bottom:20px;left:40px;right:40px;display:flex;justify-content:space-between;font-size:12px;color:#647471"><span>{note}</span><span>{num:02d} / 03</span></div></div>'''
 slides.append({'id':f'bala_music_{num:02d}','layout':'fullpage','content_bg':False,'diagram':d,'notes':note})
slide(1,'Музыку можно собрать руками','ПРОМПТ → РАБОЧИЙ Интерактивный тренажёр','Создай пианино и сетку нот.<br><br>Дай готовые аккорды, перетаскивание точек, темп, воспроизведение и очистку.<br><br>Всё — в одном HTML-файле.','editor-detail.png','Демонстрация: запустить C–Am–F–G, затем передвинуть одну ноту.')
slide(2,'Мажор → минор: меняется одна нота','ПОСЛУШАТЬ И СРАВНИТЬ','До мажор: до–ми–соль.<br>До минор: до–ми♭–соль.<br><br>Опустите среднюю ноту на полутон.<br><br>Основание и вершина трезвучия остаются прежними.','chords-detail.png','Ноты одной вертикали звучат вместе; разные позиции — последовательно.')
slide(3,'От готового примера — к своему','ПРАКТИКА ДЛЯ УЧИТЕЛЯ','Откройте тренажёр и скопируйте полный промпт в DeepSeek.<br><br>Проверьте звук, движение нот и остановку.<br><br>Задание ученику: собрать мелодию и изменить её характер.','music-trainer.png','Материалы: index.html → «Тренажёр промптов». Скриншоты сняты с работающего примера.')
(root/'decks/music.json').write_text(json.dumps({'title':'Bala City · Звуки, ноты и аккорды','slides':slides},ensure_ascii=False,indent=2))
(root/'slide_tool_config.json').write_text(json.dumps({'schema':'slide-hub/1','id':'bala_city_music','title':'Bala City · Музыка','decks_dir':'decks','mounts':{'assets':'assets','illustrations':'illustrations'},'brand':{'accent':'#fcc900','bg':'#f6f7f2'},'writable':False},ensure_ascii=False,indent=2))
rendered=''.join('<section class="slide">'+s['diagram'].replace('src="/','src="')+'</section>' for s in slides)
(root/'slides.html').write_text('''<!doctype html><html lang="ru"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Bala City · Музыка · Слайды</title><style>*{box-sizing:border-box}body{margin:0;background:#dce3dc;font:16px Arial}nav{padding:18px;text-align:center}a{color:#163b39}.slide{width:960px;height:540px;position:relative;margin:24px auto;overflow:hidden;box-shadow:0 10px 30px #163b3920}@media print{nav{display:none}.slide{margin:0;page-break-after:always;box-shadow:none}@page{size:960px 540px;margin:0}}</style><nav><a href="index.html">← Открыть интерактивный тренажёр и тренажёр</a> · Три слайда для основной презентации</nav>'''+rendered+'</html>')
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
 page=b.new_page(viewport={'width':1100,'height':700},device_scale_factor=2)
 page.goto((root/'slides.html').as_uri())
 for i,s in enumerate(page.locator('.slide').all()):
  s.screenshot(path=str(root/f'illustrations/png/slide-{i+1}.png'))
 assert page.locator('img').evaluate_all('(imgs)=>imgs.every(i=>i.complete&&i.naturalWidth>0)')
 page.pdf(path=str(root/'music-slides.pdf'),prefer_css_page_size=True,print_background=True)
 b.close()
print('Built 3 slides, JSON, HTML, PDF and screenshots')
