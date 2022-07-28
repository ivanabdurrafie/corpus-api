from flask import Flask, request, jsonify
from concordance import *
from wordCount import *
from concordance2 import *

app = Flask(__name__)     

@app.route('/getConc', methods=['GET'])
def getConc():
    keywordConc = request.args.get('keyword')
    keyword = keywordConc.lower()
    context = 4
    theConc = []
    for file in os.listdir():
        if file.endswith(".txt"):
            arrName.append(file)
            
            file_path = f"{directory_path}/{file}"
            listOfTokens = read_text_file(file_path)
            makeConc(keyword,listOfTokens,int(context),theConc,file)

    final = showConc(theConc)
    return jsonify(final)

@app.route('/getWordCount', methods=['GET'])
def getWord():
    file = request.args.get('file')
    file_exist = os.path.exists(file)
    if file_exist:
        arrName.append(file)
        file_path = f"{directory_path}/{file}"
        listOfTokens = read_text_file(file_path)
        listCount = countWord(listOfTokens)
        popular = mostCommon(listOfTokens)
        
    return jsonify( 
        WordFrequency = listCount,
        PopularWord = popular)

@app.route('/changeEncoding', methods=['GET'])
def changeEncoding():
    file = request.args.get('file')
    print(file)
    file_exist = os.path.exists(file)
    if file_exist:
        file_path = f"{directory_path}/{file}"
        blob = open(file_path, 'rb').read()
        detectEncoding = chardet.detect(blob)
        print(detectEncoding.get('encoding'))
        getEncoding = detectEncoding.get('encoding')
        if detectEncoding.get('encoding') != 'utf-8':
            with open(file_path, 'r',encoding=getEncoding) as f:
                raw = f.read()

            with open(file_path, 'w',encoding='utf-8') as f:
                f.write(raw)
                f.close()
    msg = 'Encoding berhasil diubah'
    return jsonify(msg)


@app.route('/getConc2', methods=['GET'])
def getConcNew():
    keywordConc = request.args.get('keyword')
    keyword = keywordConc.lower()
    year = request.args.get('tahun')
    specialchar = '"[]'
    listToken = []

    if year is not None:
        if year.find(','):
            arr = year.split(",")
            trim = [s.strip(specialchar) for s in arr]
            print(type(trim))            
        else:
            trim = year.strip(specialchar)
            print(trim)
        for file in trim:
            print(file)
            # arrName.append(file)
            file_path = f"{directory_path}/{file}"
            listOfTokens = read_text_file(file_path)

            for token in listOfTokens:
                listToken.append(token)
            # listToken.append(listOfTokens)
            
    elif year is None:
        print('year is false')
        for file in os.listdir():
            if file.endswith(".txt"):
                print(file)
                # arrName.append(file)        
                file_path = f"{directory_path}/{file}"
                listOfTokens = read_text_file(file_path)
                # print(listOfTokens)
                for token in listOfTokens:
                    listToken.append(token)

    print(listToken)
    corpus = Text(listToken)
    concordance = corpus.concordance_list(keyword)
    alist = list(concordance)    
    print(alist)
    # print(type(alist))
    return jsonify(alist)
    

app.run(debug=True)