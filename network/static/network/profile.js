document.addEventListener('DOMContentLoaded', () => {

    // Follow button behavior
    document.querySelector('#follow-button').addEventListener('click', function() {
        const profile_id = this.dataset.profile;
        const follower = document.querySelector('#user').innerHTML;
    
        if (this.innerHTML === 'Follow') {
            this.innerHTML = 'Unfollow';
            this.classList.remove('btn-outline-primary');
            this.classList.add('btn-primary');
        } else {
            this.innerHTML = 'Follow';
            this.classList.add('btn-outline-primary');
            this.classList.remove('btn-primary');
        }

        fetch(`/api/profile/${profile_id}`, {
            method: 'PUT',
            body: JSON.stringify({
                follower: follower
            })
        })
        .then(() => {
            fetch(`/api/profile/${profile_id}`)
            .then(response => response.json())
            .then(result => {
                const followersCount = result['followers'].length;
                document.querySelector('#followers-count').innerHTML = followersCount;
            })
        })

    })
})