// Stills for checking the cut: node preview.js out.jpg 1.0 2.1 3.3 ...  (a contact sheet of those moments)
const { chromium } = require('playwright');
const { execFileSync } = require('child_process');
const path = require('path'), fs = require('fs'), os = require('os');
(async () => {
  const [out, ...times] = process.argv.slice(2);
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'nxprev-'));
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  p.on('console', m => m.type() === 'error' && console.log('console:', m.text()));
  p.on('pageerror', e => console.log('pageerror:', e.message));
  await p.goto('file://' + path.join(__dirname, 'showreel.html'));
  await p.evaluate(() => window.ready());
  const files = [];
  for (const t of times) {
    await p.evaluate(t => window.render(t), +t);
    const f = path.join(tmp, `${String(files.length).padStart(3, '0')}.jpg`);
    await p.screenshot({ path: f, type: 'jpeg', quality: 85 });
    files.push(f);
  }
  await b.close();
  const cols = Math.min(6, files.length), rows = Math.ceil(files.length / cols);
  const args = ['-loglevel', 'error', '-y'];
  files.forEach(f => args.push('-i', f));
  const scaled = files.map((_, i) => `[${i}]scale=270:480,drawtext=text='${times[i]}':x=8:y=8:fontsize=28:fontcolor=yellow[v${i}]`).join(';');
  const layout = files.map((_, i) => `${(i % cols) * 270}_${Math.floor(i / cols) * 480}`).join('|');
  args.push('-filter_complex', `${scaled};${files.map((_, i) => `[v${i}]`).join('')}xstack=inputs=${files.length}:layout=${layout}:fill=black`, out);
  if (files.length === 1) execFileSync('ffmpeg', ['-loglevel', 'error', '-y', '-i', files[0], out]);
  else execFileSync('ffmpeg', args);
  console.log('wrote', out);
})();
