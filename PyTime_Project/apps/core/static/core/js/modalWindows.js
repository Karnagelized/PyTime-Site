const authForLike = document.getElementById('authForLike')
if (authForLike) {
  authForLike.addEventListener('show.bs.modal', event => {
    const button = event.relatedTarget
    const recipient = button.getAttribute('data-bs-whatever')

    // Update the modal's content.
    const modalTitle = authForLike.querySelector('.modal-title')
    const modalBodyInput = authForLike.querySelector('.modal-body input')

    modalTitle.textContent = `New message to ${recipient}`
    modalBodyInput.value = recipient
  })
}

const authForComment = document.getElementById('authForComment')
if (authForComment) {
  authForComment.addEventListener('show.bs.modal', event => {
    const button = event.relatedTarget
    const recipient = button.getAttribute('data-bs-whatever')

    // Update the modal's content.
    const modalTitle = authForComment.querySelector('.modal-title')
    const modalBodyInput = authForComment.querySelector('.modal-body input')

    modalTitle.textContent = `New message to ${recipient}`
    modalBodyInput.value = recipient
  })
}

const changeAvatarProfile = document.getElementById('changeAvatarProfile')
if (changeAvatarProfile) {
  changeAvatarProfile.addEventListener('show.bs.modal', event => {
    const button = event.relatedTarget
    const recipient = button.getAttribute('data-bs-whatever')

    // Update the modal's content.
    const modalTitle = changeAvatarProfile.querySelector('.modal-title')
    const modalBodyInput = changeAvatarProfile.querySelector('.modal-body input')

    modalTitle.textContent = `New message to ${recipient}`
    modalBodyInput.value = recipient
  })
}
