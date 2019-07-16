(function () {
    let reset = () => {
        document.querySelector('.game-form').classList.remove('hidden')
        document.querySelector('.game-over-wrapper').classList.add('hidden')
    }

    let word_used = (word, answer, state, score) => {
        console.log("palabra usada"); //OK
        add_item(word, "even-crossed-out")
        let result = document.querySelector('.game-over-result')
        result.innerHTML = `La palabra <em>${word}</em>, fue usada anteriormente`
        game_over()
    }

    let invalid_rule = (word, answer, state, score) => {
        console.log("regla invalida"); //OK
        add_item(word, "even-crossed-out")
        let result = document.querySelector('.game-over-result')
        result.innerHTML = `La regla es inválida para <em>${word}</em>`
        game_over()
    }

    let unsyllable = (word, answer, state, score) => {
        console.log("es monosilabo"); //OK
        add_item(word, "even-crossed-out")
        let result = document.querySelector('.game-over-result')
        result.innerHTML = `La palabra <em>${word}</em>, es monosílaba`
        game_over()
    }

    let bullshit = (word, answer, state, score) => {
        console.log("desconfio");
        let result = document.querySelector('.game-over-result')
        result.innerHTML = 'Desconfio'
        game_over()
    }

    let keep_going = (word, answer, state, score) => {
        console.log(state);
        add_item(word, "even")
        setTimeout(() => {
            add_item(answer, "odd")
        }, 1000)
    }

    let game_over = () => {
        document.querySelector('.game-form').classList.add('hidden')
        document.querySelector('.game-over-wrapper').classList.remove('hidden')
    }

    let process_response = (res) => {
        let {word, answer, state, score, game} = res
        // console.log(`the answer was ${answer}`);
        let actions = [keep_going, word_used, invalid_rule, unsyllable, bullshit]
        actions[state](word, answer, state, score)
        update_score(score)
    }

    let add_item = (word, class_) => {
        let item = document.createElement('div')
        item.className = class_
        item.innerHTML = word
        document.querySelector('.container').appendChild(item)
        document.querySelector('#word').value = ""
    }

    let update_score = (score) => {
        document.querySelector('#score-val').innerHTML = score
    }
    
    document.querySelector('#send').onclick = (e) => {
        e.preventDefault()
        let word = document.querySelector('#word').value
        var opts = {
            method: 'POST'
        }
        
        fetch(`/process/${word}`, opts).then((res) => {
            return res.json();
        }).then(process_response)

    }

    document.querySelector('#game-over').onclick = () => {
        //reset()
        window.location.replace('/')
    }

    reset()
})();