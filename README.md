<p align="center">
  <img src="https://img.shields.io/badge/version-1.0-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/python-3.10+-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/platform-Windows-lightgrey?style=for-the-badge" />
  <img src="https://img.shields.io/badge/license-MIT-orange?style=for-the-badge" />
</p>

<h1 align="center">🔐 Password Position Calculator</h1>

<p align="center">
  Educational tool for digital forensics and security research.<br>
  Shows the exact brute-force position of any password and estimated crack time.
</p>

---

## 🧑‍💼 Author

**Krystian Zarzecki**  
President of the Board — Wezafon Sp. z o.o. (brand: **Laboratorium Elektroniki**)  
Court-Appointed Expert in Digital Forensics & Teleinformatics  
District Court in Tarnobrzeg, Poland

🌐 [laboratoriumelektroniki.pl](https://laboratoriumelektroniki.pl)  
📘 [facebook.com/LaboratoriumElektroniki](https://facebook.com/LaboratoriumElektroniki)  
🐙 [github.com/studiogsm](https://github.com/studiogsm)

---

## ✨ What it does

Enter any password and the tool instantly shows:

| Metric | Description |
|---|---|
| **Position in brute-force** | Exact 1-based sequence number where this password would be found |
| **Alphabet size** | How many unique characters are in the selected charset |
| **Total combinations** | All possible passwords up to this length |
| **Progress bar** | What percentage of the search space is before this password |
| **Time to crack** | Estimated time to reach this password at selected attack speed |
| **Time to exhaust** | Time to go through the entire search space |
| **Position assessment** | Very Weak / Weak / Average / Good / Excellent |

---

## 🔤 Character Sets

Select any combination:

- 🔢 **Digits** — `0123456789` (10 chars)
- 🔡 **Lowercase** — `a-z` (26 chars)
- 🔠 **Uppercase** — `A-Z` (26 chars)
- 🔣 **Special** — `!@#$%^&*()_+-=[]{}|;'",.<>?/\`` (33 chars)

---

## ⚡ Attack Speed Presets

10 realistic scenarios via slider:

| Preset | Speed |
|---|---|
| Manual / slow script | 100 /s |
| Simple Python script | 1,000 /s |
| Optimized script | 10,000 /s |
| John the Ripper CPU | 100,000 /s |
| Hashcat CPU (MD5) | 1,000,000 /s |
| Hashcat GPU budget | 10,000,000 /s |
| Hashcat GPU mid-range | 100,000,000 /s |
| Hashcat GPU high-end | 1,000,000,000 /s |
| GPU cluster / cloud | 10,000,000,000 /s |
| Distributed / ASIC top | 10,000,000,000,000 /s |

---

## 🖥️ Usage

1. Type a password in the input field (live calculation on every keystroke)
2. Select the character sets that match your target alphabet
3. Adjust the attack speed slider
4. Read the results — position, time estimates, and strength assessment

> All calculation is done **locally** — no data leaves the computer.

---

## 📦 Requirements

- **Python 3.10+**
- `tkinter` — included with standard Python on Windows
- No external packages required

---

## 🔨 Build (compile to Windows EXE)

Place all files in one folder and run:

```
build_ppc.bat
```

Output: `dist\PasswordPositionCalculator.exe`

### Required files:
```
password_position_calculator.py   ← application source
build_ppc.bat                      ← build script
icon.ico                            ← application icon (optional, use your own)
```

---

## 📋 Version History

| Version | Changes |
|---|---|
| **v1.0** | Initial release — position calculator, 10 speed presets, 4 charset toggles, strength assessment, live calculation |

---

## ⚖️ Legal Notice

This tool is intended for **educational, forensic research, and authorized security testing only**.  
No data leaves the computer. All calculations are performed locally.

---

## 📄 License

MIT License — free to use, modify and distribute.

---

© 2025 Krystian Zarzecki / Laboratorium Elektroniki
