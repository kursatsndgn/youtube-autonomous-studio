import React from 'react';
import {
  AbsoluteFill, Audio, Sequence, interpolate, spring, staticFile,
  useCurrentFrame, useVideoConfig,
} from 'remotion';
import timeline from '../public/yeniceri/timeline.json';

type Word = { w: string; s: number; e: number };
type Scene = { id: number; title: string; audio: string; duration: number; words: Word[] };
const SCENES = timeline as Scene[];
export const FPS = 30;
const PRE = 0.6, POST = 0.9;
export const sceneFrames = (s: Scene) => Math.ceil((PRE + s.duration + POST) * FPS);
export const totalFrames = SCENES.reduce((a, s) => a + sceneFrames(s), 0);

const C = {
  bg: '#14100c', paper: '#e9dcc0', ink: '#2b1d12', red: '#a3241c', gold: '#d4a53c',
  dim: '#6b5a44', blue: '#1f4e5f', green: '#3d5a3a',
};
const SERIF = 'Georgia, "Times New Roman", serif';

const norm = (s: string) => s.toLocaleLowerCase('tr').replace(/[^a-zçğıöşü0-9]/g, '');
/** Anlatımda kelimenin (n. geçişinin) başladığı kare; bulunamazsa fallback. */
const useAt = (words: Word[]) => (key: string, n = 1, fb = 0) => {
  const k = norm(key);
  let c = 0;
  for (const w of words) if (norm(w.w).startsWith(k) && ++c === n) return Math.round((PRE + w.s) * FPS);
  return fb;
};

const Fade: React.FC<{ from: number; dur?: number; children: React.ReactNode; style?: React.CSSProperties; y?: number }> = ({ from, dur = 18, children, style, y = 30 }) => {
  const f = useCurrentFrame();
  const o = interpolate(f, [from, from + dur], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  return <div style={{ opacity: o, transform: `translateY(${(1 - o) * y}px)`, ...style }}>{children}</div>;
};

const Paper: React.FC<{ children: React.ReactNode; dark?: boolean }> = ({ children, dark }) => {
  const f = useCurrentFrame();
  const z = 1 + Math.min(f / 40000, 0.05);
  return (
    <AbsoluteFill style={{ background: dark ? `radial-gradient(circle at 50% 40%, #2a2017, ${C.bg} 75%)` : `radial-gradient(circle at 50% 45%, #f3e8cf, ${C.paper} 60%, #c9b48e)` }}>
      <AbsoluteFill style={{ transform: `scale(${z})` }}>{children}</AbsoluteFill>
      <AbsoluteFill style={{ boxShadow: 'inset 0 0 260px rgba(0,0,0,.55)', pointerEvents: 'none' }} />
    </AbsoluteFill>
  );
};

const Kicker: React.FC<{ n: number; text: string; dark?: boolean }> = ({ n, text, dark }) => (
  <Fade from={0} style={{ position: 'absolute', top: 60, left: 90, fontFamily: SERIF, color: dark ? C.gold : C.red, fontSize: 30, letterSpacing: 6, textTransform: 'uppercase' }}>
    {String(n).padStart(2, '0')} · {text}
  </Fade>
);

/** Kelime zamanlı altyazı (6–8 kelimelik gruplar, konuşulan kelime vurgulu). */
const Captions: React.FC<{ words: Word[]; dark?: boolean }> = ({ words, dark }) => {
  const f = useCurrentFrame();
  const t = f / FPS - PRE;
  const groups: Word[][] = [];
  let g: Word[] = [];
  words.forEach((w, i) => {
    g.push(w);
    const brk = /[.?!:;,]$/.test(w.w) || (words[i + 1] && words[i + 1].s - w.e > 0.35);
    if (g.length >= 8 || (brk && g.length >= 3)) { groups.push(g); g = []; }
  });
  if (g.length) groups.push(g);
  const cur = groups.find((gr, i) => t >= gr[0].s - 0.05 && t < (groups[i + 1]?.[0].s ?? gr[gr.length - 1].e + 0.6));
  if (!cur) return null;
  return (
    <div style={{ position: 'absolute', bottom: 70, width: '100%', textAlign: 'center', padding: '0 160px', boxSizing: 'border-box' }}>
      <span style={{ background: 'rgba(15,10,6,.78)', padding: '14px 28px', borderRadius: 10, fontFamily: 'Segoe UI, Arial, sans-serif', fontSize: 44, fontWeight: 700, lineHeight: 1.5, boxDecorationBreak: 'clone', WebkitBoxDecorationBreak: 'clone' }}>
        {cur.map((w, i) => (
          <span key={i} style={{ color: t >= w.s ? (t < w.e + 0.1 ? C.gold : '#fff') : 'rgba(255,255,255,.55)' }}>{w.w} </span>
        ))}
      </span>
    </div>
  );
};

/* ---------- küçük çizimler ---------- */
const Boy: React.FC<{ x: number; y: number; s?: number; c?: string }> = ({ x, y, s = 1, c = C.ink }) => (
  <g transform={`translate(${x},${y}) scale(${s})`} fill={c}>
    <circle cx={0} cy={-62} r={13} />
    <path d="M-16 -46 h32 l6 46 h-44z" />
    <rect x={-12} y={0} width={9} height={28} /><rect x={3} y={0} width={9} height={28} />
  </g>
);
const Janissary: React.FC<{ x: number; y: number; s?: number; c?: string; cap?: string }> = ({ x, y, s = 1, c = C.ink, cap = '#f4efe2' }) => (
  <g transform={`translate(${x},${y}) scale(${s})`}>
    <path d="M-14 -88 q14 -40 30 -10 q10 20 34 38 q-30 0 -50 -14z" fill={cap} stroke={c} strokeWidth={3} />
    <circle cx={0} cy={-74} r={14} fill={c} />
    <path d="M-22 -58 h44 l10 74 h-64z" fill={c} />
    <rect x={-16} y={16} width={12} height={34} fill={c} /><rect x={4} y={16} width={12} height={34} fill={c} />
    <line x1={26} y1={-70} x2={34} y2={40} stroke={c} strokeWidth={5} />
  </g>
);
const Cauldron: React.FC<{ x: number; y: number; s?: number; flip?: number }> = ({ x, y, s = 1, flip = 0 }) => {
  const f = useCurrentFrame();
  return (
    <g transform={`translate(${x},${y}) scale(${s}) rotate(${flip})`}>
      {flip === 0 && [0, 1, 2].map((i) => {
        const p = ((f + i * 20) % 60) / 60;
        return <path key={i} d={`M${-40 + i * 40} -90 q 15 -30 0 -60 q -15 -30 0 -60`} transform={`translate(0 ${-p * 40})`} stroke="#fff" strokeOpacity={0.5 * (1 - p)} strokeWidth={8} fill="none" />;
      })}
      <path d="M-120 -80 h240 q-10 150 -120 150 q-110 0 -120 -150z" fill="#b8652f" stroke="#5a2e12" strokeWidth={8} />
      <rect x={-135} y={-95} width={270} height={22} rx={10} fill="#8a4a20" />
      <path d="M-120 -60 q-50 -10 -45 40 M120 -60 q50 -10 45 40" stroke="#5a2e12" strokeWidth={10} fill="none" />
    </g>
  );
};

/* ---------- sahneler ---------- */
type SP = { s: Scene };

const S1: React.FC<SP> = ({ s }) => {
  const at = useAt(s.words); const f = useCurrentFrame();
  const book = at('defter', 1, 200);
  const tTitle = at('bu', 0, sceneFrames(s) - 330);
  const titleAt = Math.max(at('merdivenin', 1, sceneFrames(s) - 300) - 30, 0);
  return (
    <Paper dark>
      <svg width={1920} height={1080} style={{ position: 'absolute' }}>
        <path d="M0 760 L300 470 L520 640 L800 380 L1100 650 L1350 430 L1650 620 L1920 500 V1080 H0z" fill="#241b13" />
        <path d="M0 860 L400 700 L900 820 L1400 690 L1920 800 V1080 H0z" fill="#1b140e" />
        <g transform="translate(1320 560)" fill="#120d09">
          <rect x={0} y={60} width={220} height={170} /><path d="M-20 60 L110 -20 L240 60z" /><rect x={90} y={-120} width={40} height={100} /><rect x={80} y={-150} width={60} height={14} /><rect x={103} y={-180} width={14} height={60} />
        </g>
        {[0, 1, 2, 3, 4, 5, 6].map((i) => <Boy key={i} x={430 + i * 110} y={900} s={1.2} c={i === 3 && f > book + 60 ? C.red : '#0b0806'} />)}
        <g opacity={interpolate(f, [book, book + 20], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' })}>
          <rect x={150} y={640} width={190} height={130} fill={C.paper} stroke={C.gold} strokeWidth={4} transform="rotate(-6 245 705)" />
          {[0, 1, 2, 3, 4].map((i) => <line key={i} x1={175} x2={315} y1={670 + i * 20} y2={662 + i * 20} stroke={C.ink} strokeWidth={3} strokeDasharray={`${interpolate(f, [book + 20 + i * 12, book + 40 + i * 12], [0, 140], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' })} 200`} />)}
        </g>
      </svg>
      <Fade from={titleAt} dur={30} style={{ position: 'absolute', top: 150, width: '100%', textAlign: 'center', fontFamily: SERIF }}>
        <div style={{ color: C.gold, fontSize: 34, letterSpacing: 10 }}>ACEMİ OĞLANINDAN YENİÇERİ AĞASINA</div>
        <div style={{ color: '#f3e8cf', fontSize: 104, fontWeight: 700, marginTop: 10 }}>Merdiven</div>
      </Fade>
      {void tTitle}
    </Paper>
  );
};

const S2: React.FC<SP> = ({ s }) => {
  const at = useAt(s.words); const f = useCurrentFrame();
  const rules = [['8–18 yaş', at('sekiz')], ['Tek oğul alınmaz', at('tek')], ['Evli alınmaz', at('evli')], ['Zanaatkâr istenmez', at('zanaat')]] as const;
  const march = at('kafile', 1, 900), split = at('eleme', 1, 2400);
  return (
    <Paper>
      <Kicker n={2} text="Devşirme · “toplamak”" />
      <div style={{ position: 'absolute', top: 160, left: 110, fontFamily: SERIF }}>
        {rules.map(([t, a], i) => (
          <Fade key={i} from={a} style={{ fontSize: 54, color: C.ink, margin: '18px 0', borderLeft: `8px solid ${C.red}`, paddingLeft: 24, opacity: f > split ? 0.25 : 1 }}>{t}</Fade>
        ))}
      </div>
      <svg width={1920} height={1080} style={{ position: 'absolute' }}>
        {f > march && f < split + 30 && Array.from({ length: 14 }).map((_, i) => (
          <Boy key={i} x={((f - march) * 3 + i * 70) % 1100 + 820} y={620 + (i % 2) * 70} s={0.8} c={C.red} />
        ))}
        {f > split && (
          <g opacity={interpolate(f, [split, split + 20], [0, 1], { extrapolateRight: 'clamp' })} fontFamily={SERIF}>
            <circle cx={960} cy={560} r={60} fill={C.ink} /><text x={960} y={570} fill={C.paper} fontSize={30} textAnchor="middle">İstanbul</text>
            <path d="M1010 520 L1360 330" stroke={C.gold} strokeWidth={10} /><path d="M1010 600 L1360 780" stroke={C.red} strokeWidth={22} />
            <text x={1380} y={330} fontSize={60} fill={C.ink}>Enderun</text><text x={1380} y={375} fontSize={30} fill={C.dim}>az sayıda · saray</text>
            <text x={1380} y={800} fontSize={60} fill={C.red} fontWeight={700}>Acemi Ocağı</text><text x={1380} y={845} fontSize={30} fill={C.dim}>büyük çoğunluk</text>
          </g>
        )}
      </svg>
    </Paper>
  );
};

const S3: React.FC<SP> = ({ s }) => {
  const at = useAt(s.words); const f = useCurrentFrame();
  const village = at('anadolu', 1, 100), barracks = at('gelibolu', 1, 1200), coin = at('akçe', 1, 2200);
  const phase = f < barracks ? 0 : 1;
  return (
    <Paper>
      <Kicker n={3} text={phase ? 'Acemi Ocağı' : '“Türk’e verme”'} />
      <svg width={1920} height={1080} style={{ position: 'absolute' }}>
        {phase === 0 ? (
          <g opacity={interpolate(f, [village, village + 20], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' })}>
            {[0, 1, 2, 3, 4, 5].map((i) => <path key={i} d={`M0 ${640 + i * 60} Q960 ${600 + i * 60} 1920 ${650 + i * 60}`} stroke={C.green} strokeWidth={6} fill="none" opacity={0.5} />)}
            <circle cx={1550} cy={260} r={80} fill={C.gold} opacity={0.7} />
            <g transform={`translate(${600 + (f % 300)} 0)`}><Boy x={0} y={700} s={1.6} /><path d="M40 640 l140 60" stroke={C.ink} strokeWidth={8} /></g>
          </g>
        ) : (
          <g>
            <path d="M0 820 H1920" stroke={C.blue} strokeWidth={6} />
            <path d="M200 820 q300 120 600 0 l-60 -120 h-480z" fill="#5a3b22" />
            <line x1={800} y1={700} x2={1300 + Math.sin(f / 10) * 8} y2={640} stroke={C.ink} strokeWidth={6} />
            {[0, 1, 2, 3].map((i) => <Boy key={i} x={1120 + i * 110 + Math.sin(f / 10 + i) * 6} y={780} s={1.2} c={C.red} />)}
            {[0, 1, 2].map((i) => <rect key={i} x={1500 + i * 90} y={500 - i * 40} width={80} height={60} fill="#9a8a70" />)}
          </g>
        )}
      </svg>
      {f > coin && (
        <Fade from={coin} style={{ position: 'absolute', top: 170, right: 140, fontFamily: SERIF, textAlign: 'right' }}>
          <div style={{ fontSize: 120, color: C.red, fontWeight: 700 }}>1–2 akçe</div>
          <div style={{ fontSize: 40, color: C.ink }}>günlük · evlilik yok · sakal yok</div>
        </Fade>
      )}
    </Paper>
  );
};

const S4: React.FC<SP> = ({ s }) => {
  const at = useAt(s.words); const f = useCurrentFrame(); const { fps } = useVideoConfig();
  const bork = at('börk', 1, 200), ulufe = at('ulufe', 1, 400), train = at('talim', 1, 700), bek = at('bektaşi', 1, 1100), kap = at('kapıkulu', 2, 1600);
  const pop = spring({ frame: f - kap, fps, config: { damping: 12 } });
  return (
    <Paper dark>
      <Kicker n={4} text="Kapıya çıkma" dark />
      <svg width={1920} height={1080} style={{ position: 'absolute' }}>
        <g opacity={f > bork ? 1 : 0}><Janissary x={480} y={820} s={3} c="#0b0806" cap="#f4efe2" /></g>
      </svg>
      <div style={{ position: 'absolute', left: 900, top: 230, fontFamily: SERIF, color: '#f3e8cf' }}>
        <Fade from={bork} style={{ fontSize: 56, margin: 20 }}>◆ Ak börk</Fade>
        <Fade from={ulufe} style={{ fontSize: 56, margin: 20 }}>◆ Ulufe: üç ayda bir</Fade>
        <Fade from={train} style={{ fontSize: 56, margin: 20 }}>◆ Talim: ok → tüfek</Fade>
        <Fade from={bek} style={{ fontSize: 56, margin: 20 }}>◆ Pir: Hacı Bektaş-ı Veli</Fade>
      </div>
      {f > kap && (
        <AbsoluteFill style={{ background: 'rgba(10,7,4,.82)', justifyContent: 'center', alignItems: 'center', opacity: interpolate(f, [kap, kap + 10], [0, 1], { extrapolateRight: 'clamp' }) }}>
          <div style={{ fontFamily: SERIF, fontSize: 200, color: C.gold, fontWeight: 700, letterSpacing: 20, transform: `scale(${0.7 + pop * 0.3})` }}>KAPIKULU</div>
          <div style={{ fontFamily: SERIF, fontSize: 44, color: '#f3e8cf' }}>vergi yok · kendi mahkemesi · kendi zabiti</div>
        </AbsoluteFill>
      )}
    </Paper>
  );
};

const S5: React.FC<SP> = ({ s }) => {
  const at = useAt(s.words); const f = useCurrentFrame();
  const orta = at('yüz', 1, 100), kaz = at('kazan', 1, 700), flip = at('kaldırmak', 1, 1400), names = at('çorbacı', 1, 1900);
  const bars = [['Cemaat', 101, C.red], ['Bölük', 61, C.blue], ['Sekban', 34, C.green]] as const;
  const showBars = f < kaz;
  return (
    <Paper>
      <Kicker n={5} text="Orta ve kazan" />
      {showBars ? (
        <div style={{ position: 'absolute', top: 220, left: 160, right: 160, fontFamily: SERIF }}>
          <Fade from={orta} style={{ fontSize: 150, color: C.ink, fontWeight: 700 }}>196 orta</Fade>
          {bars.map(([n, v, c], i) => {
            const w = interpolate(f, [orta + 20 + i * 15, orta + 50 + i * 15], [0, v * 13], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
            return <div key={n} style={{ display: 'flex', alignItems: 'center', margin: '22px 0' }}><div style={{ width: 240, fontSize: 48, color: C.ink }}>{n}</div><div style={{ width: w, height: 56, background: c }} /><div style={{ fontSize: 48, marginLeft: 20, color: C.ink }}>{v}</div></div>;
          })}
        </div>
      ) : (
        <svg width={1920} height={1080} style={{ position: 'absolute' }}>
          <Cauldron x={f > flip ? 760 : 960} y={640} s={1.8} flip={f > flip ? interpolate(f, [flip, flip + 20], [0, 150], { extrapolateRight: 'clamp' }) : 0} />
          {f > flip && <text x={1250} y={500} fontFamily={SERIF} fontSize={90} fill={C.red} fontWeight={700} opacity={interpolate(f, [flip + 10, flip + 30], [0, 1], { extrapolateRight: 'clamp' })}>= İSYAN</text>}
          {f > names && ['Çorbacı', 'Aşçı', 'Sakabaşı', 'Vekilharç'].map((n, i) => (
            <text key={n} x={1250} y={640 + i * 80} fontFamily={SERIF} fontSize={60} fill={C.ink} opacity={interpolate(f, [names + i * 12, names + i * 12 + 15], [0, 1], { extrapolateRight: 'clamp' })}>{n}</text>
          ))}
        </svg>
      )}
    </Paper>
  );
};

const RANKS = [['Nefer', 'nefer'], ['Kara kullukçu', 'kara'], ['Aşçı ustası', 'aşçı'], ['Sakabaşı', 'sakabaşı'], ['Bayraktar', 'bayraktar'], ['Vekilharç', 'vekilharç'], ['Odabaşı', 'odabaşı'], ['Çorbacı', 'çorbacı']] as const;
const S6: React.FC<SP> = ({ s }) => {
  const at = useAt(s.words); const f = useCurrentFrame();
  const times = RANKS.map(([, k]) => at(k, 1, 99999));
  const lit = times.filter((t) => f >= t).length;
  const kidem = at('kıdem', 1, 99999), yig = at('yiğitlik', 1, 99999);
  const rungY = (i: number) => 850 - i * 92;
  return (
    <Paper>
      <Kicker n={6} text="Orta içindeki merdiven" />
      <svg width={1920} height={1080} style={{ position: 'absolute' }}>
        <line x1={300} y1={1000} x2={300} y2={140} stroke="#6b4a2a" strokeWidth={16} /><line x1={560} y1={1000} x2={560} y2={140} stroke="#6b4a2a" strokeWidth={16} />
        {RANKS.map(([n], i) => {
          const on = i < lit, cur = i === lit - 1;
          return (
            <g key={n}>
              <line x1={300} x2={560} y1={rungY(i)} y2={rungY(i)} stroke={on ? C.gold : '#8a7356'} strokeWidth={cur ? 18 : 12} />
              <text x={620} y={rungY(i) + 18} fontFamily={SERIF} fontSize={cur ? 64 : 46} fontWeight={cur ? 700 : 400} fill={on ? (cur ? C.red : C.ink) : 'rgba(43,29,18,.25)'}>{n}</text>
            </g>
          );
        })}
        {lit > 0 && <Janissary x={430} y={rungY(lit - 1) - 8} s={0.9} c={C.red} />}
        {f > kidem && <Fade from={kidem}><text /></Fade>}
      </svg>
      {f > kidem && (
        <div style={{ position: 'absolute', right: 140, top: 360, fontFamily: SERIF, textAlign: 'right' }}>
          <Fade from={kidem} style={{ fontSize: 110, color: C.ink, fontWeight: 700 }}>KIDEM</Fade>
          <Fade from={yig} style={{ fontSize: 70, color: C.red, marginTop: 20 }}>+ yiğitlik → terakki</Fade>
        </div>
      )}
    </Paper>
  );
};

const S7: React.FC<SP> = ({ s }) => {
  const at = useAt(s.words); const f = useCurrentFrame();
  const tiers = [
    { l: '196 Çorbacı', t: at('çorbacı', 1, 0), w: 1500 },
    { l: 'Zağarcıbaşı · Turnacıbaşı · Seksoncubaşı', t: at('zağarcıbaşı', 1, 300), w: 1150 },
    { l: 'Kul Kethüdası · Sekbanbaşı', t: at('kul', 1, 700), w: 800 },
    { l: 'YENİÇERİ AĞASI', t: at('ağası', 2, 2300), w: 460 },
  ];
  const cik = at('sancakbeyliğine', 1, 99999);
  return (
    <Paper dark>
      <Kicker n={7} text="Ocağın zirvesine doğru" dark />
      {tiers.map((tr, i) => (
        <Fade key={i} from={tr.t} style={{ position: 'absolute', left: (1920 - tr.w) / 2, width: tr.w, top: 700 - i * 150, height: 125, background: i === 3 ? C.gold : ['#3a2b1e', '#4d3925', '#6b4a2a'][i], color: i === 3 ? C.ink : '#f3e8cf', fontFamily: SERIF, fontSize: i === 3 ? 56 : 42, fontWeight: i === 3 ? 700 : 400, display: 'flex', alignItems: 'center', justifyContent: 'center', borderRadius: 6 }}>{tr.l}</Fade>
      ))}
      {f > cik && f < at('ağası', 2, 99999) && (
        <Fade from={cik} style={{ position: 'absolute', right: 80, top: 330, fontFamily: SERIF, fontSize: 44, color: C.gold, width: 380 }}>↗ “Çıkma”<br />sancakbeyi · kale komutanı</Fade>
      )}
    </Paper>
  );
};

const S8: React.FC<SP> = ({ s }) => {
  const at = useAt(s.words); const f = useCurrentFrame();
  const sur = at('sürpriz', 1, 600), out = at('dışarıdan', 1, 1300), two = at('hatırlarsanız', 1, 1900);
  return (
    <Paper>
      <Kicker n={8} text="Yeniçeri Ağası" />
      <svg width={1920} height={1080} style={{ position: 'absolute' }} fontFamily={SERIF}>
        <rect x={810} y={130} width={300} height={110} fill={C.gold} rx={8} />
        <text x={960} y={200} textAnchor="middle" fontSize={44} fontWeight={700} fill={C.ink}>AĞA</text>
        <rect x={260} y={760} width={440} height={110} fill={C.red} rx={8} /><text x={480} y={830} textAnchor="middle" fontSize={44} fill="#fff">Acemi Ocağı → Orta</text>
        <rect x={1220} y={760} width={440} height={110} fill={C.blue} rx={8} /><text x={1440} y={830} textAnchor="middle" fontSize={44} fill="#fff">Enderun (saray)</text>
        <path d="M480 760 C480 500 900 400 930 245" stroke={C.red} strokeWidth={14} fill="none" strokeDasharray="1400" strokeDashoffset={interpolate(f, [sur, sur + 60], [1400, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' })} opacity={f > out ? 0.25 : 1} />
        {f > out && <path d="M1440 760 C1440 500 1020 400 990 245" stroke={C.blue} strokeWidth={22} fill="none" strokeDasharray="1400" strokeDashoffset={interpolate(f, [out, out + 60], [1400, 0], { extrapolateRight: 'clamp' })} />}
        {f > out && <text x={960} y={560} textAnchor="middle" fontSize={50} fill={C.ink} opacity={interpolate(f, [out + 40, out + 60], [0, 1], { extrapolateRight: 'clamp' })}>XVI. yy’dan itibaren: dışarıdan atama</text>}
        {f > two && <text x={960} y={680} textAnchor="middle" fontSize={40} fill={C.red}>Zirve, çoğu zaman başka kapıdan gelenlere kaldı.</text>}
      </svg>
    </Paper>
  );
};

const S9: React.FC<SP> = ({ s }) => {
  const at = useAt(s.words); const f = useCurrentFrame();
  const decline = at('devşirme', 1, 0), kaz = at('kazanlar', 1, 900), y1826 = at('1826', 1, at('bin', 1, 1300)), back = at('köy', 1, 1900), next = at('enderun', 1, 2500);
  const fire = f > y1826 && f < back;
  return (
    <Paper dark>
      <Kicker n={9} text="Çözülüş · 1826" dark />
      {f < kaz && (
        <div style={{ position: 'absolute', top: 260, left: 140, fontFamily: SERIF, color: '#f3e8cf', fontSize: 58 }}>
          <Fade from={decline} style={{ margin: 20 }}>✕ Devşirme bırakılır</Fade>
          <Fade from={at('evlenmeye', 1, decline + 60)} style={{ margin: 20 }}>✕ Evlilik, dükkân, babadan oğula</Fade>
          <Fade from={at('ulufe', 1, decline + 120)} style={{ margin: 20 }}>✕ Şişen defterler, azalan asker</Fade>
        </div>
      )}
      {f >= kaz && f < y1826 && (
        <svg width={1920} height={1080} style={{ position: 'absolute' }}>
          {[0, 1, 2].map((i) => <Cauldron key={i} x={480 + i * 480} y={640} s={1} flip={interpolate(f, [kaz + i * 25, kaz + i * 25 + 20], [0, 140], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' })} />)}
          <text x={480} y={900} textAnchor="middle" fontFamily={SERIF} fontSize={44} fill="#f3e8cf">II. Osman</text>
          <text x={1440} y={900} textAnchor="middle" fontFamily={SERIF} fontSize={44} fill="#f3e8cf">III. Selim</text>
        </svg>
      )}
      {fire && (
        <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center', background: `radial-gradient(circle at 50% ${80 + Math.sin(f / 4) * 3}%, rgba(220,90,20,.75), rgba(20,10,5,.95) 60%)` }}>
          <div style={{ fontFamily: SERIF, fontSize: 220, fontWeight: 700, color: '#ffd28a' }}>1826</div>
          <Fade from={at('vaka', 1, y1826 + 200)} style={{ fontFamily: SERIF, fontSize: 64, color: '#fff' }}>Vaka-i Hayriye</Fade>
        </AbsoluteFill>
      )}
      {f >= back && (
        <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center', fontFamily: SERIF }}>
          <svg width={1920} height={1080} style={{ position: 'absolute', opacity: 0.35 }}>
            {[0, 1, 2, 3, 4, 5, 6, 7].map((i) => <rect key={i} x={760} y={900 - i * 100} width={400} height={12} fill={C.gold} />)}
          </svg>
          {f >= next && <Fade from={next} style={{ fontSize: 46, color: C.gold, letterSpacing: 6 }}>SONRAKİ VİDEO</Fade>}
          {f >= next && <Fade from={next + 10} style={{ fontSize: 130, color: '#f3e8cf', fontWeight: 700 }}>Enderun</Fade>}
        </AbsoluteFill>
      )}
    </Paper>
  );
};

const VIS = [S1, S2, S3, S4, S5, S6, S7, S8, S9];
const DARK = [true, false, false, true, false, false, true, false, true];

export const Yeniceri: React.FC = () => {
  let start = 0;
  return (
    <AbsoluteFill style={{ background: C.bg }}>
      {SCENES.map((s, i) => {
        const from = start; const dur = sceneFrames(s); start += dur;
        const V = VIS[i];
        return (
          <Sequence key={s.id} from={from} durationInFrames={dur}>
            <SceneWrap dur={dur}><V s={s} /><Captions words={s.words} dark={DARK[i]} /></SceneWrap>
            <Sequence from={Math.round(PRE * FPS)}><Audio src={staticFile(s.audio)} /></Sequence>
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};

const SceneWrap: React.FC<{ dur: number; children: React.ReactNode }> = ({ dur, children }) => {
  const f = useCurrentFrame();
  const o = interpolate(f, [0, 12, dur - 12, dur], [0, 1, 1, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  return <AbsoluteFill style={{ opacity: o }}>{children}</AbsoluteFill>;
};
