import { Message } from './Message.js'

export class Conversation {

    static _conversations = {}

    static _addConversation(id, conversation) {
        Conversation._conversations[id] = conversation;
    }

    static _createNewConversation(id) {
        return new Conversation(id)
    }

    static _modifyMessage(id, index, role, content) {
        Conversation._conversations[id].modifyMessage(index, role, content);
    }

    static _addMessage(id, role, content) {
        Conversation._conversations[id].addMessage(role, content);
    }

    static _removeMessages(id, index, count) {
        console.log("removing messages", id, index, count);
        console.log(Conversation._conversations[id])
        Conversation._conversations[id].removeMessages(index, count);
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
            "height": "45vw",
            "width": "25vw",
            "padding": "2px",
            "color": "#f0f0f0",
            "backgroundColor": "#1b1b1b",
            "border": "2px solid #f0f0f0",
            "borderRadius": "5px",
            "overflowY": "scroll",
            "display": "flex",
            "justifyContent": "flex-start",
            "flexDirection": "column",
            "alignItems": "flex-start"
        });


        this.scrollState = "jump"

        this.container.addEventListener('scroll', (e) => {
            const scrollableHeight = this.container.scrollHeight - this.container.clientHeight
            if (this.container.scrollTop >= 0.9 * scrollableHeight) {
                console.log("State is jump")
                this.scrollState = "jump"
            }
            else if (this.container.scrollTop <= 0) {
                console.log("State is stay")
                this.scrollState = "stay"
            }
        })

        this.messages = [];
        this.roles = [];
        this.role_colors = {};

        Conversation._addConversation(this.id, this);
    }

    addRole(role, backgroundColor) {
        if (!this.roles.includes(role)) {
            this.roles.push(role)
        }
        this.role_colors[role] = backgroundColor;
    }
    removeRole(role) {
        this.roles = this.roles.remove(role)

        delete this.role_colors[role]
    }

    addMessage(role, content) {
        content = content.replace(/\n/g, "<br />");
        console.log("adding message", role, content)
        this.messages.push({"role": role, "content": content})
        if (!this.roles.includes(role)) {
            this.addRole(role, chooseRandomColor())
        }
        this.container.appendChild(new Message(role, content, this.role_colors[role]))
        if (this.scrollState == "jump") {
            this.container.scrollTop = this.container.scrollHeight;
        }
        
    }

    removeMessages(index, count) {
        this.messages.splice(index, count);
        var remove_children = Array.from(this.container.children).slice(index, index + count);
        remove_children.forEach((child) => child.parentElement.removeChild(child));
    }

    modifyMessage(index, role, content) {
        content = content.replace(/\n/g, "<br />");

        this.messages[index]["role"] = role;
        this.messages[index]["content"] = content;

        if (!this.roles.includes(role)) {
            this.addRole(role, chooseRandomColor())
        }
        this.container.replaceChild(new Message(role, content, this.role_colors[role]), this.container.children[index])
    }


}


function chooseRandomColor() {
    var colors = ['#3C1053', '#6441A5', '#2A0845', '#4B0082', '#800080', '#6A0574', '#7F00FF', '#E100FF', '#B10DC9', '#AE00FF', '#FFA500', '#FF4500', '#FF8C00', '#FF7F50', '#FF6347', '#4682B4', '#0000FF', '#1E90FF', '#00BFFF', '#5F9EA0', '#008000', '#006400', '#9ACD32', '#32CD32', '#90EE90'];
    return colors[Math.floor(Math.random() * colors.length)];
}

function getRandomColor() {
    var letters = '0123456789ABCDEF';
    var color = '#';
    for (var i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
  }