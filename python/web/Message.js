
export function Message(role, content, backgroundColor) {
    var msg = document.createElement("div")
    console.log("A", backgroundColor)
    Object.assign(msg.style, {
            "width": "95%",
            "backgroundColor": backgroundColor,
            "padding": "4px",
            "marginTop": "4px"
        }   
    )
    msg.innerHTML = "<b>" + role  +"</b> <br>" + content;
    return msg
}