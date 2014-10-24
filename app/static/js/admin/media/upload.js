$(function() {

    function setInputToWidthOfText(text, factor) {
        console.log("Text: " + text);
        width = calculateWordWidth(text + 1);
        $('input[name="filename"]').animate({"width":width + factor}, 50);
    };

    function setInitialPositions() {
        var extension = $('input[name="extension"]').val();
        var filename = $('input[name="filename"]').val();
        $('.extension').html(extension); //HTML contents of the object is now set to the variable 'extension'
        if (filename) {
            setInputToWidthOfText(filename + extension, 25);
        }
        /*if no file is provided, set the starting width to the placeholder + .ext exactly*/
        else {
            setInputToWidthOfText($('input[name="filename"]').attr("placeholder") + extension, 25);
        }
    };

    // setInitialPositions();

    /* let the `btn-choose` div act as the file input */
    $(".btn-choose").click(function () {
        $('input[name="image"]').trigger('click');
        return false;
    });

    /* let the `btn-upload` div act as the submit button */
    $(".btn-upload").click(function () {
        $('form.upload-form').submit();
        return false;
    });

    /* Automatically populate the filename field when a file is chosen */
    $('input[name="image"]').change(function(){
        // var fullFilename = $(this).val().split('/').pop().split('\\').pop();
        // var pieces = fullFilename.split(".");
        // var filename = pieces[0];
        // var extension = "." + pieces[1];

        // console.log("Address: " + pieces[0] + "." + pieces[1]);
        // if (pieces[1]) {
        //     $('.extension').html("." + pieces[1].toLowerCase());
        //     $('input[name="extension"]').val(pieces[1].toLowerCase());
        // }
        // insertFileName(filename);
        // appendExtension(extension);
        
        var filename = $(this).val().split('/').pop().split('\\').pop();
        var pieces = filename.split(".");
        console.log("Address: " + pieces[0] + "." + pieces[1]);
        if (pieces[1]) {
            $('.extension').html("." + pieces[1].toLowerCase());
            $('input[name="extension"]').val(pieces[1].toLowerCase());
        }
        setInputToWidthOfText(pieces[0] + "." + pieces[1], 25);
        $('input[name="filename"]').attr("placeholder",pieces[0]);
        $('input[name="filename"]').val(pieces[0]);
    });

    function insertFileName (text) {
        $('#filename').val(text)
    }

    /* Match the width of the filename field to the width of the input */
    $('input[name="filename"]').keyup(function(e) {
            /*If the user presses the delete key, delete the placeholder*/
            console.log("this.val: " + $(this).val());
            if (e.which == 8) {
                console.log("shrink: " + $(this).val() + $('.extension').html())
                setInputToWidthOfText($(this).val() + $('.extension').html(), -1);
                $('input[name="filename"]').attr("placeholder", "");

            } else {
                setInputToWidthOfText($(this).val() + $('.extension').html(), 15);
                $('input[name="filename"]').val($(this).val());
                $('input[name="extension"]').val("." + $('.extension').html());
            }
    });



    function calculateWordWidth(text, classes) {
        classes = classes || [];
        classes.push('text-width-calculation');
        var div = document.createElement('div');
        div.setAttribute('class', classes.join(' '));
        div.innerHTML = text;
        document.body.appendChild(div);
        var width = jQuery(div).outerWidth(true);
        div.parentNode.removeChild(div);
        console.log(text.length);
        return width;
    }
    
});
