// To be used with templates/base.html line 80
function deleteNote(noteId) {
    fetch('/delete-note', {
        method: 'POST',
        body : JSON.stringify({ noteId: noteId }),
    }).then((_res) => {
        window.location.href = "/";
    });
}