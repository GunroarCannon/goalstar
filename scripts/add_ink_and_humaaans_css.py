import re

home_path = r'C:\Users\hmmm\goalstar-recall\home.html'

with open(home_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace or upgrade the .hero-title span.hl style with .ink-hl-wrap styles
old_hl_css = r'\.hero-title span\.hl \{[\s\S]*?\}'

new_hl_css = '''.hero-title span.hl {
      display: none;
    }
    .ink-hl-wrap {
      position: relative;
      display: inline-block;
      white-space: nowrap;
    }
    .ink-hl-text {
      position: relative;
      z-index: 2;
      color: #d97706;
      text-shadow: 1px 1px 0 rgba(255,255,255,0.7);
    }
    body[data-paper='night'] .ink-hl-text {
      color: #f59e0b;
      text-shadow: 1px 1px 0 rgba(0,0,0,0.9);
    }
    .ink-swash-svg {
      position: absolute;
      left: -2%;
      bottom: -15px;
      width: 106%;
      height: 28px;
      pointer-events: none;
      z-index: 1;
      overflow: visible;
    }

    /* Humaaan Hero Badge */
    .hero-humaaan-badge {
      display: flex;
      align-items: center;
      gap: 14px;
      margin-top: 24px;
      padding: 10px 16px;
      background: var(--panel);
      border: 2px solid var(--ink);
      border-radius: 6px;
      box-shadow: 4px 4px 0 var(--ink);
      position: relative;
      max-width: 430px;
    }
    .hero-avatar-img {
      height: 72px;
      width: auto;
      object-fit: contain;
      filter: drop-shadow(2px 3px 4px rgba(0,0,0,0.15));
      flex-shrink: 0;
    }
    .hero-avatar-text {
      display: flex;
      flex-direction: column;
      gap: 2px;
      font-size: 15px;
      line-height: 1.3;
    }
    .hero-avatar-text strong {
      font-family: 'Space Grotesk', monospace;
      font-size: 13px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: #10b981;
    }
    body[data-paper='night'] .hero-avatar-text strong {
      color: #34d399;
    }
    .ink-blotch-mini {
      position: absolute;
      right: 10px;
      bottom: 8px;
      width: 32px;
      height: 32px;
      pointer-events: none;
    }

    /* Use Case 2-Column Content Layout with Humaaans */
    .uc-content-flex {
      display: flex;
      gap: 24px;
      align-items: center;
      justify-content: space-between;
    }
    .uc-details {
      flex: 1;
      min-width: 0;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }
    .uc-bullet-item {
      display: flex;
      gap: 10px;
      align-items: flex-start;
      padding: 8px 12px;
      border-radius: 6px;
      border: 1.5px solid rgba(42, 45, 62, 0.15);
      background: var(--panel);
    }
    .uc-bullet-item.hurdle {
      border-left: 4px solid #ef4444;
      background: rgba(239, 68, 68, 0.04);
    }
    .uc-bullet-item.fix {
      border-left: 4px solid #10b981;
      background: rgba(16, 185, 129, 0.05);
    }
    body[data-paper='night'] .uc-bullet-item.hurdle {
      background: rgba(239, 68, 68, 0.12);
      border-color: rgba(239, 68, 68, 0.3);
    }
    body[data-paper='night'] .uc-bullet-item.fix {
      background: rgba(16, 185, 129, 0.12);
      border-color: rgba(16, 185, 129, 0.3);
    }
    .bullet-tag {
      font-family: 'Space Grotesk', monospace;
      font-size: 11px;
      font-weight: 800;
      text-transform: uppercase;
      padding: 2px 6px;
      border-radius: 4px;
      white-space: nowrap;
      margin-top: 1px;
    }
    .hurdle .bullet-tag {
      background: #fee2e2;
      color: #b91c1c;
    }
    .fix .bullet-tag {
      background: #d1fae5;
      color: #047857;
    }
    body[data-paper='night'] .hurdle .bullet-tag {
      background: #7f1d1d;
      color: #fecaca;
    }
    body[data-paper='night'] .fix .bullet-tag {
      background: #064e3b;
      color: #a7f3d0;
    }
    .uc-bullet-item p {
      margin: 0;
      font-size: 16px;
      line-height: 1.35;
      color: var(--ink);
    }
    .uc-footer-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 12px;
      margin-top: 6px;
    }
    .uc-humaaan-frame {
      flex: 0 0 140px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      background: var(--paper-warm);
      border: 2px dashed rgba(42, 45, 62, 0.35);
      border-radius: 6px;
      padding: 10px 8px;
      box-shadow: inset 1px 1px 4px rgba(0,0,0,0.06);
    }
    body[data-paper='night'] .uc-humaaan-frame {
      background: rgba(15, 23, 42, 0.5);
      border-color: rgba(245, 158, 11, 0.3);
    }
    .uc-humaaan-img {
      max-height: 135px;
      width: auto;
      object-fit: contain;
      filter: drop-shadow(2px 4px 6px rgba(0,0,0,0.18));
      transition: transform 0.3s ease;
    }
    .uc-card:hover .uc-humaaan-img {
      transform: scale(1.05) translateY(-3px);
    }
    .humaaan-caption {
      font-family: 'Caveat', cursive;
      font-size: 14px;
      font-weight: bold;
      color: var(--ink-soft);
      margin-top: 4px;
      text-align: center;
    }

    @media (max-width: 768px) {
      .uc-content-flex {
        flex-direction: column-reverse;
        align-items: stretch;
      }
      .uc-humaaan-frame {
        flex: none;
        height: 120px;
      }
      .uc-humaaan-img {
        max-height: 95px;
      }
    }'''

content = re.sub(old_hl_css, new_hl_css, content)

with open(home_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Added CSS for ink underline, Humaaans figures, and reduced-text card layout!')
