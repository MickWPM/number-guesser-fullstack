let feedback_element;
let attempts_element;
let new_game_button;
let guess_input;
let winSection;

document.addEventListener('DOMContentLoaded', () => {
    feedback_element = document.getElementById("feedback-message");
    attempts_element = document.getElementById("attempts-taken");
    new_game_button = document.getElementById("new-game-button");
    guess_input = document.getElementById("guess-input");
    winSection = document.getElementById("win-section");

    new_game_button.addEventListener('click', new_game)

    new_game()
});

async function new_game()
{
    const response = await fetch('api/new_game')
   
    if (!response.ok) {
      throw new Error('HTTP error! status: ${response.status}');
    }

    const data = await response.json();
    feedback_element.innerHTML = data['message'];
    attempts_element.innerHTML = '0'
    guess_input.value = ''
    winSection.style.display = 'none';

    console.log('New game called. Setup complete')
}

