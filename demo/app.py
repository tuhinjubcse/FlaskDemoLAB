from flask import *
import os
import torch
from fairseq.models.bart import BARTModel
import os
import time
import numpy as np
import sys
from flask_ngrok import run_with_ngrok
os.environ["CUDA_VISIBLE_DEVICES"]="2"
datadir = "/home/tuhin.chakr/conceptualmetaphor"
cpdir = "/home/tuhin.chakr/conceptualmetaphor/checkpoint-conceptualmetaphor/"
bart = None


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if (request.method == "POST"):
        source = request.form["enthinput"]
        model = request.form["modelselector"]
        os.system("echo '" + source + "' > ie.source")
        np.random.seed(4)
        torch.manual_seed(4)

        count = 1
        bsz = 1
        maxb = 200
        minb = 7

        t = 0.7
        elem = []
        for val in [5]:
            with open('ie.source') as source, open('web_output.hypo', 'w') as fout:
                sline = source.readline().strip()
                slines = [sline]
                for sline in source:
                    if count % bsz == 0:
                        with torch.no_grad():
                            hypotheses_batch = bart.sample(slines, sampling=True, sampling_topk=5  ,temperature=0.7 ,lenpen=2.0, max_len_b=30, min_len=7, no_repeat_ngram_size=3)
                            #hypotheses_batch = bart.sample(slines, beams=5, lenpen=2.0, max_len_b=maxb, min_len_b=minb, no_repeat_ngram_size=3)
                        for hypothesis in hypotheses_batch:
                            fout.write(" OUTPUT : "+hypothesis.replace('\n','') + '\n')
                            fout.flush()
                        slines = []

                    slines.append(sline.strip())
                    count += 1
                if slines != []:
                    # Below line of code for beam search
                    hypotheses_batch = bart.sample(slines, sampling=True, sampling_topk=5  ,temperature=0.7 ,lenpen=2.0, max_len_b=30, min_len=7, no_repeat_ngram_size=3)
                    #hypotheses_batch = bart.sample(slines, beams=5, lenpen=2.0, max_len_b=maxb, min_len_b=minb, no_repeat_ngram_size=3)
                    for hypothesis in hypotheses_batch:
                        fout.write(" OUTPUT : "+hypothesis.replace('\n','') + '\n')
                        fout.flush()
            with open('web_output.hypo', 'r') as file:
              argument = file.read().replace('\n', '')
            literal = " INPUT : "+request.form["enthinput"]
            return render_template("index.html", metaphor=argument,literal=literal)
    return render_template("index.html",f="")
  
if __name__ == '__main__':
    bart = BARTModel.from_pretrained(cpdir,checkpoint_file='checkpoint_best.pt',data_name_or_path=datadir)
    bart.cuda()
    bart.eval()
    np.random.seed(4)
    torch.manual_seed(4)
    print("Model loaded in main")
    app.run(host='0.0.0.0')
