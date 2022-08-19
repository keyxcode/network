document.addEventListener('DOMContentLoaded', () => {

    // Edit button behavior
    document.querySelectorAll('.edit-button').forEach(e => {
        e.addEventListener('click', function() {
            const post_id = this.dataset.post;
            const post_content = document.querySelector(`#post-${post_id}`);
            const edit_form = document.querySelector(`#form-${post_id}`);
            const edited_post = document.querySelector(`#edited-${post_id}`)

            if (this.innerHTML === 'Edit') {
                // UI Update
                post_content.classList.add('d-none');
                edit_form.classList.remove('d-none');
    
                this.classList.remove('btn-outline-primary');
                this.classList.add('btn-outline-danger');
                this.innerHTML = 'Cancel';

                // Submit the edited post
                edit_form.addEventListener('submit', e => {
                    e.preventDefault();

                    fetch(`edit_post/${post_id}`, {
                        method: 'PUT',
                        body: JSON.stringify({
                          content: edited_post.value
                        })
                      })
                      .then(() => {
                        post_content.innerHTML = edited_post.value;
                        post_content.classList.remove('d-none');
                        edit_form.classList.add('d-none');

                        this.classList.add('btn-outline-primary');
                        this.classList.remove('btn-outline-danger');
                        this.innerHTML = 'Edit';
                      })
                    }) 
                } else if (this.innerHTML === 'Cancel') {
                // UI Update
                post_content.classList.remove('d-none');
                edit_form.classList.add('d-none');
    
                this.classList.add('btn-outline-primary');
                this.classList.remove('btn-outline-danger');
                this.innerHTML = 'Edit';
            }
        })
    })

    // Like button behavior
    document.querySelectorAll('.like-button').forEach(e => {
        e.addEventListener('click', function() {
            if (this.innerHTML === 'Like') {
                this.innerHTML = 'Unlike';
                this.classList.remove('btn-outline-primary');
                this.classList.add('btn-primary');
            } else if (this.innerHTML === 'Unlike') {
                this.innerHTML = 'Like';
                this.classList.remove('btn-primary');
                this.classList.add('btn-outline-primary');    
            }
        })
    })
})