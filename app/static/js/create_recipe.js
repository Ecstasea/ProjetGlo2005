function filterIngredients() {
    var input = document.getElementById("ingredients_search");
    var filter = input.value.toUpperCase();
    var ingredients = document.getElementById("ingredient_list");
    var divs = ingredients.getElementsByTagName("div");

    for (var i = 0; i < divs.length; i++) {
        var label = divs[i].getElementsByTagName("label")[0];
        if (label) {
            var txtValue = label.textContent || label.innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                divs[i].style.display = "";
            } else {
                divs[i].style.display = "none";
            }
        }
    }
}