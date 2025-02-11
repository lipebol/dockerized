
class HasParams {

    constructor() { this.hasparams = JSON.parse(process.env.ARRAY_EMPTY) }

    Dates(request) {
        try {
            this.params = request.params.dates.split(process.env.SEPARATOR)
            if (this.params) {
                this.params.forEach((value) => { if (value !== '') { this.hasparams.push(value) } })
            }
            return this.hasparams.length === 2 || this.params[0] === process.env.MAX ? true : false
        } catch (err) { console.log(err) }
    }
}

module.exports = { HasParams }