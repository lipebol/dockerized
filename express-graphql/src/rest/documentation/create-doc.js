const swaggerUi = require(process.env.SWAGGER)


const _swaggerUI = swaggerUi.serve

const _doc = (req, res) => {
    {
        res.send(
            swaggerUi.generateHTML(
                require(
                    process.env[
                    `FILE_DOC_${req.originalUrl.split(process.env.SLASH)[2].toUpperCase()}`
                    ]
                ),
                Object.assign({}, JSON.parse(process.env.CUSTOM_DOC), {
                    "customCss": `
                        :root {
                            --first-color: #f2f2f2;
                            --second-color: #3b4151;
                        }

                        * { 
                            background-color: transparent;
                        } 
                    
                        body { 
                            padding: 0px 120px; 
                            background-color: var(--first-color); 
                            margin: 40px 0px;
                        } 
                    
                        .swagger-ui .topbar { 
                            background-color: var(--second-color); 
                            border-radius: 15px; 
                            width: 200px; 
                            margin-left: 20px;
                        } 
                        
                        .swagger-ui .info {
                            margin-top: 25px;
                        }  
                    
                        .swagger-ui .scheme-container { 
                            display: none 
                        }
                    `}
                )
            )
        )
    }
}


module.exports = { _swaggerUI, _doc }