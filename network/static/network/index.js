document.addEventListener("DOMContentLoaded", () => {

    document.querySelector('#view-posts').addEventListener('click', () => load_post("all"));
    try {
        document.querySelector('#compose').addEventListener('click', () => load_compose());
        document.querySelector('#btn-username').onclick = () => {
            id = document.querySelector('#btn-username').dataset.id;
            load_profile(id);
        };
        document.querySelector('#view-following').addEventListener('click', () => {
            user_id = document.querySelector('#view-following').dataset.id;
            load_post(user_id);
        });
    } catch (error) {}

    // By default, load the post
    load_post("all");
});

function load_post(postbox, page_num=1, profile=false) {

    // Set view
    document.querySelector('#compose-view').hidden = true;
    document.querySelector('#profile-view').hidden = true;
    document.querySelector('#post-view').hidden = false;

    // Check if for profile
    if (profile === true) {
        document.querySelector('#profile-view').hidden = false;
    }

    // Clear the view
    document.querySelector('#post-content').innerHTML='';
    step_links = document.querySelector('.pagination');
    step_links.innerHTML = '';

    // Get the posts
    fetch(`/posts/${postbox}?page=${page_num}`, {
        method: 'POST',
        body: JSON.stringify({
            profile: profile
        })
    })
    .then(response => response.json())
    .then(result => {

        // Print posts
        console.log(result);

        if (result.error) {
            alert(result.error);
        } else {
            posts = result[0];
            page_obj = result[1];
            likes = result[2];

            for (let i = 0; i < likes["length"]; i++) {

                // Loop for post and like
                post = posts[i];
                like = likes[i];
    
                // Create card element
                const element = document.createElement('div');
                element.classList.add("card", "text-white", "bg-dark");
                element.innerHTML = "";

                // Create card body
                const card_body = document.createElement('div');
                card_body.classList.add("card-body");
                card_body.innerHTML = `<p hidden=True>${post.id}</p>\n
                <p hidden=True>${post.poster_id}</p>\n
                <h6 class="card-subtitle text-muted">\n
                By <a href="#" class="btn btn-dark">${post.poster}</a> on ${post.time}</h6>\n
                <p>Likes: ${post.likes}</p>\n
                <p class="card-text">${post.body}</p>\n
                <textarea hidden=True>${post.body}</textarea>`;

                element.append(card_body);

                // If user posted the post
                if (page_obj.user_id === post.poster_id) {

                    // Create save button
                    const save_btn = document.createElement('button');
                    save_btn.classList.add("btn", "bg-white", "text-black");
                    save_btn.hidden = true;
                    save_btn.innerHTML = "Save";
                    save_btn.onclick = (event) => {
                        post_body = event.target.parentElement.children[0].children[5].value;
                        post_id = event.target.parentElement.children[0].children[0].innerHTML;

                        // Change post
                        fetch('/posts', {
                            method: 'POST',
                            body: JSON.stringify({
                                content: post_body,
                                change: true,
                                post_id: post_id
                            })
                        })
                        .then(response => response.json())
                        .then(result => {
                            // Print post
                            console.log(result.messege);

                            // Verify response
                            if (result.error) {
                                alert(result.error);
                            } else {}
                        });

                        // Set view for card-text, textarea, save-btn, and edit-btn
                        event.target.parentElement.children[0].children[4].hidden = false;
                        event.target.parentElement.children[0].children[4].innerHTML = post_body;
                        event.target.parentElement.children[0].children[5].hidden = true;
                        event.target.hidden = true;
                        event.target.parentElement.children[2].hidden = false;

                    }

                    element.append(save_btn);

                    // Create edit button and lsitener
                    const btn = document.createElement('button');
                    btn.classList.add("btn", "bg-white", "text-black");
                    btn.innerHTML = "Edit";
                    btn.onclick = (event) => {
                        card_text = event.target.parentElement.children[0].children[4];
                        texta = event.target.parentElement.children[0].children[5];
                        save = event.target.parentElement.children[1];

                        card_text.hidden = true;
                        texta.hidden = false;
                        save.hidden = false;
                        event.target.hidden = true;

                    }
                    element.append(btn);
                    
                }

                element.onclick = (event) => {
                    if (event.target.tagName.toLowerCase() === 'a') {
                        poster_id = parseInt(event.target.parentElement.parentElement.children[1].innerHTML);
                        load_profile(poster_id);
                    }
                }

                // Create like button
                const like_btn = document.createElement('button');
                like_btn.classList.add("btn", "bg-white", "text-black");
                like_btn.innerHTML = like;
                like_btn.onclick = (event) => {
                    // Change or create like model with get method
                    post_id = event.target.parentElement.children[0].children[0].innerHTML;
                    fetch(`/like/${post_id}`)
                    .then(response => response.json())
                    .then(result => {
                        console.log(result);

                        // Change innerHTML
                        if (like_btn.innerHTML === "Like") {
                            like_btn.innerHTML = "Unlike";
                        } else {
                            like_btn.innerHTML = "Like";
                        }

                        // Update the like number
                        event.target.parentElement.children[0].children[3].innerHTML = `Likes: ${result["post_like"]}`;
                    });
                }

                element.append(like_btn);
    
                // Apply element
                document.querySelector('#post-content').append(element);
            }

            // Fill in pagination
            if (page_obj.has_previous) {
                const element = document.createElement('li');
                element.classList.add("page-item");
                element.innerHTML = `<a class="page-link" href="#">Previous</a>`;
                element.onclick = () => load_post(postbox, page_obj.previous, profile);
                step_links.append(element);
            }

            // Fill in the middle
            for (let i = 1; i <= page_obj.num_pages; i++) {
                const element = document.createElement('li');
                element.classList.add("page-item");
                element.innerHTML = `<a class="page-link" href="#">${i}</a>`;
                element.onclick = () => load_post(postbox, i, profile);
                step_links.append(element);
            }

            if (page_obj.has_next) {
                const element = document.createElement('li');
                element.classList.add("page-item");
                element.innerHTML = `<a class="page-link" href="#">Next</a>`;
                element.onclick = () => load_post(postbox, page_obj.nex, profile);
                step_links.append(element);
            }
        }

        
    });
    
}

function load_profile(poster_id) {

    // Set view
    document.querySelector('#compose-view').hidden = true;
    document.querySelector('#profile-view').hidden = false;
    document.querySelector('#post-view').hidden = false;

    fetch(`/users/${poster_id}`)
    .then(response => response.json())
    .then(result => {
        console.log(result);

        // Fill in profile view
        data = result;
        document.querySelector('#username').innerHTML = data.username;
        document.querySelector('#view-followers').innerHTML = data.followers;
        document.querySelector('#following-label').innerHTML = `Following(${data.followings_num})`;

        // If user is not poster
        pf_follow = document.querySelector("#profile-follow");
        if (data.user_id != "NONE" && data.user_id != poster_id) {
            pf_follow.hidden = false;
            pf_follow.innerHTML = data.follow;
            pf_follow.dataset.id = poster_id;
        } else {
            pf_follow.hidden = true;
        }

        if (data.followings != "NONE") {
            data.followings.forEach(following => {
                const element = document.createElement('div');
                element.classList.add("row", "text-white", "bg-info");
                // If user is poster
                if (data.user_id == poster_id) {
                    element.innerHTML = `<div class="col-11">${following.influencer_name}</div>\n
                            <div class="col">\n
                            <a href="#" class="btn-unfollow" data-id="${following.influencer_id}">Unfollow</a></div>`;

                } else {
                    element.innerHTML = `<div class="col-11">${following.influencer_name}</div>`;
                }

                document.querySelector('#following-view').append(element);
            });
        } else {
            document.querySelector('#following-view').innerHTML = "<p>No followings</p>";
        }

        // Load the posts portion
        load_post(poster_id, 1, true);

    });
}

function load_compose() {

    // Set view
    document.querySelector('#post-view').hidden = true;
    document.querySelector('#profile-view').hidden = true;
    document.querySelector('#compose-view').hidden = false;

    // Clear the post form
    document.querySelector('#form-body-input').value = '';
    document.querySelector('#form').onsubmit = () => {
        body = document.querySelector('#form-body-input').value;
        // Send post
        fetch('/posts', {
            method: 'POST',
            body: JSON.stringify({
                content: body
            })
        })
        .then(response => response.json())
        .then(result => {
            // Print post
            console.log(result.messege);

            // Verify response
            if (result.error) {
                alert(result.error);
            } else {
                // Reload the post
                load_post("all");
            }
        });
    }

}