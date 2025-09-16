from fastapi import FastAPI,Request
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import random

app = FastAPI()
KEY = "birthday"
app.add_middleware(SessionMiddleware,secret_key=KEY)
functionSearchList = {0:"加6~10元",1:"減1~10元",2:"乘兩倍"}
functionSearchListLimit = {0:10,1:9,2:1}
cardsLen = 20
chance = 3
oriScore = 150

@app.post("/init")
async def Init(request: Request):
    functionList = [None] * cardsLen
    while None in functionList:
        r = random.randint(0,cardsLen-1)
        if functionList[r]==None:
            fr = random.randint(0,len(functionSearchList)-1)
            for l in functionSearchListLimit:
                if fr == l and functionList.count({"key":fr,"value":functionSearchList[fr]})<functionSearchListLimit[l]:
                    functionList[r] = {"key":fr,"value":functionSearchList[fr]}
    
    if "chance" in request.session:
        if request.session["chance"] !=0:
            request.session["chance"] = request.session["chance"]-1
    else:
        request.session["chance"] = chance
        
    return JSONResponse({"functionList":functionList,"oriScore":oriScore,"chance":request.session["chance"]})

#加6~10元
@app.post("/init/key/0")
async def Function_0(request:Request):
    oriScore = await request.json()
    r = random.randint(6,10)
    event_0={
                0: {"title": "路邊發財", "message": f"寶寶走一走被風一吹，地上飄來 {r} 元，爽啦～"},
                1: {"title": "收銀阿姨傻眼", "message": f"超商阿姨按錯計算機，寶寶多賺 {r} 元！"},
                2: {"title": "自拍變爆款", "message": f"寶寶隨手自拍被當成 NFT，瞬間賣掉賺 {r} 元。"},
                3: {"title": "天降紅包", "message": f"天空啪啦一聲掉下鈔票，寶寶直接撿到 {r} 元。"},
                4: {"title": "笑聲提款機", "message": f"寶寶笑太可愛，系統自動轉帳 {r} 元。"},
                5: {"title": "毛孩贊助", "message": f"狗狗覺得寶寶超讚，送她 {r} 元買肉乾。"},
                6: {"title": "可愛金幣", "message": f"寶寶可愛爆擊，直接掉出 {r} 元金幣。"},
                7: {"title": "ATM 爆走", "message": f"ATM 心情好，送寶寶 {r} 元小紅包。"},
                8: {"title": "路人誤認明星", "message": f"粉絲塞給寶寶 {r} 元求簽名。"},
                9: {"title": "打嗝有價", "message": f"寶寶一個可愛打嗝，被錄下來賣掉賺 {r} 元。"}
            }
    event = event_0[random.randint(0,len(event_0)-1)]
    title = event["title"]
    message = event["message"]
    oriScore+=r
    return JSONResponse({"oriScore":oriScore,"title":title,"message":message})

#減1~10元
@app.post("/init/key/1")
async def Function_1(request:Request):
    oriScore = await request.json()
    r = random.randint(1,10)
    event_1={
                 0: {"title": "太香了啦", "message": f"計程車司機收寶寶『香味費』，噴掉 {r} 元。"},
                 1: {"title": "飲料爆炸", "message": f"吸管一戳爆，清潔費扣 {r} 元。"},
                 2: {"title": "顏值稅", "message": f"自拍拍到雙下巴，系統扣 {r} 元當顏值稅。"},
                 3: {"title": "烤香腸陷阱", "message": f"香味太濃，寶寶忍不住買，多花 {r} 元。"},
                 4: {"title": "打噴嚏罰款", "message": f"寶寶噴嚏聲太大，被收走 {r} 元噪音費。"},
                 5: {"title": "傲嬌罰單", "message": f"忘記喊『我是最可愛』，自動扣 {r} 元。"},
                 6: {"title": "可愛稅", "message": f"政府公告：太萌要課稅，寶寶繳掉 {r} 元。"},
                 7: {"title": "踢石頭賠償", "message": f"走路踢到石頭，石頭索賠 {r} 元（？？）。"},
                 8: {"title": "智商押金", "message": f"寶寶放空太久，腦袋自己吞掉 {r} 元。"},
                 9: {"title": "爆笑罐裝費", "message": f"自販機吐氣泡水，額外收 {r} 元『爆笑費』。"}
             }
    event = event_1[random.randint(0,len(event_1)-1)]
    title = event["title"]
    message = event["message"]
    oriScore-=r
    return JSONResponse({"oriScore":oriScore,"title":title,"message":message})

#乘兩倍
@app.post("/init/key/2")
async def Function_2(request:Request):
    oriScore = await request.json()
    event_2={
                0: {"title": "宇宙廣播", "message": "全宇宙宣布：寶寶財富翻倍！理由：世界需要更多可愛。"},
                1: {"title": "生日加乘", "message": "寶寶生日快樂～獎勵直接翻倍！"},
                2: {"title": "VIP 模式", "message": "ATM 彈出：VIP 模式已開啟，寶寶金額翻倍！"},
                3: {"title": "可愛超標", "message": "系統警告：偵測到可愛過量 → 金錢翻倍。"},
                4: {"title": "紅包爆炸", "message": "紅包袋炸裂！金額直接翻倍。"},
                5: {"title": "幸運暴擊", "message": "寶寶打哈欠太萌，觸發幸運暴擊，全部獎勵翻倍！"},
                6: {"title": "放電成功", "message": "寶寶魅力電力滿格 → 荷包自動翻倍。"},
                7: {"title": "遊戲外掛", "message": "遊戲 BUG：寶寶金幣和經驗值全部翻倍！"},
                8: {"title": "生日彩蛋", "message": "今天是寶寶生日，所有財富翻倍！"},
                9: {"title": "命運最強卡", "message": "寶寶抽到傳說級卡片：下一張卡效果翻倍！"}
            }
    event = event_2[random.randint(0,len(event_2)-1)]
    title = event["title"]
    message = event["message"]
    oriScore*=2
    return JSONResponse({"oriScore":oriScore,"title":title,"message":message})

@app.post("/restore")
async def Restore(request:Request):
    request.session["chance"] = chance
    request.session.pop("chance", None)
    return JSONResponse({"message":"次數已重置"})

app.mount("/", StaticFiles(directory="Frontend", html=True))