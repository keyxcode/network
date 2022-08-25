document.addEventListener('DOMContentLoaded', () => {

    // Edit post buttons behavior
    document.querySelectorAll('.edit-button').forEach(e => {
        e.addEventListener('click', function() {
            if (this.innerHTML === 'Edit') {
                showHideEditArea(this, true);
                
                const post_id = this.dataset.post;
                const edited_post = document.querySelector(`#edited-${post_id}`)
                const edit_form = document.querySelector(`#form-${post_id}`);

                edit_form.addEventListener('submit', e => {
                    e.preventDefault();

                    fetch(`/api/post/${post_id}`, {
                        method: 'PUT',
                        body: JSON.stringify({
                          content: edited_post.value
                        })
                      })
                      .then(() => {
                        showHideEditArea(this, false);
                        document.querySelector(`#post-${post_id}`).innerHTML = edited_post.value;
                      })
                    }) 
                } else if (this.innerHTML === 'Cancel') {
                showHideEditArea(this, false)
            }
        })
    })

    // Like button behavior
    document.querySelectorAll('.like-button').forEach(e => {
        e.addEventListener('click', function() {
            toggleLikeButtonUI(this);

            const post_id = this.dataset.post;
            const user = document.querySelector('#user').innerHTML
            fetch(`/api/post/${post_id}`, {
                method: 'PUT',
                body: JSON.stringify({
                    user: user
                })
            })
            .then(() => {
                fetch(`/api/post/${post_id}`)
                .then(response => response.json())
                .then(result => {
                     let likeCount = result['likers'].length;
                     document.querySelector(`#like-count-${post_id}`).innerHTML = likeCount;
                })
            })
        })
    })

    // Post divs on hover behavior
    document.querySelectorAll('.hover-box').forEach(e => {
        e.addEventListener('mouseover', function() {
            this.classList.add('shadow-sm')
        })
        e.addEventListener('mouseout', function() {
            this.classList.remove('shadow-sm')
        })
    })
})

function showHideEditArea(editButton, isShowingEditArea) {
    const post_id = editButton.dataset.post;
    const post_content = document.querySelector(`#post-${post_id}`);
    const edit_form = document.querySelector(`#form-${post_id}`);

    if (isShowingEditArea) {
        console.log('hi')
        post_content.classList.add('d-none');
        edit_form.classList.remove('d-none');

        editButton.classList.remove('btn-outline-primary');
        editButton.classList.add('btn-outline-danger');
        editButton.innerHTML = 'Cancel';
    } else {
        post_content.classList.remove('d-none');
        edit_form.classList.add('d-none');

        editButton.classList.add('btn-outline-primary');
        editButton.classList.remove('btn-outline-danger');
        editButton.innerHTML = 'Edit';
    }
}

function toggleLikeButtonUI(likeButton) {
    if (likeButton.innerHTML === 'Like') {
        likeButton.innerHTML = 'Unlike';
        likeButton.classList.remove('btn-outline-primary');
        likeButton.classList.add('btn-primary');
    } else { 
        likeButton.innerHTML = 'Like';
        likeButton.classList.remove('btn-primary');
        likeButton.classList.add('btn-outline-primary');
    }  
}