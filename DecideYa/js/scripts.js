function shuffle(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}

function pairParticipants() {
    const participants = document.getElementById("participants").value.split("\n").filter(p => p.trim());
    const prizes = document.getElementById("prizes").value.split("\n").filter(p => p.trim());

    if (participants.length === 0 || prizes.length === 0) {
        alert("Debes ingresar al menos un participante y un premio.");
        return;
    }

    const shuffledParticipants = shuffle([...participants]);
    const shuffledPrizes = shuffle([...prizes]);

    const max = Math.min(shuffledParticipants.length, shuffledPrizes.length);
    const results = [];

    for (let i = 0; i < max; i++) {
        results.push(`${shuffledParticipants[i]} gana ${shuffledPrizes[i]}`);
    }

    const resultsList = document.getElementById("pairResults");
    resultsList.innerHTML = results.map(r => `<li>${r}</li>`).join("");
}

function flipCoin() {
    const coin = document.getElementById("coin");
    const coinResult = document.getElementById("coinResult");
    const coinCara = document.getElementById("coinCara");
    const coinSello = document.getElementById("coinSello");

    coin.classList.add("coin-flip"); // Iniciar la animación de giro

    // Número de giros repetidos (cambiar esto si se desea más o menos giros)
    const numOfFlips = 5;
    let currentFlip = 0;

    const flipInterval = setInterval(() => {
        // Mostrar el resultado aleatorio: Cara o Sello
        const result = Math.random() < 0.5 ? "Cara" : "Sello";

        // Mostrar la cara o el sello según el resultado
        if (result === "Cara") {
            coinCara.style.transform = "rotateY(0deg)";  // Cara visible
            coinSello.style.transform = "rotateY(180deg)";  // Sello escondido
        } else {
            coinCara.style.transform = "rotateY(180deg)";  // Cara escondida
            coinSello.style.transform = "rotateY(0deg)";  // Sello visible
        }
        coinResult.textContent = `Girando...`;
        currentFlip++;

        if (currentFlip >= numOfFlips) {
            clearInterval(flipInterval);  // Detener los giros después de la cantidad deseada
            setTimeout(() => {
                // Detener la animación después de los giros
                coin.classList.remove("coin-flip"); // Eliminar la animación de giro
            }, 100); // Duración de la animación final

            coinResult.textContent = `Resultado: ${result}`; // Mostrar el resultado
        }
    }, 500); // Tiempo entre cada "flip", ajustado para ser rápido
    
}


function createRandomGroups() {
    const participants = document.getElementById("groupParticipants").value.split("\n").filter(p => p.trim());
    const numGroups = parseInt(document.getElementById("numGroups").value);

    if (participants.length === 0 || isNaN(numGroups) || numGroups <= 0) {
        alert("Debes ingresar al menos un participante y un número de grupos válido.");
        return;
    }

    const shuffledParticipants = shuffle([...participants]);
    const groups = Array.from({ length: numGroups }, () => []);

    // Asignar participantes a grupos
    shuffledParticipants.forEach((participant, index) => {
        groups[index % numGroups].push(participant);
    });

    const resultsList = document.getElementById("groupResults");
    resultsList.innerHTML = groups.map((group, index) => {
        return `<li>Grupo ${index + 1}: ${group.join(", ")}</li>`;
    }).join("");
}

function rollDice() {
    const dice1 = document.getElementById("dice1");
    const dice2 = document.getElementById("dice2");

    // Iniciar la animación de los dados
    dice1.style.animation = "roll 1s ease-in-out infinite";
    dice2.style.animation = "roll 1s ease-in-out infinite";

    // Esperar un tiempo antes de mostrar el resultado final
    setTimeout(() => {
        const die1Result = Math.floor(Math.random() * 6) + 1;
        const die2Result = Math.floor(Math.random() * 6) + 1;

        // Detener la animación
        dice1.style.animation = "";
        dice2.style.animation = "";

        // Actualizar las imágenes de los dados
        dice1.src = `../images/dice${die1Result}.png`;
        dice2.src = `../images/dice${die2Result}.png`;

        // Mostrar el resultado final
        document.getElementById("diceResult").textContent = `Resultado: ${die1Result} y ${die2Result}`;
    }, 1000); // Esperar 1 segundo antes de mostrar el resultado
}
