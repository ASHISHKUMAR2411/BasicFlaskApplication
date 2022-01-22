function deleteNote(noteId) {
    'use strict';
    fetch('/delete-note', {
        method: 'POST',
        body: JSON.stringify({ noteId: noteId })
    }).then((_res) => {
        window.location.reload();
    });
}