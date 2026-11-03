// Renders showreel.html to nexora-promo.mp4: 1080x1920, 30 fps, 20 s, with real motion blur
// (each output frame averages SUB sub-frames spread over a 180-degree shutter) and soundtrack.wav.
// Usage: node render.js [workers=4] [sub=4]
const { chromium } = require('playwright');
const { spawn, execFileSync } = require('child_process');
const path = require('path'), fs = require('fs');

const FPS = 30, DUR = 20, FRAMES = FPS * DUR;
const WORKERS = +(process.argv[2] || 4), SUB = +(process.argv[3] || 4), SHUTTER = .5;
const dir = __dirname, tmp = path.join(dir, 'cache', 'segments');
fs.mkdirSync(tmp, { recursive: true });

async function worker(w, from, to, browser) {
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  page.on('pageerror', e => console.log(`[w${w}] pageerror`, e.message));
  await page.goto('file://' + path.join(dir, 'showreel.html'));
  await page.evaluate(() => window.ready());
  const out = path.join(tmp, `seg${w}.mp4`);
  const vf = SUB > 1 ? `tmix=frames=${SUB},select='eq(mod(n\\,${SUB})\\,${SUB - 1})',setpts=N/(${FPS}*TB)` : 'setpts=N/(30*TB)';
  const ff = spawn('ffmpeg', ['-loglevel', 'error', '-y', '-f', 'image2pipe', '-c:v', 'mjpeg', '-framerate', String(FPS * SUB), '-i', '-',
    '-vf', `${vf},format=yuv420p`, '-r', String(FPS), '-c:v', 'libx264', '-preset', 'medium', '-crf', '14', '-x264-params', 'keyint=30', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  const t0 = Date.now();
  for (let f = from; f < to; f++) {
    for (let s = 0; s < SUB; s++) {
      const off = SUB > 1 ? (s / (SUB - 1) - .5) * SHUTTER : 0;
      const t = Math.max(0, Math.min(DUR - 1e-3, (f + off) / FPS));
      await page.evaluate(t => window.render(t), t);
      const buf = await page.screenshot({ type: 'jpeg', quality: 93 });
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    }
    if ((f - from) % 30 === 0) console.log(`[w${w}] frame ${f} (${((Date.now() - t0) / 1000 / (f - from + 1)).toFixed(2)} s/frame)`);
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  await page.close();
  return out;
}

(async () => {
  const t0 = Date.now();
  const browsers = await Promise.all(Array.from({ length: WORKERS }, () => chromium.launch()));
  const per = Math.ceil(FRAMES / WORKERS);
  const segs = await Promise.all(browsers.map((b, w) => worker(w, w * per, Math.min(FRAMES, (w + 1) * per), b)));
  await Promise.all(browsers.map(b => b.close()));
  const list = path.join(tmp, 'list.txt');
  fs.writeFileSync(list, segs.map(s => `file '${s}'`).join('\n'));
  execFileSync('ffmpeg', ['-loglevel', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', list, '-i', path.join(dir, 'soundtrack.wav'),
    '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-af', 'loudnorm=I=-14:TP=-1:LRA=11', '-c:a', 'aac', '-b:a', '256k', '-ar', '48000',
    '-shortest', '-movflags', '+faststart', path.join(dir, 'nexora-promo.mp4')], { stdio: 'inherit' });
  console.log(`done in ${((Date.now() - t0) / 1000).toFixed(0)} s -> nexora-promo.mp4`);
})();
