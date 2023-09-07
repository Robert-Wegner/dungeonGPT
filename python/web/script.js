import { Conversation } from './Conversation.js'
import { Grid } from './Grid.js'

function opposite(orientation) {
    if (orientation == "left") {
        return "right"
    }
    else if (orientation == "right") {
        return "left"
    }
}
eel.expose(sayHello)
function sayHello() {
    console.log("Hello!")
}

window.onload = function() {
    var body = document.getElementsByTagName("body")[0]

    
    var testButton = document.createElement("div")
    testButton.innerHTML = "Click Me!"
    testButton.type = "button"
    testButton.onclick = () => eel.test_function()(() => null)
    body.appendChild(testButton)
    var grid = new Grid()

    var conversation = new Conversation()
    body.appendChild(conversation.container)

    var messagebox = document.getElementById("messagebox");
    var summarybox = document.getElementById("summarybox");
    var inputbox = document.getElementById("inputbox");
    var rolebox = document.getElementById("rolebox");
    var recent = document.getElementById("recent");
    var ancient = document.getElementById("ancient");

    function createMessage(orientation, role, content) {
        var msg = document.createElement("div")
        Object.assign(msg.style, {
                "alignSelf": orientation == "left" ? "flex-start" : "flex-end",
            }   
        )
        msg.className = orientation == "left" ? "textbox2" : "textbox3";
        msg.innerHTML = "<b> " + role + "</b> <br>" + content;
        return msg
    }
    
    function updateRecent(text) {
        console.log("recent", text)
        recent.innerHTML = text;
    }
    function updateAncient(text) {
        ancient.innerHTML = text;  
    }
    function synchronize(conversation) {
        console.log("synchronize: ", conversation)
    }

    var oldRole = rolebox.value;
    var oldOrientation = "left";

    inputbox.onkeydown = function(event) {
        if (event.key == "Enter") { // Enter key
            event.preventDefault();
            if (event.shiftKey) {
                inputbox.value += "\n"
            }
            else {
                var content = inputbox.value;
                var newRole = rolebox.value;
                var newOrientation = (oldRole == newRole) ? oldOrientation : opposite(oldOrientation)

                inputbox.value = "";
                oldRole = newRole;
                oldOrientation = newOrientation;
                messagebox.scrollTop = messagebox.scrollHeight;

                var msg = createMessage(newOrientation, newRole, content);
                messagebox.appendChild(msg);
                eel.add_message(newRole, content)
                //eel.get_conversation()((conv) => synchronize(conv))
                eel.get_recent()((text) => updateRecent(text))
                eel.get_ancient()((text) => updateAncient(text))                
            }
        }
    }

    var do_continue = false
    var last_response_role = "Bob"
    var last_response = "Hello, I am Bob"

    document.addEventListener('keydown', function(event) {
        if(event.key === 's') {
            do_continue = false;
        }
        else if(event.key === 'c') {
            do_continue = true;
            if (last_response_role == "Bob") {
                alice_reply(last_response)
            }
            if (last_response_role == "Alice") {
                bob_reply(last_response)
            }
        }
    });

    var bob_reply = (message) => {
        eel.bob_reply(message)((response) => {
            messagebox.appendChild(createMessage("left", "Bob", message));
            eel.get_recent()((text) => updateRecent(text))
            eel.get_ancient()((text) => updateAncient(text))
            if (do_continue) {
                alice_reply(response)
            }
            else {
                last_response_role = "Bob"
                last_response = response
            }
        })
    }
    var alice_reply = (message) => {
        eel.alice_reply(message)((response) => {
            messagebox.appendChild(createMessage("right", "Alice", message));
            eel.get_recent()((text) => updateRecent(text))
            eel.get_ancient()((text) => updateAncient(text))
            if (do_continue) {
                bob_reply(response)
            }
            else {
                last_response_role = "Alice"
                last_response = response
            }
        })
    }

    


}