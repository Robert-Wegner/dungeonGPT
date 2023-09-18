
import { Conversation } from './Conversation.js'
import { Textbox } from './Textbox.js'

export class Grid {

    static _grids = {}

    static _addGrid(id, grid) {
        Grid._grids[id] = grid;
    }

    static _addItem(grid_id, item_id, item) {
        if (grid_id in Grid._grids) {
            Grid._grids[grid_id].addItem(item_id, item);
        }
    }

    static _removeItem(grid_id, item_id, item) {
        if (grid_id in Grid._grids) {
            Grid._grids[grid_id].removeItem(item_id, item);
        }
    }

    static _createAndAddConversation(grid_id, conversation_id) {
        Grid._addItem(grid_id, conversation_id, (new Conversation(conversation_id)).container);
    }

    static _createAndAddTextbox(grid_id, textbox_id) {
        console.log("creating textbox")
        Grid._addItem(grid_id, textbox_id, (new Textbox(textbox_id)).container);
    }

    constructor(id, width, height) {

        this.id = id, 
        this.width = width;
        this.height = height;
        this.container = document.createElement("div");

        this.items = {};
        
        Object.assign(this.container.style, {
            "width": this.width,
            "display": "flex",
            "flexDirextion": "column",
            "justifyContent": "flex-start",
            "alignItems": "flex-start",
            "alignConent": "flex-start",
            "flexWrap": "wrap",
            "backgroundColor": "#222222",
            "border": "2px solid red"
        });

        Grid._addGrid(this.id, this);
    }

    addItem(id, item) {
        if (!(id in this.items)) {
            this.items[id] = item;
            this.container.appendChild(WrappedItem(item, id));
        }
        else {
            console.log("ID already exists");
        }

    }

    removeItem(id) {
        this.container.removeChild(this.items[id].parentElement);

        delete this.items[key];
        
    }

}

function WrappedItem(item, id) {
    item.id = id;
    let wrapper = document.createElement("div");
    let header = document.createElement("div");
    Object.assign(header.style, {
        padding: "2px 2px 2px 8px"
    })
    header.innerHTML = id;
    Object.assign(wrapper.style, {
        "backgroundColor": "#333333",
        "margin": "10px 0px 0px 10px"
    });
    wrapper.appendChild(header);
    wrapper.appendChild(item);

    return wrapper
}
