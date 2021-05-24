###
https://api-29-seconds.herokuapp.com/api

    GET request returns a simple page with a difficulty level and category selector.

    POST request (with difficulty and category in the header) 
        returns json data from a randomly chosen show from the category.
        The image generated is dependent on the difficulty level.

###
https://api-29-seconds.herokuapp.com/api/view
    
    Returns json data of all the shows (question and answer) as stored in the database

###
https://api-29-seconds.herokuapp.com/api/view/<category>
    
    Returns json data of all the shows in the specified category as stored in the database

###
https://api-29-seconds.herokuapp.com/api/add
    
    GET request returns a simple page with category selector and a search box 
    to add the search term(show) into the category.
    Uses the Wikipedia API to retrive information on the search term.
    
    *Does not always work 100% (Atleast 85% of the time)
    *Current workaround is replacing the text received from the Wiki api with 
    the correct text (Manual search on Wikipedia) in the url field, and then
    clicking on the confirm button.

###
// TO DO: //
*Fix above mentioned workaround.
*Return render template for error/success when using the add endpoint.
*Add links to other endpoints on main page.
- Links added
