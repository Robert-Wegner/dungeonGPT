
export function Message(backgroundColor, content) {
    var msg = document.createElement("div")
    Object.assign(msg.style, {
            "width": "90%",
            "backgroundColor": backgroundColor,
            "padding": "4px"
        }   
    )
    msg.innerHTML = content;
    return msg
}