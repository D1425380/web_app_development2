# 路由設計文件 (ROUTES)

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| **首頁/任務列表** | GET | `/` | `index.html` | 顯示所有任務與篩選選項 |
| **新增任務頁面** | GET | `/tasks/new` | `tasks/new.html` | 顯示新增任務的表單 |
| **建立任務** | POST | `/tasks/add` | — | 接收表單、存入資料庫並重導向至首頁 |
| **任務詳情** | GET | `/tasks/<int:id>` | `tasks/detail.html` | 顯示單筆任務的詳細內容 |
| **編輯任務頁面** | GET | `/tasks/<int:id>/edit` | `tasks/edit.html` | 顯示編輯任務的表單 |
| **更新任務** | POST | `/tasks/<int:id>/update` | — | 接收編輯表單並更新資料庫 |
| **更新任務狀態** | POST | `/tasks/<int:id>/status` | — | 快速變更任務狀態（例如：標記為已完成） |
| **刪除任務** | POST | `/tasks/<int:id>/delete` | — | 刪除任務並重導向至首頁 |
| **使用者列表** | GET | `/users` | `users/index.html` | (選配) 顯示所有使用者 |

---

## 2. 路由詳細說明

### 2.1 任務列表 (GET /)
- **輸入**：無（可選篩選參數如 `?status=pending`）。
- **處理邏輯**：呼叫 `Task.get_all()`。
- **輸出**：渲染 `index.html`。
- **錯誤處理**：若資料庫讀取失敗，顯示 500 錯誤頁面。

### 2.2 建立任務 (POST /tasks/add)
- **輸入**：`title`, `description`, `priority`, `due_date`, `assigned_to` (Form Data)。
- **處理邏輯**：驗證 `title` 為必填，呼叫 `Task.create()`。
- **輸出**：重導向至 `/`。
- **錯誤處理**：驗證失敗則重新導向至 `/tasks/new` 並顯示 Flash 訊息。

---

## 3. Jinja2 模板清單

| 檔案路徑 | 繼承模板 | 說明 |
| :--- | :--- | :--- |
| `base.html` | — | 包含導覽列與靜態資源引入的主版面 |
| `index.html` | `base.html` | 任務列表與操作選單 |
| `tasks/new.html` | `base.html` | 新增任務表單 |
| `tasks/edit.html` | `base.html` | 編輯任務表單 |
| `tasks/detail.html` | `base.html` | 任務詳細內容顯示 |

---

## 4. 路由骨架程式碼 (app/routes/)

### 4.1 main.py (主頁面路由)
- `index()`: 渲染首頁列表。

### 4.2 task.py (任務功能路由)
- `new_task()`: 顯示新增表單。
- `add_task()`: 執行新增動作。
- `task_detail(id)`: 顯示詳情。
- `edit_task(id)`: 顯示編輯表單。
- `update_task(id)`: 執行更新動作。
- `update_status(id)`: 執行狀態切換。
- `delete_task(id)`: 執行刪除動作。
