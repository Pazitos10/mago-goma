(function () {
    let reset = () => {
        document.querySelector('.game-form').classList.remove('hidden')
        document.querySelector('.game-over-wrapper').classList.add('hidden')
        document.querySelector('.cpu-bullshit').classList.add('hidden')
        hide_definition()
    }

    let word_used = (word, answer, state, score, gamer) => {
        if (gamer == 2){
            console.log("palabra usada"); //OK
            add_item(word, "even-crossed-out")
            let msg = `Perdiste! :( <br> La palabra <em>${answer}</em>, fue usada anteriormente`
            game_over(msg)
       }else{
            console.log("palabra usada"); //OK
            add_item(word, "odd-crossed-out")
            let msg = `Ganaste! :( <br> La palabra <em>${answer}</em>, fue usada anteriormente`
            game_over(msg)
       } 
    }

    let invalid_rule = (word, answer, state, score, gamer) => {
        if (gamer == 2){
            console.log("regla invalida"); //OK
            add_item(answer, "even-crossed-out")
            let msg = `Perdiste! :( <br> La regla es inválida para <em>${word}</em>`
            game_over(msg)
        }else{
            console.log("regla invalida"); //OK
            add_item(answer, "odd-crossed-out")
            let msg = `Ganaste! :) <br> La regla es inválida para <em>${word}</em>`
            game_over(msg)
        }
    }

    let unsyllable = (word, answer, state, score, gamer) => {
        if (gamer == 2){
            console.log("es monosilabo"); //OK
            add_item(answer, "even-crossed-out")
            let msg = `Perdiste! :( <br> La palabra <em>${answer}</em>, es monosílaba`
            game_over(msg)
        }else{
            console.log("es monosilabo"); //OK
            add_item(answer, "odd-crossed-out")
            let msg = `Ganaste! :( <br> La palabra <em>${answer}</em>, es monosílaba`
            game_over(msg)
        }
    }

    // let bullshit = (word, answer, state, score, gamer) => {
    //     console.log("desconfio");
    //     let msg
    //     if (gamer == 1){
    //         if (state == 0){
    //             msg = 'Ganó el Mago Goma'
    //             game_over(msg)
    //         }else if (state == 4) {
    //             msg = 'El Mago Goma dice: "Desconfío!"'
    //             add_item(answer, 'even')
    //             game_over(msg, is_cpu = true)
    //         } else {
    //             msg = 'Ganaste!'
    //             game_over(msg)
    //         }
            
    //     }
    // }

    let bullshit = (word, answer, state, score, gamer) => {
        console.log("desconfio");
        let msg
        if (gamer == 1){
            if (state == 0){
                 msg = 'Ganó el Mago Goma'
                 game_over(msg)
                 return
            }else if (state == 4) {
                msg = 'El Mago Goma dice: "Desconfío!"'
                add_item(answer, 'even')
                game_over(msg, is_cpu = true)
                return
            } 

        }else{
            add_item(answer, 'even')
            msg = 'Ganaste :)'
            game_over(msg)
        }
    }

    let keep_going = (word, answer, state, score, gamer) => {
        console.log(state);
        if (gamer == 1 && state == 0) { // turno CPU
            add_item(answer, "odd", 1)
            bullshit(word, answer, state, score, gamer)
        } else { // turno participante
            add_item(word, "even")
            add_item(answer, "odd", 1)
        }
    }

    let game_over = (msg, is_cpu = false) => {
        if (is_cpu){
            let result = document.querySelector('.cpu-message')
            result.innerHTML = msg
            document.querySelector('.cpu-bullshit').classList.remove('hidden')
            document.querySelector('#bullshit').classList.add('hidden')
        }else{
            let result = document.querySelector('.game-over-result')
            result.innerHTML = msg
            document.querySelector('.cpu-bullshit').classList.add('hidden')
            document.querySelector('#bullshit').classList.remove('hidden')
            document.querySelector('.game-form').classList.add('hidden')
            document.querySelector('.game-over-wrapper').classList.remove('hidden')
        }
    }

    let process_response = (res) => {
        let {word, answer, state, score, gamer} = res
        let actions = [keep_going, word_used, invalid_rule, unsyllable, bullshit]
        actions[state](word, answer, state, score, gamer)
        update_score(score)
    }

    let add_item = (word, class_, delay = 0) => {
        if (delay > 0) {
            setTimeout(() => { add_item(word, class_) }, delay * 1000)
        }else{
            let item = document.createElement('div')
            item.className = class_
            item.innerHTML = word    
            document.querySelector('.container').appendChild(item)
            document.querySelector('#word').value = ""
        }
    }

    let get_definition = () => {
        console.log("test")
        let contain = document.querySelector(".words").querySelector(".container")
        let last_word = contain.children[contain.children.length - 1].innerText
        console.log(last_word)
        var opts = { method: 'GET' }
        fetch(`/definition/${last_word}`, opts).then((res) => {
            return res.json();
        }).then(add_definition)
    }

    let add_definition = (definition) => {
        console.log(definition)
        document.querySelector("#definition").innerHTML = definition
        document.querySelector('.word-definition').classList.remove('hidden')
    } 

    let hide_definition = () => {
        document.querySelector('.word-definition').classList.add('hidden')
    }

    let update_score = (score) => {
        document.querySelector('#score-val').innerHTML = score
    }
    
    document.querySelector('#send').onclick = (e) => {
        e.preventDefault()
        let word = document.querySelector('#word').value
        var opts = { method: 'POST' }
        fetch(`/process/${word}`, opts).then((res) => {
            return res.json();
        }).then(process_response)

    }

    document.querySelector('#game-over').onclick = () => {
        window.location.replace('/')
    }
    
    document.querySelector('#bullshit').onclick = (e) => {
        e.preventDefault()
        var opts = { method: 'POST' }
        fetch(`/bullshit`, opts).then((res) => {
            return res.json();
        }).then(process_response)
    }

    document.querySelector('#close-definition').onclick = () => {
        hide_definition()
    }

    document.querySelector('.words .container div').onclick = (e) => {
        get_definition(e.target.innerHTML)
    }

    reset()
})();