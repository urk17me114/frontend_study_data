const score ={
                wins: 0,
                loss: 0,
                Tie: 0
            };
        

        function play(humanChoice) {

            
            let a = Math.random();
            let computerChoice;

            if (a > 0 && a < 1/3) {
                computerChoice = "rock";
            }
            else if (a > 1/3 && a < 2/3) {
                computerChoice = "paper";
            }
            else if (a > 2/3 && a < 1) {
                computerChoice = "scissors";
            }

            if (computerChoice == humanChoice) {
                score.Tie +=1;
                document.querySelector('.result')
                .innerHTML = `You picked ${humanChoice}. Computer picked ${computerChoice}. Tie.<br>
                Wins: ${score.wins}  Loss: ${score.loss}  Tie: ${score.Tie}`;
                
            }
            else if (computerChoice == "rock" && humanChoice == "paper") {
                score.wins +=1;
                document.querySelector('.result')
                .innerHTML = `You picked ${humanChoice}. Computer picked ${computerChoice}. Win.<br>
                WIns: ${score.wins}  Loss: ${score.loss}  Tie: ${score.Tie}`;
                               
            }
            else if (computerChoice == "paper" && humanChoice == "rock") {
                score.loss += 1;
                document.querySelector('.result').innerHTML = `
                    You picked ${humanChoice}. Computer picked ${computerChoice}. Lose.<br>
                    Wins: ${score.wins}  Loss: ${score.loss}  Tie: ${score.Tie}
                `;
            }

            else if (computerChoice == "rock" && humanChoice == "scissors") {
                score.loss += 1;
                document.querySelector('.result').innerHTML = `
                    You picked ${humanChoice}. Computer picked ${computerChoice}. Lose.<br>
                    Wins: ${score.wins}  Loss: ${score.loss}  Tie: ${score.Tie}
                `;
            }

            else if (computerChoice == "scissors" && humanChoice == "paper") {
                score.loss += 1;
                document.querySelector('.result').innerHTML = `
                    You picked ${humanChoice}. Computer picked ${computerChoice}. Lose.<br>
                    Wins: ${score.wins}  Loss: ${score.loss}  Tie: ${score.Tie}
                `;
            }

            else if (computerChoice == "paper" && humanChoice == "scissors") {
                score.wins += 1;
                document.querySelector('.result').innerHTML = `
                    You picked ${humanChoice}. Computer picked ${computerChoice}. Win.<br>
                    Wins: ${score.wins}  Loss: ${score.loss}  Tie: ${score.Tie}
                `;
            }

            else if (computerChoice == "scissors" && humanChoice == "rock") {
                score.wins += 1;
                document.querySelector('.result').innerHTML = `
                    You picked ${humanChoice}. Computer picked ${computerChoice}. Win.<br>
                    Wins: ${score.wins}  Loss: ${score.loss}  Tie: ${score.Tie}
                `;
            }

            else if (humanChoice == "Reset") {
                score.wins = 0; 
                score.loss = 0; 
                score.Tie = 0;

                document.querySelector('.result').innerHTML = `
                    Scores reset.<br>
                    Wins: ${score.wins}  Loss: ${score.loss}  Tie: ${score.Tie}
                `;
            }
        }
