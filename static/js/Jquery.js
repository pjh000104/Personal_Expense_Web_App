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
    // Show next step
    $('.next').click(function() {
        var currentStep = $(this).closest('.step');
        var input = currentStep.find('input')[0];

        // Check if the current input is valid
        if (input.checkValidity()) {
            currentStep.removeClass('active');
            currentStep.next('.step').addClass('active');
            currentStep.next('.step').find('input').focus();
        } else {
            input.reportValidity(); // Show validation message if input is invalid
        }
    });

    // Show previous step
    $('.prev').click(function() {
        var currentStep = $(this).closest('.step');
        currentStep.removeClass('active');
        currentStep.prev('.step').addClass('active');
    });

    // Handle form submission
    // $('#multiStepForm').submit(function(event) {
    //     event.preventDefault(); // Prevent default form submission

    //     // Show notification
    //     $('#notification').fadeIn().delay(800).fadeOut(); // Show for 2 seconds

    //     // Redirect to the CheckBalance.html page after a delay
    //     setTimeout(function() {
    //         window.location.href = './CheckBalance.html';
    //     }, 800); // Redirect after 2 seconds
    // });

// Function to validate positive input
function validatePositiveInput(input) {
    if (input.value < 0) {
        input.setCustomValidity("Please enter a Valid number.");
    } else {
        input.setCustomValidity("");
    }
}
$('input').on('keypress', function(event) {
    if (event.which === 13) { // 13 is the Enter key
        event.preventDefault(); // Prevent default form submission
        var currentStep = $(this).closest('.step');
        var isLastStep = currentStep.is('#step8'); // Check if it's the last step

        if (isLastStep) {
            // Submit the form if on the last step
            $('#multiStepForm').submit();
        } else {
            // Trigger click on the next button if not on the last step
            currentStep.find('.next').click();
        }
    }
});
   // Focus on the first input of the first step
    $('#step1 input').focus();
     
    // reset website 
    document.getElementByClass('reset').addEventListener('click', function() {
        // Clear all input fields and textarea
        document.getElementById('multiStepForm').reset();
    });

});