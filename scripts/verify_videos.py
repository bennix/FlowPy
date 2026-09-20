"""Validate the completed demonstrations and generate a local video gallery."""
import html
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
VIDEOS = ROOT / 'videos'
plans = json.loads((VIDEOS / 'plans.json').read_text())
feature_plans = VIDEOS / 'feature-plans.json'
if feature_plans.exists():
    plans += json.loads(feature_plans.read_text())
entries = []
for plan in plans:
    slug = plan['slug']
    timeline = json.loads((VIDEOS / f'{slug}.timeline.json').read_text())
    assert all(timeline['proof'][key] for key in ('startedEmpty', 'uiConstructed', 'expectedMatched'))
    assert len(timeline['steps']) == len(plan['steps'])
    assert timeline['steps'][0]['action'] == 'start'
    for previous, current in zip(timeline['steps'], timeline['steps'][1:]):
        assert current['start'] >= previous['audio_end'] + .4
    media = json.loads(subprocess.check_output([
        'ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json',
        str(VIDEOS / f'{slug}.mp4')], text=True))
    video = next(s for s in media['streams'] if s['codec_type'] == 'video')
    audio = next(s for s in media['streams'] if s['codec_type'] == 'audio')
    assert (video['width'], video['height'], video['codec_name']) == (1920, 1080, 'h264')
    assert audio['codec_name'] == 'aac'
    assert abs(float(media['format']['duration']) - timeline['duration']) < .1
    entries.append({'slug': slug, 'name': plan['name'], 'duration': timeline['duration'],
                    'steps': len(timeline['steps']), 'verified': True, 'group': plan.get('group')})
(VIDEOS / 'manifest.json').write_text(json.dumps(entries, ensure_ascii=False, indent=2))
cards = []
for entry in entries:
    slug = entry['slug']
    cards.append(f'''<article><h2>{html.escape(entry['name'])}</h2>
<p>{entry['duration'] / 60:.1f} 分钟 · {entry['steps']} 步 · 已运行验证</p>
<video controls preload="none" src="{slug}.mp4"></video>
<p><a href="{slug}.mp4">打开 MP4</a> · <a href="{slug}.srt">中文字幕</a></p></article>''')
(VIDEOS / 'index.html').write_text(('''<!doctype html><html lang="zh-CN"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>FlowPy 从空画布搭建 · {count} 个实例</title>
<style>body{background:#101916;color:#e3eae5;font:16px system-ui;max-width:1400px;margin:40px auto;padding:0 24px}h1{font-size:32px}p{color:#b8ccc1}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(420px,1fr));gap:24px}article{background:#1b2922;border:1px solid #34483c;padding:20px;border-radius:14px}h2{font-size:20px}video{width:100%;aspect-ratio:16/9;background:#080e0a}a{color:#a7ebc5}@media(max-width:500px){main{grid-template-columns:1fr}}</style>
<h1>FlowPy · 从空画布开始</h1><p>{count} 个独立例子。每个从零节点、零连线开始，选择节点、填写参数、连接端口，并实际运行。</p>
<p>Microsoft Edge TTS 中文解说 · 1080p MP4 · 上一步解说结束后才出现下一步操作。</p>
<main>'''.replace('{count}', str(len(entries))) + '\n'.join(cards) + '</main></html>'))
print(f'PASS: {len(entries)} videos; {sum(e["duration"] for e in entries)/60:.2f} minutes; all narration gaps >= 0.4 seconds')
