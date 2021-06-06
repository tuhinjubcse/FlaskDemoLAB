"""
Empty Flask Python page
Go to ./demo/enthymemes/app.py for reference
"""
from flask import *
from FnFrames import FnFrames

app = Flask(__name__)
counter = 0
global new_sent
new_sent=""
first_el=""
second_el=""
third_el=""
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
            print("HI")
            try:
                global target_domain
                target_domain = request.form["modelselector"]
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
                    source_domain_show="",
                    possible_sources=possible_sources,
                    dropdown_showtime="display: none;",
                    input_show="display: none;",
                    new_sent = "",
                    first_el = first_el,
                    second_el = second_el,
                    third_el = third_el,

                )
            except Exception:
                counter = 0
                print("oops")

        if counter == 2:
            print("INPUT: " + str(input))
            print("TARGET domain: " + str(target_domain))
            source_domain = possible_sources[int(request.form["options"])]
            print("SOURCE domain: " + str(source_domain))
            counter = 0

            # RUN MODEL HERE
            


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
    )


  
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
