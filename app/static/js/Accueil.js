function filterRecipes() {
    var query = document.getElementById('searchQuery').value.toLowerCase();
    var recipes = document.getElementsByClassName('recipe-card');

    for (var i = 0; i < recipes.length; i++) {
        var recipeName = recipes[i].querySelector('h3').textContent.toLowerCase();

        if (recipeName.includes(query)) {
            recipes[i].style.display = 'block';
        } else {
            recipes[i].style.display = 'none';
        }
    }
}