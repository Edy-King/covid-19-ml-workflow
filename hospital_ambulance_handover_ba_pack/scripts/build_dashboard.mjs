import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const root = path.resolve(__dirname, "..");
const outputDir = path.join(root, "outputs");
const qaDir = path.join(root, "qa_render");
await fs.mkdir(outputDir, { recursive: true });
await fs.mkdir(qaDir, { recursive: true });

const wb = Workbook.create();
const dashboard = wb.worksheets.add("Impact Dashboard");
const data = wb.worksheets.add("KPI Data");
const feedback = wb.worksheets.add("Feedback Data");
const codebook = wb.worksheets.add("Codebook");

for (const ws of [dashboard, data, feedback, codebook]) {
  ws.showGridLines = false;
}

const teal = "#1F6F8B";
const tealDark = "#164E63";
const pale = "#EAF4F2";
const pale2 = "#F3F7FA";
const grey = "#F3F4F6";
const green = "#0F766E";
const amber = "#B45309";
const red = "#B91C1C";

function title(sheet, range, text, subtitle = null) {
  sheet.getRange(range).merge();
  sheet.getRange(range).values = [[text]];
  sheet.getRange(range).format = {
    fill: tealDark,
    font: { bold: true, color: "#FFFFFF", size: 18 },
    horizontalAlignment: "center",
    verticalAlignment: "center",
  };
  sheet.getRange(range).format.rowHeightPx = 42;
  if (subtitle) {
    sheet.getRange("A2:H2").merge();
    sheet.getRange("A2:H2").values = [[subtitle]];
    sheet.getRange("A2:H2").format = {
      fill: pale,
      font: { italic: true, color: "#374151", size: 10 },
      horizontalAlignment: "center",
      verticalAlignment: "center",
      wrapText: true,
    };
    sheet.getRange("A2:H2").format.rowHeightPx = 30;
  }
}

function section(sheet, range, text) {
  sheet.getRange(range).merge();
  sheet.getRange(range).values = [[text]];
  sheet.getRange(range).format = {
    fill: teal,
    font: { bold: true, color: "#FFFFFF", size: 11 },
    horizontalAlignment: "left",
  };
}

data.getRange("A1:H1").values = [[
  "Month",
  "Phase",
  "Ambulance Arrivals",
  "Median Handover Time (min)",
  "Within 15 Min Target",
  "Incomplete Records",
  "Duplicate Questioning",
  "Escalations Within Target",
]];
data.getRange("A2:H8").values = [
  ["Jan 2026", "Baseline", 118, 25, 0.50, 0.34, 0.46, 0.55],
  ["Feb 2026", "Baseline", 126, 23, 0.53, 0.30, 0.43, 0.60],
  ["Mar 2026", "Baseline", 122, 24, 0.52, 0.31, 0.44, 0.58],
  ["Apr 2026", "Pilot launch", 124, 19, 0.64, 0.20, 0.31, 0.72],
  ["May 2026", "Post", 131, 15, 0.78, 0.12, 0.24, 0.83],
  ["Jun 2026", "Post", 128, 13, 0.84, 0.08, 0.18, 0.91],
  ["Jul 2026", "Post", 135, 12, 0.86, 0.07, 0.16, 0.93],
];
data.getRange("A1:H1").format = { fill: teal, font: { bold: true, color: "#FFFFFF" }, wrapText: true };
data.getRange("A1:H8").format.borders = { preset: "all", style: "thin", color: "#D1D5DB" };
data.getRange("C2:D8").format.numberFormat = "#,##0";
data.getRange("E2:H8").format.numberFormat = "0%";
data.getRange("A:H").format.autofitColumns();
data.freezePanes.freezeRows(1);
data.tables.add("A1:H8", true, "KPIDataTable");

feedback.getRange("A1:F1").values = [["Month", "Group", "Responses", "Satisfaction Score", "Positive Sentiment", "Top Theme"]];
feedback.getRange("A2:F21").values = [
  ["Jan 2026", "Ambulance crew", 18, 58, 0.44, "Waiting for named receiver"],
  ["Jan 2026", "Receiving nurses", 14, 62, 0.50, "Missing clinical details"],
  ["Jan 2026", "Patients/carers", 20, 60, 0.48, "Repeated questions"],
  ["Feb 2026", "Ambulance crew", 20, 60, 0.48, "Queue pressure"],
  ["Feb 2026", "Receiving nurses", 15, 63, 0.51, "Unclear escalation"],
  ["Feb 2026", "Patients/carers", 22, 61, 0.50, "Waiting uncertainty"],
  ["Mar 2026", "Ambulance crew", 17, 61, 0.50, "Variable handover quality"],
  ["Mar 2026", "Receiving nurses", 16, 64, 0.52, "Incomplete handover"],
  ["Mar 2026", "Patients/carers", 18, 62, 0.51, "Repeated questions"],
  ["Apr 2026", "Ambulance crew", 19, 70, 0.66, "Clearer receiving point"],
  ["Apr 2026", "Receiving nurses", 17, 72, 0.68, "SBAR improved confidence"],
  ["Apr 2026", "Patients/carers", 21, 70, 0.65, "Less repeated questioning"],
  ["May 2026", "Ambulance crew", 22, 78, 0.78, "Faster release"],
  ["May 2026", "Receiving nurses", 18, 80, 0.80, "Clear handover fields"],
  ["May 2026", "Patients/carers", 24, 77, 0.75, "Less uncertainty"],
  ["Jun 2026", "Ambulance crew", 24, 84, 0.86, "Named receiver works well"],
  ["Jun 2026", "Receiving nurses", 20, 82, 0.83, "Escalation clearer"],
  ["Jun 2026", "Patients/carers", 25, 80, 0.79, "Fewer repeated questions"],
  ["Jul 2026", "Ambulance crew", 21, 86, 0.88, "Reliable process"],
  ["Jul 2026", "Receiving nurses", 19, 84, 0.85, "Good audit trail"],
];
feedback.getRange("A1:F1").format = { fill: teal, font: { bold: true, color: "#FFFFFF" }, wrapText: true };
feedback.getRange("A1:F21").format.borders = { preset: "all", style: "thin", color: "#D1D5DB" };
feedback.getRange("D2:D21").format.numberFormat = "0";
feedback.getRange("E2:E21").format.numberFormat = "0%";
feedback.getRange("A:F").format.autofitColumns();
feedback.freezePanes.freezeRows(1);
feedback.tables.add("A1:F21", true, "FeedbackDataTable");

codebook.getRange("A1:C1").values = [["Field / metric", "Definition", "Evidence status"]];
codebook.getRange("A2:C13").values = [
  ["Median handover time", "Median minutes from ambulance arrival to clinical acceptance.", "Requires data-owner validation"],
  ["Within 15 Min Target", "Share of arrivals accepted into clinical pathway within 15 minutes.", "Requires data-owner validation"],
  ["Incomplete Records", "Share of handovers missing one or more required SBAR/minimum dataset fields.", "Requires data-owner validation"],
  ["Duplicate Questioning", "Share of feedback responses reporting avoidable repeated questioning.", "Requires data-owner validation"],
  ["Escalations Within Target", "Share of qualifying escalations documented within the expected response time.", "Requires data-owner validation"],
  ["Satisfaction Score", "Composite 0-100 feedback score across staff and patient/carer groups.", "Requires data-owner validation"],
  ["Baseline", "January to March 2026 average before implementation.", "Measurement period"],
  ["Pilot launch", "April 2026 implementation transition month.", "Measurement period"],
  ["Post", "May to July 2026 average after implementation.", "Measurement period"],
  ["Consulting company", "CR Allied Services Limited.", "Project identity"],
  ["Hospital", "Ambrose Alli University Health Center.", "Client setting"],
  ["Lead consultant", "Edward Osikem Okhumaile.", "Project identity"],
];
codebook.getRange("A1:C1").format = { fill: teal, font: { bold: true, color: "#FFFFFF" } };
codebook.getRange("A1:C13").format.borders = { preset: "all", style: "thin", color: "#D1D5DB" };
codebook.getRange("B:C").format.wrapText = true;
codebook.getRange("A:C").format.autofitColumns();
codebook.freezePanes.freezeRows(1);

title(
  dashboard,
  "A1:H1",
  "Ambulance Handover Process Impact Dashboard",
  "CR Allied Services Limited | Ambrose Alli University Health Center | Implementation proposal dashboard"
);
dashboard.getRange("A3:H3").merge();
dashboard.getRange("A3:H3").values = [[
  "Validation note: KPI figures require hospital data-owner review and approval before external circulation, executive sign-off, or procurement use."
]];
dashboard.getRange("A3:H3").format = {
  fill: "#FFF7ED",
  font: { color: amber, bold: true, size: 9 },
  wrapText: true,
};
dashboard.getRange("A3:H3").format.rowHeightPx = 32;

section(dashboard, "A5:H5", "Executive KPI summary");
dashboard.getRange("A6:H11").values = [
  ["KPI", "Baseline Avg", "Post Avg", "Change", "Status", "Interpretation", "", ""],
  ["Median handover time (min)", "", "", "", "", "Lower is better", "", ""],
  ["Within 15 min target", "", "", "", "", "Higher is better", "", ""],
  ["Incomplete records", "", "", "", "", "Lower is better", "", ""],
  ["Duplicate questioning", "", "", "", "", "Lower is better", "", ""],
  ["Escalations within target", "", "", "", "", "Higher is better", "", ""],
];
dashboard.getRange("B7:B11").formulas = [
  ["=AVERAGE('KPI Data'!D2:D4)"],
  ["=AVERAGE('KPI Data'!E2:E4)"],
  ["=AVERAGE('KPI Data'!F2:F4)"],
  ["=AVERAGE('KPI Data'!G2:G4)"],
  ["=AVERAGE('KPI Data'!H2:H4)"],
];
dashboard.getRange("C7:C11").formulas = [
  ["=AVERAGE('KPI Data'!D6:D8)"],
  ["=AVERAGE('KPI Data'!E6:E8)"],
  ["=AVERAGE('KPI Data'!F6:F8)"],
  ["=AVERAGE('KPI Data'!G6:G8)"],
  ["=AVERAGE('KPI Data'!H6:H8)"],
];
dashboard.getRange("D7:D11").formulas = [
  ["=C7-B7"],
  ["=C8-B8"],
  ["=C9-B9"],
  ["=C10-B10"],
  ["=C11-B11"],
];
dashboard.getRange("E7:E11").formulas = [
  ['=IF(C7<B7,"Improved","Watch")'],
  ['=IF(C8>B8,"Improved","Watch")'],
  ['=IF(C9<B9,"Improved","Watch")'],
  ['=IF(C10<B10,"Improved","Watch")'],
  ['=IF(C11>B11,"Improved","Watch")'],
];
dashboard.getRange("A6:F6").format = { fill: grey, font: { bold: true } };
dashboard.getRange("A6:F11").format.borders = { preset: "all", style: "thin", color: "#D1D5DB" };
dashboard.getRange("A7:A11").format.font = { bold: true };
dashboard.getRange("B7:D7").format.numberFormat = "0.0";
dashboard.getRange("B8:D11").format.numberFormat = "0%";
dashboard.getRange("E7:E11").format = { fill: pale, font: { bold: true, color: green }, horizontalAlignment: "center" };
dashboard.getRange("F7:F11").format.wrapText = true;

section(dashboard, "A13:D13", "Feedback pulse");
dashboard.getRange("A14:D18").values = [
  ["Metric", "Baseline Avg", "Post Avg", "Change"],
  ["Satisfaction score", "", "", ""],
  ["Positive sentiment", "", "", ""],
  ["Total feedback responses", "", "", ""],
  ["Most common post theme", "", "", ""],
];
dashboard.getRange("B15:B17").formulas = [
  ["=AVERAGE('Feedback Data'!D2:D10)"],
  ["=AVERAGE('Feedback Data'!E2:E10)"],
  ["=SUM('Feedback Data'!C2:C10)"],
];
dashboard.getRange("C15:C17").formulas = [
  ["=AVERAGE('Feedback Data'!D13:D20)"],
  ["=AVERAGE('Feedback Data'!E13:E20)"],
  ["=SUM('Feedback Data'!C13:C20)"],
];
dashboard.getRange("D15:D17").formulas = [["=C15-B15"], ["=C16-B16"], ["=C17-B17"]];
dashboard.getRange("C18").values = [["Clearer handover, named receiver, fewer repeated questions"]];
dashboard.getRange("A14:D14").format = { fill: grey, font: { bold: true } };
dashboard.getRange("A14:D18").format.borders = { preset: "all", style: "thin", color: "#D1D5DB" };
dashboard.getRange("B15:D15").format.numberFormat = "0";
dashboard.getRange("B16:D16").format.numberFormat = "0%";
dashboard.getRange("B17:D17").format.numberFormat = "#,##0";
dashboard.getRange("C18:D18").merge();
dashboard.getRange("C18:D18").format.wrapText = true;

section(dashboard, "F13:H13", "Business analyst impact statement");
dashboard.getRange("F14:H18").merge();
dashboard.getRange("F14:H18").values = [[
  "The redesigned handover model shows how structured business analysis can convert a clinical operations problem into clear requirements, role accountability, standard workflow, audit controls, and measurable service improvement. The dashboard is suitable for executive review and should be refreshed with approved hospital data during pilot operation."
]];
dashboard.getRange("F14:H18").format = {
  fill: pale2,
  wrapText: true,
  verticalAlignment: "top",
  borders: { preset: "outside", style: "thin", color: "#CBD5E1" },
};

dashboard.getRange("A21:D21").values = [["Month", "Median Time", "Within Target", "Incomplete Records"]];
dashboard.getRange("A22:D28").formulas = [
  ["='KPI Data'!A2", "='KPI Data'!D2", "='KPI Data'!E2", "='KPI Data'!F2"],
  ["='KPI Data'!A3", "='KPI Data'!D3", "='KPI Data'!E3", "='KPI Data'!F3"],
  ["='KPI Data'!A4", "='KPI Data'!D4", "='KPI Data'!E4", "='KPI Data'!F4"],
  ["='KPI Data'!A5", "='KPI Data'!D5", "='KPI Data'!E5", "='KPI Data'!F5"],
  ["='KPI Data'!A6", "='KPI Data'!D6", "='KPI Data'!E6", "='KPI Data'!F6"],
  ["='KPI Data'!A7", "='KPI Data'!D7", "='KPI Data'!E7", "='KPI Data'!F7"],
  ["='KPI Data'!A8", "='KPI Data'!D8", "='KPI Data'!E8", "='KPI Data'!F8"],
];
dashboard.getRange("A21:D21").format = { fill: grey, font: { bold: true } };
dashboard.getRange("C22:D28").format.numberFormat = "0%";
dashboard.getRange("B22:B28").format.numberFormat = "0";
dashboard.getRange("G21:H21").values = [["Month", "Incomplete Records"]];
dashboard.getRange("G22:H28").formulas = [
  ["=A22", "=D22"],
  ["=A23", "=D23"],
  ["=A24", "=D24"],
  ["=A25", "=D25"],
  ["=A26", "=D26"],
  ["=A27", "=D27"],
  ["=A28", "=D28"],
];
dashboard.getRange("G21:H21").format = { fill: grey, font: { bold: true } };
dashboard.getRange("H22:H28").format.numberFormat = "0%";

const lineChart = dashboard.charts.add("line", dashboard.getRange("A21:B28"));
lineChart.title = "Median handover time fell after launch";
lineChart.hasLegend = false;
lineChart.xAxis = { axisType: "textAxis", textStyle: { fontSize: 9 } };
lineChart.yAxis = { numberFormatCode: "0" };
lineChart.setPosition("A30", "D45");

const barChart = dashboard.charts.add("line", dashboard.getRange("G21:H28"));
barChart.title = "Incomplete records reduced";
barChart.hasLegend = false;
barChart.xAxis = { axisType: "textAxis", textStyle: { fontSize: 9 } };
barChart.yAxis = { numberFormatCode: "0%" };
barChart.setPosition("E30", "H45");

dashboard.getRange("A:H").format.font = { name: "Arial", size: 10 };
dashboard.getRange("A1:H1").format.font = { name: "Arial", bold: true, color: "#FFFFFF", size: 18 };
dashboard.getRange("A2:H2").format.font = { name: "Arial", italic: true, color: "#374151", size: 10 };
dashboard.getRange("A1:A45").format.columnWidthPx = 170;
dashboard.getRange("B1:E45").format.columnWidthPx = 112;
dashboard.getRange("F1:F45").format.columnWidthPx = 245;
dashboard.getRange("G1:H45").format.columnWidthPx = 120;
dashboard.getRange("A1:H45").format.wrapText = true;
dashboard.freezePanes.freezeRows(5);

const errorScan = await wb.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
  options: { useRegex: true, maxResults: 100 },
  summary: "formula error scan",
});
console.log(errorScan.ndjson);

const preview = await wb.render({ sheetName: "Impact Dashboard", range: "A1:H45", scale: 1, format: "png" });
await fs.writeFile(path.join(qaDir, "impact_dashboard_preview.png"), new Uint8Array(await preview.arrayBuffer()));

const output = await SpreadsheetFile.exportXlsx(wb);
await output.save(path.join(outputDir, "ambulance_handover_impact_dashboard.xlsx"));
console.log(path.join(outputDir, "ambulance_handover_impact_dashboard.xlsx"));
