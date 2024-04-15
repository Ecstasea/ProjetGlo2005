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

$(document).ready(function() {
    $('input[type="checkbox"]').change(function() {
        var ingredient_id = $(this).val();
        var quantite_input = $('#quantite_ingredient' + ingredient_id);
        if (this.checked) {
            quantite_input.prop('disabled', false);
        } else {
            quantite_input.prop('disabled', true);
        }
    });
});