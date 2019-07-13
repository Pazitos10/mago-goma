(function () {

    let process_response = (res) => {
        let {word, answer, state, score, game} = res
        // console.log(`the answer was ${answer}`);
        add_item(word, "even")
        setTimeout(() => {
            add_item(answer, "odd")
        }, 1500)
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
    
})();