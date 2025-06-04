document.addEventListener('DOMContentLoaded', () => {
    const min_num_text = document.getElementById("min-num");
    const max_num_text = document.getElementById("max-num");
    const feedback_element = document.getElementById("feedback-message");
    const attempts_element = document.getElementById("attempts-taken");
    const new_game_button = document.getElementById("new-game-button");
    const guess_input = document.getElementById("guess-input");
    const winSection = document.getElementById("win-section");
    const guess_submit_button = document.getElementById("submit-guess-button");
    const guess_form = document.getElementById('guess-form')
    const win_screen_attempts_span = document.getElementById('final-attempts')

    let winning_attempts;

    async function Setup() {
        console.log('Setup() called')
        const response = await fetch('api/game_info')
        const data = await response.json()
        min_num_text.innerHTML = data['min_num']
        max_num_text.innerHTML = data['max_num']
    }

    async function new_game(){
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

    function end_game()
    {
        console.log('end_game()');
        winSection.style.display = 'block';
        win_screen_attempts_span.innerHTML = winning_attempts
    }

    async function submit_guess(event){
        event.preventDefault()
        guess = parseInt(guess_input.value)
        console.log(guess)
        if(isNaN(guess))
        {
            feedback_element.innerHTML = 'Please enter a number for your guess!'
            console.log('Guess was NaN');
            guess_input.value = '';
            guess_input.focus();
        } else
        {
            const respose = await fetch('/api/guess',
                {
                    method: 'POST',
                    headers: {'Content-Type':'application/json'},
                    body: JSON.stringify({guess: guess})
                }
            )
            if (respose.ok){
                const msg = await respose.json()
                feedback_element.innerHTML = msg['feedback']
                attempts_element.innerHTML = msg['attempts_count']
                console.log(msg['game_over'])
                if (msg['game_over'])
                {
                    winning_attempts = msg['attempts_count'];
                    console.log('Game over confirmed')
                    end_game();
                } else
                {
                    guess_input.value = '';
                    guess_input.focus();
                }
            } else
            {
                feedback_element.innerHTML = 'Error.. Check console!'
                console.log(respose.body)
            }
        }
    }

    new_game_button.addEventListener('click', new_game);
    guess_submit_button.addEventListener('click', submit_guess);

    Setup();
    new_game();
});

