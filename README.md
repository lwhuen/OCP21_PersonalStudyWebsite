# OCP Java SE 21 — Personal Study Website

個人溫習用的 **1Z0-830**（Java SE 21 Developer）筆記站。考試日同每週日程只寫在 [`OCP-Java-SE-21-study-plan.md`](OCP-Java-SE-21-study-plan.md)。

線上看：https://lwhuen.github.io/OCP21_PersonalStudyWebsite/

---

## 這份 repo 有什麼

| 用途 | 檔案 |
|---|---|
| 溫習方法 | [`溫習策略.md`](溫習策略.md) |
| 15 週日程 | [`OCP-Java-SE-21-study-plan.md`](OCP-Java-SE-21-study-plan.md) |
| 每週筆記／詞彙 | `Week-01-notes.md` … `Week-08-notes.md`、對應 `*-glossary.md` |
| Anki | `Week-0N-anki.apkg`（學完該週再匯入） |
| 靜態網站產物 | 根目錄的 `*.html`（GitHub Pages）以及 `site/`（本機建置輸出） |
| 建置腳本 | `build_site.py` |

筆記裡的題是練習題，不是真題，也不是書上原題。參考書只用 Boyarsky / Selikoff 的 *OCP Oracle Certified Professional Java SE 21 Developer Study Guide*。

---

## 怎麼用網站

1. 打開 [首頁](https://lwhuen.github.io/OCP21_PersonalStudyWebsite/)。
2. 先讀 **溫習策略**，再跟 **15 週計劃**。
3. 只開**當週**筆記；詞彙忘記詞才查。
4. 側欄可以：
   - 搜尋詞、題、規則
   - 用書籤收藏多個位置（章、節、lab 都可以；側欄會列出全部）
   - 看本週 scroll 進度
5. 題目選完再撳眼睛圖示揭曉答案。勾選清單、書籤、答題狀態存在**這個瀏覽器**的 localStorage，唔會跟帳號同步。

本機預覽：

```powershell
cd "路徑\OCP21_PersonalStudyWebsite"
python build_site.py
cd site
python -m http.server 8777
```

然後開 http://127.0.0.1:8777/

也可以直接開 `site/index.html`（`file://`）。注意：`file://` 同 `http://` 的 localStorage 係分開嘅。

---

## 改筆記之後點更新網站

1. 改對應的 `Week-0N-notes.md` / glossary / 策略檔。
2. 重建：

```powershell
python build_site.py
```

3. 把 `site/` 同步到 repo 根目錄（Pages 讀根目錄）：

```powershell
Copy-Item -Force site\* -Destination .
```

4. commit 同 push：

```powershell
git add .
git commit -m "Update study notes and site"
git push
```

需要 Python 3，以及套件 `markdown`：

```powershell
pip install markdown
```

---

## 溫習節奏（摘要）

- **八週學完 syllabus**
- **一個月 mock**（Enthuware 由 mock 月先開）
- **三個 hold 週**保住分數
- 平日每天約 3 小時：20 分鐘錯題 Anki → 2 小時打 listing → 40 分鐘做題
- 最後兩次計時 mock 都要 **≥ 75%（38／50）** 先去考；合格線是 68%

具體日期睇 [15 週計劃](OCP-Java-SE-21-study-plan.md)。門檻同每天 checklist 睇策略同計劃兩個檔。

---

## GitHub Pages

Settings → Pages → **Deploy from a branch** → `main` → **`/(root)`**。

根目錄需要有 `index.html`。已放 `.nojekyll`，避免 Jekyll 干預。

---

## 授權同範圍

私人溫習用途。唔好把筆記當官方教材或洩漏真題。JDBC 唔喺 1Z0-830 範圍內，本站亦冇寫。
