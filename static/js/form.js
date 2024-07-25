document.addEventListener("DOMContentLoaded", function () {
    const csrf = Cookies.get('csrftoken');
    
    document.querySelectorAll(".input-form-title").forEach(title => {
        title.addEventListener("input", function(){
            fetch(`edit_title`, {
                method: "POST",
                headers: {'X-CSRFToken': csrf},
                body: JSON.stringify({
                    "title": this.value
                })

            })
            
            document.querySelectorAll(".input-form-title").forEach(ele => {
                ele.value = this.value;
            })
        })
    })
    document.querySelector("#input-form-description").addEventListener("input", function(){
        fetch('edit_description', {
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
    
    
    const editQuestion = () => {
        document.querySelectorAll(".input-question").forEach(question => {
            question.addEventListener('input', function(){
                let question_type;
                let required;
                document.querySelectorAll(".input-question-type").forEach(qp => {
                    if(qp.dataset.id === this.dataset.id) question_type = qp.value
                })
                document.querySelectorAll('.required-checkbox').forEach(rc => {
                    if(rc.dataset.id === this.dataset.id) required = rc.checked;
                })
                fetch('edit_question', {
                    method: "POST",
                    headers: {'X-CSRFToken': csrf},
                    body: JSON.stringify({
                        id: this.dataset.id,
                        question: this.value,
                        question_type: question_type,
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
                let question_type;
                document.querySelectorAll(".input-question-type").forEach(qp => {
                    if(qp.dataset.id === this.dataset.id) question_type = qp.value
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
                        question_type: question_type,
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
                fetch('edit_choice', {
                    method: "POST",
                    headers: {'X-CSRFToken': csrf},
                    body: JSON.stringify({
                        "id": this.dataset.id,
                        "choice": this.value
                    })
                })
            })
        })
    }
    editChoice()
    const removeOption = () => {
        document.querySelectorAll(".remove-option").forEach(ele => {
            ele.addEventListener("click",function(){
                fetch('remove_choice', {
                    method: "POST",
                    headers: {'X-CSRFToken': csrf},
                    body: JSON.stringify({
                        "id": this.dataset.id
                    })
                })
                .then(() => {
                    this.parentNode.parentNode.removeChild(this.parentNode)
                })
            })
        })
    }
    removeOption()
    const addOption = () => {
        document.querySelectorAll(".add-option").forEach(question =>{
            question.addEventListener("click", function(){
                fetch("add_choice", {
                    method: "POST",
                    headers: {'X-CSRFToken': csrf},
                    body: JSON.stringify({
                        "question": this.dataset.question
                    })
                })
                .then(response => response.json())
                .then(result => {
                    let element = document.createElement("div");
                    element.classList.add('choice');
                    if(this.dataset.type === "multiple choice"){
                        element.innerHTML = `<input type="radio" id="${result["id"]}" disabled>
                        <label for="${result["id"]}">
                            <input type="text" value="${result["choice"]}" class="edit-choice" data-id="${result["id"]}">
                        </label>
                        <span class="remove-option" title = "Remove" data-id="${result["id"]}">&times;</span>`;
                    }else if(this.dataset.type === "checkbox"){
                        element.innerHTML = `<input type="checkbox" id="${result["id"]}" disabled>
                        <label for="${result["id"]}">
                            <input type="text" value="${result["choice"]}" class="edit-choice" data-id="${result["id"]}">
                        </label>
                        <span class="remove-option" title = "Remove" data-id="${result["id"]}">&times;</span>`;
                    }else if(this.dataset.type === "dropdown"){
                        element.innerHTML = `
                        <label for="${result["id"]}"><i class="bi bi-circle-fill"></i>&emsp14;</label>
                        <label for="${result["id"]}">
                            <input type="text" value="${result["choice"]}" class="edit-choice" data-id="${result["id"]}">
                        </label>
                        <span class="remove-option" title = "Remove" data-id="${result["id"]}">&times;</span>`;
                    }
                    document.querySelectorAll(".choices").forEach(choices => {
                        if(choices.dataset.id === this.dataset.question){
                            choices.insertBefore(element, choices.childNodes[choices.childNodes.length -2]);
                            editChoice()
                            removeOption()
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
                fetch(`delete_question/${this.dataset.id}`, {
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
        fetch('add_question', {
            method: "POST",
            headers: {'X-CSRFToken': csrf},
            body: JSON.stringify({})
        })
        .then(response => response.json())
        .then(result => {
            let ele = document.createElement('div')
            ele.classList.add('margin-top-bottom');
            ele.classList.add('box');
            ele.classList.add('question-box');
            ele.classList.add('question');
            ele.setAttribute("data-id", result["question"].id)
            ele.innerHTML = `
            <input type="text" data-id="${result["question"].id}" class="question-title edit-on-click input-question" value="${result["question"].question}">
            <select class="question-type-select input-question-type" data-id="${result["question"].id}" data-origin_type = "${result["question"].question_type}">
                <option value="short">Short answer</option>
                <option value="paragraph">Paragraph</option>
                <option value="multiple choice" selected>Multiple choice</option>
                <option value="checkbox">Checkbox</option>
                <option value="fileupload">File Upload</option>
                <option value="dropdown">Dropdown</option>
                <option value="date">Date</option>
                <option value="time">Time</option>
            </select>
            <div class="choices" data-id="${result["question"].id}">
                <div class="choice">
                    <input type="radio" id="${result["choices"].id}" disabled>
                    <label for="${result["choices"].id}">
                        <input type="text" value="${result["choices"].choice}" class="edit-choice" data-id="${result["choices"].id}">
                    </label>
                    <span class="remove-option" title = "Remove" data-id="${result["choices"].id}">&times;</span>
                </div>
                <div class="choice">
                    <input type = "radio" id = "add-choice" disabled />
                    <label for = "add-choice" class="add-option" id="add-option" data-question="${result["question"].id}" 
                    data-type = "${result["question"].question_type}">Add option</label>
                </div>
            </div>
            <div class="choice-option">
                <input type="checkbox" class="required-checkbox" id="${result["question"].id}" data-id="${result["question"].id}">
                <label for="${result["question"].id}" class="required">Required</label>
                <div class="float-right">
                    <img src="/static/Icon/dustbin.png" alt="Delete question icon" class="question-option-icon delete-question" title="Delete question"
                    data-id="${result["question"].id}">
                </div>
            </div>
            `;
            document.querySelector("#q_ctr").appendChild(ele);
            editChoice()
            removeOption()
            changeType()
            editQuestion()
            editRequire()
            addOption()
            deleteQuestion()
        })
    })
})

