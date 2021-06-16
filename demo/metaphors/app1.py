"""
Empty Flask Python page
Go to ./demo/enthymemes/app.py for reference
"""
import torch
from fairseq.models.bart import BARTModel
import os
import time
import numpy as np
from flask import *
from FnFrames import FnFrames
os.environ["CUDA_VISIBLE_DEVICES"]="3"
datadir = "/home/tuhin.chakr/conceptualmetaphor"
cpdir = "/home/tuhin.chakr/conceptualmetaphor/checkpoint-conceptualmetaphor/"
bart = None


app = Flask(__name__)
counter = 0
global new_sent
new_sent=""
first_el=""
second_el=""
third_el=""
focus_word_index = -1
@app.route("/", methods=["GET", "POST"])
def show_domains():
    global counter

    fn = FnFrames()
    options = []
    
    if request.method == 'POST':
        if counter == 0:
            global input
            input = request.form["enthinput"]
            possible_targets_frames_output = fn.get_possible_target_frames(input)
            possible_targets = possible_targets_frames_output[0]
            focus_word_index = possible_targets_frames_output[1]
            print("INDEX: " + str(focus_word_index))

            # ONLY WORKS IS FOCUS WORD IS IN MIDDLE OF SENTENCE
            global focus_word
            focus_word = input.split()[focus_word_index]
            sent_split_focus = input.split(focus_word)
            print(sent_split_focus)
            global first_el
            first_el = sent_split_focus[0]
            global second_el
            second_el = focus_word
            global third_el
            third_el = sent_split_focus[1]
            new_focus_word = "<b>" + focus_word + "</b>"
            new_sent = input.replace(focus_word,new_focus_word)
            
            print("NEW SENT: " + str(new_sent))
            print(list(possible_targets.keys()))
            options = possible_targets[list(possible_targets.keys())[0]]
            counter = counter + 1
            return render_template(
                "index_final_tokens.html", 
                options=options, 
                input=input, 
                show_domains="display: none;",
                dropdown_show="",
                continue_show="",
                target_selection_show = "display: none;",
                gen_button="display: none;",
                source_domain_show="display: none;",
                possible_sources=[],
                dropdown_showtime="",
                input_show="display: none;",
                new_sent = new_sent,
                first_el = first_el,
                second_el = second_el,
                third_el = third_el,
            )
        if counter == 1:
            try:
                global target_domain
                target_domain = request.form["modelselector"]
                url,definition = fn.getMetadata(str(target_domain).lower().capitalize()) 
                print(url,definition)
                global possible_sources
                possible_sources = fn.get_possible_source_frames(target_domain)

                counter = counter + 1
                return render_template(
                    "index_final_tokens.html", 
                    options=options, 
                    input=input, 
                    show_domains="display: none;",
                    dropdown_show="display: none;",
                    continue_show="display: none;",
                    gen_button="",
                    target_selection_show = "",
                    target_domain_selection=target_domain,
                    target_domain_url=url,
                    target_domain_definition=definition,
                    source_domain_show="",
                    possible_sources=possible_sources,
                    dropdown_showtime="display: none;",
                    input_show="display: none;",
                    new_sent = "",
                    first_el = first_el,
                    second_el = second_el,
                    third_el = third_el,
                    show_metaphor="display:none;"
                )
            except Exception:
                counter = 0
                print("oops")

        if counter == 2:
            print("INPUT: " + str(input))
            print("TARGET domain: " + str(target_domain))
            if request.form["other"]=='':
                source_domain = possible_sources[int(request.form["options"])]
            else:
                source_domain = str(request.form["other"]).upper()
            print("SOURCE domain: " + str(source_domain))
            print("Focus word is",focus_word)
            replinp = str(input).replace(focus_word, '<V> '+focus_word+' : '+str(target_domain)+' <V>')
            modelinp = str(source_domain) + ' <EOT> '+replinp
            slines = [modelinp]
            with torch.no_grad():
                hypotheses_batch = bart.sample(slines, sampling=True, sampling_topk=5  ,temperature=0.7 ,lenpen=2.0, max_len_b=30, min_len=7, no_repeat_ngram_size=3)
            counter = 0
            metaphoricop = hypotheses_batch[0]
            return render_template(
                "index_final_tokens.html", 
                options=options,
                show_domains="", 
                dropdown_show="display: none;",
                continue_show="display: none;",
                gen_button="display: none;",
                target_selection_show = "display: none;",
                source_domain_show="display: none;",
                possible_sources=[],
                input_show="",
                new_sent = "",
                first_el = "",
                second_el = "",
                third_el = "",
                show_metaphor="",
                metaphoricop=metaphoricop
            )
            


    # default homepage view
    return render_template(
        "index_final_tokens.html", 
        options=options,
        show_domains="", 
        dropdown_show="display: none;",
        continue_show="display: none;",
        gen_button="display: none;",
        target_selection_show = "display: none;",
        source_domain_show="display: none;",
        possible_sources=[],
        input_show="",
        new_sent = "",
        first_el = "",
        second_el = "",
        third_el = "",
        show_metaphor="display:none;"
    )


  
if __name__ == '__main__':
    bart = BARTModel.from_pretrained(cpdir,checkpoint_file='checkpoint_best.pt',data_name_or_path=datadir)
    bart.cuda()
    bart.eval()
    np.random.seed(4)
    torch.manual_seed(4)
    app.run(host='0.0.0.0', debug=True)
