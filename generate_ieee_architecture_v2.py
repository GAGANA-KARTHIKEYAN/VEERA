"""
VEERA IEEE Architecture Diagram — Matplotlib v2.
Publication-quality SVG, PDF, and 300-DPI PNG.
Fixed: clipping, overlap, YES/NO branch clarity.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np
import os

# ─── colour palette ───────────────────────────────────────────────
C_BG       = "#FFFFFF"
C_NAVY     = "#1E3A8A"   # global / VLM accent
C_TEAL     = "#0D7377"   # adaptive stage accent
C_AMBER    = "#92400E"   # decision gate border
C_AMBER_BG = "#FEF3C7"   # decision gate fill
C_GREEN    = "#047857"   # pass / consensus
C_GREEN_BG = "#D1FAE5"
C_RED      = "#BE123C"   # abstention
C_RED_BG   = "#FFE4E6"
C_DARK     = "#1E293B"   # text / arrows
C_GRAY     = "#64748B"   # muted text
C_LGRAY    = "#F1F5F9"   # box fills
C_BORDER   = "#94A3B8"   # neutral border
C_WHITE    = "#FFFFFF"
C_VLM_BG   = "#EFF6FF"   # light blue VLM background
C_TEAL_BG  = "#F0FDFA"   # light teal for adaptive boxes
C_OUT_BG   = "#F8FAFC"

# ─── figure setup ─────────────────────────────────────────────────
FIG_W = 3.5
FIG_H = 8.2
DPI   = 300

fig, ax = plt.subplots(1, 1, figsize=(FIG_W, FIG_H), dpi=DPI)
ax.set_xlim(0, 100)
ax.set_ylim(0, 230)
ax.set_aspect("equal")
ax.axis("off")
fig.patch.set_facecolor(C_BG)
ax.set_facecolor(C_BG)

# ─── helper functions ─────────────────────────────────────────────
def box(x, y, w, h, fc=C_WHITE, ec=C_BORDER, lw=0.8, zorder=2, rounding=0.4):
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={rounding}",
                       facecolor=fc, edgecolor=ec, linewidth=lw, zorder=zorder,
                       transform=ax.transData, clip_on=False)
    ax.add_patch(p)
    return p

def txt(x, y, s, size=5.5, color=C_DARK, weight="normal", ha="left", va="center",
        family="sans-serif", style="normal", zorder=5):
    ax.text(x, y, s, fontsize=size, color=color, fontweight=weight,
            ha=ha, va=va, fontfamily=family, fontstyle=style,
            zorder=zorder, clip_on=False)

def arrow(x1, y1, x2, y2, color=C_DARK, lw=0.7, style="-|>", head_w=3, head_l=2.5,
          zorder=3, linestyle="-"):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=f"{style},head_width={head_w/20},head_length={head_l/20}",
                                color=color, lw=lw, linestyle=linestyle),
                zorder=zorder)

def hline(x1, y1, x2, y2, color=C_DARK, lw=0.7, ls="-", zorder=3):
    ax.plot([x1, x2], [y1, y2], color=color, lw=lw, ls=ls, zorder=zorder, clip_on=False)

# ═══════════════════════════════════════════════════════════════════
# A. INPUT BOXES
# ═══════════════════════════════════════════════════════════════════
Y_IN = 218
box(5, Y_IN, 40, 9, fc=C_LGRAY, ec=C_BORDER, lw=0.7)
txt(7, Y_IN+6.5, "INPUT IMAGE (x)", size=4.8, weight="bold", color=C_NAVY)
txt(7, Y_IN+4, "RGB image, arbitrary size", size=3.5, color=C_GRAY)
txt(7, Y_IN+2, "SmartResize preprocessing", size=3.3, color=C_GRAY)

box(55, Y_IN, 40, 9, fc=C_LGRAY, ec=C_BORDER, lw=0.7)
txt(57, Y_IN+6.5, "BINARY QUESTION (q)", size=4.8, weight="bold", color=C_NAVY)
txt(57, Y_IN+4, '"Is there a [target]?"', size=3.5, color=C_GRAY, style="italic")
txt(57, Y_IN+2, "Natural-language binary query", size=3.3, color=C_GRAY)

# merge arrows
arrow(25, Y_IN, 25, Y_IN-2, color=C_DARK, lw=0.6)
arrow(75, Y_IN, 75, Y_IN-2, color=C_DARK, lw=0.6)
hline(25, Y_IN-2, 75, Y_IN-2, color=C_DARK, lw=0.6)
arrow(50, Y_IN-2, 50, Y_IN-4, color=C_DARK, lw=0.6)

# ═══════════════════════════════════════════════════════════════════
# B. SHARED VLM CORE
# ═══════════════════════════════════════════════════════════════════
Y_VLM = 197
box(5, Y_VLM, 90, 14, fc=C_VLM_BG, ec=C_NAVY, lw=1.0)
# header bar
box(5, Y_VLM+11.5, 90, 2.5, fc=C_NAVY, ec=C_NAVY, lw=0.5, rounding=0.2)
txt(50, Y_VLM+12.7, "SHARED VISION-LANGUAGE MODEL CORE", size=4.3, weight="bold",
    color=C_WHITE, ha="center")

# inner sub-boxes
box(7, Y_VLM+1.5, 41, 8.5, fc=C_WHITE, ec=C_BORDER, lw=0.5, rounding=0.3)
txt(9, Y_VLM+8, "Qwen2.5-VL-3B-Instruct", size=4, weight="bold", color=C_DARK)
txt(9, Y_VLM+5.5, "Pre-trained vision encoder", size=3.3, color=C_GRAY)
txt(9, Y_VLM+3.5, "+ 36-layer LLM decoder", size=3.3, color=C_GRAY)

box(52, Y_VLM+1.5, 41, 8.5, fc=C_WHITE, ec=C_BORDER, lw=0.5, rounding=0.3)
txt(54, Y_VLM+8, "LoRA Adapter (Fine-Tuned)", size=4, weight="bold", color=C_DARK)
txt(54, Y_VLM+5.5, "Rank r = 8,  \u03b1 = 16", size=3.3, color=C_GRAY)
txt(54, Y_VLM+3.5, "q/k/v/o projections", size=3.3, color=C_GRAY)

# arrow down to Stage 1
arrow(50, Y_VLM, 50, Y_VLM-3, color=C_DARK, lw=0.6)
txt(52, Y_VLM-1.5, "[1] Global Pass", size=3, color=C_GRAY)

# ═══════════════════════════════════════════════════════════════════
# C. STAGE 1: GLOBAL INFERENCE
# ═══════════════════════════════════════════════════════════════════
Y_S1 = 173
box(5, Y_S1, 90, 20, fc=C_WHITE, ec=C_BORDER, lw=0.8)
box(5, Y_S1+17.5, 90, 2.5, fc=C_LGRAY, ec=C_BORDER, lw=0.5, rounding=0.2)
txt(7, Y_S1+18.7, "STAGE 1: GLOBAL INFERENCE & RELIABILITY ESTIMATION",
    size=4, weight="bold", color=C_NAVY)

txt(7, Y_S1+15.5, "\u2022 Full-image forward pass (chat template)", size=3.5, color=C_DARK)
txt(7, Y_S1+13.2, "\u2022 Extract logits at prompt boundary [0, \u22121]", size=3.5, color=C_DARK)
txt(7, Y_S1+11, "\u2022 Softmax over Token 9454 ('Yes') & 2753 ('No')", size=3.5, color=C_DARK)

# formula box
box(7, Y_S1+1.5, 86, 7.5, fc="#FAFBFF", ec="#CBD5E1", lw=0.6, rounding=0.2)
txt(10, Y_S1+7, "Empirical Reliability Gap:", size=3.8, weight="bold", color=C_DARK)
txt(10, Y_S1+4, "G(x, q) = |P(Yes) \u2212 P(No)|", size=4.8, weight="bold",
    color=C_DARK, family="serif", style="italic")
txt(60, Y_S1+4, "\u2208  [0.0, 1.0]", size=3.8, color=C_GRAY, family="serif")

# arrow to gate
arrow(50, Y_S1, 50, Y_S1-3, color=C_DARK, lw=0.6)

# ═══════════════════════════════════════════════════════════════════
# D. SUFFICIENCY GATE (DIAMOND)
# ═══════════════════════════════════════════════════════════════════
Y_GATE = 162
# Diamond
diamond_x = [50, 15, 50, 85, 50]
diamond_y = [Y_GATE+6, Y_GATE, Y_GATE-6, Y_GATE, Y_GATE+6]
ax.fill(diamond_x, diamond_y, fc=C_AMBER_BG, ec=C_AMBER, lw=1.0, zorder=2)
txt(50, Y_GATE+2, "SUFFICIENCY GATE", size=4, weight="bold", color=C_AMBER, ha="center")
txt(50, Y_GATE-0.5, "G(x, q) \u2265 \u03c4 ?", size=4.3, weight="bold",
    color=C_AMBER, ha="center", family="serif", style="italic")
txt(50, Y_GATE-2.8, "\u03c4 = 0.7853", size=3.3, color=C_AMBER, ha="center",
    family="serif", style="italic")

# ═══ YES branch (left) ═══
hline(15, Y_GATE, 9, Y_GATE, color=C_GREEN, lw=0.8)
txt(12, Y_GATE+3, "YES", size=4.2, weight="bold", color=C_GREEN, ha="center")
txt(12, Y_GATE-3.5, "G \u2265 \u03c4", size=3.2, color=C_GREEN, ha="center", family="serif")

# vertical dashed line down left side
hline(5, Y_GATE-3, 5, 28, color=C_GREEN, lw=0.8, ls=(0,(3,2)))
# arrow into final output
arrow(5, 28, 8, 28, color=C_GREEN, lw=0.8)

# "Direct Path" annotation on the line
txt(6, Y_GATE-18, "DIRECT", size=2.6, weight="bold", color=C_GREEN)
txt(6, Y_GATE-20, "PATH", size=2.6, weight="bold", color=C_GREEN)

# ═══ NO branch (downward) ═══
arrow(50, Y_GATE-6, 50, Y_GATE-11, color=C_DARK, lw=0.6)
# NO label
box(55, Y_GATE-10.5, 20, 2.8, fc=C_RED_BG, ec=C_RED, lw=0.5, rounding=0.2)
txt(57, Y_GATE-9.1, "NO (G < \u03c4)", size=3.3, weight="bold", color=C_RED)

# ═══════════════════════════════════════════════════════════════════
# E. STAGE 2: ADAPTIVE SPATIAL EVIDENCE ACQUISITION
# ═══════════════════════════════════════════════════════════════════
Y_S2 = 116
box(12, Y_S2, 83, 28, fc=C_TEAL_BG, ec=C_TEAL, lw=0.9)
# header
box(12, Y_S2+25.5, 83, 2.5, fc=C_TEAL, ec=C_TEAL, lw=0.5, rounding=0.2)
txt(14, Y_S2+26.7, "STAGE 2: ADAPTIVE SPATIAL EVIDENCE ACQUISITION",
    size=3.8, weight="bold", color=C_WHITE)

txt(14, Y_S2+23, "\u2022 Generate 4 overlapping crops (400\u00d7400 px, 50% stride):",
    size=3.5, color=C_DARK)

# 4 crop sub-boxes
cw, ch = 18, 6.5
cx_positions = [15, 35, 55, 75]
cy_crops = Y_S2 + 14
labels_top = ["c1: Top-Left", "c2: Top-Right", "c3: Centre", "c4: Bottom-Rt"]
for i in range(4):
    box(cx_positions[i], cy_crops, cw, ch, fc=C_WHITE, ec=C_TEAL, lw=0.6, rounding=0.25)
    txt(cx_positions[i]+1, cy_crops+4.5, labels_top[i], size=3.1, weight="bold", color=C_TEAL)
    txt(cx_positions[i]+1, cy_crops+2, "400\u00d7400 px", size=2.8, color=C_GRAY)

txt(14, Y_S2+11, "\u2022 Adaptive scaling for images \u2264 400 px", size=3.3, color=C_DARK)
txt(14, Y_S2+8.5, "\u2022 Each crop paired with original query q", size=3.3, color=C_DARK)
txt(14, Y_S2+5.5, "\u2022 All crops processed through shared VLM core",
    size=3.5, weight="bold", color=C_TEAL)

# Re-use annotation (inside the box, bottom right)
txt(82, Y_S2+2, "[re-uses VLM \u2191]", size=2.8, color=C_TEAL, ha="center", weight="bold")

# arrow down
arrow(50, Y_S2, 50, Y_S2-3.5, color=C_DARK, lw=0.6)

# ═══════════════════════════════════════════════════════════════════
# F. REGIONAL EVIDENCE AGGREGATION
# ═══════════════════════════════════════════════════════════════════
Y_AGG = 84
box(12, Y_AGG, 83, 26, fc=C_TEAL_BG, ec=C_TEAL, lw=0.9)
# header
box(12, Y_AGG+23.5, 83, 2.5, fc=C_TEAL, ec=C_TEAL, lw=0.5, rounding=0.2)
txt(14, Y_AGG+24.7, "REGIONAL EVIDENCE AGGREGATION & GATING",
    size=3.8, weight="bold", color=C_WHITE)

txt(14, Y_AGG+21.5, "Three mandatory failure-aware criteria:", size=3.5, weight="bold", color=C_DARK)

# criterion boxes
criteria = [
    ("1. Consensus Quorum:", "Agreement ratio Q \u2265 75%  (\u2265 3/4 crops)"),
    ("2. Crop Reliability:",  "Every agreeing crop: G(ci, q) \u2265 \u03c4"),
    ("3. Global Alignment:",  "Crop consensus matches global prediction"),
]
for i, (lbl, desc) in enumerate(criteria):
    cy_c = Y_AGG + 15 - i*5
    box(14, cy_c, 79, 4.2, fc=C_WHITE, ec="#CBD5E1", lw=0.5, rounding=0.15)
    txt(16, cy_c+2.3, lbl, size=3.3, weight="bold", color=C_TEAL)
    txt(40, cy_c+2.3, desc, size=3.1, color=C_DARK)

txt(14, Y_AGG+1.5, "\u26a0 Failure on ANY criterion \u2192 no definitive prediction",
    size=3.1, color=C_RED, weight="bold")

# Two branches from aggregation
arrow(32, Y_AGG, 32, Y_AGG-4.5, color=C_GREEN, lw=0.7)
box(20, Y_AGG-3, 22, 2.5, fc=C_GREEN_BG, ec=C_GREEN, lw=0.5, rounding=0.2)
txt(21, Y_AGG-1.7, "ALL 3 MET", size=3, weight="bold", color=C_GREEN)

arrow(68, Y_AGG, 68, Y_AGG-4.5, color=C_RED, lw=0.7)
box(56, Y_AGG-3, 24, 2.5, fc=C_RED_BG, ec=C_RED, lw=0.5, rounding=0.2)
txt(57, Y_AGG-1.7, "UNMET / CONFLICT", size=3, weight="bold", color=C_RED)

# ═══════════════════════════════════════════════════════════════════
# G. OUTCOME CARDS
# ═══════════════════════════════════════════════════════════════════
Y_OUT = 56
# Consensus Verdict (Left)
box(12, Y_OUT, 35, 18, fc=C_GREEN_BG, ec=C_GREEN, lw=0.8)
box(12, Y_OUT+15.5, 35, 2.5, fc="#A7F3D0", ec=C_GREEN, lw=0.5, rounding=0.2)
txt(14, Y_OUT+16.7, "CONSENSUS VERDICT", size=3.6, weight="bold", color="#065F46")
txt(14, Y_OUT+13, "Status: 'answered'", size=3.3, weight="bold", color=C_DARK)
txt(14, Y_OUT+10.5, "Answer: { yes | no }", size=3.3, color=C_DARK)
txt(14, Y_OUT+8, "Mean G (agree) \u2265 \u03c4", size=3, color=C_GRAY, family="serif")
txt(14, Y_OUT+5.5, "Verified by \u226575% crop", size=3, color=C_GRAY)
txt(14, Y_OUT+3, "quorum consensus", size=3, color=C_GRAY)

# Failure-Aware Abstention (Right)
box(53, Y_OUT, 35, 18, fc=C_RED_BG, ec=C_RED, lw=0.8)
box(53, Y_OUT+15.5, 35, 2.5, fc="#FECDD3", ec=C_RED, lw=0.5, rounding=0.2)
txt(55, Y_OUT+16.7, "FAILURE-AWARE ABSTENTION", size=3.3, weight="bold", color="#9F1239")
txt(55, Y_OUT+13, "Status: 'review'", size=3.3, weight="bold", color=C_DARK)
txt(55, Y_OUT+10.5, "Assessment: 'inconclusive'", size=3.3, color=C_DARK)
txt(55, Y_OUT+8, "Tied vote (2:2), weak crop,", size=3, color=C_GRAY)
txt(55, Y_OUT+5.5, "or global\u2013local contradiction", size=3, color=C_GRAY)
txt(55, Y_OUT+3, "\u2192 Escalated to human review", size=3, weight="bold", color=C_RED)

# arrows down to final output
arrow(30, Y_OUT, 30, Y_OUT-5, color=C_DARK, lw=0.6)
arrow(70, Y_OUT, 70, Y_OUT-5, color=C_DARK, lw=0.6)

# ═══════════════════════════════════════════════════════════════════
# H. FINAL OUTPUT BOX
# ═══════════════════════════════════════════════════════════════════
Y_FIN = 18
box(5, Y_FIN, 90, 31, fc=C_OUT_BG, ec=C_DARK, lw=1.0)
# header bar
box(5, Y_FIN+28.5, 90, 2.5, fc=C_DARK, ec=C_DARK, lw=0.5, rounding=0.2)
txt(50, Y_FIN+29.7, "FINAL SYSTEM OUTPUT & DIAGNOSTIC TELEMETRY",
    size=3.8, weight="bold", color=C_WHITE, ha="center")

# left block
box(7, Y_FIN+1, 42, 25, fc=C_WHITE, ec="#CBD5E1", lw=0.5, rounding=0.3)
txt(9, Y_FIN+23, "System Disposition:", size=3.6, weight="bold", color=C_DARK)
txt(9, Y_FIN+20, "\u2022 Direct confident: {Yes / No}", size=3.1, color=C_DARK)
txt(9, Y_FIN+17.5, "\u2022 Multi-crop consensus:", size=3.1, color=C_DARK)
txt(12, Y_FIN+15, "{Yes / No}", size=3.1, color=C_DARK)
txt(9, Y_FIN+12, "\u2022 Selective abstention:", size=3.1, weight="bold", color=C_RED)
txt(12, Y_FIN+9.5, "{Review}", size=3.1, weight="bold", color=C_RED)
txt(9, Y_FIN+6.5, "Safe escalation to human", size=2.8, color=C_GRAY)
txt(9, Y_FIN+4.5, "domain expert when", size=2.8, color=C_GRAY)
txt(9, Y_FIN+2.5, "evidence is inconclusive", size=2.8, color=C_GRAY)

# right block
box(52, Y_FIN+1, 41, 25, fc=C_WHITE, ec="#CBD5E1", lw=0.5, rounding=0.3)
txt(54, Y_FIN+23, "Telemetry Payload:", size=3.6, weight="bold", color=C_DARK)
txt(54, Y_FIN+20, "\u2022 reliability_score: G \u2208 [0,1]", size=2.9, color=C_GRAY)
txt(54, Y_FIN+17.5, "\u2022 crops_inspected: [0 | 4]", size=2.9, color=C_GRAY)
txt(54, Y_FIN+15, "\u2022 consensus_ratio: [0.50\u20131.00]", size=2.9, color=C_GRAY)
txt(54, Y_FIN+12.5, "\u2022 crop_bboxes: coordinates", size=2.9, color=C_GRAY)
txt(54, Y_FIN+10, "\u2022 latency_breakdown: (s)", size=2.9, color=C_GRAY)
txt(54, Y_FIN+7.5, "\u2022 evidence_history: rounds", size=2.9, color=C_GRAY)
txt(54, Y_FIN+5, "\u2022 model_version: string", size=2.9, color=C_GRAY)

# Figure caption (below diagram, separate)
txt(50, 10, "Fig. 1. Overall architecture of the proposed VEERA framework.",
    size=4, weight="normal", color=C_DARK, ha="center", family="serif", style="italic")

# ═══════════════════════════════════════════════════════════════════
# Save all formats
# ═══════════════════════════════════════════════════════════════════
os.makedirs("figures", exist_ok=True)

for base_dir in [".", "figures"]:
    base = os.path.join(base_dir, "veera_ieee_architecture")
    fig.savefig(f"{base}.svg", format="svg", dpi=DPI, bbox_inches="tight",
                pad_inches=0.08, facecolor=C_BG)
    fig.savefig(f"{base}.pdf", format="pdf", dpi=DPI, bbox_inches="tight",
                pad_inches=0.08, facecolor=C_BG)
    fig.savefig(f"{base}.png", format="png", dpi=DPI, bbox_inches="tight",
                pad_inches=0.08, facecolor=C_BG)

plt.close(fig)

# Report sizes
for ext in ["svg", "pdf", "png"]:
    p = f"veera_ieee_architecture.{ext}"
    sz = os.path.getsize(p)
    print(f"{ext.upper()}: {p} -- {sz:,} bytes")

from PIL import Image
im = Image.open("veera_ieee_architecture.png")
print(f"PNG dimensions: {im.width} x {im.height} px at {DPI} DPI")
print("\nDONE -- All exports successful!")
