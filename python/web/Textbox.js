export class Textbox {

    static _textboxes = {};

    static _addTextbox(id, textbox) {
        Textbox._textboxes[id] = textbox;
    }

    static _setContent(id, content) {
        Textbox._textboxes[id].setContent(content);
    }
    
    constructor(id) {
        this.id = id;
        this.container = document.createElement('div')
        

        Object.assign(this.container.style, {
            "border": "1px solid white",
            "width": "20vw"
        });

        this.content = "";

        Textbox._addTextbox(this.id, this);
    }

    setContent(content) {
        this.content = content;
        this.container.innerHTML = this.content;
    }

}