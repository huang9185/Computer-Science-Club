document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#addComment').onclick = () => load_answer_view();
    try{
        document.querySelectorAll('.vote').forEach(button => {
            button.onclick = () => {
                fetch(`${button.dataset.id}/vote`)
                .then(response => response.json())
                .then(result => console.log(result))

                location.reload();
            }
        });
    } catch {}
});

function load_answer_view() {
    document.querySelector('.answer-view').hidden = false;
    document.querySelector('#addComment').classList.add('disabled');

    div = document.createElement('div');
    div.classList.add("p-5", "mb-4", "rounded-3", "bg-dark");
    div.innerHTML = `<div class="card-body">\n
        <label for="answerContent" class="fs-4" style="color: white;">Enter your comment: </label>\n
        <textarea class="form-control" id="answerContent" rows="3"></textarea></div>`

    button = document.createElement('a')
    button.classList.add("btn", "btn-outline-light", "btn-lg");
    button.innerHTML = "Add Comment";
    button.onclick = () => {
        fetch(`${document.querySelector('.question-view').dataset.id}/comment`, {
            method: 'POST',
            body: JSON.stringify({
                content: document.querySelector('textarea').value
            })
        })
        .then(response => response.json())
        .then(result => console.log(result))
        .then(
            location.reload()
        )
    };
    div.children[0].append(button);

    document.querySelector('.answer-view').append(div);
}