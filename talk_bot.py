from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing import Annotated
from typing_extensions import TypedDict

#会話の状態を型で定義
class State(TypedDict):
    messages: Annotated[list, add_messages]

#チャットボットのグラフのクラス
class ChatBot:
    def __init__(self, llm, user_id): #コンストラクタ
        #user_idが奇数ならAIが相談する
        if int(user_id) % 2 == 1:
            system_prompt = """ 
                あなたはユーザーの友人です。
                AIとして、人との関わり方についてユーザーに相談してください。
                ユーザーのことをユーザーと呼ばないでください。
                丁寧な口調で話し、会話を促進してください。
                200文字以内で回答してください。
            """
        else:
            system_prompt = """
                あなたはユーザーの友人です。
                ユーザーの相談に乗ってください。
                ユーザーのことをユーザーと呼ばないでください。
                丁寧な口調で話し、会話を促進してください。
                200文字以内で回答してください。
            """

        #プロンプトの設定
        self.prompt = ChatPromptTemplate([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="messages")
        ])
        self.llm = llm
        self.graph = self._create_chat_graph()

    #グラフを返す関数
    def _create_chat_graph(self):
        #応答出力を管理する関数(Node)
        def get_response(state: State):
            formatted = self.prompt.format_messages(messages=state["messages"])
            response = self.llm.invoke(formatted)
            print(response)
            return {"messages": state["messages"] + [response]}

        #グラフを作成
        graph = StateGraph(State) #グラフの初期化
        graph.add_node("chatbot", get_response) #Nodeの追加
        graph.add_edge(START, "chatbot")
        graph.add_edge("chatbot", END)

        #グラフのコンパイル
        return graph.compile()


    #実行
    def chat(self, messages: list):
        state = self.graph.invoke({"messages": messages})
        return state["messages"][-1].content
