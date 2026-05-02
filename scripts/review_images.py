#!/usr/bin/env python3
"""
Image gallery reviewer — document-by-document grid UI.

Shows 48 images at a time (8×6 grid) for one document.
Click the red X on any image to reject it. Everything else is kept by default.
Paginate through images within a doc, then move to the next doc.

Run: python3 scripts/review_images.py
Then open: http://localhost:8765
"""

from __future__ import annotations
import json, sys, webbrowser, threading, urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).parent))
from _paths import REFS_ROOT

OUT = REFS_ROOT / "private" / "_extracted"
STATUS_PATH = OUT / "_review_status.json"
PORT = 8765

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Image Reviewer — Linear A</title>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: system-ui, sans-serif; background: #1a1a1a; color: #ddd;
       display: flex; height: 100vh; overflow: hidden; }

/* ── Left sidebar: doc list ── */
#doclist {
  width: 240px; flex-shrink: 0; background: #111;
  border-right: 1px solid #2a2a2a; overflow-y: auto; display: flex; flex-direction: column;
}
#doclist h2 { font-size: 12px; color: #666; padding: 10px 12px 6px; text-transform: uppercase; letter-spacing: 0.05em; flex-shrink: 0; }
.doc-item {
  padding: 7px 12px; cursor: pointer; font-size: 12px; color: #999;
  border-left: 3px solid transparent; line-height: 1.4;
  display: flex; flex-direction: column; gap: 2px;
}
.doc-item:hover { background: #1c1c1c; color: #ccc; }
.doc-item.active { background: #1a2a3a; border-left-color: #4a7fb5; color: #ddd; }
.doc-item.done { color: #666; }
.doc-name { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 200px; }
.doc-meta { font-size: 10px; color: #555; }
.doc-item.active .doc-meta { color: #7a9ab5; }
.doc-progress { height: 2px; background: #2a2a2a; margin-top: 3px; border-radius: 1px; }
.doc-progress-bar { height: 100%; background: #3a6a3a; border-radius: 1px; }

/* ── Main area ── */
#main { flex: 1; display: flex; flex-direction: column; overflow: hidden; }

#topbar {
  padding: 10px 16px; background: #111; border-bottom: 1px solid #2a2a2a;
  display: flex; align-items: center; gap: 12px; flex-shrink: 0;
}
#topbar h1 { font-size: 14px; color: #fff; font-weight: 600; }
#doc-title { font-size: 12px; color: #666; flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
#page-info { font-size: 12px; color: #555; white-space: nowrap; }
#overall-stats { font-size: 11px; color: #555; white-space: nowrap; }

/* ── Grid ── */
#grid-area { flex: 1; overflow-y: auto; padding: 12px; }
#grid {
  display: grid;
  grid-template-columns: repeat(8, 1fr);
  gap: 6px;
}
.img-cell {
  position: relative; background: #111; border: 1px solid #222;
  border-radius: 4px; overflow: hidden; aspect-ratio: 1;
  display: flex; align-items: center; justify-content: center;
}
.img-cell.rejected { opacity: 0.25; border-color: #5a2a2a; }
.img-cell img {
  max-width: 100%; max-height: 100%; object-fit: contain;
  display: block;
}
.img-cell .reject-btn {
  position: absolute; top: 3px; right: 3px;
  width: 22px; height: 22px; border-radius: 50%;
  background: rgba(180,40,40,0.85); border: none; cursor: pointer;
  color: #fff; font-size: 13px; line-height: 22px; text-align: center;
  opacity: 0; transition: opacity 0.15s;
  display: flex; align-items: center; justify-content: center;
}
.img-cell:hover .reject-btn { opacity: 1; }
.img-cell.rejected .reject-btn { opacity: 0.8; background: rgba(60,180,60,0.85); }
.img-cell .img-dims {
  position: absolute; bottom: 2px; left: 3px;
  font-size: 9px; color: #555; pointer-events: none;
  background: rgba(0,0,0,0.5); padding: 1px 3px; border-radius: 2px;
}

/* ── Bottom nav ── */
#bottombar {
  padding: 10px 16px; background: #111; border-top: 1px solid #2a2a2a;
  display: flex; align-items: center; gap: 10px; flex-shrink: 0;
}
.nav-btn {
  padding: 7px 16px; border-radius: 5px; border: 1px solid #333;
  background: #222; color: #bbb; cursor: pointer; font-size: 13px;
}
.nav-btn:hover { background: #2a2a2a; color: #fff; }
.nav-btn:disabled { opacity: 0.3; cursor: default; }
.nav-btn.primary { background: #1e3a5c; border-color: #4a7fb5; color: #fff; }
.nav-btn.primary:hover { background: #254a72; }
#reject-page-btn {
  margin-left: auto;
  padding: 7px 14px; border-radius: 5px; border: 1px solid #5a2a2a;
  background: #2a1010; color: #cc6666; cursor: pointer; font-size: 12px;
}
#reject-page-btn:hover { background: #3a1515; }
</style>
</head>
<body>

<div id="doclist">
  <h2>Documents</h2>
  <div id="doc-items"></div>
</div>

<div id="main">
  <div id="topbar">
    <h1>Linear A — Image Review</h1>
    <span id="doc-title">Loading…</span>
    <span id="page-info"></span>
    <span id="overall-stats"></span>
  </div>

  <div id="grid-area">
    <div id="grid"></div>
  </div>

  <div id="bottombar">
    <button class="nav-btn" id="prev-doc-btn" onclick="changeDoc(-1)">◀ Prev Doc</button>
    <button class="nav-btn" id="prev-page-btn" onclick="changePage(-1)">‹ Prev Page</button>
    <button class="nav-btn primary" id="next-page-btn" onclick="changePage(1)">Next Page ›</button>
    <button class="nav-btn primary" id="next-doc-btn" onclick="changeDoc(1)">Next Doc ▶</button>
    <button id="reject-page-btn" onclick="rejectPage()">✗ Reject this page</button>
  </div>
</div>

<script>
const PER_PAGE = 48; // 8×6

let docs = [];        // [{doc_uuid, source_path, images:[...]}]
let status = {};      // sha256 → {decision}
let docIdx = 0;
let pageIdx = 0;
let docSeen = new Set();  // doc_uuids where last page was reached

async function load() {
  const [imgResp, statResp] = await Promise.all([
    fetch('/api/images'),
    fetch('/api/status'),
  ]);
  const allImages = await imgResp.json();
  status = await statResp.json();

  // Group by doc_uuid, preserving order
  const docMap = new Map();
  for (const img of allImages) {
    if (!docMap.has(img.doc_uuid)) {
      docMap.set(img.doc_uuid, { doc_uuid: img.doc_uuid, source_path: img.source_path, images: [] });
    }
    docMap.get(img.doc_uuid).images.push(img);
  }
  docs = Array.from(docMap.values());

  renderDocList();
  showDoc(0);
}

function shortName(src) {
  // Show just the filename without path prefix clutter
  const parts = src.split('/');
  return parts[parts.length - 1].replace(/\.pdf$/i, '');
}

function docRejectedCount(doc) {
  return doc.images.filter(i => (status[i.sha256] || {}).decision === 'reject').length;
}

function renderDocList() {
  const container = document.getElementById('doc-items');
  container.innerHTML = '';
  docs.forEach((doc, i) => {
    const div = document.createElement('div');
    div.id = `doc-item-${i}`;
    container.appendChild(div);
    updateDocItem(i);
    div.onclick = () => { showDoc(i); };
  });
}

function updateDocItem(i) {
  const doc = docs[i];
  const el = document.getElementById(`doc-item-${i}`);
  if (!el) return;
  const total = doc.images.length;
  const rej = docRejectedCount(doc);
  const pct = total > 0 ? (rej / total * 100) : 0;
  const seen = docSeen.has(doc.doc_uuid);
  el.className = 'doc-item' + (i === docIdx ? ' active' : '') + (seen ? ' done' : '');
  el.innerHTML = `
    <span class="doc-name" title="${doc.source_path}">${seen ? '✓ ' : ''}${shortName(doc.source_path)}</span>
    <span class="doc-meta">${total} images · ${rej} rejected</span>
    <div class="doc-progress"><div class="doc-progress-bar" style="width:${pct}%"></div></div>
  `;
}

function showDoc(idx) {
  docIdx = Math.max(0, Math.min(idx, docs.length - 1));
  pageIdx = 0;
  document.querySelectorAll('.doc-item').forEach((el, i) => el.classList.toggle('active', i === docIdx));
  const activeEl = document.getElementById(`doc-item-${docIdx}`);
  if (activeEl) activeEl.scrollIntoView({ block: 'nearest' });
  renderGrid();
  updateNav();
}

function renderGrid() {
  const doc = docs[docIdx];
  if (!doc) return;

  const start = pageIdx * PER_PAGE;
  const pageImgs = doc.images.slice(start, start + PER_PAGE);
  const totalPages = Math.ceil(doc.images.length / PER_PAGE);

  document.getElementById('doc-title').textContent = shortName(doc.source_path);
  document.getElementById('page-info').textContent =
    `Page ${pageIdx + 1} of ${totalPages} · images ${start + 1}–${Math.min(start + PER_PAGE, doc.images.length)} of ${doc.images.length}`;

  const grid = document.getElementById('grid');
  grid.innerHTML = '';

  pageImgs.forEach(img => {
    const d = (status[img.sha256] || {}).decision;
    const rejected = d === 'reject';
    const cell = document.createElement('div');
    cell.className = 'img-cell' + (rejected ? ' rejected' : '');
    cell.innerHTML = `
      <img src="/img/${img.doc_uuid}/${img.filename}" loading="lazy"
           onerror="this.style.display='none'" alt="">
      <button class="reject-btn" title="${rejected ? 'Un-reject' : 'Reject'}"
              onclick="toggleReject('${img.sha256}', this.closest('.img-cell'))">
        ${rejected ? '✓' : '✕'}
      </button>
      <span class="img-dims">${img.width}×${img.height}</span>
    `;
    grid.appendChild(cell);
  });

  updateStats();
}

async function toggleReject(sha, cell) {
  const current = (status[sha] || {}).decision;
  const newDecision = current === 'reject' ? 'pending' : 'reject';
  status[sha] = { ...(status[sha] || {}), decision: newDecision };

  cell.classList.toggle('rejected', newDecision === 'reject');
  const btn = cell.querySelector('.reject-btn');
  btn.textContent = newDecision === 'reject' ? '✓' : '✕';
  btn.title = newDecision === 'reject' ? 'Un-reject' : 'Reject';

  await fetch('/api/status', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ sha256: sha, decision: newDecision }),
  });

  // Update sidebar count
  const doc = docs[docIdx];
  const rej = docRejectedCount(doc);
  const el = document.getElementById(`doc-item-${docIdx}`);
  if (el) {
    el.querySelector('.doc-meta').textContent = `${doc.images.length} images · ${rej} rejected`;
    el.querySelector('.doc-progress-bar').style.width = (rej / doc.images.length * 100) + '%';
  }
  updateStats();
}

async function rejectPage() {
  const doc = docs[docIdx];
  const start = pageIdx * PER_PAGE;
  const pageImgs = doc.images.slice(start, start + PER_PAGE);
  for (const img of pageImgs) {
    status[img.sha256] = { ...(status[img.sha256] || {}), decision: 'reject' };
  }
  await fetch('/api/bulk-list', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ shas: pageImgs.map(i => i.sha256), decision: 'reject' }),
  });
  renderGrid();
  renderDocList();
}

function changePage(delta) {
  const doc = docs[docIdx];
  const totalPages = Math.ceil(doc.images.length / PER_PAGE);
  const newPage = pageIdx + delta;
  if (delta > 0 && newPage >= totalPages) {
    // Last page done — mark doc seen and advance to next doc
    docSeen.add(doc.doc_uuid);
    updateDocItem(docIdx);
    if (docIdx < docs.length - 1) {
      showDoc(docIdx + 1);
    }
    return;
  }
  pageIdx = Math.max(0, Math.min(newPage, totalPages - 1));
  renderGrid();
  updateNav();
  document.getElementById('grid-area').scrollTop = 0;
}

function changeDoc(delta) {
  showDoc(docIdx + delta);
  document.getElementById('grid-area').scrollTop = 0;
}

function updateNav() {
  const doc = docs[docIdx];
  const totalPages = Math.ceil((doc?.images.length || 0) / PER_PAGE);
  document.getElementById('prev-doc-btn').disabled = docIdx === 0;
  document.getElementById('next-doc-btn').disabled = docIdx >= docs.length - 1;
  document.getElementById('prev-page-btn').disabled = pageIdx === 0;
  document.getElementById('next-page-btn').disabled = pageIdx >= totalPages - 1;
}

function updateStats() {
  const totalImgs = docs.reduce((s, d) => s + d.images.length, 0);
  const totalRej = Object.values(status).filter(v => v.decision === 'reject').length;
  const autoRej = Object.values(status).filter(v => v.decision === 'auto_rejected').length;
  document.getElementById('overall-stats').textContent =
    `${totalRej} rejected · ${autoRej} auto-culled · ${totalImgs - totalRej - autoRej} kept`;
}

document.addEventListener('keydown', e => {
  if (e.key === 'ArrowRight' || e.key === 'n') changePage(1);
  if (e.key === 'ArrowLeft'  || e.key === 'p') changePage(-1);
  if (e.key === ']') changeDoc(1);
  if (e.key === '[') changeDoc(-1);
});

load();
</script>
</body>
</html>
"""


def load_status() -> dict:
    if STATUS_PATH.exists():
        return json.loads(STATUS_PATH.read_text())
    return {}


def save_status(status: dict):
    STATUS_PATH.write_text(json.dumps(status, indent=2, ensure_ascii=False) + "\n")


def build_image_list() -> list[dict]:
    images = []
    for mf in sorted(OUT.glob("*/manifest.json")):
        manifest = json.loads(mf.read_text())
        doc_uuid = manifest["uuid"]
        source = manifest.get("source_path", "")
        for img in manifest.get("images", []):
            sha = img.get("sha256", "")
            if not sha:
                continue
            path = img.get("file", "")
            filename = Path(path).name if path else ""
            dec = (load_status().get(sha) or {}).get("decision", "")
            if dec == "auto_rejected":
                continue  # hide auto-culled from gallery
            images.append({
                "sha256": sha,
                "doc_uuid": doc_uuid,
                "source_path": source,
                "filename": filename,
                "width": img.get("width", 0),
                "height": img.get("height", 0),
                "size_bytes": img.get("bytes", 0),
                "page": img.get("page", 0),
            })
    return images


class Handler(BaseHTTPRequestHandler):
    images: list[dict] = []
    status: dict = {}

    def log_message(self, fmt, *args):
        pass

    def send_json(self, data, code=200):
        body = json.dumps(data).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path

        if path in ("/", "/index.html"):
            body = HTML.encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", len(body))
            self.end_headers()
            self.wfile.write(body)

        elif path == "/api/images":
            self.send_json(Handler.images)

        elif path == "/api/status":
            self.send_json(Handler.status)

        elif path.startswith("/img/"):
            parts = path[5:].split("/", 1)
            if len(parts) == 2:
                doc_uuid, filename = parts
                img_path = OUT / doc_uuid / "images" / filename
                if img_path.exists():
                    data = img_path.read_bytes()
                    ext = img_path.suffix.lower().lstrip(".")
                    mime = {"png": "image/png", "jpg": "image/jpeg",
                            "jpeg": "image/jpeg", "gif": "image/gif",
                            "webp": "image/webp"}.get(ext, "application/octet-stream")
                    self.send_response(200)
                    self.send_header("Content-Type", mime)
                    self.send_header("Content-Length", len(data))
                    self.end_headers()
                    self.wfile.write(data)
                    return
            self.send_response(404)
            self.end_headers()

        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length))
        path = urllib.parse.urlparse(self.path).path

        if path == "/api/status":
            sha = body.get("sha256")
            decision = body.get("decision")
            if sha and decision:
                Handler.status[sha] = {**(Handler.status.get(sha) or {}), "decision": decision}
                save_status(Handler.status)
            self.send_json({"ok": True})

        elif path == "/api/bulk":
            doc_uuid = body.get("doc_uuid")
            decision = body.get("decision", "reject")
            count = 0
            for img in Handler.images:
                if img["doc_uuid"] == doc_uuid:
                    Handler.status[img["sha256"]] = {
                        **(Handler.status.get(img["sha256"]) or {}),
                        "decision": decision,
                    }
                    count += 1
            save_status(Handler.status)
            self.send_json({"ok": True, "count": count})

        elif path == "/api/bulk-list":
            shas = body.get("shas", [])
            decision = body.get("decision", "reject")
            for sha in shas:
                Handler.status[sha] = {**(Handler.status.get(sha) or {}), "decision": decision}
            save_status(Handler.status)
            self.send_json({"ok": True, "count": len(shas)})

        else:
            self.send_response(404)
            self.end_headers()


def main():
    if not OUT.exists():
        print(f"No extraction folder at {OUT}")
        print("Run extract_all_pdfs.py first, then cull_images.py, then this.")
        sys.exit(1)

    print("Loading image index…", end=" ", flush=True)
    Handler.status = load_status()
    Handler.images = build_image_list()

    n_docs = len({img["doc_uuid"] for img in Handler.images})
    auto_rej = sum(1 for v in Handler.status.values() if v.get("decision") == "auto_rejected")
    print(f"{len(Handler.images)} images across {n_docs} documents ({auto_rej} auto-culled, hidden)")

    url = f"http://localhost:{PORT}"
    print(f"Starting server at {url}  (Ctrl+C to stop)\n")
    print("Keyboard shortcuts:")
    print("  → / n    next page       ← / p    prev page")
    print("  ]        next document   [        prev document")

    threading.Timer(1.0, lambda: webbrowser.open(url)).start()
    server = HTTPServer(("localhost", PORT), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
