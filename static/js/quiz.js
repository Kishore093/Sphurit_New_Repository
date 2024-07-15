document.addEventListener("DOMContentLoaded", function () {
    const csrf = Cookies.get('csrftoken');
    // document.body.style.backgroundColor =  document.querySelector("#bg-color").innerHTML;
    // document.body.style.color =  document.querySelector("#text-color").innerHTML;
    // document.querySelector("#customize-theme-btn").addEventListener('click', () => {
    //     document.querySelector("#customize-theme").style.display = "block";
    //     document.querySelector("#close-customize-theme").addEventListener('click', () => {
    //         document.querySelector("#customize-theme").style.display = "none";
    //     })
    //     window.onclick = e => {
    //         if(e.target == document.querySelector("#customize-theme")) document.querySelector("#customize-theme").style.display = "none";
    //     }
    // })
    
    // document.querySelectorAll(".txt-clr").forEach(element => {
    //     element.style.color = document.querySelector("#text-color").innerHTML;
    // })
    document.querySelectorAll(".input-quiz-title").forEach(title => {
        title.addEventListener("input", function(){
            fetch(`edit_quiz_title`, {
                method: "POST",
                headers: {'X-CSRFToken': csrf},
                body: JSON.stringify({
                    "title": this.value
                })

            })
            
            document.querySelectorAll(".input-quiz-title").forEach(ele => {
                ele.value = this.value;
            })
        })
    })
    document.querySelector("#input-quiz-description").addEventListener("input", function(){
        fetch('edit_quiz_description', {
            method: "POST",
            headers: {'X-CSRFToken': csrf},
            body: JSON.stringify({
                "description": this.value
            })
        })
    })
    document.querySelectorAll(".textarea-adjust").forEach(tx => {
        tx.style.height = "auto";
        tx.style.height = (10 + tx.scrollHeight)+"px";
        tx.addEventListener('input', e => {
            tx.style.height = "auto";
            tx.style.height = (10 + tx.scrollHeight)+"px";
        })
    })
    
    // document.querySelector("#input-bg-color").addEventListener("input", function(){
    //     document.body.style.backgroundColor = this.value;
    //     fetch('edit_background_color', {
    //         method: "POST",
    //         headers: {'X-CSRFToken': csrf},
    //         body: JSON.stringify({
    //             "bgColor": this.value
    //         })
    //     })
    // })
    // document.querySelector("#input-text-color").addEventListener("input", function(){
    //     document.querySelectorAll(".txt-clr").forEach(element => {
    //         element.style.color = this.value;
    //     })
    //     fetch('edit_text_color', {
    //         method: "POST",
    //         headers: {'X-CSRFToken': csrf},
    //         body: JSON.stringify({
    //             "textColor": this.value
    //         })
    //     })
    // })
    // document.querySelectorAll(".open-setting").forEach(ele => {
    //     ele.addEventListener('click', () => {
    //         document.querySelector("#setting").style.display = "block";
    //     })
    //     document.querySelector("#close-setting").addEventListener('click', () => {
    //         document.querySelector("#setting").style.display = "none";
    //     })
    //     window.onclick = e => {
    //         if(e.target == document.querySelector("#setting")) document.querySelector("#setting").style.display = "none";
    //     }
    // })
    // document.querySelectorAll("#send-form-btn").forEach(btn => {
    //     btn.addEventListener("click", () => {
    //         document.querySelector("#send-form").style.display = "block";
    //     })
    //     document.querySelector("#close-send-form").addEventListener("click", () => {
    //         document.querySelector("#send-form").style.display = "none";
    //     })
    //     window.onclick = e => {
    //         if(e.target == document.querySelector("#send-form")) document.querySelector("#send-form").style.display = "none";
    //     }
    // })
    // document.querySelectorAll("[copy-btn]").forEach(btn => {
    //     btn.addEventListener("click", () => {
    //         var url = document.getElementById("copy-url");
    //         navigator.clipboard.writeText(url.value);
    //         document.querySelector("#send-form").style.display = "none";
    //     })
    // })
    // document.querySelector("#setting-form").addEventListener("submit", e => {
    //     e.preventDefault();
    //     fetch('edit_setting', {
    //         method: "POST",
    //         headers: {'X-CSRFToken': csrf},
    //         body: JSON.stringify({
    //             "collect_email": document.querySelector("#collect_email").checked,
    //             "is_quiz": document.querySelector("#is_quiz").checked,
    //             "authenticated_responder": document.querySelector("#authenticated_responder").checked,
    //             "confirmation_message": document.querySelector("#comfirmation_message").value,
    //             "edit_after_submit": document.querySelector("#edit_after_submit").checked,
    //             "allow_view_score": document.querySelector("#allow_view_score").checked,
    //         })
    //     })
    //     document.querySelector("#setting").style.display = "none";
    //     if(!document.querySelector("#collect_email").checked){
    //         if(document.querySelector(".collect-email")) document.querySelector(".collect-email").parentNode.removeChild(document.querySelector(".collect-email"))
    //     }else{
    //         if(!document.querySelector(".collect-email")){
    //             let collect_email = document.createElement("div");
    //             collect_email.classList.add("collect-email")
    //             collect_email.innerHTML = `<h3 class="question-title">Email address <span class="require-star">*</span></h3>
    //             <input type="text" autoComplete="off" aria-label="Valid email address" disabled dir = "auto" class="require-email-edit"
    //             placeholder = "Valid email address" />
    //             <p class="collect-email-desc">This form is collecting email addresses. <span class="open-setting">Change settings</span></p>`
    //             document.querySelector("#form-head").appendChild(collect_email)
    //         }
    //     }
    //     if(document.querySelector("#is_quiz").checked){
    //         if(!document.querySelector("#add-score")){
    //             let is_quiz = document.createElement('a')
    //             is_quiz.setAttribute("href", "score");
    //             is_quiz.setAttribute("id", "add-score");
    //             is_quiz.innerHTML = `<img src = "/static/Icon/score.png" id="add-score" class = "form-option-icon" title = "Add score" alt = "Score icon" />`;
    //             document.querySelector(".question-options").appendChild(is_quiz)
    //         }
    //         if(!document.querySelector(".score")){
    //             let quiz_nav = document.createElement("span");
    //             quiz_nav.classList.add("col-4");
    //             quiz_nav.classList.add("navigation");
    //             quiz_nav.classList.add('score');
    //             quiz_nav.innerHTML =   `<a href = "score" class="link">Scores</a>`;
    //             [...document.querySelector(".form-navigation").children].forEach(element => {
    //                 element.classList.remove("col-6")
    //                 element.classList.add('col-4')
    //             })
    //             document.querySelector(".form-navigation").insertBefore(quiz_nav, document.querySelector(".form-navigation").childNodes[2])
    //         }
    //     }else{
    //         if(document.querySelector("#add-score")) document.querySelector("#add-score").parentNode.removeChild(document.querySelector("#add-score"))
    //         if(document.querySelector(".score")){
    //             [...document.querySelector(".form-navigation").children].forEach(element => {
    //                 element.classList.remove("col-4")
    //                 element.classList.add('col-6')
    //             })
    //             document.querySelector(".score").parentNode.removeChild(document.querySelector(".score"))
    //         }
    //     }
    // })
    // document.querySelector("#delete-form").addEventListener("submit", e => {
    //     e.preventDefault();
    //     if(window.confirm("Are you sure? This action CANNOT be undone.")){
    //         fetch('delete', {
    //             method: "DELETE",
    //             headers: {'X-CSRFToken': csrf}
    //         })
    //         .then(() => window.location = "/")
    //     }
    // })
    const editQuestion = () => {
        document.querySelectorAll(".input-question").forEach(question => {
            question.addEventListener('input', function(){
                let required;
                document.querySelectorAll('.required-checkbox').forEach(rc => {
                    if(rc.dataset.id === this.dataset.id) required = rc.checked;
                })
                fetch('edit_quiz_question', {
                    method: "POST",
                    headers: {'X-CSRFToken': csrf},
                    body: JSON.stringify({
                        id: this.dataset.id,
                        question: this.value,
                        required: required
                    })
                })
            })
        })
    }
    editQuestion();
    const editRequire = () => {
        document.querySelectorAll(".required-checkbox").forEach(checkbox => {
            checkbox.addEventListener('input', function(){
                let question;
                document.querySelectorAll('.input-question').forEach(q => {
                    if(q.dataset.id === this.dataset.id) question = q.value
                })
                fetch('edit_quiz_question', {
                    method: "POST",
                    headers: {'X-CSRFToken': csrf},
                    body: JSON.stringify({
                        id: this.dataset.id,
                        question: question,
                        required: this.checked
                    })
                })
            })
        })
    }
    editRequire()
    const editChoice = () => {
        document.querySelectorAll(".edit-choice").forEach(choice => {
            choice.addEventListener("input", function(){
                fetch('edit_quiz_choice', {
                    method: "POST",
                    headers: {'X-CSRFToken': csrf},
                    body: JSON.stringify({
                        "id": this.dataset.id,
                        "choice": this.value
                    })
                }).then(response => response.json())
                .then(result => {
                    var op = document.getElementById(`ak${result['id']}`);
                    var labels = op.getElementsByTagName('label');
                    labels[0].innerText  = result['choice'];

                });
            })
        })
    }
    editChoice()
    const removeOption = () => {
        document.querySelectorAll(".remove-option").forEach(ele => {
            ele.addEventListener("click",function(){
                fetch('remove_quiz_choice', {
                    method: "POST",
                    headers: {'X-CSRFToken': csrf},
                    body: JSON.stringify({
                        "id": this.dataset.id
                    })
                })
                .then(response => response.json())
                .then(result => {
                    var op = document.getElementById(`ak${result['id']}`);
                    var ak = document.getElementById(`option${result['id']}`);
                    if (op !== null && ak !== null) {
                        op.remove();
                        ak.remove();
                    }
                    // option length validation max 4 add
                    document.querySelectorAll(`.c-${$(this).data('filter')}`).forEach((opt, i) =>{
                        if(i+1 < 4){
                            document.getElementById(`add_option${$(this).data('filter')}`).style.display = "block";
                            // document.getElementById(`answer-key`).style.display = "none";
                        }
                    });
                })
            })
        })
    }
    removeOption()
    const addOption = () => {
        document.querySelectorAll(".add-option").forEach(question =>{
            question.addEventListener("click", function(){
                fetch("add_quiz_choice", {
                    method: "POST",
                    headers: {'X-CSRFToken': csrf},
                    body: JSON.stringify({
                        "question": this.dataset.question
                    })
                })
                .then(response => response.json())
                .then(result => {
                    let addOp = document.getElementById(`add_option${this.dataset.question}`);
                    // option class list
                    let opt_ele = document.createElement("div");
                    opt_ele.classList.add('choice');
                    opt_ele.classList.add(`c-${this.dataset.question}`);
                    opt_ele.id = `option${result["id"]}`;
                    // answer key class list
                    var answer_key = document.getElementById(`answer-key${this.dataset.question}`);
                    let ak_ele = document.createElement("div");
                    ak_ele.classList.add('form-check');
                    ak_ele.classList.add(`form-check-inline`);
                    ak_ele.id = `ak${result["id"]}`;
                    if(this.dataset.type === "multiple choice"){
                        opt_ele.innerHTML = `<input type="radio" id="${result["id"]}" disabled>
                        <label for="${result["id"]}">
                            <input type="text" value="${result["choice"]}" class="edit-choice" data-id="${result["id"]}">
                        </label>
                        <span class="remove-option" title="Remove" data-filter="${this.dataset.question}" data-id="${result["id"]}">&times;</span>`;

                        ak_ele.innerHTML = `
                            <input class="form-check-input" type="radio" name="${this.dataset.question}-answer" id="choice-${result["id"]}"
                             data-id="${this.dataset.question}" value="${result["id"]}" answer-key data-question_type="${this.dataset.type}">
                            <label for="choice-${result["id"]}">${result['choice']}</label>
                        `;
                    }
                    
                    document.querySelectorAll(`.choices${this.dataset.question}`).forEach(choices => {
                        if(choices.dataset.id === this.dataset.question){
                            choices.insertBefore(opt_ele, addOp);
                            answer_key.appendChild(ak_ele);
                            editChoice()
                            removeOption()
                            editAnswerKey()
                        }
                    });

                    // option length validation max 4 add
                    document.querySelectorAll(`.c-${this.dataset.question}`).forEach((opt, i) =>{
                        if(i+1 === 4){
                            document.getElementById(`add_option${this.dataset.question}`).style.display = "none";
                            // document.getElementById('answer-key').style.display = "block";
                        }
                    });
                })
            })
        })
    }
    addOption()
    const deleteQuestion = () => {
        document.querySelectorAll(".delete-question").forEach(question => {
            question.addEventListener("click", function(){
                fetch(`delete_quiz_question/${this.dataset.id}`, {
                    method: "DELETE",
                    headers: {'X-CSRFToken': csrf},
                })
                .then(() => {
                    document.querySelectorAll(".question").forEach(q =>{
                        if(q.dataset.id === this.dataset.id){
                            q.parentNode.removeChild(q)
                        }
                    })
                })
            })
        })
    }
    deleteQuestion()
    const changeType = () => {
        document.querySelectorAll(".input-question-type").forEach(ele => {
            ele.addEventListener('input', function(){
                let required;
                let question;
                document.querySelectorAll('.required-checkbox').forEach(rc => {
                    if(rc.dataset.id === this.dataset.id) required = rc.checked;
                })
                document.querySelectorAll('.input-question').forEach(q => {
                    if(q.dataset.id === this.dataset.id) question = q.value
                })
                fetch('edit_question', {
                    method: "POST",
                    headers: {'X-CSRFToken': csrf},
                    body: JSON.stringify({
                        id: this.dataset.id,
                        question: question,
                        question_type: this.value,
                        required: required
                    })
                })

                if(this.dataset.origin_type === "multiple choice" || this.dataset.origin_type === "checkbox" || this.dataset.origin_type === "dropdown"){
                    document.querySelectorAll(".choices").forEach(choicesElement => {
                        if(choicesElement.dataset.id === this.dataset.id){
                            if(this.value === "multiple choice" || this.value === "checkbox" || this.value === "dropdown"){
                                fetch(`get_choice/${this.dataset.id}`, {
                                    method: "GET"
                                })
                                .then(response => response.json())
                                .then(result => {
                                    let ele = document.createElement("div");
                                    ele.classList.add('choices');
                                    ele.setAttribute("data-id", result["question_id"])
                                    let choices = '';
                                    if(this.value === "multiple choice"){
                                        for(let i in result["choices"]){
                                            if(i){ choices += `<div class="choice">
                                            <input type="radio" id="${result["choices"][i].id}" disabled>
                                            <label for="${result["choices"][i].id}">
                                                <input type="text" data-id="${result["choices"][i].id}" class="edit-choice" value="${result["choices"][i].choice}">
                                            </label>
                                            <span class="remove-option" title="Remove" data-id="${result["choices"][i].id}">&times;</span></div>`}
                                        }
                                        ele.innerHTML = `<div class="choice">${choices}</div>
                                        <div class="choice">
                                            <input type = "radio" id = "add-choice" disabled />
                                            <label for = "add-choice" class="add-option" id="add-option" data-question="${result["question_id"]}"
                                            data-type = "${this.value}">Add option</label>
                                        </div>`;
                                    }else if(this.value === "checkbox"){
                                        for(let i in result["choices"]){
                                            if(i){choices += `<div class="choice">
                                            <input type="checkbox" id="${result["choices"][i].id}" disabled>
                                            <label for="${result["choices"][i].id}">
                                                <input type="text" data-id="${result["choices"][i].id}" class="edit-choice" value="${result["choices"][i].choice}">
                                            </label>
                                            <span class="remove-option" title="Remove" data-id="${result["choices"][i].id}">&times;</span></div>`}
                                        }
                                        ele.innerHTML = `<div class="choice">${choices}</div>
                                        <div class="choice">
                                            <input type = "checkbox" id = "add-choice" disabled />
                                            <label for = "add-choice" class="add-option" id="add-option" data-question="${result["question_id"]}"
                                            data-type = "${this.value}">Add option</label>
                                        </div>`;
                                    }else if(this.value === "dropdown"){
                                        for(let i in result["choices"]){
                                            if(i){choices += `<div class="choice">
                                            <label for="{{choice.id}}"><i class="bi bi-circle-fill"></i>&emsp14;</label>
                                            <label for="${result["choices"][i].id}">
                                                <input type="text" data-id="${result["choices"][i].id}" class="edit-choice" value="${result["choices"][i].choice}">
                                            </label>
                                            <span class="remove-option" title="Remove" data-id="${result["choices"][i].id}">&times;</span></div>`}
                                        }
                                        ele.innerHTML = `<div class="choice">${choices}</div>
                                        <div class="choice">
                                            <label for="{{choice.id}}"><i class="bi bi-circle-fill"></i>&emsp14;</label>
                                            <label for = "add-choice" class="add-option" id="add-option" data-question="${result["question_id"]}"
                                            data-type = "${this.value}">Add option</label>
                                        </div>`;
                                    }
                                    
                                    choicesElement.parentNode.replaceChild(ele, choicesElement);
                                    editChoice()
                                    removeOption()
                                    changeType()
                                    editQuestion()
                                    editRequire()
                                    addOption()
                                    deleteQuestion()
                                })
                            }else{
                                if(this.value === "short"){
                                    choicesElement.parentNode.removeChild(choicesElement)
                                    let ele = document.createElement("div");
                                    ele.innerHTML = `<div class="answers" data-id="${this.dataset.id}">
                                    <input type ="text" class="short-answer" disabled placeholder="Short answer text" />
                                    </div>`
                                    this.parentNode.insertBefore(ele, this.parentNode.childNodes[4])
                                }else if(this.value === "paragraph"){
                                    choicesElement.parentNode.removeChild(choicesElement)
                                    let ele = document.createElement("div");
                                    ele.innerHTML = `<div class="answers" data-id="${this.dataset.id }">
                                    <textarea class="long-answer" disabled placeholder="Long answer text" ></textarea>
                                    </div>`
                                    this.parentNode.insertBefore(ele, this.parentNode.childNodes[4])
                                }else if(this.value === "date"){
                                    choicesElement.parentNode.removeChild(choicesElement)
                                    let ele = document.createElement("div");
                                    ele.innerHTML = `<div class="answers" data-id="${this.dataset.id}">
                                    <input type ="date" class="short-answer" disabled placeholder="date" />
                                    </div>`
                                    this.parentNode.insertBefore(ele, this.parentNode.childNodes[4])
                                }else if(this.value === "time"){
                                    choicesElement.parentNode.removeChild(choicesElement)
                                    let ele = document.createElement("div");
                                    ele.innerHTML = `<div class="answers" data-id="${this.dataset.id}">
                                    <input type ="time" class="short-answer" disabled placeholder="time" />
                                    </div>`
                                    this.parentNode.insertBefore(ele, this.parentNode.childNodes[4])
                                }else if(this.value === "fileupload"){
                                    choicesElement.parentNode.removeChild(choicesElement)
                                    let ele = document.createElement("div");
                                    ele.innerHTML = `<div class="answers" data-id="${this.dataset.id}">
                                    <input type ="file" class="short-answer" disabled placeholder="file" />
                                    </div>`
                                    this.parentNode.insertBefore(ele, this.parentNode.childNodes[4])
                                }
                            }
                        }
                    })
                }else{
                    document.querySelectorAll(".question-box").forEach(question => {
                        document.querySelectorAll(".answers").forEach(answer => {
                            if(answer.dataset.id === this.dataset.id){
                                answer.parentNode.removeChild(answer)
                            }
                        })
                        if((this.value === "multiple choice" || this.value === "checkbox" || this.value === "dropdown") && question.dataset.id === this.dataset.id){
                            fetch(`get_choice/${this.dataset.id}`, {
                                method: "GET"
                            })
                            .then(response => response.json())
                            .then(result => {
                                let ele = document.createElement("div");
                                ele.classList.add('choices');
                                ele.setAttribute("data-id", result["question_id"])
                                let choices = '';
                                if(this.value === "multiple choice"){
                                    for(let i in result["choices"]){
                                        if(i){ choices += `<div class="choice">
                                        <input type="radio" id="${result["choices"][i].id}" disabled>
                                        <label for="${result["choices"][i].id}">
                                            <input type="text" data-id="${result["choices"][i].id}" class="edit-choice" value="${result["choices"][i].choice}">
                                        </label>
                                        <span class="remove-option" title="Remove" data-id="${result["choices"][i].id}">&times;</span></div>`}
                                    }
                                    ele.innerHTML = `<div class="choice">${choices}</div>
                                    <div class="choice">
                                        <input type = "radio" id = "add-choice" disabled />
                                        <label for = "add-choice" class="add-option" id="add-option" data-question="${result["question_id"]}"
                                        data-type = "${this.value}">Add option</label>
                                    </div>`;
                                }else if(this.value === "checkbox"){
                                    for(let i in result["choices"]){
                                        if(i){choices += `<div class="choice">
                                        <input type="checkbox" id="${result["choices"][i].id}" disabled>
                                        <label for="${result["choices"][i].id}">
                                            <input type="text" data-id="${result["choices"][i].id}" class="edit-choice" value="${result["choices"][i].choice}">
                                        </label>
                                        <span class="remove-option" title="Remove" data-id="${result["choices"][i].id}">&times;</span></div>`}
                                    }
                                    ele.innerHTML = `<div class="choice">${choices}</div>
                                    <div class="choice">
                                        <input type = "checkbox" id = "add-choice" disabled />
                                        <label for = "add-choice" class="add-option" id="add-option" data-question="${result["question_id"]}"
                                        data-type = "${this.value}">Add option</label>
                                    </div>`;
                                }else if(this.value === "dropdown"){
                                    for(let i in result["choices"]){
                                        if(i){choices += `<div class="choice">
                                        <label for="{{choice.id}}"><i class="bi bi-circle-fill"></i>&emsp14;</label>
                                        <label for="${result["choices"][i].id}">
                                            <input type="text" data-id="${result["choices"][i].id}" class="edit-choice" value="${result["choices"][i].choice}">
                                        </label>
                                        <span class="remove-option" title="Remove" data-id="${result["choices"][i].id}">&times;</span></div>`}
                                    }
                                    ele.innerHTML = `<div class="choice">${choices}</div>
                                    <div class="choice">
                                        <label for="{{choice.id}}"><i class="bi bi-circle-fill"></i>&emsp14;</label>
                                        <label for = "add-choice" class="add-option" id="add-option" data-question="${result["question_id"]}"
                                        data-type = "${this.value}">Add option</label>
                                    </div>`;
                                }
                                
                                question.insertBefore(ele, question.childNodes[4])
                                editChoice()
                                removeOption()
                                changeType()
                                editQuestion()
                                editRequire()
                                addOption()
                                deleteQuestion()
                            })
                        }else{
                            if(this.value === "short"){
                                let ele = document.createElement("div");
                                ele.innerHTML = `<div class="answers" data-id="${this.dataset.id}">
                                <input type ="text" class="short-answer" disabled placeholder="Short answer text" />
                                </div>`
                                this.parentNode.insertBefore(ele, this.parentNode.childNodes[4])
                            }else if(this.value === "paragraph"){
                                let ele = document.createElement("div");
                                ele.innerHTML = `<div class="answers" data-id="${this.dataset.id}">
                                <textarea class="long-answer" disabled placeholder="Long answer text" ></textarea>
                                </div>`
                                this.parentNode.insertBefore(ele, this.parentNode.childNodes[4])
                            }else if(this.value === "date"){
                                let ele = document.createElement("div");
                                ele.innerHTML = `<div class="answers" data-id="${this.dataset.id}">
                                <input type ="date" class="short-answer" disabled placeholder="date" />
                                </div>`
                                this.parentNode.insertBefore(ele, this.parentNode.childNodes[4])
                            }else if(this.value === "time"){
                                let ele = document.createElement("div");
                                ele.innerHTML = `<div class="answers" data-id="${this.dataset.id}">
                                <input type ="time" class="short-answer" disabled placeholder="time" />
                                </div>`
                                this.parentNode.insertBefore(ele, this.parentNode.childNodes[4])
                            }else if(this.value === "fileupload"){
                                let ele = document.createElement("div");
                                ele.innerHTML = `<div class="answers" data-id="${this.dataset.id}">
                                <input type ="file" class="short-answer" disabled placeholder="file" />
                                </div>`
                                this.parentNode.insertBefore(ele, this.parentNode.childNodes[4])
                            }
                        }
                    })
                }
                this.setAttribute("data-origin_type", this.value);
            })
        })
    }
    changeType()


    document.getElementById("add-question").addEventListener("click", () => {
        fetch('add_quiz_question', {
            method: "POST",
            headers: {'X-CSRFToken': csrf},
            body: JSON.stringify({})
        })
        .then(response => response.json())
        .then(result => {
            let ele = document.createElement('div');
            ele.innerHTML = result['question']

            // ele.classList.add('margin-top-bottom');
            // ele.classList.add('box');
            // ele.classList.add('question-box');
            // ele.classList.add('question');
            // ele.setAttribute("data-id", result["question"].id)
            // ele.innerHTML = `
            // <input type="text" data-id="${result["question"].id}" placeholder="Question title" class="question-title edit-on-click input-question" value="${result["question"].question}">
           
            // <div class="choices" data-id="${result["question"].id}">
            //     <div class="choice c-${result["question"].id}">
            //         <input type="radio" id="${result["choices"].id}" disabled>
            //         <label for="${result["choices"].id}">
            //             <input type="text" value="${result["choices"].choice}" class="edit-choice" data-id="${result["choices"].id}">
            //         </label>
            //         <span class="remove-option" title="Remove" data-filter="${result["question"].id}" data-id="${result["choices"].id}">&times;</span>
            //     </div>
            //     <div class="choice" id="add_option${result["question"].id}" style="display:block">
            //         <input type = "radio" id = "add-choice" disabled />
            //         <label for = "add-choice" class="add-option" id="add-option" data-question="${result["question"].id}" 
            //         data-type = "${result["question"].question_type}">Add option</label>
            //     </div>
            // </div>
            // {% if '${result['form_type']}'=='True' %}
            //     <div class="d-flex justify-content-between">
            //         <div class="answer-key" id="answer-key{{question.id}}" style="display: {% if question.choices.all.count > 3 %}block{% else %}none{% endif %};">
            //             <span>Answer Key -</span>&emsp;
            //             {% for i in question.choices.all %}
            //             <div class="form-check form-check-inline">
            //                 <input class="form-check-input" type="radio" name="{{question.id}}-answer" id="choice-{{i.id}}"
            //                  data-id="{{question.id}}" value="{{i.id}}" answer-key data-question_type = "{{question.question_type}}" {% if i.is_answer %} checked {% endif %}>
            //                 <label for="choice-{{i.id}}">{{i.choice}}</label>
            //             </div>
            //             {% endfor %}
            //         </div>
            //         <div class="question-score">
            //             <label for="score">Points</label>
            //             <input type="number" data-id="{{question.id}}" id="score" class="input-score" value="{{question.score}}">
            //         </div>
            //     </div>
            // {% endif %}
            // <div class="choice-option">
            //     <input type="checkbox" class="required-checkbox" id="${result["question"].id}" data-id="${result["question"].id}">
            //     <label for="${result["question"].id}" class="required">Required</label>
            //     <div class="float-right">
            //         <img src="/static/Icon/dustbin.png" alt="Delete question icon" class="question-option-icon delete-question" title="Delete question"
            //         data-id="${result["question"].id}">
            //     </div>
            // </div>
            // `;
            document.querySelector("#q_ctr").appendChild(ele);
            editChoice()
            removeOption()
            changeType()
            editQuestion()
            editRequire()
            addOption()
            deleteQuestion()
            editAnswerKey()
        })
    })

    // document.querySelector("#delete-form").addEventListener("submit", e => {
    //     e.preventDefault();
    //     if(window.confirm("Are you sure? This action CANNOT be undone.")){
    //         fetch('delete', {
    //             method: "DELETE",
    //             headers: {'X-CSRFToken': csrf}
    //         })
    //         .then(() => window.location = "/")
    //     }
    // })

    // document.querySelectorAll(".input-score").forEach(element => {
    //     element.addEventListener("input", function(){
    //         fetch('edit_quiz_score', {
    //             method: "POST",
    //             headers: {'X-CSRFToken': csrf},
    //             body: JSON.stringify({
    //                 question_id: this.dataset.id,
    //                 score: this.value
    //             })
    //         })
    //     })
    // })

    document.querySelectorAll(".input-score").forEach(element => {
        element.addEventListener("input", function(){
            fetch('edit_score', {
                method: "POST",
                headers: {'X-CSRFToken': csrf},
                body: JSON.stringify({
                    question_id: this.dataset.id,
                    score: this.value
                })
            })
        })
    })
    function editAnswerKey(){
        document.querySelectorAll("[answer-key]").forEach(element => {
            element.addEventListener("input", function(){
                if(this.dataset.question_type === "multiple choice"){
                    fetch('quiz_answer_key', {
                        method: "POST",
                        headers: {'X-CSRFToken': csrf},
                        body: JSON.stringify({
                            "question_id": this.dataset.id,
                            "answer_key": document.querySelector(`input[name="${this.name}"]:checked`).value
                        })
                    })
                }
            })
        })
    }
    editAnswerKey()
})

