
export class Exposer {

    static exposed = []

    static expose(func, id) {
        if (!(id in Exposer.exposed)) {
            console.log("successfully exposed", func, id)
            Exposer.exposed[id] = func;
            eel.expose(func, id);
        } else {
            throw new Error(`ID ${id} already exists.`);
        }
    }

}

