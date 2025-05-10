// Get the calculator display input element from HTML
const calculatorDisplay = document.getElementById('display');

// Function to add a number or operator to the display
function appendToDisplay(value) {
    // Add the clicked button's value to the display
    calculatorDisplay.value += value;
}

// Function to clear the calculator display
function clearDisplay() {
    // Set display value to empty
    calculatorDisplay.value = '';
}

// Function to calculate the result
async function calculate() {
    try {
        // Get the math expression from display
        const mathExpression = calculatorDisplay.value;
        
        // If display is empty, don't do anything
        if (!mathExpression) return;

        // Send the expression to our Python calculator server
        const serverResponse = await fetch('http://localhost:5000/calculate', {
            // Use POST method to send data
            method: 'POST',
            // Tell server we're sending JSON data
            headers: {
                'Content-Type': 'application/json',
            },
            // Convert the expression to JSON format
            body: JSON.stringify({ 
                expression: mathExpression 
            })
        });

        // Get the calculation result from server
        const resultData = await serverResponse.json();
        
        // If calculation was successful, show the result
        if (resultData.success) {
            calculatorDisplay.value = resultData.result;
        } else {
            // If there was an error, show 'Error'
            calculatorDisplay.value = 'Error';
        }
    } catch (error) {
        // If something went wrong (like server not responding)
        console.error('Calculation error:', error);
        calculatorDisplay.value = 'Error';
    }
}
