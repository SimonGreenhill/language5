$(function () {
    $('#picker').keypad({target: $(':input:first'), 
    // layout: ['àáâãäåæçèéêë', 'ìííîïñòóôõöø', 'ðþùúûüýÿ' + $.keypad.ENTER + $.keypad.SHIFT]});
<<<<<<< local
    layout: ['àáâãäåæçèéêëəìííîïñŋòóôõöøðþùúûüʔřɬ' + $.keypad.ENTER + $.keypad.SHIFT]});
=======
    layout: ['àáâãäåạɐæʌèéêëɛəìííîïɨịɩñŋòóôõöøðɔþùúûüụųʔřɬɤƀꝑšʷᵘ·' + $.keypad.ENTER + $.keypad.SHIFT]});
>>>>>>> other
    var keypadTarget = null; 
    $(':input').focus(function() { 
    if (keypadTarget != this) { 
        keypadTarget = this; 
        $('#picker').keypad('option', {target: this}); 
    } 
   }); 
});







