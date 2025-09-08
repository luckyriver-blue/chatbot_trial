#streamlitのデフォルトのヘッダーなどを非表示
hide_st_style = '''
<style>
    div[data-testid="stToolbar"] {
    visibility: hidden;
    height: 0%;
    position: fixed;
    }
    div[data-testid="stDecoration"] {
    visibility: hidden;
    height: 0%;
    position: fixed;
    }
    #MainMenu {
    visibility: hidden;
    height: 0%;
    }
    header {
    visibility: hidden;
    height: 0%;
    }
    footer {
    visibility: hidden;
    height: 0%;
    }
    .appview-container .main .block-container{
        padding-top: 1rem;
        padding-right: 3rem;
        padding-left: 3rem;
        padding-bottom: 1rem;
    }  
    .reportview-container {
        padding-top: 0rem;
        padding-right: 3rem;
        padding-left: 3rem;
        padding-bottom: 0rem;
    }
    header[data-testid="stHeader"] {
        z-index: -1;
    }
    .block-container {
        padding-top: 0rem !important;
    }
    @media (max-width: 700px) { 
        .block-container {
        padding-left: 0rem !important;
        padding-right: 0rem !important;
        max-width: 90% !important;
        }
    }
</style>
'''

#会話のスタイリング
message_style = '''
<style>
    .messages {
        display: inline-block;
        word-wrap: break-word;
        background-color: #f0f0f0;
        padding: 10px;
        border-radius: 10px;
    }
</style>
'''
  
#送信欄のスタイリング
input_style = '''
<style>
    .stButton > button {
    border-radius: 20px;
    }
    .stButton > button:hover {
        border-color: #ff2b2b;
    }
    div[data-testid="InputInstructions"] > span:nth-child(1) {
        visibility: hidden;
    }
</style>
'''