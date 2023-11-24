from fastapi import FastAPI, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import fitz
from fastapi.responses import FileResponse
from io import BytesIO
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


def IntersecOfSets(array):
    s1 = set(array.pop(0))
    s2 = set(array.pop(0))
    result = s1.intersection(s2)
    if len(array) > 2:
      for element in array:
        result = result.intersection(element)

    # Converts resulting set to list
    final_list = list(result)
    return final_list

@app.post('/convert_pdf')
async def convert_pdf(uploaded_pdf: UploadFile):
    print("FILE: ", uploaded_pdf.filename)
    with fitz.open(stream=BytesIO(uploaded_pdf.file.read())) as document:
        if len(document) > 2:
            # ----- FIND DUPLICATES ----- #
            all_elements = []
            for page in document:
                elements = []
                for area in page.get_text('blocks'):
                    box = fitz.Rect(area[:4])
                    if not box.is_empty:
                        elements.append(area[4])
                all_elements.append(elements)
        duplicates = IntersecOfSets(all_elements) if len(document) > 2 else [] # all the elements that are in common within all pages

        # ----- REMOVE DUPLICATES AND CLEAN TEXT ----- #
        dirty_text = []                                             # collect the "dirty" to compare the line with the previous one
        clean_text = ''                                             # put the clean text
        header_text = ''                                            # put the header text
        header_missing = True                                       # when False because we are at page 2 and collected everything
        for page in document:
            all_linetext = []                                       # use to remove duplicate lines
            for element in page.get_text('blocks'):
                header = False                                      # True when text is part of the header 
                box = fitz.Rect(element[:4])
                if not box.is_empty:
                    if element[4] in duplicates:                     # check if normal text or header text
                        header = True
                    linetext = page.get_textpage(box).extractWORDS() # get all the single words (inside the box) and their positioning 
                    if linetext not in all_linetext:
                        all_linetext.append(linetext)
                        if linetext != []:
                            dirty_text.append(linetext[0])
                            if header_missing and header: 
                                header_text += linetext[0][4] + ' '
                            elif not header:
                                if linetext[0][4] == 'Etichetta' and linetext[0][4] + ' ' + linetext[1][4] == 'Etichetta paziente':
                                    del linetext[0:2]
                                if linetext == []:
                                    continue
                                if linetext[0][4].isupper():
                                  clean_text += '\n' + linetext[0][4] + ' '
                                else:
                                  clean_text += linetext[0][4] + ' '
                        for i, line in enumerate(linetext[1:]): 
                            if line[4] == 'Etichetta' and line[4] + ' ' + linetext[i+2][4] == 'Etichetta paziente':
                                continue
                            if line[4] == 'paziente' and linetext[i][4] + ' ' + line[4] == 'Etichetta paziente':
                                continue

                            x1 = abs(dirty_text[-1][0] - line[0])
                            x2 = abs(dirty_text[-1][1] - line[1])
                            x3 = abs(dirty_text[-1][2] - line[2])
                            x4 = abs(dirty_text[-1][3] - line[3])
                            if (x1+x2+x3+x4 > 4):                      # compare the position of each word to remove duplicates
                                #check if we are on the same line, in terms of coordinates or text recognition 
                                if(dirty_text[-1][1] == line[1] and dirty_text[-1][3] == line[3]) or (dirty_text[-1][6] == line[6]):
                                    if header_missing and header: 
                                        header_text += line[4] + ' '
                                    elif not header: 
                                        clean_text += line[4] + ' '
                                else:
                                    line_break = line[6] - dirty_text[-1][6]
                                    if header_missing and header:
                                        header_text += min(2, line_break)*'\n' + line[4] + ' '
                                    elif not header:
                                        clean_text += line_break*'\n' + line[4] + ' '
                                dirty_text.append(line)

                        if header_missing and header: 
                            header_text += '\n\n' 
                        elif not header:
                            if clean_text[-1] == '.':
                                clean_text += '\n\n'
                            else:
                                clean_text += '\n'
            header_missing = False   

        # ----- ADD DUPLICATES AT THE END AND RETURN TEXT ----- #
        # clean_text += '\n\n ---------- HEADERS --------- \n'
        # clean_text += header_text

        return {'pdf_text': clean_text}
    
@app.post('/return_pdf')
async def return_pdf(uploaded_pdf: UploadFile):
    filename = './pymupdf.pdf'
    document =  fitz.open(stream=BytesIO(uploaded_pdf.file.read()), filetype='pdf')
    for page in document:
        for area in page.get_text('blocks'):
            box = fitz.Rect(area[:4])
            if not box.is_empty:
                page.add_rect_annot(box)
    
    output_pdf = BytesIO()                          
    document.save(filename)                         
    output_pdf.seek(0)                             
    return FileResponse(filename, filename='pymupdf.pdf')