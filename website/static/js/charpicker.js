$(function () {
    $('#picker').keypad({target: $(':input:first'), 
    // layout: ['àáâãäåæçèéêë', 'ìííîïñòóôõöø', 'ðþùúûüýÿ' + $.keypad.ENTER + $.keypad.SHIFT]});
    layout: ['àáâãäåạɐæʌèéêëɛəìííîïɨịɩñṋɲŋòóôõöøðɔþùúûüụųʔřɬɤƀꝑšʷᵘ·ðʋ˥˩ěʉγʰᵐḳɣḭ' + $.keypad.ENTER + $.keypad.SHIFT]});
    var keypadTarget = null; 
    $(':input').focus(function() { 
    if (keypadTarget != this) { 
        keypadTarget = this; 
        $('#picker').keypad('option', {target: this}); 
    } 
   }); 
});
