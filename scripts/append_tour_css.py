p = r"C:\Users\hmmm\goalstar-recall\css\style.css"
with open(p, "a", encoding="utf-8") as f:
    f.write("""

/* ---- Tour Trigger & Replay Buttons ---- */
.tour-nav-btn {
  background: #fef3c7;
  color: #92400e;
  border: 1.5px solid #d97706;
  border-radius: 99px;
  padding: 4px 11px;
  font-family: inherit;
  font-weight: 700;
  font-size: 12.5px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 5px;
  transition: all 0.15s ease;
  box-shadow: 0 1px 2px rgba(217, 119, 6, 0.15);
}
.tour-nav-btn:hover {
  background: #fde68a;
  transform: translateY(-1px);
}
.tour-resee-box {
  padding: 10px 0 4px;
  border-top: 1px dashed var(--border);
  margin-top: 12px;
}
.tour-side-btn {
  width: 100%;
  background: var(--panel-2);
  border: 1.5px dashed #d97706;
  color: #b45309;
  border-radius: 6px;
  padding: 7px 10px;
  font-family: var(--hand, 'Patrick Hand', cursive);
  font-size: 14.5px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.15s ease;
  text-align: center;
}
.tour-side-btn:hover {
  background: #fef3c7;
  border-color: #b45309;
}
""")
print("Appended tour styles successfully!")
