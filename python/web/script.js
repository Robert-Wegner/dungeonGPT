import { Conversation } from './Conversation.js'
import { Textbox } from './Textbox.js'
import { Grid } from './Grid.js'
//import { Exposer } from './Exposer.js'

function opposite(orientation) {
    if (orientation == "left") {
        return "right"
    }
    else if (orientation == "right") {
        return "left"
    }
}

function sayHello() {
    console.log("Hello!");
}

window.onload = function() {
    var body = document.getElementsByTagName("body")[0];

    eel.expose(sayHello)


    var testButton = document.createElement("div");
    testButton.innerHTML = "Click Me!";
    testButton.type = "button";
    testButton.onclick = () => eel.test_function()(() => null);
    body.appendChild(testButton);


    var grid = new Grid("main_grid", "90vw", "90vh");

    //grid.addItem("main_conversation", (new Conversation("main_conversation")).container);
    //Grid._addItem("main_grid", "character_textbox", (new Textbox("character_textbox")).container);
    //Grid._createAndAddConversation("main_grid", "secondary_conversation");

    eel.expose(grid.makeJoke, "cringe");

    eel.expose(Grid._addItem, "Grid_addItem");
    eel.expose(Grid._createAndAddConversation, "Grid_createAndAddConversation");
    eel.expose(Grid._createAndAddTextbox, "Grid_createAndAddTextbox");
    eel.expose(Conversation._modifyMessage, "Conversation_modifyMessage");
    eel.expose(Conversation._createNewConversation, "Conversation_createNewConversation");
    eel.expose(Conversation._addMessage, "Conversation_addMessage");
    eel.expose(Conversation._removeMessages, "Conversation_removeMessages");
    eel.expose(Conversation._addRole, "Conversation_addRole");
    eel.expose(Conversation._removeRole, "Conversation_removeRole");
    eel.expose(Textbox._setContent, "Textbox_setContent");

    body.appendChild(grid.container);

}
