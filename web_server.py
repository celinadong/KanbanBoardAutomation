import requests
import base64
from starlette.applications import Starlette
from starlette.responses import HTMLResponse, JSONResponse
from starlette.middleware.cors import CORSMiddleware
import uvicorn, aiohttp, asyncio
import github_conn

# application init
app = Starlette()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_headers=['X-Requested-With', 'Content-Type'])

subscription_key = "1de9548a300042d1a8c5bf4d1f8233b6"
vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v2.0/"
text_recognition_url = vision_base_url + "read/core/asyncBatchAnalyze"
headers = {'Ocp-Apim-Subscription-Key': subscription_key, 'Content-Type': 'application/octet-stream'}

@app.route('/')
def index(request):
    return HTMLResponse("Hello World")

@app.route('/getText', methods=['POST'])
async def get_text(request):
#     req_form = await request.form()
#     data = await (req_form['file'].read())
    
    body = await request.body()
    
    data = base64.b64decode(body)
    
    response = requests.post(
        text_recognition_url,
        headers=headers,
        data=data)
    
    response.raise_for_status()
    analysis = {}
    poll = True
    
    while (poll):
        response_final = requests.get(response.headers["Operation-Location"], headers=headers)
        analysis = response_final.json()

        if ("recognitionResults" in analysis):
            poll = False
        if ("status" in analysis and analysis['status'] == 'Failed'):
            poll = False
    
    if ("recognitionResults" in analysis):
        texts = [line["text"] for line in analysis["recognitionResults"][0]["lines"]]
        digit_index = [i for i in range(len(texts)) if texts[i].isdigit()]
        project_id = 2841426
        print(texts)
        print(digit_index)

        if len(digit_index) == 0:
            card_id = 0
            note = " ".join(texts)
                
            github_conn.update_card_by_id(project_id, card_id, note)
        else:
            column = texts[0] if not texts[0].isdigit() else None
            for i in range(len(digit_index)):
                start_index = digit_index[i]
                next_start_index = None if i == len(digit_index) - 1 else digit_index[i+1]

                card_id = texts[start_index].replace(" ", "")
                print(card_id)

                if next_start_index is None:
                    note = " ".join(texts[start_index+1:])
                else:
                    note = " ".join(texts[start_index+1:next_start_index])
                
                github_conn.update_card_by_id(project_id, card_id, note, column)

    return HTMLResponse(str(texts))

if __name__ == '__main__':
    uvicorn.run(app=app, host='0.0.0.0', port=1997)
    
