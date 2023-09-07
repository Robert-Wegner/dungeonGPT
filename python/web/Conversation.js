import { Message } from './Message.js'

export class Conversation {

    constructor() {

        this.hasInput = true

        this.container = document.createElement('div')
        

        Object.assign(this.container.style, {
            "border": "1px solid white",
            "width": "20vw"
        })

        this.input = document.createElement("textarea")
        this.input.rows = 6
        Object.assign(this.container.style, {
            "border": "1px solid white",
            "width": "95%",
            "textAlign": "left",
            "padding": "2px",
            "color": "#f0f0f0",
            "backgroundColor": "#2b2b2b",
            "border": "2px solid #f0f0f0",
            "borderRadius": "5px"
        })

        this.messages = []
        this.roles = []
        this.role_colors = {}
    }
    addRole(role, backgroundColor) {
        if (!this.roles.includes(new_role)) {
            this.roles.append(role)
        }
        Object.assign(self.role_colors, {
            role: backgroundColor
        })
    }
    removeRole(role) {
        this.roles = this.roles.remove(role)

        delete this.role_colors[role]
    }
    addMessage(role, content) {
        this.messages.append({"role": role, "content": content})
        this.container.appendChild(new Message(this.role_colors[role], content))
    }

    removeMessage
}