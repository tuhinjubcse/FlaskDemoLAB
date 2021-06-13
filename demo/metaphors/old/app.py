"""
Empty Flask Python page
Go to ./demo/enthymemes/app.py for reference
"""
from flask import *
from FnFrames import FnFrames

app = Flask(__name__)
counter = 0
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
            focus_word = input.split()[focus_word_index]
            new_focus_word = "<b>" + focus_word + "</b>"
            new_sent = input.replace(focus_word,new_focus_word)
            print("NEW SENT: " + str(new_sent))
            print(list(possible_targets.keys()))
            options = possible_targets[list(possible_targets.keys())[0]]
            counter = counter + 1
            return render_template(
                "index.html", 
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
            )
        if counter == 1:
            print("HI")
            try:
                target_domain = request.form["modelselector"]
                possible_sources = fn.get_possible_source_frames(target_domain)

                print(target_domain)
                return render_template(
                    "index.html", 
                    options=options, 
                    input=input, 
                    show_domains="display: none;",
                    dropdown_show="",
                    continue_show="display: none;",
                    gen_button="",
                    target_selection_show = "",
                    target_domain_selection=target_domain,
                    source_domain_show="",
                    possible_sources=possible_sources,
                    dropdown_showtime="display: none;",

                )
            except Exception:
                counter = 0
                print("oops")


    
    # if button is pressed
    return render_template(
        "index.html", 
        options=options,
        show_domains="", 
        dropdown_show="display: none;",
        continue_show="display: none;",
        gen_button="display: none;",
        target_selection_show = "display: none;",
        source_domain_show="display: none;",
        possible_sources=[],
    )


  
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
