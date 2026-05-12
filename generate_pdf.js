/**
 * RE Support System — Enterprise PDF Generator
 * Uses: marked (MD→HTML) + puppeteer (HTML→PDF) + mermaid.js (diagrams)
 */

const fs   = require('fs');
const path = require('path');

// ── Resolve marked ────────────────────────────────────────────────────────────
let marked;
try { marked = require('marked').marked || require('marked'); }
catch(e) { console.error('marked not found'); process.exit(1); }

// ── Read the markdown source ──────────────────────────────────────────────────
const mdPath = path.join(__dirname, 'RE_Support_Functional_Flow_Document.md');
const mdRaw  = fs.readFileSync(mdPath, 'utf8');

// ── Convert markdown → HTML (keep mermaid blocks as-is for JS rendering) ─────
const renderer = new (require('marked').Renderer || Object)();
const bodyHtml = marked(mdRaw, {
  gfm: true,
  breaks: false,
  headerIds: true,
  mangle: false,
});

// ── Wrap mermaid code blocks so the JS can find them ─────────────────────────
const processedHtml = bodyHtml.replace(
  /<pre><code class="language-mermaid">([\s\S]*?)<\/code><\/pre>/g,
  (_, code) => {
    // Decode HTML entities that marked encoded
    const decoded = code
      .replace(/&amp;/g, '&')
      .replace(/&lt;/g, '<')
      .replace(/&gt;/g, '>')
      .replace(/&quot;/g, '"')
      .replace(/&#39;/g, "'");
    return `<div class="mermaid-wrapper"><div class="mermaid">${decoded}</div></div>`;
  }
);

// ── Build the full enterprise HTML ───────────────────────────────────────────
const fullHtml = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<title>RE Support System — Functional Flow Document</title>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"><\/script>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  --blue-900: #0B2545;
  --blue-800: #13315C;
  --blue-700: #1A4080;
  --blue-600: #1D5299;
  --blue-400: #3B82C4;
  --blue-300: #93B8DB;
  --blue-100: #E8F0FA;
  --blue-50:  #F4F8FD;
  --gray-900: #1A1A2E;
  --gray-700: #374151;
  --gray-500: #6B7280;
  --gray-300: #D1D5DB;
  --gray-100: #F3F4F6;
  --gray-50:  #FAFAFA;
  --white:    #FFFFFF;
  --font:     'Inter', -apple-system, sans-serif;
  --mono:     'JetBrains Mono', 'Courier New', monospace;
  --radius:   6px;
  --shadow:   0 2px 8px rgba(0,0,0,.10);
}

/* ── Page (A4) ── */
@page {
  size: A4 portrait;
  margin: 22mm 18mm 22mm 18mm;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { font-size: 10.5pt; }
body {
  font-family: var(--font);
  color: var(--gray-700);
  line-height: 1.7;
  background: var(--white);
  -webkit-font-smoothing: antialiased;
}

/* ────── COVER PAGE ────── */
.cover-page {
  page-break-after: always;
  height: 267mm;
  background: linear-gradient(155deg, #0B2545 0%, #1A4080 55%, #1D5299 100%);
  color: #fff;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
}
.cover-circle-1 {
  position: absolute; top: -80px; right: -80px;
  width: 320px; height: 320px; border-radius: 50%;
  background: rgba(255,255,255,.04);
  border: 1px solid rgba(255,255,255,.08);
}
.cover-circle-2 {
  position: absolute; bottom: 40px; right: 20px;
  width: 180px; height: 180px; border-radius: 50%;
  background: rgba(255,255,255,.03);
  border: 1px solid rgba(255,255,255,.06);
}
.cover-top {
  background: rgba(255,255,255,.08);
  padding: 14px 36px;
  display: flex; align-items: center; gap: 12px;
  border-bottom: 1px solid rgba(255,255,255,.12);
}
.cover-logo {
  width: 38px; height: 38px; border-radius: 8px;
  background: #3B82C4;
  display: flex; align-items: center; justify-content: center;
  font-size: 15pt; font-weight: 800; letter-spacing: -1px;
}
.cover-app { font-size: 9pt; font-weight: 600; letter-spacing: .1em; text-transform: uppercase; opacity: .8; }
.cover-body {
  flex: 1; padding: 48px 36px 28px;
  display: flex; flex-direction: column; justify-content: center;
}
.cover-badge {
  display: inline-block;
  background: rgba(255,255,255,.12);
  border: 1px solid rgba(255,255,255,.22);
  border-radius: 20px;
  padding: 4px 14px; margin-bottom: 22px;
  font-size: 7.5pt; font-weight: 600;
  letter-spacing: .1em; text-transform: uppercase;
  color: #93B8DB; width: fit-content;
}
.cover-title {
  font-size: 34pt; font-weight: 800;
  line-height: 1.08; letter-spacing: -1px;
  margin-bottom: 6px; color: #fff;
}
.cover-title span { color: #93B8DB; }
.cover-subtitle {
  font-size: 12pt; font-weight: 400;
  color: rgba(255,255,255,.72); line-height: 1.45;
  max-width: 480px; margin-bottom: 36px;
}
.cover-line { width: 56px; height: 3px; border-radius: 2px;
  background: linear-gradient(90deg, #93B8DB, transparent);
  margin-bottom: 32px;
}
.cover-grid {
  display: grid; grid-template-columns: 1fr 1fr;
  gap: 12px; max-width: 440px; margin-bottom: 36px;
}
.cover-card {
  background: rgba(255,255,255,.07);
  border: 1px solid rgba(255,255,255,.12);
  border-radius: var(--radius); padding: 10px 14px;
}
.cover-card .lbl { font-size: 7pt; text-transform: uppercase; letter-spacing: .09em; color: #93B8DB; font-weight: 600; margin-bottom: 3px; }
.cover-card .val { font-size: 9pt; font-weight: 500; color: rgba(255,255,255,.9); }
.cover-stats { display: flex; gap: 22px; }
.c-stat .num { font-size: 22pt; font-weight: 800; color: #fff; display: block; }
.c-stat .lbl { font-size: 7pt; text-transform: uppercase; letter-spacing: .08em; color: #93B8DB; font-weight: 600; }
.cover-footer {
  background: rgba(0,0,0,.22);
  padding: 12px 36px;
  display: flex; justify-content: space-between;
  font-size: 7.5pt; color: rgba(255,255,255,.45);
  border-top: 1px solid rgba(255,255,255,.1);
}

/* ────── TOC PAGE ────── */
.toc-page { page-break-after: always; padding: 8px 0 20px; }
.toc-h { font-size: 18pt; font-weight: 700; color: var(--blue-800);
  padding-bottom: 8px; border-bottom: 2px solid var(--blue-600); margin-bottom: 4px; }
.toc-sub { font-size: 8.5pt; color: var(--gray-500); margin-bottom: 22px; }
.toc-row { display: flex; align-items: baseline; padding: 5.5px 0;
  border-bottom: 1px dotted var(--gray-300); font-size: 9.5pt; }
.toc-row.l1 { font-weight: 600; color: var(--blue-800); }
.toc-row.l2 { padding-left: 18px; font-size: 9pt; color: var(--gray-700); }
.toc-row.l3 { padding-left: 34px; font-size: 8.5pt; color: var(--gray-500); }
.toc-n { min-width: 30px; font-weight: 700; color: var(--blue-600); }
.toc-dots { flex:1; margin: 0 8px; }

/* ────── RUNNING HEADER / FOOTER ────── */
.page-header {
  display: flex; justify-content: space-between;
  font-size: 7.5pt; color: var(--gray-500);
  padding-bottom: 6px; margin-bottom: 18px;
  border-bottom: 1px solid var(--gray-300);
}
.page-header strong { color: var(--blue-600); }
.page-footer {
  display: flex; justify-content: space-between;
  font-size: 7.5pt; color: var(--gray-500);
  padding-top: 6px; margin-top: 22px;
  border-top: 1px solid var(--gray-300);
}

/* ────── SECTION BANNER ────── */
h1 {
  font-family: var(--font);
  font-size: 16pt; font-weight: 700;
  color: var(--white);
  background: linear-gradient(135deg, var(--blue-900), var(--blue-700));
  padding: 18px 22px; margin: 0 0 22px 0;
  border-radius: 0 0 var(--radius) var(--radius);
  page-break-before: always; page-break-after: avoid;
  position: relative; overflow: hidden;
}
h1::before {
  content:''; position:absolute; top:0; left:0; right:0; height:3px;
  background: linear-gradient(90deg, #93B8DB, var(--blue-400), transparent);
}

/* ────── HEADINGS ────── */
h2 {
  font-size: 13pt; font-weight: 700; color: var(--blue-800);
  margin: 26px 0 12px; padding-bottom: 6px;
  border-bottom: 2px solid var(--blue-100);
  position: relative; page-break-after: avoid;
}
h2::after {
  content:''; position:absolute; bottom:-2px; left:0;
  width:36px; height:2px; background: var(--blue-600);
}
h3 { font-size: 11.5pt; font-weight: 700; color: var(--blue-700); margin: 18px 0 8px; page-break-after:avoid; }
h4 { font-size: 10.5pt; font-weight: 600; color: var(--gray-700); margin: 14px 0 6px; page-break-after:avoid; }
h5, h6 { font-size: 10pt; font-weight: 600; color: var(--gray-500); margin: 10px 0 6px; }

/* ────── PARAGRAPH ────── */
p { margin: 0 0 12px; }
strong { font-weight: 700; color: var(--gray-900); }
em { font-style: italic; }
a { color: var(--blue-600); text-decoration: none; }
del { text-decoration: line-through; color: var(--gray-500); }

/* ────── CODE ────── */
code {
  font-family: var(--mono); font-size: 8.5pt;
  background: var(--gray-100); color: var(--blue-700);
  padding: 2px 5px; border-radius: 4px;
  border: 1px solid var(--gray-300);
}
pre {
  background: #1E293B; color: #E2E8F0;
  border-radius: var(--radius); padding: 14px 16px;
  font-family: var(--mono); font-size: 8pt; line-height: 1.6;
  margin: 14px 0 18px; page-break-inside: avoid;
  border-left: 3px solid var(--blue-400);
  box-shadow: var(--shadow); overflow: hidden;
}
pre code { background:transparent; color:inherit; border:none; padding:0; font-size:inherit; }

/* ────── TABLES ────── */
table { width:100%; border-collapse:collapse; margin:12px 0 20px;
  font-size: 9pt; page-break-inside: auto; box-shadow: var(--shadow);
  border-radius: var(--radius); overflow:hidden; }
thead { background: linear-gradient(135deg, var(--blue-800), var(--blue-700)); color: var(--white); }
thead th { padding:9px 11px; text-align:left; font-weight:600; font-size:8.5pt; letter-spacing:.03em; border:none; }
tbody tr:nth-child(even) { background: var(--blue-50); }
tbody tr:nth-child(odd)  { background: var(--white); }
tbody tr { page-break-inside:avoid; }
td { padding:7px 11px; border-bottom:1px solid var(--gray-100); vertical-align:top; line-height:1.5; }
tr:last-child td { border-bottom:none; }

/* ────── LISTS ────── */
ul, ol { padding-left:22px; margin:6px 0 12px; }
li { margin-bottom:5px; line-height:1.6; }
li::marker { color: var(--blue-600); }
ul ul, ol ol { margin:4px 0 4px 8px; }

/* ────── BLOCKQUOTE ────── */
blockquote {
  background: linear-gradient(135deg, var(--blue-50), var(--white));
  border-left: 4px solid var(--blue-600);
  border-radius: 0 var(--radius) var(--radius) 0;
  margin: 14px 0; padding: 12px 16px;
  color: var(--blue-800); font-size: 10pt;
  box-shadow: var(--shadow); page-break-inside: avoid;
}
blockquote p { margin:0; }

/* ────── HR ────── */
hr { border:none; border-top:1px solid var(--gray-300); margin:20px 0; }

/* ────── MERMAID ────── */
.mermaid-wrapper {
  background: var(--white);
  border: 1px solid var(--gray-300); border-radius: var(--radius);
  padding: 18px; margin: 18px 0; text-align: center;
  page-break-inside: avoid; box-shadow: var(--shadow);
}
.mermaid { display:inline-block; max-width:100%; }
.mermaid svg { max-width:100%; height:auto; }

/* ────── PRINT ────── */
@media print {
  h1 { page-break-before: always; }
  h1, h2, h3, h4 { page-break-after: avoid; }
  table, pre, blockquote, .mermaid-wrapper { page-break-inside: avoid; }
  tr { page-break-inside: avoid; }
}
</style>
</head>
<body>

<!-- ══ COVER PAGE ══════════════════════════════════════════════════════════ -->
<div class="cover-page">
  <div class="cover-circle-1"></div>
  <div class="cover-circle-2"></div>

  <div class="cover-top">
    <div class="cover-logo">RSS</div>
    <span class="cover-app">re_support &nbsp;·&nbsp; Frappe / ERPNext v15+</span>
  </div>

  <div class="cover-body">
    <div class="cover-badge">Enterprise Documentation · Version 1.0 · 2026</div>
    <div class="cover-title">Real Estate<br/><span>Support System</span></div>
    <p class="cover-subtitle">
      Enterprise Functional Flow &amp; Solution Architecture Document<br/>
      Complaints · Defects · Possession · RERA · Self-Service Portal · Analytics
    </p>
    <div class="cover-line"></div>

    <div class="cover-grid">
      <div class="cover-card"><div class="lbl">Document Type</div><div class="val">Functional Flow &amp; Architecture</div></div>
      <div class="cover-card"><div class="lbl">Version</div><div class="val">1.0 — April 2026</div></div>
      <div class="cover-card"><div class="lbl">Platform</div><div class="val">Frappe / ERPNext v15+</div></div>
      <div class="cover-card"><div class="lbl">Classification</div><div class="val">Confidential — Internal Use</div></div>
    </div>

    <div class="cover-stats">
      <div class="c-stat"><span class="num">6</span><span class="lbl">Modules</span></div>
      <div class="c-stat"><span class="num">26+</span><span class="lbl">DocTypes</span></div>
      <div class="c-stat"><span class="num">9</span><span class="lbl">Reports</span></div>
      <div class="c-stat"><span class="num">7</span><span class="lbl">Roles</span></div>
      <div class="c-stat"><span class="num">14</span><span class="lbl">Sections</span></div>
    </div>
  </div>

  <div class="cover-footer">
    <span>Prepared for: Functional &amp; Implementation Teams</span>
    <span>re_support · frappe.io / erpnext.com</span>
    <span>April 2026</span>
  </div>
</div>

<!-- ══ TABLE OF CONTENTS ═══════════════════════════════════════════════════ -->
<div class="toc-page">
  <div class="toc-h">Table of Contents</div>
  <div class="toc-sub">Real Estate Support System — Enterprise Functional Flow Document</div>
  ${[
    ['1','System Overview','l1'],
    ['1.1','Purpose of the System','l2'],
    ['1.2','Business Problem Solved','l2'],
    ['1.3','Industry / Domain','l2'],
    ['1.4','Main Objectives','l2'],
    ['1.5','Core Functionalities','l2'],
    ['1.6','System Scope','l2'],
    ['1.7','Target Users','l2'],
    ['1.8','Business Benefits','l2'],
    ['2','High-Level System Architecture','l1'],
    ['2.1','Overall Architecture','l2'],
    ['2.2','Frontend Architecture','l2'],
    ['2.3','Backend Architecture','l2'],
    ['2.4','Request-Response Flow','l2'],
    ['2.5','Authentication Flow','l2'],
    ['2.6','Module Interaction Diagram','l2'],
    ['3','Module-Wise Functional Breakdown','l1'],
    ['3.1','Module 1: Complaint Management','l2'],
    ['3.2','Module 2: Defect & Snagging','l2'],
    ['3.3','Module 3: Possession Management','l2'],
    ['3.4','Module 4: RERA Escalation','l2'],
    ['3.5','Module 5: Buyer Portal','l2'],
    ['3.6','Module 6: Reports & Analytics','l2'],
    ['4','End-to-End Business Process Flows','l1'],
    ['4.1','Buyer Complaint → Resolution','l2'],
    ['4.2','Defect Inspection → Buyer Acceptance','l2'],
    ['4.3','Possession Handover Flow','l2'],
    ['4.4','RERA Escalation Flow','l2'],
    ['4.5','Buyer Self-Service Portal Journey','l2'],
    ['5','Role-Based System Flow','l1'],
    ['5.1','Role Definitions & Responsibilities','l2'],
    ['5.2','Role-Based Permission Matrix','l2'],
    ['5.3','Dashboard Visibility by Role','l2'],
    ['6','Database & Data Flow Understanding','l1'],
    ['7','API & Service Flow','l1'],
    ['8','UI / Screen Flow Documentation','l1'],
    ['9','Automation & Background Process Flow','l1'],
    ['10','Reports & Analytics Flow','l1'],
    ['11','Security & Access Control Flow','l1'],
    ['12','Error Handling & Exception Flow','l1'],
    ['13','Integration Flow','l1'],
    ['14','Complete System Flow Summary','l1'],
    ['A','Appendix A: Naming Series Reference','l1'],
    ['B','Appendix B: Workflow State Matrix','l1'],
    ['C','Appendix C: Installation Reference','l1'],
  ].map(([n,label,cls])=>`
    <div class="toc-row ${cls}">
      <span class="toc-n">${n}</span>
      <span>${label}</span>
      <span class="toc-dots"></span>
    </div>`).join('')}
</div>

<!-- ══ BODY CONTENT ════════════════════════════════════════════════════════ -->
<div class="content">
${processedHtml}
</div>

<script>
mermaid.initialize({
  startOnLoad: true,
  theme: 'base',
  themeVariables: {
    primaryColor:        '#1D5299',
    primaryTextColor:    '#ffffff',
    primaryBorderColor:  '#13315C',
    lineColor:           '#6B7280',
    secondaryColor:      '#E8F0FA',
    tertiaryColor:       '#F4F8FD',
    background:          '#ffffff',
    nodeBorder:          '#1D5299',
    clusterBkg:          '#E8F0FA',
    titleColor:          '#0B2545',
    edgeLabelBackground: '#ffffff',
    fontFamily:          'Inter, sans-serif',
    fontSize:            '12px',
  },
  flowchart: { curve: 'basis', padding: 18 },
  sequence:  { actorMargin: 50, messageMargin: 18 },
});
<\/script>
</body>
</html>`;

// ── Write HTML ────────────────────────────────────────────────────────────────
const htmlPath = path.join(__dirname, 'RE_Support_Functional_Flow_Document.html');
fs.writeFileSync(htmlPath, fullHtml, 'utf8');
console.log(`✅ HTML written → ${htmlPath}`);

// ── Generate PDF with Puppeteer ───────────────────────────────────────────────
(async () => {
  const puppeteer = require('puppeteer');

  console.log('🚀 Launching headless Chrome (this may take a moment)...');
  const browser = await puppeteer.launch({
    headless: 'new',
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-dev-shm-usage',
      '--disable-web-security',
      '--allow-file-access-from-files',
    ],
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1200, height: 1600 });

  const fileUrl = 'file:///' + htmlPath.replace(/\\/g, '/');
  console.log(`📄 Loading HTML from: ${fileUrl}`);

  await page.goto(fileUrl, { waitUntil: 'networkidle0', timeout: 90000 });

  // Wait for Mermaid diagrams to render (up to 30s)
  console.log('⏳ Waiting for Mermaid diagrams...');
  await page.waitForFunction(
    () => {
      const divs = document.querySelectorAll('.mermaid');
      if (divs.length === 0) return true; // no diagrams
      return Array.from(divs).every(d => d.querySelector('svg') !== null);
    },
    { timeout: 30000 }
  ).catch(() => console.warn('⚠️  Some diagrams may not have rendered (check network).'));

  // Extra settle time for fonts + render
  await new Promise(r => setTimeout(r, 2500));

  const outputPath = path.join(__dirname, 'RE_Support_Functional_Flow_Document.pdf');
  console.log('🖨️  Printing to PDF...');

  await page.pdf({
    path: outputPath,
    format: 'A4',
    printBackground: true,
    margin: { top: '22mm', right: '18mm', bottom: '22mm', left: '18mm' },
    displayHeaderFooter: true,
    headerTemplate: `
      <div style="width:100%;display:flex;justify-content:space-between;align-items:center;
                  font-family:Inter,sans-serif;font-size:8pt;color:#6B7280;
                  padding:0 18mm 4px;border-bottom:1px solid #E5E7EB;">
        <span>Real Estate Support System — Functional Flow Document</span>
        <span style="color:#1D5299;font-weight:600;">re_support · ERPNext v15+</span>
      </div>`,
    footerTemplate: `
      <div style="width:100%;display:flex;justify-content:space-between;align-items:center;
                  font-family:Inter,sans-serif;font-size:8pt;color:#6B7280;
                  padding:4px 18mm 0;border-top:1px solid #E5E7EB;">
        <span>Confidential — Internal Use Only</span>
        <span>Version 1.0 · 2026</span>
        <span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span>
      </div>`,
  });

  await browser.close();

  const sizeKB = (require('fs').statSync(outputPath).size / 1024).toFixed(0);
  console.log(`\n✅  PDF generated successfully!`);
  console.log(`📁  File : ${outputPath}`);
  console.log(`📦  Size : ${sizeKB} KB`);
})();
