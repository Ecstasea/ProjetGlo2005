function filterRecipes() {
    var query = document.getElementById('searchQuery').value.toLowerCase(); // Convert input to lowercase
    var recipes = document.getElementsByClassName('recipe-card'); // Get all recipe cards

    // Loop through each recipe card
    for (var i = 0; i < recipes.length; i++) {
        var recipeName = recipes[i].querySelector('h3').textContent.toLowerCase(); // Get recipe name

        // Check if the recipe name contains the query
        if (recipeName.includes(query)) {
            recipes[i].style.display = 'block'; // Show the recipe card
        } else {
            recipes[i].style.display = 'none'; // Hide the recipe card
        }
    }
}