const { sequelizeConnect } = require(process.env.INSTANCE_POSTGRESQL_PATH)
const { DataTypes } = require(process.env.ORM)


/// Schema PostgreSQL: 'jobs'
const _JOBSWEBSITES = sequelizeConnect.define("_JOBSWEBSITES", {
    id: { primaryKey: true, type: DataTypes.INTEGER, allowNull: false },
    name: { type: DataTypes.STRING },
    url: { type: DataTypes.STRING },
    relative_path: { type: DataTypes.JSONB },
    date_created: { type: DataTypes.STRING },
    time_created: { type: DataTypes.STRING }
}, {
    schema: process.env.SCHEMA_JOBS,
    tableName: "website",
    timestamps: false
})


/// Schema PostgreSQL: 'jobs'
const _JOBSKEYWORDS = sequelizeConnect.define("_JOBSKEYWORDS", {
    id: { primaryKey: true, type: DataTypes.INTEGER, allowNull: false },
    content: { type: DataTypes.STRING },
    date_created: { type: DataTypes.STRING },
    time_created: { type: DataTypes.STRING }
}, {
    schema: process.env.SCHEMA_JOBS,
    tableName: "keyword",
    timestamps: false
})



module.exports = { _JOBSWEBSITES, _JOBSKEYWORDS }