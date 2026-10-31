S=/tmp/claude-0/-home-user/d683bb50-b1f3-59a3-8e5f-5f21e64e8c5a/scratchpad/gh; cd $S; D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 grad_v.mp4); python3 - <<EOF
import json, numpy as np, wave
R=44100; D=float("$D"); L=json.load(open('grad_log.json')); OFF=0.85
N=int(R*(D+1)); out=np.zeros(N)
def env(n,a=.01,r=3): t=np.arange(n)/R; return np.minimum(1,t/a)*np.exp(-t*r)
def tone(t0,f,dur,v=.2,kind='sine',dec=3):
    i=int(max(0,t0)*R); n=int(dur*R); t=np.arange(n)/R
    w=np.sin(2*np.pi*f*t) if kind=='sine' else (2*np.abs(2*((f*t)%1)-1)-1)
    s=w*env(n,r=dec)*v; j=min(N,i+n); out[i:j]+=s[:j-i]
def noise(t0,dur,v=.2,lp=0.3):
    i=int(t0*R); n=int(dur*R); x=np.random.randn(n)
    for k in range(1,n): x[k]=x[k-1]*(1-lp)+x[k]*lp
    s=x*np.hanning(n)*v; j=min(N,i+n); out[i:j]+=s[:j-i]
nt=lambda m:440*2**((m-69)/12)
ev={}
for t,k in L: ev.setdefault(k,[]).append(t-OFF)
t_open=ev['open'][0]; t_asc=ev['ascend'][0]; t_bell=ev['bell'][0]; t_hi=ev['hi'][0]; t_memo=ev['memo'][0]
M=[72,76,79,77,76,72,74,0,71,74,77,76,74,71,72,0,69,72,76,74,72,69,71,0,67,71,74,72,0,0]
t=t_open; i=0
while t<D-1:
    step=.5 if t<t_memo else .62
    if t_asc-0.5<t<t_asc+0.2: t+=step; continue
    m=M[i%len(M)]
    if m: tone(t,nt(m),1.4,.10,'sine',2.2); tone(t,nt(m+12),.6,.03,'tri',4)
    if i%4==0: tone(t,nt(48 if (i//4)%2==0 else 43),2.0,.05,'sine',1.2)
    t+=step; i+=1
for t in ev.get('card',[])+ev.get('memo',[]): [tone(t+k*.07,f,.5,.06,'tri',5) for k,f in enumerate((1047,1319,1568))]
for t in ev.get('pick',[]): tone(t,880,.3,.05,'tri',6)
noise(t_hi+.5,.35,.5,.5); [tone(t_hi+.7+k*.06,f,.6,.08,'tri',4) for k,f in enumerate((1568,2093,2637,3136))]
for k in range(14): tone(t_asc+k*.14, 1046*2**(k/12), 1.2, .05, 'tri', 2)
noise(t_asc,3.5,.08,.05)
for f,v in ((130.8,.35),(261.6,.18),(392,.08),(523,.05)): tone(t_bell,f,5,v,'sine',.7)
out=out/np.max(np.abs(out))*.85
w=wave.open('grad.wav','w'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(R); w.writeframes((out*32767).astype(np.int16).tobytes()); w.close()
EOF
ffmpeg -loglevel error -y -i grad_v.mp4 -i grad.wav -map 0:v -map 1:a -c:v copy -af "loudnorm=I=-15:TP=-1:LRA=11" -c:a aac -b:a 160k -ar 44100 -shortest -movflags +faststart grad.mp4
