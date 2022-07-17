async function getSong(pl) {
    let a;
    playlist = pl;
    a = await Promise.resolve($.get( "/getsong", {url: pl} ))

    return {data: a.data, url: a.url};
  
}

function createNode(b64) {
    const audio = document.createElement("audio");
    const source = document.createElement("source");
    audio.appendChild(source);
    source.setAttribute("src", "data:audio/wav;base64," + b64.data)
    audio.setAttribute("url", b64.url)
    const element = document.getElementById("audioContainer");
    element.appendChild(audio);
    audio.onended = (e) => {$("#urlS").attr("href", e.target.nextSibling.getAttribute('url'));e.target.nextSibling.volume=$('#volume').val();e.target.nextSibling.play();e.target.remove();audios.splice(0,1)};
    return audio
}

function loop() {
    console.log(audios.length)
    if (audios.length < 5 && !inProcess) {
        console.log("adding another")
        inProcess = true;
        getSong(playlist).then(d => {audios.push(createNode(d)); inProcess=  false;$("#skip").css("display", "block")});
        
    }
 
}

function play() {
    var audio = audios[0];
    if (audio.paused) {
        audio.play();
    }else{
        audio.pause();
    }
}

function skip() {
    audios[0].remove();
    audios.splice(0,1);
    audios[0].volume = $("#volume").val();
    audios[0].play()
    if (audios.length == 1) {
        $("#skip").css("display", "none")
    }
    $('#urlS').attr('href', audios[0].getAttribute('url'))
}
