import dash
import pyodbc
import datetime
import pyodbc
from dash import html, dcc
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import requests

# 連接資料庫
def get_sql_server_connection():
    conn_str = (
           "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=AJE7-LAPTOP\\MSSQLSERVER01;"
        "DATABASE=info;"
        "UID=ouo;"
        "PWD=10111011;"
    )
    return pyodbc.connect(conn_str)

# 定義標題和標誌
def Header(app):
    title_img = html.Img(
        src=app.get_asset_url("諸葛.png"),
        style={
            "margin": 0,        # 移除所有邊距
            "padding": 0,       # 移除所有填補
            "height": 50,      # 設定標題高度
        }
    )
    logo = html.Img(
        src=app.get_asset_url("001.1.png"),
        style={
            "margin": 0,        # 移除所有邊距
            "padding": 0,       # 移除所有填補
            "height": 50,       # 設定 logo 高度
            "border-radius": "50%" 
        }
    )

    # AI 生成的警語
    ai_disclaimer = html.P(
        "AI 生成內容，僅供參考",
        style={
            "margin": 0,        # 移除所有邊距
            "padding": 0,       # 移除所有填補
            "font-size": "20px",
            "color": "gray",
            "margin": 0  # 移除所有邊距
        }
    )

    return dbc.Row(
        [
            dbc.Col(title_img, width="auto"),  # 自動調整寬度
            dbc.Col(logo, width="auto"),       # 自動調整寬度
            dbc.Col(ai_disclaimer, width="auto")  # 自動調整寬度
        ],
        align="center",
        justify="start",  # 左對齊
        style={
            "margin": 0,        # 移除所有邊距
            "padding": 0,       # 移除所有填補
            "height": "30px",   # 設定行高
            "position": "relative",  # 使用相對定位
            "top": "-10px"       # 向上移動 5px
        }
    )

# 起始畫面
def start_screen():
    return dbc.Container(
        fluid=True,
        style={
            "background-image": "url('/assets/background.jpg')",
            "background-size": "cover",
            "height": "100vh",
            "width": "100vw",
            "color": "black",  # 將文字顏色改為黑色
            "font-size": "18px",
            "padding": "20px",
            "margin": "0"
        },
        children=[
            Header(app),
            html.Hr(style={"border-top-color":"#808080"}),
            dbc.Row(
                justify="center",  # 水平居中對齊
                children=[
                    dbc.Col(
                        width={"size": 5, "offset": 2},  # 調整寬度和偏移量
                        children=[
                            dbc.Card(
                                style={
                                    "width": "30rem",
                                    "padding": "2rem",
                                    "border-radius": "20px",
                                    "background-color": "#808080",
                                    "color": "black",
                                    "display": "flex",
                                    "font-weight": "bold",
                                    "flex-direction": "column",
                                    "justify-content": "center",
                                },
                children=[
                    html.H4("歡迎使用資訊小諸葛!", className="text-center", style={"font-weight": "bold","color": "black",}),  # 粗體標題
                    html.Div(
                        [
                            dbc.Label("員工編號:"),
                            dbc.Input(id="user-name", type="text", placeholder="請輸入您的員編"),
                        ],
                        style={"margin-bottom": "15px"}
                    ),
                    html.Div(
                        [
                            dbc.Label("單位:"),
                            dbc.Input(id="user-unit", type="text", placeholder="請輸入您的單位"),
                        ],
                        style={"margin-bottom": "15px"}
                    ),
                    dbc.Button("開始使用", id="start-button", color="primary", className="mt-3"),
     ],
                            ),
                        ]
                    ),
                ]
            ),
        ]
    )

# 定義訊息框
def textbox(text, box="AI", name="Chatbot"):
    text = text.replace(f"{name}:", "").replace("You:", "")
    max_length = 1000  # 設定最大字數
    text = text[:max_length] 

    # 將AI回應中的\n替換為&ensp，以便在html中正確顯示換行
    text = text.replace("\n", "&ensp;")

    base_style = {
        "max-width": "96%",
        "width": "max-content",
        "padding": "10px 15px", 
        "border-radius": "20px",  # 將邊框半徑調大一點，使外觀更柔和
        "margin-bottom": "20px",
        "font-weight": "bold",
        "color": "black", 
        "border": "none", 
    }

    if box == "user":
        style = {
            **base_style,
            "margin-left": "auto",
            "margin-right": 0
        }
        user_color = "#6A6AFF" 
        return dbc.Card(html.Div(text, style={"white-space": "pre-wrap"}),  # 使用pre-wrap保留換行和空格
                        style={**style, "background-color": user_color}, body=True, inverse=False)
    elif box == "AI":
        style = {
            **base_style,
            "margin-left": 0,
            "margin-right": "auto"
        }
        ai_color = "#ffffff" 
        thumbnail = html.Img(
            src=app.get_asset_url("001.1.png"),
            style={
                "border-radius": "50%",
                "height": "36px",
                "margin-right": "5px",
                "float": "left"
            },
        )
        # 使用 dcc.Markdown 告訴Dash不要轉義text中的HTML標籤
        textbox = dbc.Card(dcc.Markdown(text, dangerously_allow_html=True), 
                           style={**style, "background-color": ai_color}, body=True, inverse=False)
        return html.Div([thumbnail, textbox])
    else:
        raise ValueError("Incorrect option for box.")

def log_section():
    fake_logs = [
        "我輸入密碼無法登，怎麼辦",
        "公司應用系統入口網站的部分連結無法直接開啟，怎麼辦",
        "車站地震儀GDS異常，怎麼辦",
        "我想知道手機與iPad取消隨機MAC設定(iPhone的iOS系統)步驟",
        "我的滑鼠、鍵盤故障，怎麼辦",
    ]
    
    log_items = [
        dbc.Card(
            html.Div(log, style={
                "white-space": "nowrap",          # 防止文本换行
                "overflow": "hidden",             # 隐藏超出部分
                "text-overflow": "ellipsis",      # 超出部分显示省略号
            }),
            style={
                "border-radius": "10px",
                "margin-bottom": "10px",
                "padding": "10px",
                "background-color": "#8E8E8E",
                "color": "black",
                "width": "calc(100% - 20px)"      # 维持目前宽度
            }
        ) for log in fake_logs
    ]

    return html.Div(
    id="log-section",
    children=[
        html.H5("過去熱門詢問", style={"font-weight": "bold"}),
        html.Div(
            id="log-content",
            children=log_items,
            style={
                "height": "calc(90vh - 65px)", 
                "overflow-y": "auto", 
                "text-align": "left",  # 将文字对齐方式设置为左对齐，避免文字也翻转
            }
        ),
    ],
        style={
            "border": "4px solid #815414",
            "border-radius": "10px",
            "padding": "10px",
            "height": "calc(90vh - 10px)",
            "background-color": "rgba(0, 0, 0, 0)",
            "color": "white",
            "font-weight": "bold",
            "float": "left",
            "width": "100%"
        }
    )

# 定義FAQ區塊
def faq_section():
    faqs = {
        "硬體相關問題": [
            {
                "question": "我的電腦開不了機了，怎麼辦？",
                "answer": [
                    "1. 確認電源插頭是否插好，並檢查插座是否有電。",
                    "2. 確認電腦本身的電源開關是否打開。",
                    "3. 如果以上兩點無問題，嘗試換一個電源插座，或者使用其他電器來測試該插座是否正常運作。"
                ]
            },
            {
                "question": "我的電腦開機後，發出奇怪的噪音，聽起來像是風扇或硬碟的聲音，該怎麼處理？",
                "answer": [
                    "1. 檢查風扇：確認電腦的風扇是否有異常聲音，如果是，可能需要清潔風扇或更換損壞的風扇。",
                    "2. 硬碟偵測：使用硬碟檢測工具來檢查硬碟的健康狀態，如果硬碟出現問題，請及早備份資料並更換硬碟。",
                    "3.  避免過熱：確保電腦放置在通風良好的位置，避免過熱可能導致硬體元件運轉不穩定或產生噪音。"
                ]
            },
            {
                "question": "我的螢幕無畫面，怎麼辦？",
                "answer": [
                    "1. 查看電源線兩端有無鬆脫。",
                    "2. 電源燈號未亮，開關可能未開。",
                    "3. D-SUB線兩端未插緊。",
                    "4. 報修EFMS系統派請廠商處理。",
                    "5. 電話撥打8471聯絡資訊處處理。"
                ]
            },
        ],
        "軟體相關問題": [
            {
                "question": "我無法上網了。",
                "answer": [
                    "1. 請檢查您的網路連線是否正常。",
                    "2. 請嘗試將電腦重新啟動。"
                ]
            },
            {
                "question": "我的網路不通，怎麼辦？",
                "answer": [
                    "1.設備有無異動。有。未申請IPMAC異動。.請至http://scada.trtc.com.tw:5555/ IPMAC管理網站申請,多人網路不通的話報修efms工單子系統別選行政光纖網系統。"
                ]
            }
        ]
    }

    faq_items = []
    for category, questions in faqs.items():
        category_items = []
        for faq in questions:
            question_item = html.Details(
                [
                    html.Summary(faq["question"], style={"font-weight": "bold", "color": "black"}),  # 問題字體顏色為黑色
                    html.Div(
                        [html.P(step, style={"font-weight": "bold", "color": "black"}) for step in faq["answer"]],  # 答案字體顏色為黑色
                        style={"color": "black"} # 整體字體顏色為黑色
                    )
                ],
                style={
                    "border": "4px solid #000000",
                    "border-radius": "10px",
                    "margin-bottom": "10px",
                    "padding": "10px",
                    "background-color": "#BBFFBB" # 白色底色
                }
            )
            category_items.append(question_item)
        
        category_section = html.Details(
            [
                html.Summary(category, style={"font-size": "20px", "font-weight": "bold", "color": "black"}),  # 大項分類字體
                html.Div(category_items)
            ],
            style={
                "border-radius": "10px",
                "margin-bottom": "20px",
                "padding": "10px",
                "background-color": "#8E8E8E"# 灰色底色
            }
        )
        
        faq_items.append(category_section)

    return html.Div(
        id="faq-section",
        children=[
            html.H5("常見問題", style={"font-weight": "bold"}),
            html.Div(
                faq_items,
                style={"height": "calc(45vh - 65px)", "overflow-y": "auto"}  # 調整高度為 45vh
            ),
            html.H5("文件內參考來源", style={"font-weight": "bold", "margin-top": "20px"}),
            html.Div(
                id="reference-sources",
                style={
                    "height": "calc(45vh - 65px)",
                    "overflow-y": "auto",
                    "background-color": "white",
                    "border-radius": "10px",
                    "padding": "10px",
                    "border": "5px solid #8E8E8E"  # 加粗邊框，設置顏色
                }
            )
        ],
        style={
            "border": "4px solid #815414",  # 邊框，邊條調粗
            "border-radius": "10px",
            "padding": "10px",
            "height": "calc(90vh - 10px)",
            "background-color": "rgba(0, 0, 0, 0)",
            "color": "white",
            "font-weight": "bold"
        }
    )

# 設定輸入控制
controls = dbc.InputGroup(
    children=[
        dbc.Input(
            id="user-input",
            placeholder="想詢問什麼...",
            type="text",
            className="custom-input",  # 添加自定義類別
            style={
                "background-color": "#5B4B00", 
                "color": "#ffffff", 
                "border": "0px solid White"
            } 
        ),
        dbc.InputGroupText(
            dbc.Button(
                "傳送",
                id="submit",
                style={
                    "background-color": "#cb7c2c", 
                    "color": "#000000",
                    "border": "0px solid White"
                }
            ),
            style={
                "background-color": "#815414",
                "border": "0px solid White" 
            } 
        ),
    ],
    style={"background-color": "transparent", "width": "100%"},
    id="controls"
)

# 定義對話顯示區域
conversation = html.Div(
    style={
        "display": "flex",
        "flex-direction": "column",
        "background-color": "rgba(0, 0, 0, 0)",
        "color": "white",
        "height": "calc(90vh - 10px)",
    },
    children=[
        html.Div(
            id="display-conversation",
            style={
                "flex-grow": "1",
                "overflow-y": "auto",
                "padding-right": "5px", 
            }
        ),
        html.Div(controls, style={"width": "100%"})  # 保留 controls
    ]
)

# 建 Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

app.layout = html.Div(
    id="app-content",
    children=[
        dcc.Location(id="url"),
        dbc.Spinner(
            [html.Div(id="loading-component")],
            color="primary",
            spinner_style={"width": "5rem", "height": "5rem"}
        ),
        html.Div(id="page-content"),
        dbc.Modal(  # 加入 modal
            [
                dbc.ModalHeader(dbc.ModalTitle("注意 !")),
                dbc.ModalBody("請填寫員工編號和單位！"),
                dbc.ModalFooter(
                    dbc.Button(
                        "關閉", id="close-modal", className="ml-auto", n_clicks=0
                    )
                ),
            ],
            id="modal",
            is_open=False,
        ),
    ]
)

app.css.append_css({
    'external_url': '/assets/style.css' 
})

# 回調函數：根據 URL 切換頁面
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/": 
        return start_screen()
    elif pathname == "/chat":
        return dbc.Container(
            fluid=True,
            style={
            "background-image": "url('/assets/background.jpg')",
            "background-size": "cover",
            "height": "100vh",
            "width": "100vw",
            "color": "white",
            "font-size": "18px",
            "padding": "20px",
            "margin": "0"
        },
            children=[
                Header(app),
                html.Hr(),
                dcc.Store(id="store-conversation", data=""),
                dbc.Row([
                    dbc.Col(log_section(), md=2),
                    dbc.Col(conversation, md=7),
                    dbc.Col(faq_section(), md=3)
                ], style={"height": "calc(100vh - 132px)"}),
                # spinner,  # 從聊天頁面中移除 spinner
            ]
        )
    else:  # 預設顯示起始畫面
        return start_screen()

# 修改 start_button_click 回調函數
@app.callback(
    Output("url", "pathname"),
    Output("modal", "is_open"),
    Input("start-button", "n_clicks"),
    Input("close-modal", "n_clicks"),  # 新增一個 Input，用於關閉 modal
    State("user-name", "value"),
    State("user-unit", "value"),
    prevent_initial_call=True
)
def handle_inputs(start_button_clicks, close_modal_clicks, name, unit):
    ctx = dash.callback_context

    if not ctx.triggered:
        return dash.no_update, False  # modal 保持關閉

    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_id == "start-button":
        if not name or not unit:
            return dash.no_update, True  # 打開 modal
        else:
            conn = None
            try:
                # 連接 SQL Server 並插入數據
                conn = get_sql_server_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO UserLogs (Name, Unit, StartTime) VALUES (?, ?, ?)",
                    (name, unit, datetime.datetime.now())
                )
                conn.commit()
            except Exception as e:
                print(f"Error inserting into database: {e}")
            finally:
                if conn:
                    try:
                        conn.close()
                    except Exception as e:
                        print(f"Error closing connection: {e}")

            return "/chat", False  # 跳轉到聊天頁面，modal 保持關閉

    elif triggered_id == "close-modal":
        return dash.no_update, False  # 關閉 modal

    else:
        return dash.no_update, False  # 其他情況下，modal 保持關閉

# 定義回調函數以更新對話顯示
@app.callback(
    Output("display-conversation", "children"),
    Input("store-conversation", "data")
)
def update_display(chat_history):
    # 根據對話記錄生成對應的文本框
    return [
        textbox(x, box="user") if i == 0 or (i > 0 and i % 3 == 0) else textbox(x, box="AI") 
        for i, x in enumerate(chat_history.split("<split>")[:-1])
    ]

# 定義回調函數以清除輸入框
@app.callback(
    Output("user-input", "value"),
    Input("submit", "n_clicks"),
    Input("user-input", "n_submit"),
    State("user-input", "value")
)
def clear_input(n_clicks, n_submit, user_input):
    # 當按下提交按鈕或按下回車鍵時清除輸入框
    if n_clicks or n_submit:
        return ""
    return dash.no_update


# 定義回調函數以運行查詢
@app.callback(
    Output("store-conversation", "data"),
    Output("loading-component", "children"),
    Output("reference-sources", "children"),
    Input("submit", "n_clicks"),
    Input("user-input", "n_submit"),
    State("user-input", "value"),
    State("store-conversation", "data")
)
def run_query(n_clicks, n_submit, user_input, chat_history):
    ctx = dash.callback_context  # 获取 callback context

    if not ctx.triggered:  # 如果沒有任何 Input 觸發，則不執行
        return chat_history, None, []

    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]  # 獲取觸發 callback 的 Input 的 ID

    if triggered_id not in ["submit", "user-input"]:  # 如果觸發的 Input 不是 "submit" 或 "user-input"，則不執行
        return chat_history, None, []

    if user_input is None or user_input == "":
        return chat_history, None, [] 

    chat_history += f"You: {user_input}<split>"

    loading_output = dcc.Loading(
    id="loading",
    type="default",
    children=html.Div(id="loading-output", className="loading-icon"), 
    style={ 
        'display': 'flex',
        'justify-content': 'center',
        'align-items': 'center',
        'height': '100%'
    }
)

    def extract_category(ai_response):
        # 在這裡實作你的邏輯，從 ai_response 中提取類別
        # 這個範例假設類別永遠是 AI 回答的第一個詞：
        return ai_response.split()[0] 

        # 或者，如果類別在 AI 回答中有特定的格式，例如 "**所屬類別**：硬體問題"：
        # category_keyword = "**所屬類別**" 
        # if category_keyword in ai_response:
        #     category_start = ai_response.find(category_keyword) + len(category_keyword)
        #     category_end = ai_response.find("\n", category_start) 
        #     return ai_response[category_start:category_end].strip()
        # else:
        #     return "Unknown" 

    try:
        response = requests.post("http://127.0.0.1:5000/ask", json={"question": user_input})
        response.raise_for_status() 
        data = response.json() 
        ai_response = data.get("answer", "無法獲取回應") 

        # 提取類別
        category1 = extract_category(ai_response) 

        # 在這裡獲取參考來源，並將其添加到 reference_sources
        reference_sources = data.get("doc1", [])

    except requests.exceptions.RequestException as e:
        # 錯誤處理：將錯誤訊息添加到聊天記錄和參考來源區塊中
        error_message = f"查詢時發生錯誤"
        chat_history += f"Chatbot: {error_message}<split>"
        return chat_history, html.Div(), reference_sources_output

    except ValueError as e:
        # 錯誤處理：將錯誤訊息添加到聊天記錄和參考來源區塊中
        error_message = f"查詢時發生錯誤，無法解析回應"
        chat_history += f"Chatbot: {error_message}<split>"
        return chat_history, html.Div(), reference_sources_output

    chat_history += f"{ai_response}<split>"
    chat_history += f"Chatbot: 還有想詢問的嗎 ? 都可以試著問我喔 !!!<split>"

    # 更新參考來源區塊，提取 doc1 中的 page_content
    reference_sources_output = [
        html.P(source.get("page_content", ""), style={"color": "black"}) 
        for source in reference_sources if source 
    ]

    # 如果 reference_sources 為空，顯示錯誤訊息
    if not reference_sources_output:
        reference_sources_output = [html.P("無參考來源", style={"color": "red"})]

    return chat_history, html.Div(), reference_sources_output  # 返回三個 Output

# 運行 Dash 應用
if __name__ == "__main__":
    app.run_server(debug=True)
