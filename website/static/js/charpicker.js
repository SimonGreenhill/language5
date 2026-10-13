// Character picker: buttons in #picker insert a character at the cursor of the
// last focused text field (including rows added later by the formset plugin).
document.addEventListener('DOMContentLoaded', function () {
    var picker = document.getElementById('picker');
    if (!picker) { return; }
    var chars = 'àáâãäåạɐæʌèéêëɛəìíîïɨịɩñṋɲŋòóôõöøðɔþùúûüụųʔřɬɤƀꝑšʷᵘ·ʋ˥˩ěʉγʰᵐḳɣḭ';
    var target = null;
    document.addEventListener('focusin', function (e) {
        if (e.target.matches('input[type=text], input:not([type]), textarea')) { target = e.target; }
    });
    Array.from(chars).forEach(function (ch) {
        var b = document.createElement('button');
        b.type = 'button';
        b.className = 'btn btn-mini charpicker-key';
        b.textContent = ch;
        b.addEventListener('mousedown', function (e) { e.preventDefault(); });  // keep focus in the field
        b.addEventListener('click', function () {
            if (!target) { return; }
            target.setRangeText(ch, target.selectionStart, target.selectionEnd, 'end');
            target.dispatchEvent(new Event('input', {bubbles: true}));
            target.focus();
        });
        picker.appendChild(b);
    });
});
