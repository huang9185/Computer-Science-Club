document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#questionBtn').onclick = () => {
        // Check if question textarea is valid
        if (document.querySelector('#questionContent').value === '') {
            alert("Question content cannot be empty.");
        } else if (document.querySelector('#questionInput').value === '') {
            alert("Question title cannot be empty.")
        } else {
            // Create a question
            fetch('faq', {
                method: 'POST',
                body : JSON.stringify({
                    title: document.querySelector('#questionInput').value,
                    content: document.querySelector('#questionContent').value
                })
            })
            .then(response => response.json())
            .then(result => console.log(result))
            .then(location.reload())
        }
    }
});