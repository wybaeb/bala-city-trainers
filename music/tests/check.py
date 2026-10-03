from pathlib import Path
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':1440,'height':1100},device_scale_factor=1)
 errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto((root/'index.html').as_uri())
 assert page.locator('.dot').count()==12
 page.screenshot(path=str(root/'illustrations/png/music-editor.png'),full_page=True)
 page.get_by_role('button',name='Очистить',exact=True).click()
 assert page.locator('.dot').count()==0
 page.get_by_role('button',name='Cm · До минор',exact=True).click()
 assert page.evaluate('notes.map(n=>n.midi)')==[60,63,67]
 assert page.evaluate('notes.every(n=>n.len===4)')
 page.screenshot(path=str(root/'illustrations/png/music-minor.png'),full_page=True)
 dot=page.locator('.dot[data-id]').filter(has_text='').first
 # Move G4 up one semitone with keyboard, then move back.
 dot.first.focus();page.keyboard.press('ArrowUp')
 assert 68 in page.evaluate('notes.map(n=>n.midi)')
 page.keyboard.press('ArrowDown')
 assert 67 in page.evaluate('notes.map(n=>n.midi)')
 # Drag E-flat to E: Cm becomes C.
 source=page.locator('.cell[data-midi="63"][data-step="0"] .dot').bounding_box()
 target=page.locator('.cell[data-midi="64"][data-step="0"]').bounding_box()
 page.mouse.move(source['x']+10,source['y']+5);page.mouse.down()
 page.mouse.move(target['x']+15,target['y']+8,steps=5);page.mouse.up()
 assert sorted(page.evaluate('notes.map(n=>n.midi)'))==[60,64,67]
 page.get_by_role('button',name='▶ Играть',exact=True).click();page.wait_for_timeout(180)
 assert page.evaluate('playing && voices.size===3')
 assert page.evaluate("ctx.state==='running'")
 assert page.locator('.cell.playing').count()==20
 page.get_by_role('button',name='■ Стоп',exact=True).click()
 assert page.evaluate('!playing && voices.size===0')
 page.get_by_role('button',name='Удалить выбранную',exact=True).click()
 assert page.locator('.dot').count()==2
 page.get_by_role('button',name='▶ Загадать аккорд',exact=True).click()
 answer=page.evaluate('question');page.locator('[data-answer="'+answer+'"]').click()
 assert 'Верно' in page.locator('#feedback').inner_text()
 # Four-beat chord placement at last beat is bounded to grid.
 page.get_by_role('button',name='Такт 4, доля 4',exact=True).click()
 page.get_by_role('button',name='G · Соль мажор',exact=True).click()
 assert page.evaluate('notes.filter(n=>n.step===15).every(n=>n.len===1)')
 page.get_by_role('button',name='Пример C–Am–F–G',exact=True).click()
 page.locator('#trainTab').click();page.screenshot(path=str(root/'illustrations/png/music-trainer.png'),full_page=True)
 page.locator('#exTab').click();page.set_viewport_size({'width':390,'height':844})
 assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
 page.screenshot(path=str(root/'illustrations/png/music-mobile.png'),full_page=True)
 # Touch pointer path using an actual touch-enabled mobile context.
 mobile=browser.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True)
 mp=mobile.new_page();mp.goto((root/'index.html').as_uri())
 mp.get_by_role('button',name='Очистить',exact=True).tap()
 mp.locator('.cell[data-midi="70"][data-step="0"]').tap()
 assert mp.locator('.dot').count()==1
 assert not errors,errors
 browser.close()
print('PASS: presets, durations, editing, drag, keyboard, audio graph, playback, stop, quiz, boundaries, mobile tap, no JS errors')
