document.addEventListener('DOMContentLoaded', () => {

    document.querySelectorAll('.edit-button').forEach(e => {
        e.addEventListener('click', function() {
            console.log(this.dataset.post);
        })
    })
})