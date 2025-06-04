let feedback_element;
let new_game_button;

document.addEventListener('DOMContentLoaded', () => {
    feedback_element = document.getElementById("feedback-message");
    new_game_button = document.getElementById("new-game-button");
    new_game_button.addEventListener('click', new_game)
});

async function new_game()
{
    const response = await fetch('api/new_game')
   
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    feedback_element.innerHTML = data['message'];
}

