"""Edit real UI recordings; complete each Edge TTS segment before the next action."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import math
from pathlib import Path
import subprocess

from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
VIDEOS=ROOT/'videos'
FONT='/System/Library/Fonts/STHeiti Light.ttc'


def duration(path):
    return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(path)],text=True).strip())


def wrap(text,font,maxwidth):
    draw=ImageDraw.Draw(Image.new('RGB',(10,10)))
    lines=[];line=''
    for char in text:
        if draw.textlength(line+char,font=font)>maxwidth:
            lines.append(line);line=char
        else:line+=char
    if line:lines.append(line)
    return lines


def overlay(plan,index,path):
    im=Image.new('RGBA',(1920,1080),(0,0,0,0));draw=ImageDraw.Draw(im)
    draw.rectangle((0,0,1920,75),fill='#101916')
    draw.rectangle((0,990,1920,1080),fill='#101916')
    font=ImageFont.truetype(FONT,26);titlefont=ImageFont.truetype(FONT,28)
    draw.text((32,23),'FlowPy  /  '+plan['name'],font=titlefont,fill='#D5E9DD')
    right=f'{index+1:02d} / {len(plan["steps"]):02d}  ·  从零搭建'
    draw.text((1920-draw.textlength(right,font=font)-35,24),right,font=font,fill='#A7EBC5')
    lines=wrap(plan['steps'][index]['text'],font,1840)
    if len(lines)>2:
        font=ImageFont.truetype(FONT,22);lines=wrap(plan['steps'][index]['text'],font,1840)
    for i,line in enumerate(lines[:2]):
        draw.text(((1920-draw.textlength(line,font=font))/2,1000+i*32),line,font=font,fill='#E3EAE5')
    draw.rectangle((0,987,int(1920*(index+1)/len(plan['steps'])),990),fill='#A7EBC5')
    im.save(path)


def render(slug, plans_path=VIDEOS/'plans.json'):
    plans=json.loads(Path(plans_path).read_text());plan=next(p for p in plans if p['slug']==slug)
    markers=json.loads((VIDEOS/'raw'/(slug+'.steps.json')).read_text())
    raw=VIDEOS/'raw'/markers.get('raw_file',slug+'.mp4')
    meta=json.loads((VIDEOS/'raw'/markers.get('meta_file',slug+'.meta.json')).read_text())
    if not markers['proof']['startedEmpty'] or not markers['proof']['expectedMatched']:
        raise ValueError('未通过从空白搭建与运行验证')
    if len(markers['steps'])!=len(plan['steps']):raise ValueError('步骤数量不一致')
    folder=VIDEOS/'segments'/slug;folder.mkdir(parents=True,exist_ok=True)
    timeline=[];clock=0.0
    for step in markers['steps']:
        index=step['index'];audio=VIDEOS/'audio'/slug/f'{index:02}.mp3'
        audio_duration=duration(audio)
        # Start the intro on the verified empty canvas, after the New action finishes.
        start=step['end']-0.13 if step['action']=='start' else step['start']
        end=step['end']
        source_duration=max(.13,end-start)
        speed=2.5 if step['action'] in ('node','edge','enter','leave','stdin') else 1.0
        total=math.ceil(max(audio_duration+.75,source_duration*speed+.3)*30)/30
        info={'index':index,'action':step['action'],'text':plan['steps'][index]['text'],'source_start':max(0,start-meta['first_frame_epoch']),'source_duration':source_duration,'start':clock,'duration':total,'audio_start':clock+.15,'audio_end':clock+.15+audio_duration,'audio_duration':audio_duration,'speed_factor':speed}
        timeline.append(info);clock+=total
        overlay(plan,index,folder/f'{index:02}.png')
    def segment(info):
        i=info['index'];out=folder/f'{i:02}.mp4'
        video_filter=f"[0:v]setpts=(PTS-STARTPTS)*{info['speed_factor']},fps=30,scale=1920:914:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:76:color=0x101916,tpad=stop_mode=clone:stop_duration={info['duration']}[bg];[bg][2:v]overlay=0:0:shortest=1[v];[1:a]adelay=150:all=1,apad=pad_dur={info['duration']}[a]"
        command=['ffmpeg','-v','error','-y','-ss',str(info['source_start']),'-t',str(info['source_duration']),'-i',str(raw),'-i',str(VIDEOS/'audio'/slug/f'{i:02}.mp3'),'-loop','1','-i',str(folder/f'{i:02}.png'),'-filter_complex',video_filter,'-map','[v]','-map','[a]','-t',str(info['duration']),'-c:v','libx264','-threads','2','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-ar','48000','-r','30',str(out)]
        subprocess.run(command,check=True)
        return out
    with ThreadPoolExecutor(max_workers=3) as pool:
        outputs=list(pool.map(segment,timeline))
    concat=folder/'concat.txt';concat.write_text(''.join("file '%s'\n"%str(path) for path in outputs))
    output=VIDEOS/(slug+'.mp4')
    subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(concat),'-c','copy','-movflags','+faststart','-metadata','title=FlowPy · '+plan['name'],str(output)],check=True)
    for previous,current in zip(timeline,timeline[1:]):
        assert current['start']>=previous['audio_end']+.4
    report={'slug':slug,'name':plan['name'],'voice':'zh-CN-XiaoxiaoNeural','tts':'Microsoft Edge TTS','recording':'ScreenCaptureKit dedicated FlowPy window; actual CUA UI interactions','width':1920,'height':1080,'duration':duration(output),'steps':timeline,'proof':markers['proof'],'next_action_after_audio':True}
    (VIDEOS/(slug+'.timeline.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2))
    def srt_time(seconds):
        milliseconds=round(seconds*1000);hours,milliseconds=divmod(milliseconds,3600000);minutes,milliseconds=divmod(milliseconds,60000);seconds,milliseconds=divmod(milliseconds,1000)
        return f'{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}'
    (VIDEOS/(slug+'.srt')).write_text('\n\n'.join(f'{i+1}\n{srt_time(s["start"])} --> {srt_time(s["start"]+s["duration"])}\n{s["text"]}' for i,s in enumerate(timeline))+'\n')
    print('RENDERED',slug,report['duration'],flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--plans',default=str(VIDEOS/'plans.json'));parser.add_argument('slugs',nargs='+');args=parser.parse_args()
    for slug in args.slugs:render(slug, args.plans)
