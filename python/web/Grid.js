
export class Grid {
    constructor(width, height) {
        this.width = width
        this.height = height
        this.container = document.createElement("div")

        self.items = []

        Object.assign(this.container.style, {
            "width": this.width,
            "height": this.height,
            "display": "flex",
            "flexDirextion": "column",
            "justifyContent": "space-evenly",
            "alignItems": "stretch",
            "flexWrap": "wrap",
            "backgroundColor": "#333333",
            "border": "2px solid white"
        })
    }

    addItem(item) {
        self.items.append(item)
        this.container.appendChild(WrappedItem(item))
    }
}

function WrappedItem(item) {
    wrapper = document.createElement("div")
    Object.assign(wrapper.style, {
        "max-height": "40vh",
        "backgroundColor": "#555555"
    })
    wrapper.appendChild(item)

    return wrapper
}