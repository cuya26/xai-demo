from fastapi import FastAPI, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import pdftotext
from model import generate_output

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http:\/\/131\.175\.15\.22:61111\/hbd-demo\/*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/compute_output')
async def answer_question_list(request: Request):
    request_data = await request.json()
    input_text = request_data['input_text']
    output_text = generate_output(input_text)
    return {'output_text': output_text}


@app.post('/convert_pdf')
async def convert_pdf (uploaded_pdf: UploadFile):
    print("file:", uploaded_pdf.filename)
    print(uploaded_pdf)
    print(type(uploaded_pdf))
    # with pdfplumber.open(uploaded_pdf.file) as pdf:
    #     pdf_text = ''
    #     for page in pdf.pages:
    #         ## pdf_text += page.extract_text(y_tolerance=1) + '\n'
    #         pdf_text += page.dedupe_chars().extract_text() + '\n'


    pdf = pdftotext.PDF(uploaded_pdf.file, physical=True)
    pdf_text = "\n\n\n\n\n".join(pdf)

    # pdf_text = extract_text(uploaded_pdf.file)

    return {'pdf_text': pdf_text }