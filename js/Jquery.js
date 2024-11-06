$(document).ready(function() {
    // move the active calss from nav to another //
    $(".nav-item").click(function(){ 
        $('.nav-item').find('.nav-link').removeClass('active')
        $(this).find('.nav-link').addClass('active')
    })
    // Show the button when the "Next Step" button is clicked
    $('#Step').on('click', function() {
        $('.step-active').removeClass('hidden'); // Remove the hidden class to show the button
    });
    
});
    