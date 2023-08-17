const addChannelModal = document.querySelector('#layout-modal-add-container');
const addOpenModal = document.querySelector('.add-channels-btn')
const addcloseModal = document.querySelector('#modal-add-close-btn')

addOpenModal.addEventListener('click', () => {
    addChannelModal.showModal();
    addChannelModal.style.display='block';
    addChannelModal.style.position="float";
    addChannelModal.style.top="50%";
    addChannelModal.style.left="50%";
    addChannelModal.style.transform="translate(-50%, -50%)";
})


addcloseModal.addEventListener('click', () => {
    addChannelModal.style.display='none'
    addChannelModal.close();
})

const deleteChaneneModal = document.querySelector('#layout-modal-delete-container')
const deleteOpenModal = document.querySelector('.list-delete-channel-btn')
const deletecloseModal = document.querySelector('#modal-delete-close-btn')

deleteOpenModal.addEventListener('click', () => {
    deleteChaneneModal.showModal();
    deleteChaneneModal.style.display='block';
    deleteChaneneModal.style.position="float";
    deleteChaneneModal.style.top="50%";
    deleteChaneneModal.style.left="50%";
    deleteChaneneModal.style.transform="translate(-50%, -50%)";
})

deletecloseModal.addEventListener('click', () => {
    deleteChaneneModal.style.display='none'
    deleteChaneneModal.close();
})