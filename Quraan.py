import sys, json, os
from PySide6.QtCore import Qt, QUrl, QTimer, QPoint
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QLineEdit, QPushButton, QLabel, QFrame, QScrollArea, QGridLayout, QSizePolicy)
from PySide6.QtGui import QPixmap, QFontDatabase
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput

# ── resolve base path (works both as .py and as PyInstaller .exe) ─────────────
def _base():
    return getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
BASE = _base()
def res(rel): return os.path.join(BASE, rel)

S = """
QMainWindow,QWidget{background:transparent}
#Win{background:#090909;border:1px solid #1c1c1c;border-radius:16px}
#Bar{background:#0b0b0b;border-bottom:1px solid #222;border-top-left-radius:16px;border-top-right-radius:16px}
#Title{color:#d4af37;font-size:18px;font-weight:bold;letter-spacing:3px}
#Back,#Close{background:#111;color:#666;border:1px solid #222;border-radius:7px;padding:5px 12px;font-size:13px}
#Back:hover{color:#d4af37;border-color:#554400} #Close:hover{background:#1c0000;color:#cc3333}
#Search{background:#0e0e0e;border:1px solid #252525;border-radius:10px;color:#ddd;padding:11px 15px;font-size:15px}
#Search:focus{border-color:#d4af37}
QScrollArea{background:transparent;border:none}
QScrollBar:vertical{background:transparent;width:5px;margin:0}
QScrollBar::handle:vertical{background:#2a2a2a;border-radius:2px;min-height:25px}
QScrollBar::handle:vertical:hover{background:#d4af37}
QScrollBar::add-line:vertical,QScrollBar::sub-line:vertical{height:0}
#Card{background:#111;border:1px solid #222;border-radius:12px}
#Card:hover{background:#151500;border-color:#d4af37}
#CardT{color:#ddd;font-size:13px;font-weight:bold;background:transparent;border:none}
#CardS{color:#d4af37;font-size:11px;background:transparent;border:none}
#VCard{background:#0d0d0d;border:1px solid #1c1c1c;border-radius:12px;margin:2px 0}
#VCard:hover{border-color:#2a2a2a}
#VCardHL{background:#0d0d00;border:1px solid #d4af37;border-radius:12px;margin:2px 0}
#ANum{color:#d4af37;font-size:12px;background:#120e00;border:1px solid #2a2000;border-radius:5px;padding:2px 6px;max-width:52px;min-width:38px}
#ATxt{color:#f0ead6;font-size:24px;font-family:'Amiri','Traditional Arabic',serif;background:transparent;border:none}
#TTxt{color:#8a7040;font-size:13px;background:transparent;border:none;padding-top:8px;margin-top:6px;border-top:1px solid #1a1a00}
#TipLbl{color:#444;font-size:11px;background:transparent;border:none;padding:2px 0 0 0}
#SRow{background:#0d0d0d;border:1px solid #1c1c1c;border-radius:10px;margin:2px 0}
#SRow:hover{border-color:#d4af37;background:#0f0d00}
#SMeta{color:#d4af37;font-size:12px;background:transparent;border:none}
#SCnt{color:#888;font-size:12px;background:transparent;border:none}
#SAya{color:#ccc;font-size:18px;font-family:'Amiri','Traditional Arabic',serif;background:transparent;border:none}
#SHdr{background:#0b0900;border:1px solid #252000;border-radius:11px}
#SName{color:#d4af37;font-size:21px;font-weight:bold;background:transparent;border:none}
#SCntL{color:#555;font-size:13px;background:transparent;border:none}
#ZCard{background:#0c0900;border:1px solid #2a2000;border-radius:13px}
#ZTxt{color:#f0ead6;font-size:20px;font-family:'Amiri','Traditional Arabic',serif;background:transparent;border:none}
#ZRep{color:#d4af37;font-size:15px;font-weight:bold;background:transparent;border:none}
#PBar{background:#0b0b0b;border-top:1px solid #1a1a1a;border-bottom-left-radius:16px;border-bottom-right-radius:16px}
#PLbl{color:#444;font-size:13px;background:transparent;border:none}
#PBtn{background:#d4af37;color:#000;border:none;border-radius:19px;font-size:14px;font-weight:bold;min-width:38px;min-height:38px;max-width:38px;max-height:38px}
#PBtn:hover{background:#e8c84a}
#ImgOv{background:#050505;border-radius:13px;border:1px solid #222}
#ImgF{background:#0a0a0a;border:1px solid #222;border-radius:10px}
#ICap{color:#555;font-size:12px;background:transparent;border:none}
#IClose{background:#141414;color:#777;border:1px solid #2a2a2a;border-radius:7px;padding:5px 12px;font-size:13px}
#IClose:hover{background:#1c0000;color:#ff4444}
#SecT{color:#d4af37;font-size:16px;font-weight:bold;letter-spacing:2px;padding:4px 0 12px;background:transparent;border:none}
#Info{color:#555;font-size:13px;background:transparent;border:none}
"""

class Card(QFrame):
    def __init__(self, title, tag, fn, sub="", img_path=""):
        super().__init__(); self.setObjectName("Card"); self.setFixedSize(165, 130)
        self.setCursor(Qt.PointingHandCursor); self._fn = fn; self._tag = tag
        self._data = img_path or title
        lay = QVBoxLayout(self); lay.setContentsMargins(10, 8, 10, 8); lay.setAlignment(Qt.AlignCenter)
        if img_path and os.path.exists(img_path):
            il = QLabel()
            il.setPixmap(QPixmap(img_path).scaled(125, 65, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            il.setAlignment(Qt.AlignCenter); il.setStyleSheet("background:transparent;border:none"); lay.addWidget(il)
        t = QLabel(title); t.setObjectName("CardT"); t.setAlignment(Qt.AlignCenter); t.setWordWrap(True); lay.addWidget(t)
        if sub:
            s = QLabel(sub); s.setObjectName("CardS"); s.setAlignment(Qt.AlignCenter); lay.addWidget(s)
    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton: self._fn(self._tag, self._data)
    def contextMenuEvent(self, e): e.ignore()  # disable right-click menu


class VCard(QFrame):
    def __init__(self, aya, taf, no, highlight_word="", obj_name="VCard"):
        super().__init__(); self.setObjectName(obj_name); self.setCursor(Qt.PointingHandCursor)
        self._open = False
        lay = QVBoxLayout(self); lay.setContentsMargins(16, 12, 16, 12); lay.setSpacing(0)
        row = QHBoxLayout(); row.setSpacing(10)
        n = QLabel(f"﴾{no}﴿"); n.setObjectName("ANum"); n.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        if highlight_word and highlight_word in aya:
            aya_html = aya.replace(highlight_word,
                f'<span style="color:#d4af37;background:#1a1400;padding:0 2px;border-radius:2px">{highlight_word}</span>')
            self._a = QLabel(aya_html); self._a.setTextFormat(Qt.RichText)
        else:
            self._a = QLabel(aya)
        self._a.setObjectName("ATxt"); self._a.setWordWrap(True)
        self._a.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self._a.setTextInteractionFlags(Qt.TextSelectableByMouse)
        row.addWidget(n, 0, Qt.AlignTop); row.addWidget(self._a, 1); lay.addLayout(row)
        self._tip = QLabel("اضغط لعرض التفسير ▾"); self._tip.setObjectName("TipLbl"); self._tip.setAlignment(Qt.AlignRight)
        lay.addWidget(self._tip)
        self._t = QLabel(taf if taf else "التفسير غير متوفر.")
        self._t.setObjectName("TTxt"); self._t.setWordWrap(True)
        self._t.setAlignment(Qt.AlignRight); self._t.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self._t.setVisible(False); lay.addWidget(self._t)

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self._open = not self._open
            self._t.setVisible(self._open)
            self._tip.setText("اضغط لإخفاء التفسير ▴" if self._open else "اضغط لعرض التفسير ▾")
    def contextMenuEvent(self, e): e.ignore()


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.player = QMediaPlayer(); self.ao = QAudioOutput()
        self.player.setAudioOutput(self.ao); self.ao.setVolume(1.0)
        self.setWindowFlags(Qt.FramelessWindowHint); self.setAttribute(Qt.WA_TranslucentBackground)
        self.setContextMenuPolicy(Qt.NoContextMenu)  # disable right-click app-wide
        self.resize(950, 670); self.setLayoutDirection(Qt.RightToLeft)
        self.hist = []; self._dp = None; self._img_w = None; self._pending_scroll = None
        self.Q = self._j("quran"); self.T = self._j("tafsir"); self.A = self._j("adhkar")
        self._tidx = {(str(t.get("number","")), str(t.get("aya",""))): t.get("text","") for t in self.T}
        self._build(); self.nav("main")

    def _j(self, n):
        p = res(f"data/{n}.json")
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f: return json.load(f)
            except: pass
        return []

    def _build(self):
        self.win = QWidget(); self.win.setObjectName("Win"); self.win.setStyleSheet(S)
        self.win.setContextMenuPolicy(Qt.NoContextMenu)
        r = QVBoxLayout(self.win); r.setContentsMargins(0, 0, 0, 0); r.setSpacing(0)
        bar = QFrame(); bar.setObjectName("Bar"); bar.setFixedHeight(52)
        bl = QHBoxLayout(bar); bl.setContentsMargins(12, 0, 12, 0)
        self.bk = QPushButton("⟵ رجوع"); self.bk.setObjectName("Back")
        self.bk.setCursor(Qt.PointingHandCursor); self.bk.clicked.connect(self.back); self.bk.hide()
        ti = QLabel("االمصحف الشريف"); ti.setObjectName("Title"); ti.setAlignment(Qt.AlignCenter)
        cl = QPushButton("✕"); cl.setObjectName("Close"); cl.setCursor(Qt.PointingHandCursor); cl.clicked.connect(self.close)
        bl.addWidget(self.bk); bl.addStretch(); bl.addWidget(ti); bl.addStretch(); bl.addWidget(cl)
        r.addWidget(bar)
        dv = QFrame(); dv.setFixedHeight(1); dv.setStyleSheet("background:#2a2200"); r.addWidget(dv)
        sc = QWidget(); sc.setStyleSheet("background:transparent")
        sl = QHBoxLayout(sc); sl.setContentsMargins(12, 7, 12, 3)
        self.sb = QLineEdit(); self.sb.setObjectName("Search")
        self.sb.setPlaceholderText("🔍  ابحث في القرآن الكريم...")
        self.sb.setLayoutDirection(Qt.RightToLeft); self.sb.textChanged.connect(self._search)
        sl.addWidget(self.sb); r.addWidget(sc)
        self.sa = QScrollArea(); self.sa.setWidgetResizable(True); self.sa.setLayoutDirection(Qt.RightToLeft)
        self.cw = QWidget(); self.cw.setStyleSheet("background:transparent")
        self.cl = QVBoxLayout(self.cw); self.cl.setContentsMargins(12, 4, 12, 4); self.cl.setSpacing(7)
        self.sa.setWidget(self.cw); r.addWidget(self.sa, 1)
        pd = QFrame(); pd.setFixedHeight(1); pd.setStyleSheet("background:#1a1a1a"); r.addWidget(pd)
        pb = QFrame(); pb.setObjectName("PBar"); pb.setFixedHeight(54)
        pl = QHBoxLayout(pb); pl.setContentsMargins(16, 0, 16, 0)
        self.plbl = QLabel("جاهز للتشغيل"); self.plbl.setObjectName("PLbl")
        self.dt = QLabel("○ ○ ○"); self.dt.setStyleSheet("color:#1e1e1e;font-size:10px;letter-spacing:4px"); self.dt.setFixedWidth(55)
        self.pp = QPushButton("▶"); self.pp.setObjectName("PBtn"); self.pp.setCursor(Qt.PointingHandCursor); self.pp.clicked.connect(self._tog)
        pl.addWidget(self.plbl, 1); pl.addWidget(self.dt); pl.addWidget(self.pp); r.addWidget(pb)
        self.setCentralWidget(self.win)
        self._di = 0; self._dtimer = QTimer(self); self._dtimer.timeout.connect(self._dots)

    def contextMenuEvent(self, e): e.ignore()  # block right-click on main window

    def _dots(self):
        f = ["● ○ ○","○ ● ○","○ ○ ●","○ ● ○"]; self._di = (self._di+1)%4
        self.dt.setStyleSheet("color:#d4af37;font-size:10px;letter-spacing:4px"); self.dt.setText(f[self._di])

    def _clr(self):
        while self.cl.count():
            it = self.cl.takeAt(0)
            if it.widget(): it.widget().deleteLater()

    def nav(self, tgt, data=None):
        if tgt == "search_results":
            if self.hist and self.hist[-1][0] == "search_results": self.hist[-1] = (tgt, data)
            else: self.hist.append((tgt, data))
        elif not self.hist or self.hist[-1] != (tgt, data): self.hist.append((tgt, data))
        self.bk.setVisible(len(self.hist) > 1); self._clr()
        lbs = {"main":"الرئيسية","q_list":" سور القران الكريم","a_list":"الأذكار","i_list":"سور قصيرة للصلاة"}
        lb = f'نتائج: «{data}»' if tgt == "search_results" else lbs.get(tgt)
        if lb:
            t = QLabel(lb); t.setObjectName("SecT"); t.setAlignment(Qt.AlignRight); self.cl.addWidget(t)
        {"main":self._main,"q_list":lambda:self._grid("q"),"a_list":lambda:self._grid("a"),
         "i_list":lambda:self._grid("i"),"open_surah":lambda:self._surah(data),
         "open_surah_word":lambda:self._surah_word(data),"open_zekr":lambda:self._zekr(data),
         "view_img":lambda:self._img(data),"search_results":lambda:self._sres(data)
        }.get(tgt, lambda:None)()
        self.cl.addStretch()
        QTimer.singleShot(0, lambda: self.sa.verticalScrollBar().setValue(0))
        if self._pending_scroll:
            w = self._pending_scroll; self._pending_scroll = None
            QTimer.singleShot(80, lambda: self._scroll_to(w))

    def _scroll_to(self, widget):
        try:
            pos = widget.mapTo(self.cw, QPoint(0, 0))
            self.sa.verticalScrollBar().setValue(max(0, pos.y() - 60))
        except: pass

    def back(self):
        if len(self.hist) > 1: self.hist.pop(); p = self.hist.pop(); self.nav(p[0], p[1])

    def _search(self, txt):
        txt = txt.strip()
        if not txt: self.nav("main")
        elif len(txt) >= 2: self.nav("search_results", txt)

    def _sres(self, txt):
        res_v = [v for v in self.Q if txt in v.get("aya_text_emlaey","")]
        if not res_v:
            l = QLabel(f'لا نتائج لـ «{txt}»'); l.setObjectName("Info"); l.setAlignment(Qt.AlignCenter); self.cl.addWidget(l); return
        from collections import OrderedDict
        by_s = OrderedDict()
        for v in res_v:
            by_s.setdefault(v["sura_name_ar"], []).append(v)
        total = QLabel(f"وُجدت  «{txt}»  في  {len(res_v)}  آية  ضمن  {len(by_s)}  سورة")
        total.setObjectName("Info"); total.setAlignment(Qt.AlignRight); self.cl.addWidget(total)
        for sn, verses in by_s.items():
            sf = QFrame(); sf.setObjectName("SRow"); sf.setCursor(Qt.PointingHandCursor)
            payload = {"sura":sn,"word":txt,"first_aya":verses[0]["aya_no"]}
            sf.mousePressEvent = lambda e, p=payload: (e.button()==Qt.LeftButton) and self.nav("open_surah_word", p)
            sfl = QVBoxLayout(sf); sfl.setContentsMargins(14,10,14,10); sfl.setSpacing(5)
            hr = QHBoxLayout()
            total_occ = sum(v.get("aya_text_emlaey","").count(txt) for v in verses)
            cnt_lbl = QLabel(f"تكررت  {total_occ}  مرة  في  {len(verses)}  آية")
            cnt_lbl.setObjectName("SCnt")
            sname_lbl = QLabel(f"سورة {sn}  ◂  اضغط للانتقال"); sname_lbl.setObjectName("SMeta")
            hr.addWidget(cnt_lbl); hr.addStretch(); hr.addWidget(sname_lbl)
            sfl.addLayout(hr)
            for v in verses[:3]:
                hi = v.get("aya_text_emlaey","").replace(txt,
                    f'<span style="color:#d4af37;background:#1a1400;padding:0 2px">{txt}</span>')
                al = QLabel(f"({v['aya_no']})  {hi}"); al.setObjectName("SAya")
                al.setWordWrap(True); al.setAlignment(Qt.AlignRight); al.setTextFormat(Qt.RichText)
                sfl.addWidget(al)
            if len(verses) > 3:
                ml = QLabel(f"... و {len(verses)-3} آية أخرى"); ml.setObjectName("Info"); ml.setAlignment(Qt.AlignRight); sfl.addWidget(ml)
            self.cl.addWidget(sf)

    def _surah_word(self, payload):
        sn = payload["sura"]; word = payload["word"]; first_aya = str(payload["first_aya"])
        vs = sorted([v for v in self.Q if v["sura_name_ar"]==sn], key=lambda x:int(x["aya_no"]))
        if not vs: return
        self._audio(vs[0]["sura_no"], f"سورة {sn}")
        h = QFrame(); h.setObjectName("SHdr"); hl = QVBoxLayout(h); hl.setSpacing(3); hl.setContentsMargins(12,10,12,10)
        n = QLabel(f"سورة {sn}"); n.setObjectName("SName"); n.setAlignment(Qt.AlignCenter)
        c = QLabel(f"عدد الآيات: {len(vs)}  •  البحث عن: «{word}»"); c.setObjectName("SCntL"); c.setAlignment(Qt.AlignCenter)
        hl.addWidget(n); hl.addWidget(c); self.cl.addWidget(h)
        target = None
        for v in vs:
            taf = self._tidx.get((str(v["sura_no"]),str(v["aya_no"])),"التفسير غير متوفر.")
            is_match = word in v.get("aya_text_emlaey","")
            vc = VCard(v["aya_text_emlaey"], taf, v["aya_no"],
                       highlight_word=word if is_match else "", obj_name="VCardHL" if is_match else "VCard")
            self.cl.addWidget(vc)
            if str(v["aya_no"]) == first_aya and target is None: target = vc
        if target: self._pending_scroll = target

    def _grid(self, mode):
        w = QWidget(); w.setStyleSheet("background:transparent")
        g = QGridLayout(w); g.setSpacing(11); g.setAlignment(Qt.AlignRight|Qt.AlignTop)
        if mode == "q":
            seen = set(); i = 0
            for s in self.Q:
                if s["sura_no"] not in seen:
                    g.addWidget(Card(f"سورة {s['sura_name_ar']}","open_surah",self.nav),i//5,i%5)
                    seen.add(s["sura_no"]); i += 1
        elif mode == "a":
            for i,a in enumerate(self.A):
                g.addWidget(Card(a["zekr"][:26]+"...","open_zekr",self.nav,f"× {a.get('repeat','1')}"),i//5,i%5)
        elif mode == "i":
            img_dir = res("img")
            if os.path.exists(img_dir):
                for i,f in enumerate(sorted(x for x in os.listdir(img_dir) if x.lower().endswith((".png",".jpg",".jpeg")))):
                    full = os.path.join(img_dir, f)
                    g.addWidget(Card(f.rsplit(".",1)[0],"view_img",self.nav,img_path=full),i//5,i%5)
        self.cl.addWidget(w)

    def _main(self):
        w = QWidget(); w.setStyleSheet("background:transparent")
        g = QGridLayout(w); g.setSpacing(14)
        for i,(n,t,s) in enumerate([("فهرس السور","q_list"," سور القران الكريم"),("الأذكار","a_list","أذكار وأدعية"),("سور قصيرة للصلاة","i_list","صفحات مصورة")]):
            g.addWidget(Card(n,t,self.nav,s),0,i)
        self.cl.addWidget(w)

    def _surah(self, name):
        sn = name.replace("سورة ","")
        vs = sorted([v for v in self.Q if v["sura_name_ar"]==sn], key=lambda x:int(x["aya_no"]))
        if not vs: return
        self._audio(vs[0]["sura_no"], name)
        h = QFrame(); h.setObjectName("SHdr"); hl = QVBoxLayout(h); hl.setSpacing(3); hl.setContentsMargins(12,10,12,10)
        n = QLabel(f"سورة {sn}"); n.setObjectName("SName"); n.setAlignment(Qt.AlignCenter)
        c = QLabel(f"عدد الآيات: {len(vs)}"); c.setObjectName("SCntL"); c.setAlignment(Qt.AlignCenter)
        hl.addWidget(n); hl.addWidget(c); self.cl.addWidget(h)
        for v in vs:
            taf = self._tidx.get((str(v["sura_no"]),str(v["aya_no"])),"التفسير غير متوفر.")
            self.cl.addWidget(VCard(v["aya_text_emlaey"],taf,v["aya_no"]))

    def _zekr(self, snip):
        item = next((a for a in self.A if a["zekr"].startswith(snip.rstrip("."))),None)
        if not item: return
        f = QFrame(); f.setObjectName("ZCard"); fl = QVBoxLayout(f); fl.setContentsMargins(20,16,20,16); fl.setSpacing(8)
        t = QLabel(item["zekr"]); t.setObjectName("ZTxt"); t.setWordWrap(True); t.setAlignment(Qt.AlignRight); fl.addWidget(t)
        r = QLabel(f"التكرار: {item.get('repeat','1')}"); r.setObjectName("ZRep"); fl.addWidget(r)
        self.cl.addWidget(f)

    def _img(self, path):
        # hide old overlay without destroying the scroll content behind it
        if self._img_w:
            self._img_w.hide(); self._img_w.deleteLater(); self._img_w = None
        ow = QWidget(self.win); ow.setObjectName("ImgOv")
        ow.setGeometry(6, 52, self.win.width()-12, self.win.height()-58)
        ow.setContextMenuPolicy(Qt.NoContextMenu)
        ol = QVBoxLayout(ow); ol.setContentsMargins(14,10,14,12); ol.setSpacing(8)
        cr = QHBoxLayout()
        cb = QPushButton("✕  إغلاق"); cb.setObjectName("IClose"); cb.setCursor(Qt.PointingHandCursor)
        # FIX: close button only hides overlay — scroll content stays intact
        cb.clicked.connect(lambda: self._close_img())
        cr.addStretch(); cr.addWidget(cb); ol.addLayout(cr)
        fr = QFrame(); fr.setObjectName("ImgF"); fl = QVBoxLayout(fr); fl.setContentsMargins(6,6,6,6)
        il = QLabel(); px = QPixmap(path)
        if not px.isNull():
            il.setPixmap(px.scaled(ow.width()-60, ow.height()-120, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        il.setAlignment(Qt.AlignCenter); il.setStyleSheet("background:transparent;border:none"); fl.addWidget(il)
        ol.addWidget(fr)
        cp = QLabel(os.path.splitext(os.path.basename(path))[0]); cp.setObjectName("ICap"); cp.setAlignment(Qt.AlignCenter); ol.addWidget(cp)
        self._img_w = ow; ow.show(); ow.raise_()

    def _close_img(self):
        """Hide image overlay and restore the image grid view."""
        if self._img_w:
            self._img_w.hide(); self._img_w.deleteLater(); self._img_w = None
        # pop the view_img entry from history and go back to i_list
        self.hist = [(t,d) for t,d in self.hist if t != "view_img"]
        self.nav("i_list")

    def _audio(self, no, name):
        p = res(f"Quraan/{str(no).zfill(3)}.mp3")
        if not os.path.exists(p): return
        self.player.setSource(QUrl.fromLocalFile(p)); self.player.play()
        self.plbl.setText(f"تشغيل: {name}"); self.pp.setText("◾"); self._dtimer.start(380)

    def _tog(self):
        if self.player.playbackState() == QMediaPlayer.PlayingState:
            self.player.pause(); self.pp.setText("▶"); self._dtimer.stop()
            self.dt.setText("○ ○ ○"); self.dt.setStyleSheet("color:#1e1e1e;font-size:10px;letter-spacing:4px")
        else:
            self.player.play(); self.pp.setText("◾"); self._dtimer.start(380)

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton: self._dp = e.globalPosition().toPoint() - self.frameGeometry().topLeft()
    def mouseMoveEvent(self, e):
        if e.buttons() == Qt.LeftButton and self._dp: self.move(e.globalPosition().toPoint() - self._dp)
    def mouseReleaseEvent(self, e): self._dp = None
    def resizeEvent(self, e):
        super().resizeEvent(e)
        if self._img_w and self._img_w.isVisible():
            self._img_w.setGeometry(6, 52, self.win.width()-12, self.win.height()-58)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setContextMenuPolicy = lambda *a: None  # extra guard
    for f in (res("Amiri-Regular.ttf"), res("fonts/Amiri-Regular.ttf")):
        if os.path.exists(f): QFontDatabase.addApplicationFont(f)
    w = App(); w.show(); sys.exit(app.exec())