import { Message } from './Message.js'

export class Conversation {

    static _conversations = {}

    static _addConversation(id, conversation) {
        Conversation._conversations[id] = conversation;
    }

    static _addMessage(id, role, content) {
        console.log("Okay: ", Conversation._conversations[id].addMessage, id, role, content);
        Conversation._conversations[id].addMessage(role, content);
    }
    static _addRole(id, role, backgroundColor) {
        Conversation._conversations[id].addRole(role, backgroundColor);
    }
    static _removeRole(id, role) {
        Conversation._conversations[id].removeRole(role);
    }
    
    constructor(id) {

        this.id = id;
        this.hasInput = false;

        this.container = document.createElement('div');
        

        Object.assign(this.container.style, {
            "border": "1px solid white",
            "width": "20vw"
        });

        this.input = document.createElement("textarea");
        this.input.rows = 6;
        Object.assign(this.container.style, {
            "border": "1px solid white",
            "width": "95%",
            "textAlign": "left",
            "padding": "2px",
            "color": "#f0f0f0",
            "backgroundColor": "#2b2b2b",
            "border": "2px solid #f0f0f0",
            "borderRadius": "5px"
        });

        this.messages = [];
        this.roles = [];
        this.role_colors = {};

        Conversation._addConversation(this.id, this);
    }

    addRole(role, backgroundColor) {
        if (!this.roles.includes(role)) {
            this.roles.push(role)
        }
        Object.assign(this.role_colors, {
            role: backgroundColor
        })
    }
    removeRole(role) {
        this.roles = this.roles.remove(role)

        delete this.role_colors[role]
    }

    addMessage(role, content) {
        console.log("Adding message");
        this.messages.push({"role": role, "content": content})
        if (!(role in this.roles)) {
            this.addRole(role, getRandomColor())
        }
        this.container.appendChild(new Message(this.role_colors[role], content))
    }

}

function getRandomColor() {
    var letters = '0123456789ABCDEF';
    var color = '#';
    for (var i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
  }