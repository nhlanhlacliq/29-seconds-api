https://api-29-seconds.herokuapp.com/api

    GET request returns a simple page with a difficulty level and category selector.

    POST request (with difficulty and category in the header) 
        returns json data from a randomly chosen show from the category.
        The image generated is dependent on the difficulty level.


https://api-29-seconds.herokuapp.com/api/view
    
    Returns a json data of all the shows (question and answer) as stored in the database


https://api-29-seconds.herokuapp.com/api/view/<category>
    
    Returns a json data of all the shows in the specified category as stored in the database