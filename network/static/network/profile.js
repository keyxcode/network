document.addEventListener('DOMContentLoaded', () => {

    // Follow button behavior
    document.querySelector('#follow-button').addEventListener('click', function() {
        const profile_id = this.dataset.profile;
        const current_user = document.querySelector('#user').innerHTML;

        updateFollowsBackEnd(current_user, profile_id);
        switchFollowButtonUIState(this);
    })
})

function switchFollowButtonUIState(button) {
    if (button.innerHTML === 'Follow') {
        button.innerHTML = 'Unfollow';
        button.classList.remove('btn-outline-primary');
        button.classList.add('btn-primary');
    } else {
        button.innerHTML = 'Follow';
        button.classList.add('btn-outline-primary');
        button.classList.remove('btn-primary');
    }
}

function updateFollowsBackEnd(current_user, profile_id) {
    fetch(`/api/profile/${profile_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            current_user: current_user
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
}