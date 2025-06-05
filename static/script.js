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
    const submit_score_button = document.getElementById('submit-score-button')
    const player_name = document.getElementById('playerName')
    const leaderboard_list = document.getElementById('leaderboard-list')

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

    async function submit_high_score(){
        event.preventDefault()
        console.log('Submitting high score')
        let playerName = document.querySelector("input[name='playerName']").value;
        console.log(playerName)
        const respose = await fetch('/api/leaderboard',
            {
                method: 'POST',
                headers: {'Content-Type':'application/json'},
                body: JSON.stringify({'name': playerName, 'score':winning_attempts})
            });
            
        if (respose.ok){
            const msg = await respose.json()
            feedback_element.innerHTML = 'High score submitted!'
            console.log('High score submitted')
            //REFRESH LEADERBOARD
            update_high_scores()
            new_game()
        } else
        {
            feedback_element.innerHTML = 'Error.. Check console!'
            console.log(respose.body)
        }
    }

    async function update_high_scores()
    {
        console.log('Updating high scores')
        const respose = await fetch('/api/leaderboard');
        const scores = await respose.json()
        let score_index = 0
        let scorestring = ""
        leaderboard_list.innerHTML = ''
        if (scores.length == 0)
        {
            const noScoresLi = document.createElement('li');
            noScoresLi.textContent = "No high scores yet! You can be the first!";
            leaderboard_list.appendChild(noScoresLi);
        } else
        {
            scores.forEach(score => {
                const scoreLi = document.createElement('li');
                // Set text content for the list item
                // Using index + 1 for 1-based numbering
                scoreLi.textContent = `${score.name} (${score.score})`; 
                leaderboard_list.appendChild(scoreLi);
            });
        }
    }

    new_game_button.addEventListener('click', new_game);
    guess_submit_button.addEventListener('click', submit_guess);
    submit_score_button.addEventListener('click', submit_high_score)

    Setup();
    update_high_scores();
    new_game();
});

