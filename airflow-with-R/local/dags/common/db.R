### https://github.com/r-dbi/RPostgres

conn <- DBI::dbConnect(
  RPostgres::Postgres(), host=Sys.getenv('HOST_SERVER'), port='5432', 
  dbname=Sys.getenv('DATABASE'), user=Sys.getenv('USER'), password=Sys.getenv('PASSWORD')
)

select_db <- function(command) { 
  data <- DBI::dbGetQuery(conn, command)
  names(data) <- toupper(names(data))
  return(data) 
}