const fs = require("fs");
const path = require("path");
const MarkdownIt = require("markdown-it");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  BorderStyle, ExternalHyperlink, LevelFormat, WidthType, Table, TableRow,
  TableCell, ShadingType, FootnoteReferenceRun,
} = require("docx");

const [, , inputPath, outputPath] = process.argv;
if (!inputPath || !outputPath) {
  console.error("usage: node md2docx.js <input.md> <output.docx>");
  process.exit(1);
}

let src = fs.readFileSync(inputPath, "utf8");
src = src.replace(/\r\n/g, "\n");

// ---- Footnote definitions: lines like "[^label]: text" ----
const footnoteDefs = {};
src = src.replace(/^\[\^([^\]]+)\]:[ \t]*(.+)$/gm, (m, label, text) => {
  footnoteDefs[label] = text.trim();
  return "";
});

const md = new MarkdownIt({ html: false, linkify: false, breaks: false });
const tokens = md.parse(src, {});

const bodySize = 24; // 12pt
const smallSize = 20; // 10pt

let footnoteCounter = 0;
const footnoteIdByLabel = {};
const footnotesForDoc = {};

function getFootnoteId(label) {
  if (footnoteIdByLabel[label]) return footnoteIdByLabel[label];
  footnoteCounter += 1;
  footnoteIdByLabel[label] = footnoteCounter;
  const text = footnoteDefs[label] || label;
  footnotesForDoc[footnoteCounter] = {
    children: [new Paragraph({ children: [new TextRun({ text, size: smallSize })] })],
  };
  return footnoteCounter;
}

const FOOTNOTE_RE = /\[\^([^\]]+)\]/g;

function textToRuns(text, marks) {
  const runs = [];
  let lastIndex = 0;
  FOOTNOTE_RE.lastIndex = 0;
  let match;
  while ((match = FOOTNOTE_RE.exec(text)) !== null) {
    if (match.index > lastIndex) {
      runs.push(makeTextRun(text.slice(lastIndex, match.index), marks));
    }
    runs.push(new FootnoteReferenceRun(getFootnoteId(match[1])));
    lastIndex = FOOTNOTE_RE.lastIndex;
  }
  if (lastIndex < text.length) {
    runs.push(makeTextRun(text.slice(lastIndex), marks));
  }
  return runs.length ? runs : [makeTextRun(text, marks)];
}

function makeTextRun(text, marks) {
  const opts = { text, size: marks.code ? smallSize : bodySize };
  if (marks.bold) opts.bold = true;
  if (marks.italics) opts.italics = true;
  if (marks.code) opts.font = "Consolas";
  return new TextRun(opts);
}

// Build an array of TextRun/FootnoteReferenceRun/ExternalHyperlink from inline children
function buildRuns(children, baseMarks) {
  const marks = Object.assign({ bold: false, italics: false, code: false }, baseMarks);
  const out = [];
  let i = 0;
  while (i < children.length) {
    const t = children[i];
    switch (t.type) {
      case "text":
        if (t.content) out.push(...textToRuns(t.content, marks));
        i += 1;
        break;
      case "code_inline":
        out.push(makeTextRun(t.content, Object.assign({}, marks, { code: true })));
        i += 1;
        break;
      case "softbreak":
      case "hardbreak":
        out.push(new TextRun({ text: "", break: 1 }));
        i += 1;
        break;
      case "strong_open": {
        const close = findClose(children, i, "strong_close");
        out.push(...buildRuns(children.slice(i + 1, close), Object.assign({}, marks, { bold: true })));
        i = close + 1;
        break;
      }
      case "em_open": {
        const close = findClose(children, i, "em_close");
        out.push(...buildRuns(children.slice(i + 1, close), Object.assign({}, marks, { italics: true })));
        i = close + 1;
        break;
      }
      case "s_open": {
        const close = findClose(children, i, "s_close");
        out.push(...buildRuns(children.slice(i + 1, close), marks));
        i = close + 1;
        break;
      }
      case "link_open": {
        const close = findClose(children, i, "link_close");
        const href = (t.attrs || []).find(a => a[0] === "href");
        const inner = buildRuns(children.slice(i + 1, close), marks);
        if (href) {
          out.push(new ExternalHyperlink({ children: inner, link: href[1] }));
        } else {
          out.push(...inner);
        }
        i = close + 1;
        break;
      }
      case "image":
        if (t.content) out.push(...textToRuns(t.content, marks));
        i += 1;
        break;
      default:
        i += 1;
    }
  }
  return out;
}

function findClose(children, openIdx, closeType) {
  let depth = 0;
  const openType = children[openIdx].type;
  for (let j = openIdx; j < children.length; j++) {
    if (children[j].type === openType) depth++;
    else if (children[j].type === closeType) {
      depth--;
      if (depth === 0) return j;
    }
  }
  return children.length - 1;
}

const HEADING_LEVELS = [
  HeadingLevel.HEADING_1, HeadingLevel.HEADING_2, HeadingLevel.HEADING_3,
  HeadingLevel.HEADING_4, HeadingLevel.HEADING_5, HeadingLevel.HEADING_6,
];

const children = [];
const listStack = []; // { ref, ordered }
let listRefCounter = 0;
let blockquoteDepth = 0;

let i = 0;
while (i < tokens.length) {
  const t = tokens[i];
  switch (t.type) {
    case "heading_open": {
      const level = parseInt(t.tag.slice(1), 10);
      const inline = tokens[i + 1];
      const runs = buildRuns(inline.children, {});
      children.push(new Paragraph({
        heading: HEADING_LEVELS[Math.min(level - 1, 5)],
        children: runs,
      }));
      i += 3;
      break;
    }
    case "paragraph_open": {
      const inline = tokens[i + 1];
      const runs = buildRuns(inline.children, {});
      const para = {
        spacing: { after: 160, line: 360 },
        children: runs.length ? runs : [new TextRun("")],
      };
      if (listStack.length) {
        const top = listStack[listStack.length - 1];
        para.numbering = { reference: top.ref, level: listStack.length - 1 };
      } else if (blockquoteDepth > 0) {
        para.indent = { left: 480 * blockquoteDepth };
      } else {
        para.indent = { firstLine: 480 };
      }
      children.push(new Paragraph(para));
      i += 3;
      break;
    }
    case "bullet_list_open": {
      listRefCounter += 1;
      listStack.push({ ref: "bullet-" + listRefCounter, ordered: false });
      i += 1;
      break;
    }
    case "bullet_list_close": {
      listStack.pop();
      i += 1;
      break;
    }
    case "ordered_list_open": {
      listRefCounter += 1;
      listStack.push({ ref: "ordered-" + listRefCounter, ordered: true });
      i += 1;
      break;
    }
    case "ordered_list_close": {
      listStack.pop();
      i += 1;
      break;
    }
    case "blockquote_open":
      blockquoteDepth += 1;
      i += 1;
      break;
    case "blockquote_close":
      blockquoteDepth -= 1;
      i += 1;
      break;
    case "hr":
      children.push(new Paragraph({
        spacing: { before: 200, after: 200 },
        border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "999999", space: 1 } },
        children: [],
      }));
      i += 1;
      break;
    case "fence":
    case "code_block": {
      const text = t.content.replace(/\n$/, "");
      const lines = text.length ? text.split("\n") : [""];
      for (const line of lines) {
        children.push(new Paragraph({
          shading: { fill: "F2F2F2", type: ShadingType.CLEAR },
          spacing: { after: 0 },
          children: [new TextRun({ text: line.length ? line : " ", font: "Consolas", size: smallSize })],
        }));
      }
      i += 1;
      break;
    }
    case "table_open": {
      let j = i + 1;
      const rows = [];
      let currentRow = null;
      let isHeaderRow = false;
      while (tokens[j].type !== "table_close") {
        const tt = tokens[j];
        if (tt.type === "tr_open") {
          currentRow = [];
        } else if (tt.type === "tr_close") {
          rows.push({ cells: currentRow, header: isHeaderRow });
          currentRow = null;
        } else if (tt.type === "thead_open") {
          isHeaderRow = true;
        } else if (tt.type === "thead_close") {
          isHeaderRow = false;
        } else if (tt.type === "th_open" || tt.type === "td_open") {
          const inline = tokens[j + 1];
          const runs = buildRuns(inline.children, {});
          currentRow.push({ runs, header: tt.type === "th_open" });
          j += 2; // skip inline + close tag next iteration handles close
        }
        j += 1;
      }
      const colCount = rows.length ? rows[0].cells.length : 1;
      const tableWidth = 9360;
      const colWidth = Math.floor(tableWidth / colCount);
      const colWidths = new Array(colCount).fill(colWidth);
      const border = { style: BorderStyle.SINGLE, size: 2, color: "BFBFBF" };
      const borders = { top: border, bottom: border, left: border, right: border };
      const tableRows = rows.map(r => new TableRow({
        children: r.cells.map(c => new TableCell({
          borders,
          width: { size: colWidth, type: WidthType.DXA },
          shading: c.header ? { fill: "E7EEF5", type: ShadingType.CLEAR } : undefined,
          margins: { top: 80, bottom: 80, left: 120, right: 120 },
          children: [new Paragraph({
            children: c.runs.length ? c.runs : [new TextRun("")],
          })],
        })),
      }));
      children.push(new Table({
        width: { size: tableWidth, type: WidthType.DXA },
        columnWidths: colWidths,
        rows: tableRows,
      }));
      children.push(new Paragraph({ children: [], spacing: { after: 160 } }));
      i = j + 1;
      break;
    }
    default:
      i += 1;
  }
}

const bulletRefs = [];
const orderedRefs = [];
for (let n = 1; n <= listRefCounter; n++) {
  bulletRefs.push("bullet-" + n);
  orderedRefs.push("ordered-" + n);
}

const numbering = {
  config: [
    ...bulletRefs.map(ref => ({
      reference: ref,
      levels: [0, 1, 2, 3].map(level => ({
        level,
        format: LevelFormat.BULLET,
        text: level === 0 ? "•" : level === 1 ? "◦" : "▪",
        alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 720 * (level + 1), hanging: 360 } } },
      })),
    })),
    ...orderedRefs.map(ref => ({
      reference: ref,
      levels: [0, 1, 2, 3].map(level => ({
        level,
        format: LevelFormat.DECIMAL,
        text: `%${level + 1}.`,
        alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 720 * (level + 1), hanging: 360 } } },
      })),
    })),
  ],
};

const titleBase = path.basename(inputPath, ".md");

const doc = new Document({
  styles: {
    default: { document: { run: { font: "SimSun", size: bodySize } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, font: "SimHei" },
        paragraph: { spacing: { before: 360, after: 240 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, font: "SimHei" },
        paragraph: { spacing: { before: 280, after: 200 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 26, bold: true, font: "SimHei" },
        paragraph: { spacing: { before: 240, after: 160 }, outlineLevel: 2 } },
      { id: "Heading4", name: "Heading 4", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 24, bold: true, font: "SimHei" },
        paragraph: { spacing: { before: 200, after: 120 }, outlineLevel: 3 } },
    ],
  },
  numbering: listRefCounter ? numbering : undefined,
  footnotes: footnoteCounter ? footnotesForDoc : undefined,
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 },
      },
    },
    children: [
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 400 },
        children: [new TextRun({ text: titleBase.replace(/^\d+[._]?\s*/, ""), bold: true, size: 36 })],
      }),
      ...children,
    ],
  }],
});

Packer.toBuffer(doc).then(buffer => {
  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  fs.writeFileSync(outputPath, buffer);
  console.log("OK " + outputPath);
}).catch(err => {
  console.error("FAIL " + inputPath + ": " + err.message);
  process.exit(1);
});
