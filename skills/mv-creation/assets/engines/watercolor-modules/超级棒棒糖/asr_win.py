import sys, os, numpy as np, wave, sherpa_onnx
from pathlib import Path
from scipy.signal import resample_poly
sv=os.environ.get('MV_SENSEVOICE_DIR', str(Path.home() / '.cache' / 'mv-creation' / 'models' / 'sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2024-07-17'))
rec=sherpa_onnx.OfflineRecognizer.from_sense_voice(model=sv+'/model.int8.onnx',tokens=sv+'/tokens.txt',use_itn=False,language='zh',num_threads=2)
w=wave.open(sys.argv[1]); sr=w.getframerate(); ch=w.getnchannels()
a=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float32)/32768
a=a.reshape(-1,ch).mean(1); a=resample_poly(a,16000,sr).astype(np.float32); a/= (np.abs(a).max()*1.1)
win=float(sys.argv[2]); step=float(sys.argv[3])
t=0
while t < len(a)/16000-1:
    s=rec.create_stream(); seg=a[int(t*16000):int((t+win)*16000)]
    s.accept_waveform(16000,seg); rec.decode_stream(s); r=s.result
    print(f"{t:5.1f}-{t+win:5.1f}: ", ' '.join(f"{tok}@{t+ts:.2f}" for tok,ts in zip(r.tokens,r.timestamps) if not tok.startswith('<')))
    t+=step
