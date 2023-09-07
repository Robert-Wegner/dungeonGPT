
import { Conversation } from './Conversation.js'


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


    constructor(id, width, height) {

        this.id = id, 
        this.width = width;
        this.height = height;
        this.container = document.createElement("div");

        this.items = {};
        this.itemWrappers
        Object.assign(this.container.style, {
            "width": this.width,
            "height": this.height,
            "display": "flex",
            "flexDirextion": "column",
            "justifyContent": "space-evenly",
            "alignItems": "stretch",
            "flexWrap": "wrap",
            "backgroundColor": "#333333",
            "border": "2px solid red"
        });

        Grid._addGrid(this.id, this);
    }

    addItem(id, item) {
        if (!(id in this.items)) {
            this.items[id] = item;
            this.container.appendChild(WrappedItem(item, id));
            console.log("Successfully add item to grid", item, id)
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
    header.innerHTML = id;
    Object.assign(wrapper.style, {
        "max-height": "40vh",
        "backgroundColor": "#555555"
    });
    wrapper.appendChild(header);
    wrapper.appendChild(item);

    return wrapper
}
