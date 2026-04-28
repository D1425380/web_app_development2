# 流程圖設計文件 (FLOWCHART)

## 1. 使用者流程圖 (User Flow)

此流程圖展示了使用者在「任務管理系統」中的主要操作路徑。

```mermaid
flowchart TD
    Start([使用者開啟網頁]) --> Home[首頁 - 任務列表]
    Home --> Action{要執行什麼操作？}
    
    Action -->|新增| New[進入新增任務頁面]
    New --> Input[填寫標題、截止日與分配成員]
    Input --> Submit[點擊送出]
    Submit --> Success{建立成功？}
    Success -->|是| Home
    Success -->|否| New
    
    Action -->|修改狀態| Status[點擊狀態選單]
    Status --> Update[更新為：進行中/已完成]
    Update --> Home
    
    Action -->|查看詳情| Detail[進入任務詳情頁面]
    Detail --> Back[點擊返回]
    Back --> Home
    
    Action -->|編輯內容| Edit[進入編輯頁面]
    Edit --> Save[修改內容並儲存]
    Save --> Home
    
    Action -->|刪除任務| Delete[點擊刪除按鈕]
    Delete --> Confirm{確認刪除？}
    Confirm -->|是| Home
    Confirm -->|否| Home
```

---

## 2. 系統序列圖 (Sequence Diagram)

此圖以「新增任務」為例，展示資料如何在各元件間傳遞。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Model as Database Model
    participant DB as SQLite
    
    User->>Browser: 填寫任務表單並點擊送出
    Browser->>Flask: POST /tasks/add
    Flask->>Model: 呼叫 Task.create(data)
    Model->>DB: INSERT INTO tasks (title, desc, status, ...)
    DB-->>Model: 回傳成功 (Last Insert ID)
    Model-->>Flask: 回傳 Task 物件
    Flask-->>Browser: HTTP 302 重導向至 /index
    Browser->>Flask: GET /index
    Flask->>Model: 呼叫 Task.all()
    Model->>DB: SELECT * FROM tasks
    DB-->>Model: 回傳任務清單
    Model-->>Flask: 回傳物件清單
    Flask-->>Browser: 渲染 index.html (含新任務)
    Browser-->>User: 顯示更新後的任務列表
```

---

## 3. 功能清單與路由對照表

根據流程圖規劃的初步路由規劃：

| 功能 | HTTP 方法 | URL 路徑 | 說明 |
| :--- | :--- | :--- | :--- |
| 任務列表 (首頁) | GET | `/` | 顯示所有任務 |
| 新增任務頁面 | GET | `/tasks/new` | 顯示新增表單 |
| 執行新增任務 | POST | `/tasks/add` | 接收表單並存入資料庫 |
| 任務詳情 | GET | `/tasks/<id>` | 顯示單筆任務內容 |
| 編輯任務頁面 | GET | `/tasks/<id>/edit` | 顯示編輯表單 |
| 執行更新任務 | POST | `/tasks/<id>/update` | 更新任務資料 |
| 刪除任務 | POST | `/tasks/<id>/delete` | 刪除單筆任務 |
| 更新任務狀態 | POST | `/tasks/<id>/status` | 快速切換狀態 (進行中/已完成) |
