
class SetRequestResponse {

    constructor() { try { this.object = this.init() } catch (err) { console.log(err) } }


    init() { return JSON.parse(process.env.OBJECT_EMPTY) }


    url(originalUrl) {
        try {
            return originalUrl
                .split(process.env.QUESTION)[0]
                .split(process.env.SLASH).slice(2)
        } catch (err) { console.log(err) }
    }


    model(model) {
        try {
            if (model.name && model.table) {
                this.object.model = `_${(model.name + model.table).toUpperCase()}`
            } else { this.object.model = model }
        } catch (err) { console.log(err) }
    }


    filter(args) {
        try {
            if (args) {
                this.object.filter = args.name && args.column ? /// <--- REST
                    process.env[`${(args.name + args.column).toUpperCase()}`] :
                    typeof (args) === process.env.TYPE_STRING ? /// <--- GraphQL
                        args : Object.keys(args)[0].toString()
            }
        } catch (err) { console.log(err) }
    }


    query(query) { /// <--- REST
        try {
            if (query) {
                let [param] = Object.keys(query)
                let [arg] = Object.values(query)
                if (param && arg) { this.object.params = { [param]: arg } }
            }
        } catch (err) { console.log(err) }
    }


    param(args) { /// <--- GraphQL
        try {
            if (args) {
                this.object.params = Object.values(args)[0] === process.env.ASTERISK ? undefined :
                    { [args.periodo ? 'dates' : 'multi']: Object.values(args)[0] }
            }
        } catch (err) { console.log(err) }
    }


    page(pagination) {
        try {
            if (pagination !== undefined) {
                this.object.page = parseInt(pagination) <= 0 ? 1 : parseInt(pagination)
            }
        } catch (err) { console.log(err) }
    }


    count() { try { this.object.count = process.env.ASTERISK } catch (err) { console.log(err) } }


    fields(context) {
        try {
            if (context) {
                this.object.fields = context.fieldNodes[0].selectionSet.selections.map(
                    value => value.name.value
                )
            }
        } catch (err) { console.log(err) }
    }


    lookup(...args) {
        try {
            if (args) {
                this.object.lookup = args.length === 1 ?
                    args[0] : { path: args[0], populate: args[1] }
            }
        } catch (err) { console.log(err) }
    }


    finally() {
        this.request = this.object
        this.object = this.init()
        return this.request
    }
}

const set = new SetRequestResponse()

module.exports = { set }