document.addEventListener("DOMContentLoaded", function () {
  const authForm = document.querySelector('.auth-form');
  const topicInput = document.querySelector('#topic');
  const generatorForm = document.querySelector('.generator-form');
  const generatedNotes = document.getElementById('generated-notes');
  const copyNotesButton = document.getElementById('copy-notes');
  const downloadNotesButton = document.getElementById('download-notes');
  const regenerateNotesButton = document.getElementById('regenerate-notes');
  const clearNotesButton = document.getElementById('clear-notes');
  const clearTopicButton = document.getElementById('clear-topic');
  const outputEmpty = document.querySelector('.output-empty');

  if (authForm) {
    const firstInput = authForm.querySelector('input');
    if (firstInput) {
      firstInput.focus();
    }

    authForm.addEventListener('submit', function (event) {
      const inputs = Array.from(authForm.querySelectorAll('input[required]'));
      let hasError = false;

      inputs.forEach(function (input) {
        const trimmed = input.value.trim();
        input.value = trimmed;

        if (!trimmed) {
          hasError = true;
          input.classList.add('input-error');
        } else {
          input.classList.remove('input-error');
        }
      });

      if (hasError) {
        event.preventDefault();
        const firstError = authForm.querySelector('.input-error');
        firstError?.focus();
      }
    });
  }

  if (generatorForm) {
    generatorForm.addEventListener('submit', function (event) {
      if (!topicInput || !topicInput.value.trim()) {
        event.preventDefault();
        topicInput.value = '';
        topicInput.classList.add('input-error');
        topicInput.focus();
      }
    });
  }

  if (clearTopicButton && topicInput) {
    clearTopicButton.addEventListener('click', function () {
      topicInput.value = '';
      topicInput.classList.remove('input-error');
      topicInput.focus();
    });
  }

  function updateActionButtonsState() {
    const disabled = !generatedNotes;
    [copyNotesButton, downloadNotesButton, regenerateNotesButton, clearNotesButton].forEach(function (button) {
      if (button) {
        button.disabled = disabled;
      }
    });
  }

  function getNotesText() {
    if (!generatedNotes) {
      return '';
    }
    return Array.from(generatedNotes.querySelectorAll('.note-section')).map(function (section) {
      const title = section.querySelector('h3')?.textContent || '';
      const content = section.querySelector('p')?.textContent || '';
      return title + '\n' + content;
    }).join('\n\n');
  }

  if (copyNotesButton) {
    copyNotesButton.addEventListener('click', function () {
      const text = getNotesText();
      if (!text) {
        return;
      }
      navigator.clipboard.writeText(text).then(function () {
        copyNotesButton.textContent = 'Copied!';
        setTimeout(function () {
          copyNotesButton.textContent = 'Copy Notes';
        }, 1500);
      });
    });
  }

  if (downloadNotesButton) {
    downloadNotesButton.addEventListener('click', function () {
      const text = getNotesText();
      if (!text) {
        return;
      }
      const blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = 'study-notes.txt';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
    });
  }

  if (regenerateNotesButton && generatorForm && topicInput) {
    regenerateNotesButton.addEventListener('click', function () {
      if (!topicInput.value.trim()) {
        topicInput.classList.add('input-error');
        topicInput.focus();
        return;
      }
      generatorForm.requestSubmit();
    });
  }

  if (clearNotesButton) {
    clearNotesButton.addEventListener('click', function () {
      if (generatedNotes) {
        generatedNotes.style.display = 'none';
      }
      if (outputEmpty) {
        outputEmpty.style.display = 'block';
      }
      updateActionButtonsState();
    });
  }

  updateActionButtonsState();
});

