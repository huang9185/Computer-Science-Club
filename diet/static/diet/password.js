document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#verify').addEventListener('click', () => verify_id());

    // Default
    load_verify();
});

function load_verify() {
    document.querySelector('#verify-view').hidden = false;
    document.querySelector('#password-view').hidden = true;
}

function verify_id() {
    fetch('/diet/password', {
        method: 'POST',
        body: JSON.stringify({
            username: document.querySelector('#username').value,
            email: document.querySelector('#email').value
        })
    })
    .then(response => response.json())
    .then(result => {

        // Print result
        console.log(result);

        if (result.error) {
            alert(result.error);
        } else {
            load_password(result.id);
        }
    });
}

function load_password(user_id) {
    document.querySelector('#verify-view').hidden = true;
    document.querySelector('#password-view').hidden = false;

    document.querySelector('#confirm').onclick = () => {
        password = document.querySelector('#password').value;
        confirmation = document.querySelector('#confirmation').value;

        if (password === confirmation) {
            fetch('/diet/password', {
                method:'PUT',
                body: JSON.stringify({
                    password: password,
                    id: user_id
                })
            })
            .then(response => response.json())
            .then(result => {
                console.log(result);
                alert(result.message);
            })
        } else {
            alert('Two passwords are not the same');
        }
    }
}