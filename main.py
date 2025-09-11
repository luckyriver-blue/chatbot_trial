import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from style_and_javascript.style import hide_st_style, message_style, input_style
from config.set_llm import llm
from config.set_firebase import firebase_project_settings
from talk_bot import ChatBot
import datetime

#スタイリング
st.markdown(hide_st_style, unsafe_allow_html=True)
st.markdown(message_style, unsafe_allow_html=True)
st.markdown(input_style, unsafe_allow_html=True)


# Firebase Admin SDKの初期化
if not firebase_admin._apps:
  cred = credentials.Certificate(firebase_project_settings)
  firebase_admin.initialize_app(cred)

# Firestoreのインスタンスを取得
db = firestore.client()


# セッションステートの初期化
if "user_id" not in st.session_state:
    #ログイン（実験参加者のid認証）
    user_id = st.text_input("学籍番号を入力してエンターを押してください")
    if user_id:
        st.session_state['user_id'] = user_id
        st.rerun()
    st.stop()

#Firestoreのデータへのアクセス
ref = db.collection("users").document(st.session_state["user_id"]).collection("conversation").order_by("timestamp")

if "input" not in st.session_state:
    st.session_state["input"] = ""
if "placeholder" not in st.session_state:
    st.session_state["placeholder"] = ""
#time（開始時間）や、messagesがない場合は、一旦firebase上にないか探す
if "time" not in st.session_state:
    docs = ref.get()
    if docs:
        st.session_state["time"] = docs[0].to_dict()["timestamp"]
        st.session_state["messages"] = [doc.to_dict() for doc in docs]
    else:
        st.session_state["time"] = None
        st.session_state["messages"] = []

# #Firebaseから有効な参加者IDを取得する関数
# def get_valid_ids():
#   valid_ids = []
#   users = db.collection("users").stream()

#   for user in users:
#     valid_ids.append(user.id)
  
#   return valid_ids




#会話履歴の表示
def show_messages():
    for i, message in enumerate(st.session_state["messages"]):
        if message["role"] == "human":
            st.markdown(f'''
            <div style="display: flex;">
                <div style="display: flex; margin-left: auto; max-width: 65%;">
                <div class="messages">{message["content"]}</div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
        else:
            with st.chat_message(message["role"]):
                st.markdown(f'''
                <div style="max-width: 80%;" class="messages">{message["content"]}</div>
                ''', unsafe_allow_html=True)


#送信ボタンが押されたとき
def send_message():
    #firestoreへの保存のためのアクセス
    add_ref = db.collection("users").document(st.session_state["user_id"]).collection("conversation")
    input = st.session_state["input"]
    if input == "":
        st.session_state["placeholder"] = "メッセージを入力してください！"
        return
    st.session_state["input"] = ""
    st.session_state["placeholder"] = ""
    #新しい入力を追加
    input_message_data = {"role": "human", "content": input, "timestamp": firestore.SERVER_TIMESTAMP}
    add_ref.add(input_message_data)
    #最初の送信だったら、タイマー開始（最初のtimestampを控える）
    if st.session_state["time"] == None:
        st.session_state["time"] = ref.get()[0].to_dict()["timestamp"]
    time = datetime.datetime.now(datetime.timezone.utc) - st.session_state["time"]
    st.session_state["messages"].append(input_message_data)
    #新しい入力応答を追加
    bot = ChatBot(llm, user_id=st.session_state["user_id"], time=time)
    response = bot.chat(st.session_state["messages"])
    output_message_data = {"role": "ai", "content": response, "timestamp": firestore.SERVER_TIMESTAMP}
    add_ref.add(output_message_data)
    st.session_state["messages"].append(output_message_data)

#会話終了後
if st.session_state["time"] != None and datetime.datetime.now(datetime.timezone.utc) - st.session_state["time"] > datetime.timedelta(minutes=10):
    st.markdown(
                f'<br>これで会話は終了です。<br><a href="https://nagoyapsychology.qualtrics.com/jfe/form/SV_23orSJSGkW2uu0e?user_id={st.session_state["user_id"]}">こちら</a>をクリックしてアンケートに答えてください。',
                unsafe_allow_html=True
    )
    show_messages()
    st.stop()
else: #最初〜会話中の提示
    #条件分け（今はuser_idが奇数ならaiが相談する）
    if int(st.session_state["user_id"]) % 2 == 1:
        st.write("AIからの相談に乗りましょう。")
        if st.session_state["messages"] == []:
            st.session_state["messages"].append({"role": "ai", "content": "人とのコミュニケーションについて悩んでいるので相談に乗ってもらえますか。"})
    else:
        st.write("AIにお悩みを相談しましょう。")
        if st.session_state["messages"] == []:
            st.session_state["messages"].append({"role": "ai", "content": "何か相談事はありますか。"})
    show_messages()


with st._bottom:
    left_col, right_col = st.columns([4,1], vertical_alignment="bottom")
    left_col.text_area(
        "input_message",
        key="input",
        height=70,
        placeholder=st.session_state['placeholder'],
        label_visibility="collapsed",
    )
    right_col.button("送信", on_click=send_message, use_container_width=True)